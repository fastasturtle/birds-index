#!/usr/bin/env python3
"""Build data/species.json: a trilingual (ru / en / Latin) index of world bird species.

Backbone: AviList v2025b (species only). Russian names are taken from a cascade
of sources, matched by exact (normalised) scientific name:

    1. IOC World Bird List Multilingual 15.2   -> ru_source "ioc"
    2. eBird taxonomy API, locale=ru            -> ru_source "ebird"
    3. Wikidata P1843 (taxon common name, ru)   -> ru_source "wikidata"
    4. data/overrides.csv (applied last)        -> ru_source "manual"

Then the Russian name is normalised: synonyms ("Хохлатый фазан, чир",
"Гуменник (лесной гуменник)") go from `ru` to the list `ru_alt`, and index
fields are computed: `ru_head` (leading noun), `ru_book` (book spelling with a
lower-case first letter), `en_head` (last word of the English name). `ru_ebird`
keeps the eBird/Clements Russian name when it differs from the final `ru`
(normalised comparison; suppressed by an override `field = ru_ebird`, value "-").

Former scientific names go to `sci_prev` (list of {name, kind, sources}) and
`sci_book_prev` (one name for the book's "= ..." line): from
data/raw/IOC_15.2_vs_other_lists.xlsx (IOC 15.2/15.1, Clements 2025, BirdLife
v10, H&M 4.1, HBW, Peters, S&M 1993; rows joined on the AviList column), from
historical eBird taxonomies 2015-2024 (cached in data/cache/), and from
overrides `field = sci_prev`.

It also writes data/taxa.json: orders and families (in systematic order) with
Russian names from the ZMMU passerine spreadsheet (family header rows) ->
"zmmu", Wikidata (P1843 / ru label of the order or family item) -> "wikidata",
and data/overrides.csv (sci = order or family name, field = ru) -> "manual".

Usage:
    uv run scripts/build.py            # download whatever is missing, then build
    uv run scripts/build.py --offline  # use only files already on disk
    uv run scripts/build.py --fetch    # force re-download of every source
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import re
import shutil
import sys
import time
import unicodedata
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
WIKIDATA_TAXA_PATH = CACHE / "wikidata-taxa-ru.json"
ZMMU_PASSERINE_PATH = RAW / "Birds_rus_names_passerine.xlsx"
VS_LISTS_PATH = RAW / "IOC_15.2_vs_other_lists.xlsx"
OVERRIDES_PATH = DATA / "overrides.csv"
OUT_JSON = DATA / "species.json"
OUT_DOCS_JSON = ROOT / "docs" / "data" / "species.json"
OUT_TAXA_JSON = DATA / "taxa.json"
OUT_DOCS_TAXA_JSON = ROOT / "docs" / "data" / "taxa.json"
OUT_REPORT = DATA / "report.md"

AVILIST_URL = "https://www.avilist.org/wp-content/uploads/2026/06/AviList-v2025b-10Jun2026-extended.xlsx"
IOC_URL = "https://worldbirdnames.org/Multiling%20IOC%2015.2.xlsx"
EBIRD_URL = "https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json&locale=ru&cat=species"
WIKIDATA_SPARQL = "https://query.wikidata.org/sparql"
ZMMU_PASSERINE_URL = "https://zmmu.msu.ru/files/publications/Birds_rus_names_passerine.xlsx"
VS_LISTS_URL = "https://www.worldbirdnames.org/IOC_15.2_vs_other_lists.xlsx"
EBIRD_HISTORY_URL = "https://api.ebird.org/v2/ref/taxonomy/ebird"

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
    "id", "seq", "order", "family", "family_en", "sci", "authority", "auth", "en",
    "ru", "ru_alt", "ru_head", "ru_head_source", "ru_book", "en_head", "ru_ebird",
    "ru_source", "ru_status", "ioc_sci", "sci_prev", "sci_book_prev", "extinct", "iucn",
]
# Fields computed by normalise_names / add_ebird_names / build_sci_prev; only
# ru_alt, ru_head, ru_ebird (value "-" = suppress) and sci_prev ("Genus species"
# adds, "-Genus species" removes) may be given in overrides.csv (handled specially).
DERIVED_FIELDS = {"ru_head_source", "ru_book", "en_head", "sci_book_prev"}


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


AUTH_YEAR = re.compile(r"(.*?),\s*(\d{4}[a-z]?)")
AUTH_SUFFIX = re.compile(r"\b(Jr|Sr)\.?$")
AUTH_TRAILING_INITIALS = re.compile(r"\s+[A-Z]{1,3}$")


def normalise_authority(raw: str | None) -> str | None:
    """AviList authority -> conventional zoological form without initials.

    "Linnaeus, C, 1758" -> "Linnaeus, 1758"; "(Latham, J, 1790)" -> "(Latham, 1790)";
    two authors "A & B, year"; three or more "A, B & C, year". Authors are
    separated by ";" and written "Surname, Initials" (Jr/Sr kept as a suffix);
    an author without a comma is kept, minus trailing initials ("Zhao C" ->
    "Zhao"), so full names such as "Liu Yang" or "Suparno" survive. Strings
    that do not end in a year are returned unchanged.
    """
    if raw is None:
        return None
    text = raw.strip()
    paren = text.startswith("(") and text.endswith(")")
    if paren:
        text = text[1:-1].strip()
    m = AUTH_YEAR.fullmatch(text)
    if not m:
        return raw
    names = []
    for part in m.group(1).split(";"):
        part = part.strip()
        if "," in part:
            surname, initials = (x.strip() for x in part.rsplit(",", 1))
            suffix = AUTH_SUFFIX.search(initials)
            if suffix:
                surname = f"{surname} {suffix.group(1)}"
        else:
            surname = AUTH_TRAILING_INITIALS.sub("", part)
        names.append(surname)
    if len(names) == 1:
        authors = names[0]
    else:
        authors = ", ".join(names[:-1]) + " & " + names[-1]
    out = f"{authors}, {m.group(2)}"
    return f"({out})" if paren else out


def _test_normalise_authority() -> None:
    cases = {
        "Linnaeus, C, 1758": "Linnaeus, 1758",
        "(Latham, J, 1790)": "(Latham, 1790)",
        "Sclater, PL; von Hochstetter, F, 1861": "Sclater & von Hochstetter, 1861",
        "Tennyson, AJD; Palma, RL; Robertson, HA; Worthy, TH; Gill, BJ, 2003":
            "Tennyson, Palma, Robertson, Worthy & Gill, 2003",
        "(d'Orbigny, ACVMD; de Lafresnaye, NFAA, 1837)": "(d'Orbigny & de Lafresnaye, 1837)",
        "Phelps, WH Sr; Phelps, WH Jr, 1946": "Phelps Sr & Phelps Jr, 1946",
        "Zhou F; Jiang A, 2008": "Zhou & Jiang, 2008",
        "Indrawan, M; Rasmussen, PC; Sunarto, 2008": "Indrawan, Rasmussen & Sunarto, 2008",
        "(Oustalet, J-FÉ, 1880)": "(Oustalet, 1880)",
        "Mahood, SP; Hong Chamnan; Poole, CM, 2013": "Mahood, Hong Chamnan & Poole, 2013",
    }
    for raw, want in cases.items():
        got = normalise_authority(raw)
        assert got == want, f"normalise_authority({raw!r}) = {got!r}, want {want!r}"
    assert normalise_authority(None) is None


LEFTOVER_INITIALS = re.compile(r", [A-Z]{1,3}[,;)]|, [A-Z]{1,3}$")


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
            "auth": normalise_authority(clean(row.get("Authority"))),
            "en": clean(row.get("English_name_AviList")),
            "ru": None,
            "ru_alt": [],
            "ru_ebird": None,
            "ru_head": None,
            "ru_head_source": None,
            "ru_book": None,
            "en_head": None,
            "ru_source": None,
            "ru_status": "missing",
            "ioc_sci": None,  # exact matching only in this version
            "sci_prev": [],
            "sci_book_prev": None,
            "_ebird_code": clean(row.get("Species_code_Cornell_Lab")),
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


# ---- previous scientific names (sci_prev)

# Columns of IOC_15.2_vs_other_lists.xlsx (0-based) and a fragment of each
# header, checked on load so that a changed layout fails loudly.
VS_COLUMNS = {
    "ioc152": (1, "(v15.2)"),
    "rank": (2, "Rank"),
    "notes": (3, "Notes"),
    "avilist": (4, "AviList"),
    "clements2025": (6, "Clements"),
    "birdlife10": (7, "BirdLife"),
    "hm4": (9, "Howard and Moore"),
    "hbw": (10, "Handbook of the Birds of the World, Lynx"),
    "peters": (11, "Peters"),
    "tif": (12, "TiF"),
    "gaudin": (13, "Gaudin"),
    "sm93": (14, "Sibley"),
    "ioc151": (15, "(v15.1)"),
}
# Lists taken from the comparison file (TiF and Gaudin are alternative
# classifications, not former ones, and are not used).
VS_LISTS = ("ioc152", "ioc151", "clements2025", "birdlife10", "hm4", "hbw", "peters", "sm93")
EBIRD_HISTORY_YEARS = (2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024)  # no 2020 version
# "Freshness" of a source: lower = more recent. Used to sort sci_prev and its sources.
PREV_SOURCE_ORDER = (["override", "ioc15.2", "ioc15.1", "clements2025", "birdlife10"]
                     + [f"ebird{y}" for y in sorted(EBIRD_HISTORY_YEARS, reverse=True)]
                     + ["hm4", "hbw", "sm93", "peters"])
PREV_SOURCE_RANK = {s: i for i, s in enumerate(PREV_SOURCE_ORDER)}
VS_SOURCE_CODE = {"ioc152": "ioc15.2", "ioc151": "ioc15.1"}
PREV_KINDS = ("genus", "genus_ending", "epithet", "spelling", "concept")
BOOK_PREV_KINDS = {"genus", "genus_ending", "epithet"}

LIGATURES = str.maketrans({"æ": "ae", "Æ": "Ae", "œ": "oe", "Œ": "Oe", "ß": "ss",
                           "“": "", "”": "", '"': "", "'": "", "’": "", "?": "", ".": ""})
OLD_GENUS = re.compile(r"[A-Z][a-z]+")
OLD_EPITHET = re.compile(r"[a-z](-[a-z]+)?[a-z]*")
EPITHET_ENDINGS = re.compile(r"(orum|arum|ius|ior|ium|ia|us|um|is|es|os|on|ae|ii|er|ra|rum|re|a|e|i|o)$")


def parse_old_name(raw) -> list[str] | None:
    """Normalise a name as written in an older checklist; return its words.

    Diacritics and ligatures are dropped ("Aërornis" -> "Aerornis",
    "florentiæ" -> "florentiae"), as are quotes, "?" and dots. A capitalised
    word in parentheses is a subgenus and is dropped; a lower-case one is
    Peters's notation for the species a form belongs to and becomes the middle
    word of a trinomial ("Collocalia (francica?) elaphra" -> Collocalia
    francica elaphra). Hyphens go ("Hirund-apus", "albo-gularis"), except after a single
    letter in an epithet ("v-nigrum").
    Returns None if the result is not a binomial or trinomial.
    """
    if raw is None:
        return None
    text = unicodedata.normalize("NFKD", str(raw).translate(LIGATURES))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))

    def paren(m):
        inner = m.group(1).strip()
        return " " if inner[:1].isupper() else f" {inner} "
    text = re.sub(r"\(([^)]*)\)", paren, text)
    words = text.split()
    if not 2 <= len(words) <= 3:
        return None
    words = [words[0].replace("-", "")] + [w.lower() if len(w.split("-")[0]) == 1 else w.lower().replace("-", "")
                          for w in words[1:]]
    if not OLD_GENUS.fullmatch(words[0]) or not all(OLD_EPITHET.fullmatch(w) for w in words[1:]):
        return None
    return words


def _epithet_stem(ep: str) -> str:
    return EPITHET_ENDINGS.sub("", ep)


def _similar(a: str, b: str, ratio: float) -> bool:
    return difflib.SequenceMatcher(None, a, b).ratio() >= ratio


def classify_prev(old: str, sci: str) -> str:
    """Kind of a former binomial `old` relative to the current name `sci`.

    genus        other genus, same epithet (Anas formosa -> Sibirionetta formosa)
    genus_ending other genus, epithet changed only to agree in gender, or a
                 spelling variant of it (Nyctea scandiaca -> Bubo scandiacus)
    epithet      other epithet (Apteryx haastii -> Apteryx maxima), also with
                 another genus (Ptilinopus bernsteinii -> Megaloprepia formosa)
    spelling     same genus (or a spelling variant of it), epithet differs
                 only in its ending or spelling (Emblema modesta -> E. modestum)
    """
    og, oe = old.split()
    ng, ne = sci.split()
    if oe == ne:
        ep = "same"
    elif _epithet_stem(oe) == _epithet_stem(ne) or (
            min(len(oe), len(ne)) >= 5 and _similar(oe, ne, 0.8)):
        ep = "ending"
    else:
        ep = "other"
    same_genus = og == ng or (min(len(og), len(ng)) >= 5 and _similar(og, ng, 0.85))
    if ep == "other":
        return "epithet"
    if same_genus:
        return "spelling"
    return "genus" if ep == "same" else "genus_ending"


def _test_prev() -> None:
    assert parse_old_name("Collocalia (francica?) elaphra") == ["Collocalia", "francica", "elaphra"]
    assert parse_old_name("Parus (Periparus) ater") == ["Parus", "ater"]
    assert parse_old_name("Aërornis senex") == ["Aerornis", "senex"]
    assert parse_old_name("Hirund-apus ernsti") == ["Hirundapus", "ernsti"]
    assert parse_old_name("Somateria mollissima v-nigrum") == ["Somateria", "mollissima", "v-nigrum"]
    assert parse_old_name("Eurostopodus albo-gularis") == ["Eurostopodus", "albogularis"]
    assert classify_prev("Anas formosa", "Sibirionetta formosa") == "genus"
    assert classify_prev("Nyctea scandiaca", "Bubo scandiacus") == "genus_ending"
    assert classify_prev("Chlidonias nigra", "Chlidonias niger") == "spelling"
    assert classify_prev("Elaenia cherrei", "Elaenia cherriei") == "spelling"
    assert classify_prev("Apteryx haastii", "Apteryx maxima") == "epithet"
    assert classify_prev("Ptilinopus bernsteinii", "Megaloprepia formosa") == "epithet"
    assert classify_prev("Carduelis spinus", "Spinus spinus") == "genus"


def load_vs_lists(path: Path, avi_names: set[str]) -> tuple[dict, list, Counter]:
    """Former names from IOC_15.2_vs_other_lists.xlsx, keyed by AviList name.

    The sheet aligns species and subspecies rows of IOC 15.2 with AviList and
    older lists. Rows are grouped into blocks: a species row and the
    subspecies rows under it. A block is linked to the AviList species in its
    own AviList cell; failing that (a species of IOC or an older list that
    AviList lumps), to the single AviList species whose subspecies fill the
    AviList cells of the block's rows. Collected (name, kind, source):

    * linked directly: every list's binomial that differs from the AviList
      name, classified by classify_prev; a trinomial (the list kept the
      species as a subspecies of another) is `concept`;
    * linked directly, subspecies rows without an AviList entry: trinomials
      whose last epithet is the species' epithet and whose species epithet is
      another one ("Struthio camelus molybdophanes") -> `concept`;
    * linked through subspecies: the list's species name (a species now
      included in the AviList one, e.g. Corvus cornix in Corvus corone) ->
      `concept`.

    Returns ({avilist_sci: [(name, kind, source)]}, unlinked blocks,
    unparsed [(avilist_sci, source, raw)], stats).
    """
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = ws.iter_rows(values_only=True)
    header = next(rows)
    for key, (col, frag) in VS_COLUMNS.items():
        if frag not in str(header[col] or ""):
            raise SystemExit(f"{path.name}: column {col} should be {key} ({frag!r}), "
                             f"found {str(header[col])[:60]!r}")
    blocks: list[list] = []
    for row in rows:
        rank = clean(row[VS_COLUMNS["rank"][0]])
        if rank == "species":
            blocks.append([row, []])
        elif rank and blocks:
            blocks[-1][1].append(row)
    wb.close()

    def cell(row, key):
        return clean(row[VS_COLUMNS[key][0]])

    out: dict[str, list] = {}
    unlinked, unparsed = [], []
    stats: Counter = Counter()
    for srow, ssp_rows in blocks:
        avi = cell(srow, "avilist")
        if avi:
            if avi not in avi_names:
                stats["avilist name not in AviList"] += 1
                unlinked.append((srow, "AviList cell not an AviList species"))
                continue
            stats["linked directly"] += 1
            g, e = avi.split()
            for key in VS_LISTS:
                raw = cell(srow, key)
                words = parse_old_name(raw)
                if raw and words is None:
                    unparsed.append((avi, VS_SOURCE_CODE.get(key, key), raw))
                if not words:
                    continue
                name = " ".join(words)
                if len(words) == 3:
                    out.setdefault(avi, []).append((name, "concept", key))
                elif name != avi:
                    out.setdefault(avi, []).append((name, classify_prev(name, avi), key))
            stem = _epithet_stem(e)
            for row in ssp_rows:
                if cell(row, "avilist"):
                    continue
                for key in VS_LISTS:
                    words = parse_old_name(cell(row, key))
                    if (words and len(words) == 3 and _epithet_stem(words[2]) == stem
                            and _epithet_stem(words[1]) != stem):
                        out.setdefault(avi, []).append((" ".join(words), "concept", key))
            continue
        parents = {" ".join(str(cell(r, "avilist")).split()[:2])
                   for r in ssp_rows if cell(r, "avilist")}
        parents &= avi_names
        if len(parents) != 1:
            stats["unlinked species rows"] += 1
            unlinked.append((srow, "no AviList species" if not parents
                             else "several AviList species: " + ", ".join(sorted(parents))))
            continue
        target = parents.pop()
        stats["linked through subspecies"] += 1
        for key in VS_LISTS:
            words = parse_old_name(cell(srow, key))
            if words and " ".join(words) != target:
                out.setdefault(target, []).append((" ".join(words), "concept", key))
    return out, unlinked, unparsed, stats


def ebird_history_path(year: int) -> Path:
    return CACHE / f"ebird-taxonomy-{year}.json"


def fetch_ebird_history(year: int, dest: Path) -> None:
    """Fetch one historical eBird taxonomy (species only); cache name and code."""
    log(f"  downloading eBird taxonomy {year}")
    r = requests.get(EBIRD_HISTORY_URL, params={"fmt": "json", "cat": "species", "version": year},
                     headers={"User-Agent": USER_AGENT}, timeout=300)
    r.raise_for_status()
    data = [{"sciName": x["sciName"], "speciesCode": x["speciesCode"]}
            for x in r.json() if x.get("category") == "species"]
    if not data:
        raise ValueError(f"eBird taxonomy {year} is empty")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def load_ebird_history(records, mode: str) -> tuple[dict, dict, Counter]:
    """Former names from historical eBird taxonomies, keyed by AviList name.

    Versions are walked from the newest down. In each, a species is joined on
    its eBird species code (AviList `Species_code_Cornell_Lab`); if the code
    is not there (codes change with splits: norgos -> norgos1), on the name
    the species had in the next newer version (at first, the current AviList
    name). Group ("[... Group]") and subspecies entries are not species and
    are skipped. Returns ({sci: [(name, kind, source)]}, {year: status}, stats).
    """
    status = {}
    versions = []
    for year in sorted(EBIRD_HISTORY_YEARS, reverse=True):
        path = ebird_history_path(year)
        if mode == "fetch" or (mode == "default" and not path.exists()):
            try:
                fetch_ebird_history(year, path)
            except Exception as exc:  # noqa: BLE001 - keep the old cache or skip
                log(f"  WARNING: eBird taxonomy {year} not downloaded: {exc}")
        if not path.exists():
            status[year] = "SKIPPED (not available)"
            continue
        by_code, by_sci = {}, set()
        for x in json.loads(path.read_text(encoding="utf-8")):
            name = clean(x.get("sciName"))
            if not name or "[" in name or len(name.split()) != 2:
                continue
            by_code[x["speciesCode"]] = name
            by_sci.add(name)
        versions.append((year, path, by_code, by_sci))

    out: dict[str, list] = {}
    stats: Counter = Counter()
    for year, path, by_code, by_sci in versions:
        stats[year] = 0
    for rec in records:
        last = rec["sci"]
        for year, path, by_code, by_sci in versions:
            name = by_code.get(rec["_ebird_code"]) if rec["_ebird_code"] else None
            if name is None and last in by_sci:
                name = last
                stats[f"ebird{year}: code not found, joined by the newer name"] += 1
            if name is None:
                continue
            stats[year] += 1
            last = name
            if name != rec["sci"]:
                out.setdefault(rec["sci"], []).append(
                    (name, classify_prev(name, rec["sci"]), f"ebird{year}"))
    for year, path, by_code, by_sci in versions:
        status[year] = (f"`{path.relative_to(ROOT)}`, {len(by_code)} species, "
                        f"{stats.pop(year)} AviList species joined")
    return out, status, stats


def build_sci_prev(records, collected: list[dict]) -> Counter:
    """Fill sci_prev and sci_book_prev from the collected former names.

    A name that is the current name of another AviList species is not a
    synonym but that species (a broader concept in the old list): `concept`.
    The same name from several sources is one entry; if one source makes it
    a `concept` (in practice: the comparison file shows the old list's
    species was broader, while an older eBird version reused the species
    code under that name), it stays a concept. Overrides (`field = sci_prev`) add
    names ("Genus species; Genus species", source "override") or remove them
    ("-Genus species"), after everything else.
    """
    current = {r["sci"] for r in records}
    stats: Counter = Counter()
    conflicts: set[tuple[str, str]] = set()
    ebird_concepts: set[tuple[str, str]] = set()
    homonyms: set[tuple[str, str]] = set()
    holders: dict[str, set[str]] = {}  # former name -> AviList species it is collected for
    for src in collected:
        for sci, items in src.items():
            for name, _, _ in items:
                holders.setdefault(name, set()).add(sci)
    by_stem: dict[str, set[str]] = {}
    for sci in current:
        by_stem.setdefault(_epithet_stem(sci.split()[1]), set()).add(sci)

    def ebird_concept(name: str, sci: str) -> bool:
        """An older eBird name with another epithet that belongs to another
        AviList species (same epithet and the old genus, the current genus,
        or that species also has this former name): eBird kept the species
        code for one daughter of a split (norgos = Accipiter gentilis is now
        Astur atricapillus), so the name is a broader concept, not a synonym."""
        og, oe = name.split()
        return any(other != sci and (other.split()[0] in (og, sci.split()[0])
                                     or other in holders.get(name, ()))
                   for other in by_stem.get(_epithet_stem(oe), ()))
    for rec in records:
        merged: dict[str, dict] = {}
        items = [it for src in collected for it in src.get(rec["sci"], [])]
        items += [(name, None, "override") for name in rec.get("_prev_add", [])]
        for name, kind, source in items:
            source = VS_SOURCE_CODE.get(source, source)
            if kind is None:  # override: classify like any other name
                kind = "concept" if len(name.split()) == 3 else classify_prev(name, rec["sci"])
            if kind != "concept" and name in current:
                kind = "concept"
                homonyms.add((rec["sci"], name))
            elif kind == "epithet" and source.startswith("ebird") and ebird_concept(name, rec["sci"]):
                kind = "concept"
                ebird_concepts.add((rec["sci"], name))
            ent = merged.setdefault(name, {"name": name, "kind": kind, "sources": []})
            if ent["kind"] != kind and "concept" in (ent["kind"], kind):
                ent["kind"] = "concept"
                conflicts.add((rec["sci"], name))
            if source not in ent["sources"]:
                ent["sources"].append(source)
        for name in rec.get("_prev_del", []):
            if merged.pop(name, None) is None:
                stats["override removals with no effect"] += 1
                rec.setdefault("_prev_del_unused", []).append(name)
        for ent in merged.values():
            ent["sources"].sort(key=PREV_SOURCE_RANK.__getitem__)
        rec["sci_prev"] = sorted(merged.values(),
                                 key=lambda e: (PREV_SOURCE_RANK[e["sources"][0]], e["name"]))
        rec["sci_book_prev"] = next((e["name"] for e in rec["sci_prev"]
                                     if e["kind"] in BOOK_PREV_KINDS), None)
    stats["names that are a concept in one source, a synonym in another -> concept"] = len(conflicts)
    stats["current names of another species -> concept"] = len(homonyms)
    stats["eBird names of another species kept under a reused code -> concept"] = len(ebird_concepts)
    return stats


# ---- order / family names

ZMMU_HEADER = re.compile(r"([A-Z][a-z]+idae)\b\s*[-–—]?\s*(.*)")
# Stressed vowels in the ZMMU file are Latin look-alikes: "Стрелкú" (ú = и́),
# "Яхý" (ý = у́).
STRESS_MARKS = str.maketrans({"á": "а", "é": "е", "ó": "о", "ú": "и", "ý": "у", "í": "и",
                              "\u0301": None})


def normalise_taxon_ru(name: str | None) -> str | None:
    """Strip whitespace, drop stress marks, capitalise the first letter."""
    name = clean((name or "").translate(STRESS_MARKS))
    if not name:
        return None
    return name[0].upper() + name[1:]


def load_zmmu_families(path: Path, species_family: dict[str, str],
                       families: set[str]) -> tuple[dict[str, str], list[str]]:
    """Return ({family_key: Russian name}, warnings) from the ZMMU passerine list.

    Family header rows look like "Pittidae - Питтовые" (alternative names in
    parentheses are dropped). Each header is checked against the AviList
    families of the species listed under it: if the header's Latin name is not
    an AviList family, or none of those species belongs to it (slips such as
    a misspelt or wrongly repeated header), the name is given to the majority
    family of those species instead, but only if that family has no header of
    its own.
    """
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    blocks: list[list] = []  # [latin, russian, Counter of AviList families]
    for row in ws.iter_rows(values_only=True):
        a = clean(row[0]) if row else None
        rest = [clean(v) for v in row[1:4]] if row else []
        if not a:
            continue
        m = ZMMU_HEADER.fullmatch(a)
        if m and not any(rest):
            ru = re.sub(r"\([^)]*\)", "", m.group(2))
            blocks.append([m.group(1), normalise_taxon_ru(ru), Counter()])
        elif blocks and sci_key(a) in species_family:
            blocks[-1][2][species_family[sci_key(a)]] += 1
    wb.close()

    out: dict[str, str] = {}
    warnings: list[str] = []
    deferred = []
    for latin, ru, fams in blocks:
        if not ru:
            continue
        majority = fams.most_common(1)[0][0] if fams else None
        if latin in families and (not fams or fams[latin] > 0):
            out.setdefault(latin.lower(), ru)
        else:
            deferred.append((latin, ru, majority))
    for latin, ru, majority in deferred:
        if majority and majority.lower() not in out:
            out[majority.lower()] = ru
            warnings.append(f"ZMMU header {latin!r} ({ru}) lists {majority} species; "
                            f"used for {majority}")
        else:
            warnings.append(f"ZMMU header {latin!r} ({ru}) not used "
                            f"(majority AviList family of its species: {majority or 'none'})")
    return out, warnings


WIKIDATA_TAXA_QUERY = """
SELECT ?item ?sci ?rank ?ru ?label ?aves WHERE {{
  VALUES ?sci {{ {names} }}
  VALUES ?rank {{ wd:Q36602 wd:Q35409 }}
  ?item wdt:P225 ?sci ;
        wdt:P105 ?rank .
  OPTIONAL {{ ?item wdt:P1843 ?ru . FILTER(LANG(?ru) = "ru") }}
  OPTIONAL {{ ?item rdfs:label ?label . FILTER(LANG(?label) = "ru") }}
  BIND(EXISTS {{ ?item wdt:P171+ wd:Q5113 }} AS ?aves)
}}
"""


def fetch_wikidata_taxa(dest: Path, names: list[str]) -> None:
    """One SPARQL query (VALUES list) for the order/family items; cache raw rows."""
    log(f"  querying Wikidata SPARQL for {len(names)} order/family names")
    values = " ".join(json.dumps(n) for n in names)
    bindings = sparql_retry(WIKIDATA_TAXA_QUERY.format(names=values), attempts=2)
    rows = [{
        "item": b["item"]["value"].rsplit("/", 1)[-1],
        "sci": b["sci"]["value"],
        "rank": "order" if b["rank"]["value"].endswith("/Q36602") else "family",
        "ru": b.get("ru", {}).get("value"),
        "label": b.get("label", {}).get("value"),
        "aves": b.get("aves", {}).get("value") == "true",
    } for b in bindings]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({"queried": sorted(names), "rows": rows},
                               ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"  cached {len(rows)} Wikidata order/family rows")


def load_wikidata_taxa(path: Path) -> dict[tuple[str, str], str]:
    """Return {(rank, sci_key): Russian name}.

    Items placed under Aves win over homonyms elsewhere. P1843 (ru) is
    preferred, choosing the value equal to the ru label if there are several
    (else the first sorted); otherwise the ru label if it contains Cyrillic.
    """
    rows = json.loads(path.read_text(encoding="utf-8"))["rows"]
    items: dict[tuple[str, str], dict[str, dict]] = {}
    for r in rows:
        it = items.setdefault((r["rank"], sci_key(r["sci"])), {}).setdefault(
            r["item"], {"ru": set(), "label": None, "aves": False})
        if r.get("ru"):
            it["ru"].add(normalise_taxon_ru(r["ru"]))
        if r.get("label"):
            it["label"] = normalise_taxon_ru(r["label"])
        it["aves"] = it["aves"] or bool(r.get("aves"))
    out = {}
    for key, cands in items.items():
        pool = [c for c in cands.values() if c["aves"]] or list(cands.values())
        for c in sorted(pool, key=lambda c: (not c["ru"], not c["label"])):
            names = sorted(c["ru"])
            if names:
                out[key] = c["label"] if c["label"] in names else names[0]
                break
            if c["label"] and CYRILLIC.search(c["label"]):
                out[key] = c["label"]
                break
    return out


def build_taxa(records) -> dict[str, list[dict]]:
    """Orders and families with species counts and first sequence number."""
    orders: dict[str, dict] = {}
    families: dict[str, dict] = {}
    for r in records:
        o = orders.setdefault(r["order"], {"sci": r["order"], "ru": None, "ru_source": None,
                                           "seq": r["seq"], "count": 0})
        o["seq"] = min(o["seq"], r["seq"])
        o["count"] += 1
        f = families.setdefault(r["family"], {"sci": r["family"], "en": r["family_en"],
                                              "ru": None, "ru_source": None,
                                              "order": r["order"], "seq": r["seq"],
                                              "count": 0})
        f["seq"] = min(f["seq"], r["seq"])
        f["count"] += 1
    return {"orders": sorted(orders.values(), key=lambda t: t["seq"]),
            "families": sorted(families.values(), key=lambda t: t["seq"])}


def apply_taxa_names(taxa, zmmu: dict[str, str], wikidata_taxa: dict) -> None:
    for rank, items in (("order", taxa["orders"]), ("family", taxa["families"])):
        for t in items:
            key = sci_key(t["sci"])
            for source, name in (("zmmu", zmmu.get(key) if rank == "family" else None),
                                 ("wikidata", wikidata_taxa.get((rank, key)))):
                if name:
                    t["ru"], t["ru_source"] = name, source
                    break


def apply_taxa_overrides(taxa, overrides) -> list[str]:
    by_key = {sci_key(t["sci"]): t for t in taxa["orders"] + taxa["families"]}
    warnings = []
    for ov in overrides:
        t = by_key[sci_key(ov["sci"])]
        field = (ov.get("field") or "").strip()
        if field != "ru":
            warnings.append(f"override with unsupported field {field!r} for taxon {ov['sci']!r}")
            continue
        t["ru"] = normalise_taxon_ru(ov.get("value"))
        t["ru_source"] = "manual" if t["ru"] else None
    return warnings


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


def apply_overrides(records, overrides, taxon_keys=frozenset()) -> list[str]:
    """Apply manual species overrides in file order; return a list of warnings.

    Rows whose `sci` is an order or family name (taxon_keys) are skipped here;
    apply_taxa_overrides handles them.
    """
    by_key = {sci_key(r["sci"]): r for r in records}
    warnings = []
    for ov in overrides:
        if sci_key(ov["sci"]) in taxon_keys and sci_key(ov["sci"]) not in by_key:
            continue
        rec = by_key.get(sci_key(ov["sci"]))
        field = (ov.get("field") or "").strip()
        value = clean(ov.get("value"))
        if rec is None:
            warnings.append(f"override for unknown species {ov['sci']!r}")
            continue
        if field not in FIELDS or field in ("ru_source", "ru_status") or field in DERIVED_FIELDS:
            warnings.append(f"override with unsupported field {field!r} for {ov['sci']!r}")
            continue
        if field == "ru_alt":
            # "a; b" -> accumulated on top of the automatic alternatives
            rec.setdefault("_alt_manual", []).extend(
                cap_first(x) for x in (clean(v) for v in (value or "").split(";")) if x)
            continue
        if field == "ru_head":
            rec["_head_manual"] = value
            continue
        if field == "ru_ebird":
            if value == "-":
                rec["_ebird_suppressed"] = True
            else:
                warnings.append(f"override ru_ebird for {ov['sci']!r}: only '-' (suppress) "
                                f"is supported, got {value!r}")
            continue
        if field == "sci_prev":
            # "Genus species; -Genus species": add / remove former names
            for item in (clean(v) for v in (value or "").split(";")):
                if not item:
                    continue
                remove = item.startswith("-")
                words = parse_old_name(item.lstrip("- "))
                if not words:
                    warnings.append(f"override sci_prev for {ov['sci']!r}: "
                                    f"not a binomial or trinomial: {item!r}")
                    continue
                rec.setdefault("_prev_del" if remove else "_prev_add", []).append(" ".join(words))
            continue
        if field == "ru" and value == "-":
            value = None  # "-" = remove a wrong name: the species becomes "missing"
        if field == "seq":
            value = int(value) if value else rec["seq"]
        rec[field] = value
        if field == "ru":
            rec["ru_source"] = "manual" if value else None
    return warnings


# --------------------------------------------------------------------------- name normalisation

def cap_first(text: str) -> str:
    return text[:1].upper() + text[1:] if text else text


LATIN = re.compile(r"[A-Za-z]")
MIXED_WORD = re.compile(r"\S+")


def mixed_script_words(name: str | None) -> list[str]:
    """Words mixing Cyrillic and Latin letters (look-alike typos: "Cкоморох")."""
    return [w for w in MIXED_WORD.findall(name or "")
            if CYRILLIC.search(w) and LATIN.search(w)]


# "Гуменник (лесной гуменник)": the parenthesised part is taken as an
# alternative name only if it looks like a name, not like a comment.
PAREN = re.compile(r"^(?P<main>[^()]+?)\s*\((?P<alt>[^()]+)\)\s*$")
PAREN_NOT_NAME = re.compile(r"[A-Za-z0-9=?.:;]|\b(?:вид|подвид|подвиды|форма|группа|включая|"
                            r"кроме|см|ранее|прежде|s\.l|возможно)\b", re.IGNORECASE)
ALT_SPLIT = re.compile(r"\s*,\s*|\s+/\s+|\s+или\s+")


def split_ru(name: str) -> tuple[str, list[str], str | None]:
    """Split a Russian name with synonyms into (main, alternatives, problem).

    "Хохлатый фазан, чир" -> ("Хохлатый фазан", ["Чир"]); separators: comma,
    " / ", " или ". "Гуменник (лесной гуменник)" -> ("Гуменник", ["Лесной
    гуменник"]). A parenthesis that does not look like a name (Latin, digits,
    punctuation, words such as "подвид", more than four words) is left as is
    and reported via `problem`.
    """
    alts: list[str] = []
    m = PAREN.match(name)
    if m:
        inner = clean(m.group("alt"))
        if PAREN_NOT_NAME.search(inner) or len(inner.split()) > 4:
            return name, [], f"parenthesis kept: {name!r}"
        name, alts = clean(m.group("main")), [inner]
    elif "(" in name or ")" in name:
        return name, [], f"parenthesis kept: {name!r}"
    parts = [p for p in (clean(x) for x in ALT_SPLIT.split(name)) if p]
    return cap_first(parts[0]), [cap_first(p) for p in parts[1:] + alts], None


# Adjective endings, incl. participles in -ся ("кланяющаяся") and possessive
# adjectives in -ья/-ье/-ьи/-ий ("сорочья", "лисья").
ADJ_END = re.compile(r"(?:ый|ий|ой|ая|яя|ое|ее|ые|ие|ья|ье|ьи|ьё)(?:ся)?$")
# Possessive adjectives: "Стеллеров", "Бэрова", "дарвинов", "буйволов".
POSSESSIVE_END = re.compile(r"(?:ов|ова|ово|ев|ева|ево|ёв|ёва|ин|ина|ино)$")
# Possessives formed from common nouns: lower case in book spelling.
COMMON_POSSESSIVES = {"крокодилов", "фараонов", "буйволов"}


def ru_head(name: str | None) -> tuple[str | None, bool]:
    """Leading word ("nest") of a Russian species name, and a doubt flag.

    Words before the first noun are dropped if they are adjectives (endings
    -ый/-ий/-ой/-ая/-яя/-ое/-ее/-ые/-ие, -ья/-ье, participles in -ся) or
    possessive adjectives (-ов(а)/-ев(а)/-ин(а)) followed by a lower-case word
    ("Стеллеров морской орёл", "буйволов ткач"; but "Пингвин Адели"). The first
    remaining word is the head; everything after it is a genitive or an
    apposition ("гусь Росса", "фазан микадо", "конёк пуны"). Hyphenated words
    count as one ("лебедь-шипун"). Flagged as doubtful: every word looks like
    an adjective (the last word is taken), a lower-case word follows the head
    (apposition, or a typo in an adjective), or a capitalised head after
    other words. The head is returned with a lower-case first letter.
    """
    if not name:
        return None, False
    words = name.split()
    head, doubtful = words[-1], True
    for i, w in enumerate(words):
        base = w.lower()
        # an adjective is always followed by a lower-case word; before a
        # capitalised genitive the word is a noun ("Козодой Пригожина")
        if i + 1 < len(words) and words[i + 1][:1].islower() and (
                ADJ_END.search(base) or POSSESSIVE_END.search(base)):
            continue
        head = w
        # doubtful: a capitalised head after other words, or a lower-case
        # word after the head (apposition such as "конёк пуны", or a typo)
        doubtful = (i > 0 and w[:1].isupper()) or (
            i + 1 < len(words) and words[i + 1][:1].islower())
        break
    return head[:1].lower() + head[1:], doubtful


def en_head(name: str | None) -> str | None:
    """Last word of the English name (a hyphenated word is kept whole)."""
    if not name:
        return None
    return name.split()[-1]


def ru_book(name: str | None, en: str | None) -> tuple[str | None, bool]:
    """Russian name in book spelling: first letter lower case, unless the first
    word is a possessive adjective formed from a proper name ("Стеллерова
    сойка", "Магелланов гусь"): a capitalised word in -ов(а)/-ев(а)/-ин(а)
    followed by a lower-case word ("Пингвин Адели" is not one). The English
    "'s" ("Steller's Jay") confirms it; without it the capital is kept unless
    the word is a known possessive of a common noun (COMMON_POSSESSIVES:
    "Крокодилов сторож", "Фараонов филин"). Other words are unchanged
    ("гусь Росса"). Returns (name, capital kept)."""
    if not name:
        return None, False
    words = name.split()
    first = words[0].lower()
    if (len(words) > 1 and words[0][:1].isupper() and words[1][:1].islower()
            and POSSESSIVE_END.search(first) and not ADJ_END.search(first)
            and ("'s" in (en or "") or first not in COMMON_POSSESSIVES)):
        return name, True
    return name[:1].lower() + name[1:], False


def _test_names() -> None:
    assert split_ru("Хохлатый фазан, чир") == ("Хохлатый фазан", ["Чир"], None)
    assert split_ru("Гуменник (лесной гуменник)") == ("Гуменник", ["Лесной гуменник"], None)
    assert split_ru("Синьга") == ("Синьга", [], None)
    assert split_ru("Птица (подвид X)")[2]
    for name, want in {"Белолобый гусь": "гусь", "Лебедь-шипун": "лебедь-шипун",
                       "Гусь Росса": "гусь", "Малая канадская казарка": "казарка",
                       "Эму": "эму", "Пеганка-раджа": "пеганка-раджа",
                       "Стеллеров морской орёл": "орёл"}.items():
        got = ru_head(name)
        assert got == (want, False), f"ru_head({name!r}) = {got!r}, want {want!r}"
    assert en_head("Eastern Whip-poor-will") == "Whip-poor-will"
    assert en_head("Emu") == "Emu"
    assert en_head("Florida Scrub-Jay") == "Scrub-Jay"
    assert ru_book("Белолобый гусь", "Greater White-fronted Goose") == ("белолобый гусь", False)
    assert ru_book("Гусь Росса", "Ross's Goose") == ("гусь Росса", False)
    assert ru_book("Стеллеров морской орёл", "Steller's Sea Eagle") == ("Стеллеров морской орёл", True)
    assert ru_book("Розовый пеликан", "Great White Pelican")[1] is False
    assert ru_book("Магелланов гусь", "Upland Goose") == ("Магелланов гусь", True)
    assert ru_book("Крокодилов сторож", "Egyptian Plover") == ("крокодилов сторож", False)
    assert ru_book("Пингвин Адели", "Adelie Penguin") == ("пингвин Адели", False)
    for name, want in {"Бурая кланяющаяся крачка": "крачка",
                       "Сорочья кукушка": "кукушка", "Красноклювый буйволов ткач": "ткач",
                       "Пингвин Адели": "пингвин", "Козодой Пригожина": "козодой"}.items():
        assert ru_head(name) == (want, False), (name, ru_head(name))
    assert ru_head("Фазан микадо") == ("фазан", True)


def normalise_names(records) -> dict[str, list]:
    """Split synonyms out of `ru` into `ru_alt`, merge manual ru_alt, compute
    ru_head / ru_book / en_head. Returns lists for the build report."""
    log_ = {"split": [], "paren_kept": [], "mixed": [], "head_doubtful": [],
            "book_capital": []}
    for rec in records:
        alts: list[str] = []
        if rec["ru"]:
            main, auto, problem = split_ru(rec["ru"])
            if problem:
                log_["paren_kept"].append((rec["sci"], rec["ru"]))
            elif auto:
                log_["split"].append((rec["sci"], rec["ru"], main, "; ".join(auto),
                                      rec["ru_source"]))
            rec["ru"] = main
            alts = auto
        for a in alts + rec.pop("_alt_manual", []):
            if a not in rec["ru_alt"] and a != rec["ru"]:
                rec["ru_alt"].append(a)
        for name in [rec["ru"], rec["en"], *rec["ru_alt"]]:
            if mixed_script_words(name):
                log_["mixed"].append((rec["sci"], name))
        manual = rec.pop("_head_manual", None)
        if manual and rec["ru"]:
            rec["ru_head"], rec["ru_head_source"] = manual, "manual"
        elif rec["ru"]:
            rec["ru_head"], doubtful = ru_head(rec["ru"])
            rec["ru_head_source"] = "auto"
            if doubtful:
                log_["head_doubtful"].append((rec["sci"], rec["ru"], rec["ru_head"]))
        else:
            rec["ru_head"] = rec["ru_head_source"] = None
        rec["ru_book"], kept = ru_book(rec["ru"], rec["en"])
        if kept:
            log_["book_capital"].append((rec["sci"], rec["ru"], rec["en"]))
        rec["en_head"] = en_head(rec["en"])
    return log_


# Purely orthographic variants treated as equal when comparing with eBird:
# (variant, accepted) pairs of case-folded substrings; the variant is
# rewritten to the accepted spelling (Volkov & Koblik: «камышовка»).
SPELLING_EQUIV = [("камышевк", "камышовк")]


def apply_spelling_equiv(name: str) -> str:
    """Rewrite SPELLING_EQUIV variants in a display name to the accepted
    spelling, keeping the case of the first letter of each occurrence."""
    for variant, accepted in SPELLING_EQUIV:
        name = re.sub(variant, lambda m: (accepted[0].upper() if m.group()[0].isupper()
                                          else accepted[0]) + accepted[1:],
                      name, flags=re.IGNORECASE)
    return name


def ru_compare_key(name: str) -> str:
    """Normalised form for comparing Russian names: part before the first comma,
    case-folded, ё = е, spaces and hyphens ignored, SPELLING_EQUIV variants
    rewritten to one spelling."""
    name = name.split(",")[0].casefold().replace("ё", "е")
    for variant, accepted in SPELLING_EQUIV:
        name = name.replace(variant, accepted)
    return re.sub(r"[\s\-\u2010-\u2015]+", "", name)


def add_ebird_names(records, ebird) -> tuple[list, list]:
    """Set `ru_ebird` to the eBird Russian name where it differs from the final
    `ru` (not for ru_source = ebird). Returns (suppressed, unused suppressions)."""
    suppressed, unused = [], []
    for rec in records:
        name = ebird.get(sci_key(rec["sci"]))
        differs = bool(name and rec["ru"] and rec["ru_source"] != "ebird"
                       and ru_compare_key(name) != ru_compare_key(rec["ru"]))
        if rec.pop("_ebird_suppressed", False):
            (suppressed if differs else unused).append((rec["sci"], rec["ru"], name))
            differs = False
        rec["ru_ebird"] = apply_spelling_equiv(name) if differs else None
    return suppressed, unused


def _test_compare_key() -> None:
    assert ru_compare_key("Белощекий бюль-бюль") == ru_compare_key("Белощёкий бюльбюль")
    assert ru_compare_key("Хохлатый фазан, чир") == ru_compare_key("хохлатый  фазан")
    assert ru_compare_key("Камышовка") == ru_compare_key("Камышевка")
    assert ru_compare_key("Тростниковая камышевка") == ru_compare_key("Тростниковая камышовка")
    assert ru_compare_key("Камышевка-барсучок") == ru_compare_key("Камышовка барсучок")
    assert ru_compare_key("КАМЫШЕВКИ") == ru_compare_key("камышовки")
    assert ru_compare_key("Камышевка") != ru_compare_key("Камышница")
    assert apply_spelling_equiv("Бамбуковая камышевка") == "Бамбуковая камышовка"
    assert apply_spelling_equiv("Камышевка-барсучок") == "Камышовка-барсучок"
    assert apply_spelling_equiv("Южная дроздовидная камышевка") == "Южная дроздовидная камышовка"


def finalise(records):
    for rec in records:
        if rec["ru"] is None:
            rec["ru_source"], rec["ru_status"] = None, "missing"
        elif rec["ru_source"] in ("ioc", "manual"):
            rec["ru_status"] = "ok"
        else:
            rec["ru_status"] = "ok_fallback"


def write_json(records, taxa):
    payload = json.dumps([{k: r[k] for k in FIELDS} for r in records],
                         ensure_ascii=False, separators=(",", ":"))
    OUT_JSON.write_text(payload, encoding="utf-8")
    OUT_TAXA_JSON.write_text(json.dumps(taxa, ensure_ascii=False, separators=(",", ":")),
                             encoding="utf-8")
    OUT_DOCS_JSON.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUT_JSON, OUT_DOCS_JSON)
    shutil.copyfile(OUT_TAXA_JSON, OUT_DOCS_TAXA_JSON)


def md_table(rows, headers) -> list[str]:
    def esc(v):
        return "" if v is None else str(v).replace("|", "\\|")
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(esc(v) for v in row) + " |" for row in rows]
    return out


def duplicate_ru(records) -> list[tuple[str, list[dict]]]:
    """Russian names (case-insensitive) shared by several species."""
    by_name: dict[str, list[dict]] = {}
    for r in records:
        if r["ru"]:
            by_name.setdefault(r["ru"].casefold(), []).append(r)
    return [(recs[0]["ru"], recs) for recs in by_name.values() if len(recs) > 1]


def alt_clashes(records) -> list[tuple[str, str, str]]:
    """ru_alt entries equal to the main Russian name of another species."""
    main = {r["ru"].casefold(): r["sci"] for r in records if r["ru"]}
    return [(r["sci"], a, main[a.casefold()]) for r in records for a in r["ru_alt"]
            if a.casefold() in main and main[a.casefold()] != r["sci"]]


PREV_EXAMPLES = ("Sibirionetta formosa", "Spinus spinus", "Calidris pugnax", "Astur gentilis",
                 "Corvus corone", "Apteryx maxima", "Bubo scandiacus", "Setophaga petechia")


def prev_report(records, prev_log) -> tuple[list[str], dict]:
    """Report section and counts for sci_prev / sci_book_prev."""
    with_prev = [r for r in records if r["sci_prev"]]
    kinds, sources = Counter(), Counter()
    kind_species, source_species = Counter(), Counter()
    for r in with_prev:
        for e in r["sci_prev"]:
            kinds[e["kind"]] += 1
            sources.update(e["sources"])
        kind_species.update({e["kind"] for e in r["sci_prev"]})
        source_species.update({s for e in r["sci_prev"] for s in e["sources"]})
    book = [r for r in records if r["sci_book_prev"]]
    counts = {
        "sci_prev_species": len(with_prev),
        "sci_prev_names": sum(kinds.values()),
        "sci_book_prev": len(book),
        "sci_prev_vs_unlinked": len(prev_log["unlinked"]),
        "sci_prev_vs_unparsed": len(prev_log["unparsed"]),
    }
    L = ["", f"## Former scientific names (`sci_prev`): {len(with_prev)} species", "",
         "Former combinations from `data/raw/IOC_15.2_vs_other_lists.xlsx` (IOC 15.2, IOC 15.1, "
         "Clements 2025, BirdLife v10, H&M 4.1, HBW, Peters, S&M 1993; rows joined on the AviList "
         "column) and historical eBird taxonomies (`ebirdYYYY`, joined on the species code), plus "
         "`field = sci_prev` overrides. AviList protonyms are not included. `sci_book_prev` is the "
         "first name of kind genus / genus_ending / epithet (the list is sorted by the most recent "
         "source, then by name). eBird versions are read from the public API without a key; "
         "there is no 2020 version.", ""]
    L += [f"- eBird {y}: {st}" for y, st in prev_log["ebird_status"].items()]
    L += [f"- {k}: {v}" for k, v in sorted(prev_log["stats"].items())]
    L += ["", "### By kind", ""]
    L += md_table([(k, kind_species[k], kinds[k]) for k in PREV_KINDS],
                  ["kind", "species", "names"])
    L += ["", "### By source", ""]
    L += md_table([(s, source_species[s], sources[s]) for s in PREV_SOURCE_ORDER if sources[s]],
                  ["source", "species", "names"])
    L += ["", f"Species with `sci_book_prev`: {len(book)}.", ""]

    def fmt(r):
        return "; ".join(f"{e['name']} ({e['kind']}: {', '.join(e['sources'])})"
                         for e in r["sci_prev"])
    by_sci = {r["sci"]: r for r in records}
    sample = [by_sci[s] for s in PREV_EXAMPLES if s in by_sci]
    step = max(1, len(book) // (30 - len(sample)))
    sample += [r for r in book[::step] if r not in sample][:30 - len(sample)]
    L += ["### Examples (30)", ""]
    L += md_table([(r["sci"], r["sci_book_prev"] or "", fmt(r)) for r in sample],
                  ["Scientific name", "sci_book_prev", "sci_prev"])
    L += ["", f"### Rows of the comparison file not joined to AviList ({len(prev_log['unlinked'])})", "",
          "Species rows with no AviList name of their own and no AviList subspecies under them "
          "(hybrids, doubtful and extinct forms, lumps noted only in the Notes column). "
          "Join by hand with `field = sci_prev` if needed.", ""]

    def names(row):
        return "; ".join(f"{VS_SOURCE_CODE.get(k, k)}: {clean(row[VS_COLUMNS[k][0]])}"
                         for k in VS_LISTS + ("tif", "gaudin", "avilist")
                         if clean(row[VS_COLUMNS[k][0]]))

    def note(row):
        text = clean(row[VS_COLUMNS["notes"][0]]) or ""
        return text if len(text) <= 120 else text[:119] + "…"
    L += md_table([(row[0], names(row), why, note(row)) for row, why in prev_log["unlinked"]],
                  ["IOC 15.2 seq.", "names", "why", "notes (shortened)"])
    if prev_log["unparsed"]:
        L += ["", f"### Names not parsed as a binomial ({len(prev_log['unparsed'])})", ""]
        L += md_table(prev_log["unparsed"], ["AviList species", "source", "as written"])
    if prev_log["unused_removals"]:
        L += ["", "### `sci_prev` override removals with no effect", ""]
        L += [f"- {sci}: {name}" for sci, name in prev_log["unused_removals"]]
    return L, counts


def write_report(records, ioc, ebird, wikidata, status, warnings, taxa, taxa_warnings,
                 names_log, ebird_log, prev_log) -> dict:
    avi_keys = {sci_key(r["sci"]) for r in records}
    total = len(records)
    by_source = Counter(r["ru_source"] for r in records)
    missing = [r for r in records if r["ru"] is None]
    extinct = Counter(r["extinct"] for r in records if r["extinct"])
    not_in_ioc = [r for r in records if sci_key(r["sci"]) not in ioc]
    ioc_only = sorted((v for k, v in ioc.items() if k not in avi_keys), key=lambda v: v["sci"])
    suppressed, unused_suppress = ebird_log
    suppressed_keys = {sci_key(s[0]) for s in suppressed}
    diffs = []
    for r in records:
        key = sci_key(r["sci"])
        a, b = (ioc.get(key) or {}).get("ru"), ebird.get(key)
        if a and b and a.casefold() != b.casefold():
            diffs.append((r["sci"], a, b, r["ru_ebird"] or "",
                          "yes" if key in suppressed_keys else ""))
    for sci, ru, name in unused_suppress:
        warnings = warnings + [f"override ru_ebird '-' for {sci!r} has no effect "
                               f"(eBird name {name!r} does not differ from ru {ru!r})"]

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
        "ru_ebird": sum(1 for r in records if r["ru_ebird"]),
        "ru_ebird_suppressed": len(suppressed),
        "auth_leftover_initials": sum(1 for r in records
                                      if r["auth"] and LEFTOVER_INITIALS.search(r["auth"])),
    }
    dups = duplicate_ru(records)
    clashes = alt_clashes(records)
    heads = Counter(r["ru_head"] for r in records if r["ru_head"])
    counts.update({
        "ru_split_synonyms": len(names_log["split"]),
        "ru_with_alt": sum(1 for r in records if r["ru_alt"]),
        "ru_alt_total": sum(len(r["ru_alt"]) for r in records),
        "ru_paren_kept": len(names_log["paren_kept"]),
        "mixed_script_names": len(names_log["mixed"]),
        "ru_duplicates": len(dups),
        "ru_alt_clashes": len(clashes),
        "ru_heads": len(heads),
        "ru_head_manual": sum(1 for r in records if r["ru_head_source"] == "manual"),
        "ru_head_doubtful": len(names_log["head_doubtful"]),
        "ru_book_capital_kept": len(names_log["book_capital"]),
    })
    for rank in ("orders", "families"):
        src = Counter(t["ru_source"] for t in taxa[rank])
        counts[f"{rank}"] = len(taxa[rank])
        for s in ("zmmu", "wikidata", "manual"):
            counts[f"{rank}_ru_{s}"] = src.get(s, 0)
        counts[f"{rank}_ru_missing"] = src.get(None, 0)

    prev_lines, prev_counts = prev_report(records, prev_log)
    counts.update(prev_counts)

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
        ("`ru_ebird` set (eBird name differs from `ru`)", counts["ru_ebird"]),
        ("`ru_ebird` suppressed by override", counts["ru_ebird_suppressed"]),
        ("`auth` with leftover initials", counts["auth_leftover_initials"]),
        ("Species with `sci_prev` (former scientific names)", counts["sci_prev_species"]),
        ("Species with `sci_book_prev`", counts["sci_book_prev"]),
        ("Names with mixed Cyrillic/Latin words", counts["mixed_script_names"]),
        ("Russian names shared by several species", counts["ru_duplicates"]),
        ("`ru` split into `ru` + `ru_alt`", counts["ru_split_synonyms"]),
        ("Species with `ru_alt`", counts["ru_with_alt"]),
        ("`ru_alt` names in total", counts["ru_alt_total"]),
        ("`ru_alt` equal to another species' `ru`", counts["ru_alt_clashes"]),
        ("Distinct `ru_head`", counts["ru_heads"]),
        ("`ru_head` doubtful (auto)", counts["ru_head_doubtful"]),
        ("`ru_head` manual", counts["ru_head_manual"]),
        ("`ru_book` with the capital kept", counts["ru_book_capital_kept"]),
    ], ["Metric", "Count"])

    L += ["", "## Russian names: checks and index fields", ""]
    L += ["", f"### Words mixing Cyrillic and Latin letters ({len(names_log['mixed'])})", "",
          "Look-alike letters (e.g. Latin C in \"Cкоморох\"); fix in `data/overrides.csv`.", ""]
    L += md_table(names_log["mixed"], ["Scientific name", "Name"])
    L += ["", f"### Russian names shared by several species ({len(dups)})", "",
          "Not fixed automatically; resolve in `data/overrides.csv` when the right name is known.", ""]
    L += md_table([(name, "; ".join(f"*{r['sci']}* ({r['en']}, {r['ru_source']})" for r in recs))
                   for name, recs in dups], ["Russian name", "Species (English, source)"])
    L += ["", f"### Synonyms split out of `ru` ({len(names_log['split'])})", "",
          "Separators: comma, \" / \", \" или \", parentheses. The first part stays in `ru`, "
          "the rest go to `ru_alt` (first letter capitalised).", ""]
    L += md_table(names_log["split"], ["Scientific name", "Source name", "ru", "ru_alt", "ru_source"])
    L += ["", f"### Parentheses left in `ru` ({len(names_log['paren_kept'])})", "",
          "The parenthesis does not look like a name (comment, Latin, digits); not split.", ""]
    L += md_table(names_log["paren_kept"], ["Scientific name", "ru"])
    L += ["", f"### `ru_alt` equal to another species' `ru` ({len(clashes)})", ""]
    L += md_table(clashes, ["Scientific name", "ru_alt", "is `ru` of"])
    L += ["", "### Top 50 `ru_head` (index nests)", ""]
    L += md_table(heads.most_common(50), ["ru_head", "Species"])
    L += ["", f"### Doubtful `ru_head` ({len(names_log['head_doubtful'])})", "",
          "All-adjective names, a lower-case word after the head (apposition such as "
          "\"конёк пуны\" or a typo), or a capitalised head after other words. "
          "Fix systematic errors in `ru_head()`, single ones with `field = ru_head` in overrides.", ""]
    L += md_table(names_log["head_doubtful"], ["Scientific name", "ru", "ru_head"])
    L += ["", f"### `ru_book` with the capital kept ({len(names_log['book_capital'])})", "",
          "First word is a possessive adjective from a proper name.", ""]
    L += md_table([(sci, ru, en, "yes" if "'s" in (en or "") else "")
                   for sci, ru, en in names_log["book_capital"]],
                  ["Scientific name", "ru", "English", "English has 's"])

    L += ["", "## Orders and families: Russian names", "",
          "Sources: ZMMU passerine list family headers (`zmmu`), Wikidata (`wikidata`), "
          "`data/overrides.csv` (`manual`). Written to `data/taxa.json`.", ""]
    L += md_table([(rank, counts[rank], counts[f"{rank}_ru_zmmu"], counts[f"{rank}_ru_wikidata"],
                    counts[f"{rank}_ru_manual"], counts[f"{rank}_ru_missing"])
                   for rank in ("orders", "families")],
                  ["Rank", "Total", "zmmu", "wikidata", "manual", "missing"])
    if taxa_warnings:
        L += ["", "### Taxon name warnings", ""] + [f"- {w}" for w in taxa_warnings]
    missing_taxa = [("order", t["sci"], "", t["count"]) for t in taxa["orders"] if not t["ru"]]
    missing_taxa += [("family", t["sci"], t["en"], t["count"]) for t in taxa["families"]
                     if not t["ru"]]
    L += ["", f"### Orders and families without a Russian name ({len(missing_taxa)})", ""]
    L += md_table(missing_taxa, ["Rank", "Scientific name", "English", "Species"])

    L += ["", f"## AviList species not found in IOC ({len(not_in_ioc)})", ""]
    L += md_table([(r["sci"], r["en"], r["ru_source"] or "—") for r in not_in_ioc],
                  ["Scientific name", "English", "ru_source"])
    L += ["", f"## Species with no Russian name anywhere ({len(missing)})", ""]
    L += md_table([(r["sci"], r["en"]) for r in missing], ["Scientific name", "English"])
    L += ["", f"## IOC species not found in AviList ({len(ioc_only)})", ""]
    L += md_table([(v["sci"], v["en"], v["ru"]) for v in ioc_only],
                  ["IOC scientific name", "English (IOC)", "Russian (IOC)"])
    L += ["", f"## IOC and eBird Russian names differ ({len(diffs)})", "",
          "Case-insensitive comparison of the raw names. `ru` always prefers IOC; "
          "the eBird name is kept in `ru_ebird` when it still differs from the final `ru` "
          "after normalisation (ё = е, spaces and hyphens ignored, part before a comma), "
          "unless suppressed with `field = ru_ebird`, value `-` in `data/overrides.csv` "
          "(column «подавлено»).", ""]
    L += md_table(diffs, ["Scientific name", "IOC", "eBird", "ru_ebird", "подавлено"])
    L += prev_lines
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
    _test_normalise_authority()
    _test_names()
    _test_compare_key()
    _test_prev()

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
    overrides = load_overrides(OVERRIDES_PATH)
    taxa = build_taxa(records)
    taxon_keys = {sci_key(t["sci"]) for t in taxa["orders"] + taxa["families"]}
    species_keys = {sci_key(r["sci"]) for r in records}
    warnings = apply_overrides(records, overrides, taxon_keys)
    names_log = normalise_names(records)
    ebird_log = add_ebird_names(records, ebird)
    finalise(records)

    # former scientific names
    prev_sources = []
    prev_log = {"unlinked": [], "unparsed": [], "stats": Counter()}
    if ensure_file(VS_LISTS_PATH, VS_LISTS_URL, mode, required=False):
        vs, prev_log["unlinked"], prev_log["unparsed"], vs_stats = load_vs_lists(
            VS_LISTS_PATH, {r["sci"] for r in records})
        prev_sources.append(vs)
        prev_log["stats"].update(vs_stats)
        status["IOC 15.2 vs other lists (former names)"] = (
            f"`{VS_LISTS_PATH.relative_to(ROOT)}`, {len(vs)} species with names")
    else:
        status["IOC 15.2 vs other lists (former names)"] = "SKIPPED (not available)"
    eb_prev, prev_log["ebird_status"], eb_stats = load_ebird_history(records, mode)
    prev_sources.append(eb_prev)
    prev_log["stats"].update(eb_stats)
    status["eBird taxonomies 2015–2024 (former names)"] = (
        f"{sum(not v.startswith('SKIPPED') for v in prev_log['ebird_status'].values())} of "
        f"{len(EBIRD_HISTORY_YEARS)} versions"
        + ("" if all(not v.startswith("SKIPPED") for v in prev_log["ebird_status"].values())
           else ", SOME SKIPPED (not available)"))
    prev_log["stats"].update(build_sci_prev(records, prev_sources))
    prev_log["unused_removals"] = [(r["sci"], n) for r in records for n in r.get("_prev_del_unused", [])]

    # order / family Russian names
    taxa_warnings: list[str] = []
    zmmu = {}
    if ensure_file(ZMMU_PASSERINE_PATH, ZMMU_PASSERINE_URL, mode, required=False):
        zmmu, taxa_warnings = load_zmmu_families(
            ZMMU_PASSERINE_PATH, {sci_key(r["sci"]): r["family"] for r in records},
            {t["sci"] for t in taxa["families"]})
        status["ZMMU passerine list (family names)"] = (
            f"`{ZMMU_PASSERINE_PATH.relative_to(ROOT)}`, {len(zmmu)} families")
    else:
        status["ZMMU passerine list (family names)"] = "SKIPPED (not available)"
    taxon_names = sorted(t["sci"] for t in taxa["orders"] + taxa["families"])
    cached_names = None
    if WIKIDATA_TAXA_PATH.exists():
        try:
            cached_names = json.loads(WIKIDATA_TAXA_PATH.read_text(encoding="utf-8"))["queried"]
        except Exception:  # noqa: BLE001 - corrupt cache: refetch
            cached_names = None
    if mode == "fetch" or (mode == "default" and (
            cached_names is None or not set(taxon_names) <= set(cached_names))):
        try:
            fetch_wikidata_taxa(WIKIDATA_TAXA_PATH, taxon_names)
        except Exception as exc:  # noqa: BLE001
            log(f"  WARNING: Wikidata order/family query failed: {exc}")
    wikidata_taxa = {}
    if WIKIDATA_TAXA_PATH.exists():
        wikidata_taxa = load_wikidata_taxa(WIKIDATA_TAXA_PATH)
        status["Wikidata orders/families (ru)"] = (
            f"`{WIKIDATA_TAXA_PATH.relative_to(ROOT)}`, {len(wikidata_taxa)} taxa")
    else:
        status["Wikidata orders/families (ru)"] = "SKIPPED (unreachable or no cache)"
    apply_taxa_names(taxa, zmmu, wikidata_taxa)
    taxa_warnings += apply_taxa_overrides(
        taxa, [ov for ov in overrides
               if sci_key(ov["sci"]) in taxon_keys and sci_key(ov["sci"]) not in species_keys])

    write_json(records, taxa)
    counts = write_report(records, ioc, ebird, wikidata, status, warnings, taxa, taxa_warnings,
                          names_log, ebird_log, prev_log)

    print(f"Wrote {OUT_JSON.relative_to(ROOT)}, {OUT_TAXA_JSON.relative_to(ROOT)}, "
          f"{OUT_DOCS_JSON.relative_to(ROOT)}, {OUT_DOCS_TAXA_JSON.relative_to(ROOT)}, "
          f"{OUT_REPORT.relative_to(ROOT)}")
    for name, state in status.items():
        print(f"  {name}: {state}")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    for w in taxa_warnings:
        print(f"  taxon warning: {w}")
    for rank in ("orders", "families"):
        missing = [t["sci"] for t in taxa[rank] if not t["ru"]]
        print(f"  {rank} without Russian name ({len(missing)}): {', '.join(missing) or '-'}")


if __name__ == "__main__":
    main()
