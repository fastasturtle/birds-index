#!/usr/bin/env python3
"""Build data/species.json: a trilingual (ru / en / Latin) index of world bird species.

Backbone: AviList v2025b (species only). Russian names are taken from a cascade
of sources, matched by exact (normalised) scientific name:

    1. IOC World Bird List Multilingual 15.2   -> ru_source "ioc"
    2. eBird taxonomy API, locale=ru            -> ru_source "ebird"
    3. Wikidata P1843 (taxon common name, ru)   -> ru_source "wikidata"
    4. data/overrides.csv (applied last)        -> ru_source "manual"

Usage:
    uv run scripts/build.py            # download whatever is missing, then build
    uv run scripts/build.py --offline  # use only files already on disk
    uv run scripts/build.py --fetch    # force re-download of every source
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

import openpyxl
import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
CACHE = DATA / "cache"

AVILIST_PATH = RAW / "AviList-v2025b-extended.xlsx"
IOC_PATH = RAW / "IOC-Multiling-15.2.xlsx"
EBIRD_PATH = CACHE / "ebird-taxonomy-ru.json"
WIKIDATA_PATH = CACHE / "wikidata-ru-p1843.json"
OVERRIDES_PATH = DATA / "overrides.csv"
OUT_JSON = DATA / "species.json"
OUT_DOCS_JSON = ROOT / "docs" / "data" / "species.json"
OUT_REPORT = DATA / "report.md"

AVILIST_URL = "https://www.avilist.org/wp-content/uploads/2026/06/AviList-v2025b-10Jun2026-extended.xlsx"
IOC_URL = "https://worldbirdnames.org/Multiling%20IOC%2015.2.xlsx"
EBIRD_URL = "https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json&locale=ru&cat=species"
WIKIDATA_SPARQL = "https://query.wikidata.org/sparql"

USER_AGENT = "birds-index-build/0.1 (https://github.com/fastasturtle/birds-index)"
CYRILLIC = re.compile(r"[Ѐ-ӿ]")

EXTINCT_MAP = {
    "extinct": "extinct",
    "(extinct)": "extinct",
    "extinct in the wild": "extinct_in_wild",
    "possibly extinct": "possibly_extinct",
    "(possibly extinct)": "possibly_extinct",
    "possibly extinct in the wild": "possibly_extinct",
    "previously extinct in the wild, but reintroduced": None,
}

FIELDS = [
    "id", "seq", "order", "family", "family_en", "sci", "authority", "en",
    "ru", "ru_source", "ru_status", "ioc_sci", "extinct", "iucn",
]


# --------------------------------------------------------------------------- helpers

def sci_key(name: str | None) -> str:
    """Normalise a scientific name for matching: lower case, single spaces."""
    return " ".join(str(name or "").split()).lower()


def clean(value) -> str | None:
    """Strip and collapse whitespace; empty -> None."""
    if value is None:
        return None
    text = " ".join(str(value).split())
    return text or None


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


def download(url: str, dest: Path, timeout: int = 300) -> None:
    """Download url to dest atomically (via a .part file)."""
    log(f"  downloading {url}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(url, stream=True, timeout=timeout,
                      headers={"User-Agent": USER_AGENT}) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
    tmp.replace(dest)


def ensure_file(path: Path, url: str, mode: str, required: bool) -> bool:
    """Make sure `path` exists according to mode ('offline' | 'default' | 'fetch').

    Returns True if the file is available. Raises if a required file is missing.
    """
    need = mode == "fetch" or not path.exists()
    if need and mode != "offline":
        try:
            download(url, path)
        except Exception as exc:  # noqa: BLE001 - report and continue
            log(f"  WARNING: download failed for {url}: {exc}")
    if path.exists():
        return True
    if required:
        raise SystemExit(f"Required file missing: {path} (run without --offline to download it)")
    return False


def xlsx_rows(path: Path, sheet: str | None = None):
    """Yield (header, row) dicts from the first (or named) worksheet."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    rows = ws.iter_rows(values_only=True)
    header = [str(h).strip() if h is not None else "" for h in next(rows)]
    for row in rows:
        yield dict(zip(header, row))
    wb.close()


# --------------------------------------------------------------------------- sources

def load_avilist(path: Path) -> list[dict]:
    """Return AviList species rows as base output records (in sequence order)."""
    records = []
    for row in xlsx_rows(path):
        if clean(row.get("Taxon_rank")) != "species":
            continue  # also skips the second, human-readable header row
        status = clean(row.get("Extinct_or_possibly_extinct"))
        if status is not None and status.lower() not in EXTINCT_MAP:
            raise SystemExit(f"Unknown extinction status {status!r} for {row.get('Scientific_name')}")
        records.append({
            "id": clean(row.get("AvibaseID")),
            "seq": int(row["Sequence"]),
            "order": clean(row.get("Order")),
            "family": clean(row.get("Family")),
            "family_en": clean(row.get("Family_English_name")),
            "sci": clean(row.get("Scientific_name")),
            "authority": clean(row.get("Authority")),
            "en": clean(row.get("English_name_AviList")),
            "ru": None,
            "ru_source": None,
            "ru_status": "missing",
            "ioc_sci": None,  # exact matching only in this version
            "extinct": EXTINCT_MAP[status.lower()] if status else None,
            "iucn": clean(row.get("IUCN_Red_List_Category")),
        })
    records.sort(key=lambda r: r["seq"])
    return records


def load_ioc(path: Path) -> dict[str, dict]:
    """Return {sci_key: {"sci", "en", "ru"}} from the IOC multilingual list."""
    out = {}
    for row in xlsx_rows(path, sheet="List"):
        sci = clean(row.get("IOC_15.2"))
        if not sci:
            continue
        out[sci_key(sci)] = {"sci": sci, "en": clean(row.get("English")),
                             "ru": clean(row.get("Russian"))}
    return out


def load_ebird(path: Path) -> dict[str, str]:
    """Return {sci_key: Russian name} from the eBird taxonomy (locale=ru).

    eBird falls back to English when no Russian name exists, so names without
    any Cyrillic are treated as missing.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for item in data:
        if item.get("category") != "species":
            continue
        name = clean(item.get("comName"))
        if name and CYRILLIC.search(name):
            out[sci_key(item.get("sciName"))] = name
    return out


def sparql(query: str, timeout: int = 180) -> list[dict]:
    r = requests.get(WIKIDATA_SPARQL, params={"query": query, "format": "json"},
                     headers={"User-Agent": USER_AGENT,
                              "Accept": "application/sparql-results+json"},
                     timeout=timeout)
    r.raise_for_status()
    return r.json()["results"]["bindings"]


WIKIDATA_QUERY = """
SELECT ?item ?sci ?ru WHERE {{
  ?item wdt:P105 wd:Q7432 ;
        wdt:P225 ?sci ;
        wdt:P1843 ?ru .
  FILTER(LANG(?ru) = "ru")
  {extra}
}}
"""

WIKIDATA_LABELS = """
SELECT ?item ?label WHERE {{
  VALUES ?item {{ {items} }}
  ?item rdfs:label ?label . FILTER(LANG(?label) = "ru")
}}
"""


def sparql_retry(query: str, attempts: int = 3) -> list[dict]:
    for attempt in range(attempts):
        try:
            return sparql(query)
        except Exception as exc:  # noqa: BLE001
            if attempt == attempts - 1:
                raise
            log(f"  SPARQL request failed ({exc.__class__.__name__}); retrying")
            time.sleep(10 * (attempt + 1))
    raise AssertionError("unreachable")


def fetch_wikidata(dest: Path) -> None:
    """Fetch all species items with a Russian P1843 into a JSON cache.

    Not restricted to birds: the result set is small (~11k rows) and matching
    against AviList by scientific name restricts it anyway. Tries one query
    first; if it fails, splits the query by the first letter of the taxon name.
    Russian labels are then fetched only for taxa with several ru names (used
    to pick one); a failure there is not fatal.
    """
    log("  querying Wikidata SPARQL")
    try:
        bindings = sparql_retry(WIKIDATA_QUERY.format(extra=""), attempts=2)
    except Exception as exc:  # noqa: BLE001
        log(f"  single query failed ({exc.__class__.__name__}); splitting by initial letter")
        bindings = []
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            bindings += sparql_retry(WIKIDATA_QUERY.format(
                extra=f'FILTER(STRSTARTS(UCASE(STR(?sci)), "{letter}"))'))
        # names not starting with A-Z (rare; e.g. leading quote); best effort
        try:
            bindings += sparql_retry(WIKIDATA_QUERY.format(
                extra='FILTER(!REGEX(STR(?sci), "^[A-Za-z]"))'))
        except Exception as exc2:  # noqa: BLE001
            log(f"  non-A-Z query failed ({exc2.__class__.__name__}); ignoring")
    rows = [{
        "item": b["item"]["value"].rsplit("/", 1)[-1],
        "sci": b["sci"]["value"],
        "ru": b["ru"]["value"],
        "label": None,
    } for b in bindings]

    names_per_item = Counter(r["item"] for r in rows)
    multi = sorted(i for i, n in names_per_item.items() if n > 1)
    labels = {}
    try:
        for i in range(0, len(multi), 200):
            batch = " ".join(f"wd:{q}" for q in multi[i:i + 200])
            for b in sparql_retry(WIKIDATA_LABELS.format(items=batch)):
                labels[b["item"]["value"].rsplit("/", 1)[-1]] = b["label"]["value"]
    except Exception as exc:  # noqa: BLE001
        log(f"  WARNING: label query failed ({exc.__class__.__name__}); continuing without labels")
    for r in rows:
        r["label"] = labels.get(r["item"])

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    log(f"  cached {len(rows)} Wikidata rows ({len(multi)} items with several ru names)")


def load_wikidata(path: Path) -> dict[str, str]:
    """Return {sci_key: Russian name}. If several ru names exist for a taxon,
    prefer the one equal to the item's Russian label, else the first sorted."""
    rows = json.loads(path.read_text(encoding="utf-8"))
    by_sci: dict[str, list[tuple[str, str | None]]] = {}
    for row in rows:
        name = clean(row.get("ru"))
        if name:
            by_sci.setdefault(sci_key(row["sci"]), []).append((name, clean(row.get("label"))))
    out = {}
    for key, cands in by_sci.items():
        labels = {lab for _, lab in cands if lab}
        names = sorted({n for n, _ in cands})
        preferred = [n for n in names if n in labels]
        out[key] = (preferred or names)[0]
    return out


def load_overrides(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if (row.get("sci") or "").strip()]


# --------------------------------------------------------------------------- build

def apply_cascade(records, ioc, ebird, wikidata):
    for rec in records:
        key = sci_key(rec["sci"])
        for source, table in (("ioc", ioc), ("ebird", ebird), ("wikidata", wikidata)):
            if source == "ioc":
                name = (table.get(key) or {}).get("ru")
            else:
                name = table.get(key)
            if name:
                rec["ru"], rec["ru_source"] = name, source
                break


def apply_overrides(records, overrides) -> list[str]:
    """Apply manual overrides in file order; return a list of warnings."""
    by_key = {sci_key(r["sci"]): r for r in records}
    warnings = []
    for ov in overrides:
        rec = by_key.get(sci_key(ov["sci"]))
        field = (ov.get("field") or "").strip()
        value = clean(ov.get("value"))
        if rec is None:
            warnings.append(f"override for unknown species {ov['sci']!r}")
            continue
        if field not in FIELDS or field in ("ru_source", "ru_status"):
            warnings.append(f"override with unsupported field {field!r} for {ov['sci']!r}")
            continue
        if field == "seq":
            value = int(value) if value else rec["seq"]
        rec[field] = value
        if field == "ru":
            rec["ru_source"] = "manual" if value else None
    return warnings


def finalise(records):
    for rec in records:
        if rec["ru"] is None:
            rec["ru_source"], rec["ru_status"] = None, "missing"
        elif rec["ru_source"] in ("ioc", "manual"):
            rec["ru_status"] = "ok"
        else:
            rec["ru_status"] = "ok_fallback"


def write_json(records):
    payload = json.dumps([{k: r[k] for k in FIELDS} for r in records],
                         ensure_ascii=False, separators=(",", ":"))
    OUT_JSON.write_text(payload, encoding="utf-8")
    OUT_DOCS_JSON.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUT_JSON, OUT_DOCS_JSON)


def md_table(rows, headers) -> list[str]:
    def esc(v):
        return "" if v is None else str(v).replace("|", "\\|")
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(esc(v) for v in row) + " |" for row in rows]
    return out


def write_report(records, ioc, ebird, wikidata, status, warnings) -> dict:
    avi_keys = {sci_key(r["sci"]) for r in records}
    total = len(records)
    by_source = Counter(r["ru_source"] for r in records)
    missing = [r for r in records if r["ru"] is None]
    extinct = Counter(r["extinct"] for r in records if r["extinct"])
    not_in_ioc = [r for r in records if sci_key(r["sci"]) not in ioc]
    ioc_only = sorted((v for k, v in ioc.items() if k not in avi_keys), key=lambda v: v["sci"])
    diffs = []
    for r in records:
        key = sci_key(r["sci"])
        a, b = (ioc.get(key) or {}).get("ru"), ebird.get(key)
        if a and b and a.casefold() != b.casefold():
            diffs.append((r["sci"], a, b))

    counts = {
        "total": total,
        "ru_present": total - len(missing),
        "ioc": by_source.get("ioc", 0),
        "ebird": by_source.get("ebird", 0),
        "wikidata": by_source.get("wikidata", 0),
        "manual": by_source.get("manual", 0),
        "missing": len(missing),
        "extinct": extinct.get("extinct", 0),
        "extinct_in_wild": extinct.get("extinct_in_wild", 0),
        "possibly_extinct": extinct.get("possibly_extinct", 0),
        "not_in_ioc": len(not_in_ioc),
        "ioc_not_in_avilist": len(ioc_only),
        "ioc_ebird_diff": len(diffs),
    }

    L = ["# Build report", ""]
    L += ["## Sources", ""]
    for name, state in status.items():
        L.append(f"- **{name}**: {state}")
    if warnings:
        L += ["", "### Override warnings", ""] + [f"- {w}" for w in warnings]
    L += ["", "## Counts", ""]
    L += md_table([
        ("Total species (AviList)", total),
        ("Russian name present", counts["ru_present"]),
        ("— from IOC", counts["ioc"]),
        ("— from eBird", counts["ebird"]),
        ("— from Wikidata", counts["wikidata"]),
        ("— manual override", counts["manual"]),
        ("Russian name missing", counts["missing"]),
        ("Extinct", counts["extinct"]),
        ("Extinct in the wild", counts["extinct_in_wild"]),
        ("Possibly extinct", counts["possibly_extinct"]),
        ("AviList species not in IOC (exact name)", counts["not_in_ioc"]),
        ("IOC species not in AviList (exact name)", counts["ioc_not_in_avilist"]),
        ("IOC vs eBird Russian name differs", counts["ioc_ebird_diff"]),
    ], ["Metric", "Count"])

    L += ["", f"## AviList species not found in IOC ({len(not_in_ioc)})", ""]
    L += md_table([(r["sci"], r["en"], r["ru_source"] or "—") for r in not_in_ioc],
                  ["Scientific name", "English", "ru_source"])
    L += ["", f"## Species with no Russian name anywhere ({len(missing)})", ""]
    L += md_table([(r["sci"], r["en"]) for r in missing], ["Scientific name", "English"])
    L += ["", f"## IOC species not found in AviList ({len(ioc_only)})", ""]
    L += md_table([(v["sci"], v["en"], v["ru"]) for v in ioc_only],
                  ["IOC scientific name", "English (IOC)", "Russian (IOC)"])
    L += ["", f"## IOC and eBird Russian names differ ({len(diffs)})", "",
          "Report only; the JSON always prefers IOC. First 50 examples:", ""]
    L += md_table(diffs[:50], ["Scientific name", "IOC", "eBird"])
    OUT_REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")
    return counts


# --------------------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--offline", action="store_true", help="use only files already on disk")
    g.add_argument("--fetch", action="store_true", help="force re-download of all sources")
    args = ap.parse_args()
    mode = "offline" if args.offline else "fetch" if args.fetch else "default"
    log(f"mode: {mode}")

    status = {}
    ensure_file(AVILIST_PATH, AVILIST_URL, mode, required=True)
    ensure_file(IOC_PATH, IOC_URL, mode, required=True)
    status["AviList v2025b"] = f"`{AVILIST_PATH.relative_to(ROOT)}`"
    status["IOC Multilingual 15.2"] = f"`{IOC_PATH.relative_to(ROOT)}`"

    ebird = {}
    if ensure_file(EBIRD_PATH, EBIRD_URL, mode, required=False):
        ebird = load_ebird(EBIRD_PATH)
        status["eBird taxonomy (ru)"] = f"`{EBIRD_PATH.relative_to(ROOT)}`, {len(ebird)} species with Cyrillic names"
    else:
        status["eBird taxonomy (ru)"] = "SKIPPED (not available)"

    wikidata = {}
    if mode == "fetch" or (mode == "default" and not WIKIDATA_PATH.exists()):
        try:
            fetch_wikidata(WIKIDATA_PATH)
        except Exception as exc:  # noqa: BLE001
            log(f"  WARNING: Wikidata query failed: {exc}")
    if WIKIDATA_PATH.exists():
        wikidata = load_wikidata(WIKIDATA_PATH)
        status["Wikidata P1843 (ru)"] = f"`{WIKIDATA_PATH.relative_to(ROOT)}`, {len(wikidata)} taxa"
    else:
        status["Wikidata P1843 (ru)"] = "SKIPPED (unreachable or no cache)"

    log("loading AviList and IOC")
    records = load_avilist(AVILIST_PATH)
    ioc = load_ioc(IOC_PATH)

    apply_cascade(records, ioc, ebird, wikidata)
    warnings = apply_overrides(records, load_overrides(OVERRIDES_PATH))
    finalise(records)

    write_json(records)
    counts = write_report(records, ioc, ebird, wikidata, status, warnings)

    print(f"Wrote {OUT_JSON.relative_to(ROOT)}, {OUT_DOCS_JSON.relative_to(ROOT)}, {OUT_REPORT.relative_to(ROOT)}")
    for name, state in status.items():
        print(f"  {name}: {state}")
    for k, v in counts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
