"""Catalogue of layout ideas for the print edition: one PDF of 46 pages
(contents + 15 variants of a list page, 15 of a Russian index page and 15 of
an English index page), all set from the same data fragment.

    uv run --with typst python print/catalog/build_catalog.py [--only list3,ru5] [--no-png]

Data preparation reuses print/build_print.py (imported, not copied): species
records (c2_species), sort keys, Russian definitions of nests. Every variant
is compiled separately from catalog.typ (sys.inputs kind/v) so that it can flow
past its first page; only page 1 goes into the catalogue. The script then
  * checks every page for words sticking out of the type area or of a column
    (geometry is reported by each variant as metadata <geom>);
  * checks that the obligatory nests are on the index pages (<hw> metadata);
  * merges contents + 45 pages into out/catalog.pdf and renders out/png/*.png.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import typst

HERE = Path(__file__).resolve().parent
PRINT = HERE.parent
REPO = PRINT.parent
OUT = HERE / "out"
PARTS = OUT / "parts"
PNG = OUT / "png"
FONTS = [str(HERE / "fonts"), str(PRINT / "fonts")]

sys.path.insert(0, str(PRINT))
import build_print as bp  # noqa: E402

from variants import VARIANTS, KIND_RU  # noqa: E402

RU_LETTERS = "АБВГДЕЖЗИЙК"
EN_LETTERS = "ABCDEFG"
RU_REQUIRED = ("гусь", "казарка", "куропатка")
EN_REQUIRED = ("Duck", "Goose")
NB = bp.NBSP


# ---------------------------------------------------------------- data
def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def num_rec(s: dict, main: bool = True) -> dict:
    return {"n": s["n"], "main": main, "sci": s["g"] + " " + s["e"], "abbr": s["g"][0] + "." + NB + s["e"], "en": s["en"]}


def rng(a: int, b: int) -> str:
    return str(a) if a == b else f"{a}{bp.RDASH}{b}"


def prepare() -> dict:
    species = json.loads((REPO / "data/species.json").read_text(encoding="utf-8"))
    taxa = json.loads((REPO / "data/taxa.json").read_text(encoding="utf-8"))
    species.sort(key=lambda r: r["seq"])
    sel = [r for r in species if r["order"] in bp.SAMPLE_ORDERS]
    sp = bp.c2_species(sel)
    for s, r in zip(sp, sel):
        s["Ru"] = r.get("ru")                       # capitalised (IOC form)
        s["au"] = bp.nb_auth(r.get("auth"))         # author as one string
        s["iucn"] = r.get("iucn")
        s["rh"] = r.get("ru_head")
        s["eh"] = r.get("en_head")
        s["rd"] = bp.ru_definition(r["ru_book"], r["ru_head"]) if r.get("ru_book") else None

    tx_o = {o["sci"]: o for o in taxa["orders"]}
    tx_f = {f["sci"]: f for f in taxa["families"]}
    orders, families = [], {}
    for s, r in zip(sp, sel):
        if not orders or orders[-1]["sci"] != s["o"]:
            orders.append({"sci": s["o"], "ru": tx_o.get(s["o"], {}).get("ru"), "a": s["n"], "b": s["n"]})
        orders[-1]["b"] = s["n"]
        f = families.setdefault(s["f"], {"sci": s["f"], "ru": tx_f.get(s["f"], {}).get("ru"),
                                         "en": tx_f.get(s["f"], {}).get("en") or r.get("family_en"),
                                         "a": s["n"], "b": s["n"]})
        f["b"] = s["n"]
    for t in orders + list(families.values()):
        t["cnt"] = bp.count_txt(t["b"] - t["a"] + 1, bp.VID)
        t["rng"] = rng(t["a"], t["b"])
    # genera: range and count, in list order
    genera: dict[str, dict] = {}
    for s in sp:
        g = genera.setdefault(s["g"], {"g": s["g"], "a": s["n"], "b": s["n"], "f": s["f"]})
        g["b"] = s["n"]
    for g in genera.values():
        g["cnt"] = bp.count_txt(g["b"] - g["a"] + 1, bp.VID)
        g["rng"] = rng(g["a"], g["b"])

    return {
        "species": [s for s in sp if s["n"] <= 176],     # the list pages never reach Galliformes
        "orders": orders, "families": families, "genera": genera,
        "ru": ru_index(sp, orders, families),
        "en": en_index(sp, families),
    }


# ---------------------------------------------------------------- Russian index
def ru_index(sp, orders, families) -> dict:
    names = []   # every Russian name: main and alternative
    for s in sp:
        if not s["ru"]:
            continue
        names.append({"book": s["ru"], "head": s["rh"], "def": s["rd"], "main": True, "s": s})
        for alt in s["alt"]:
            head = bp.ru_head_fn(alt)[0]
            names.append({"book": alt, "head": head, "def": bp.ru_definition(alt, head),
                          "main": False, "s": s})
    taxa = [{"name": (o["ru"] or o["sci"]).lower(), "rng": o["rng"], "sci": o["sci"], "rank": "отряд"}
            for o in orders if o["ru"]]
    taxa += [{"name": f["ru"].lower(), "rng": f["rng"], "sci": f["sci"], "rank": "семейство"}
             for f in families.values() if f["ru"]]

    def ok(word: str) -> bool:
        return bp.ru_letter(word) in RU_LETTERS

    # flat, direct order: «белолобый гусь 49»
    flat = []
    for nm in names:
        flat.append({"t": nm["book"], "h": nm["head"], "nums": [num_rec(nm["s"], nm["main"])], "alt": not nm["main"],
                     "x": nm["s"]["x"], "en": nm["s"]["en"], "kind": "sp",
                     "ref": None if nm["main"] else nm["s"]["ru"]})
    for t in taxa:
        flat.append({"t": t["name"], "h": t["name"], "rng": t["rng"], "sci": t["sci"], "kind": "taxon"})
    flat = [e for e in flat if ok(e["t"])]
    flat.sort(key=lambda e: bp.ru_sort_key(e["t"]))
    for e in flat:
        e["L"] = bp.ru_letter(e["t"])

    # inverted, no nests: «гусь белолобый 49»
    inv = []
    for nm in names:
        d = nm["def"] if nm["def"] != nm["head"] else ""
        inv.append({"h": nm["head"], "d": d, "t": (nm["head"] + " " + d).strip(),
                    "nums": [num_rec(nm["s"], nm["main"])], "alt": not nm["main"], "x": nm["s"]["x"],
                    "kind": "sp", "ref": None if nm["main"] else inverted(nm["s"])})
    for t in taxa:
        words = t["name"].split()
        h = words[-1]
        d = " ".join(words[:-1][::-1])
        inv.append({"h": h, "d": d, "t": (h + " " + d).strip(), "rng": t["rng"], "sci": t["sci"], "kind": "taxon"})
    inv = [e for e in inv if ok(e["h"])]
    inv.sort(key=lambda e: (bp.head_sort_key(e["h"]), bp.ru_sort_key(e["d"])))
    for e in inv:
        e["L"] = bp.ru_letter(e["h"])

    # nests by ru_head
    nests: dict[str, dict] = {}
    for nm in names:
        nest = nests.setdefault(nm["head"], {"hw": nm["head"], "nums": [], "defs": {}})
        d = nm["def"]
        if d == nm["head"] or not d:
            nest["nums"].append(num_rec(nm["s"], nm["main"]))
        else:
            key = (d, not nm["main"])
            nest["defs"].setdefault(key, {"d": d, "alt": not nm["main"], "nums": [], "x": nm["s"]["x"],
                                          "en": nm["s"]["en"],
                                          "ref": None if nm["main"] else nm["s"]["ru"]})
            nest["defs"][key]["nums"].append(num_rec(nm["s"], nm["main"]))
    units = []
    heads = set(nests)
    for hw, nest in nests.items():
        defs = sorted(nest["defs"].values(), key=lambda d: (bp.ru_sort_key(d["d"]), d["alt"]))
        also = sorted([h for h in heads if h != hw and h.startswith(hw + "-")], key=bp.ru_sort_key)
        units.append({"kind": "nest", "hw": hw, "nums": nest["nums"], "defs": defs, "also": also,
                      "key": bp.head_sort_key(hw)})
    for t in taxa:
        units.append({"kind": "taxon", "hw": t["name"], "rng": t["rng"], "sci": t["sci"], "rank": t["rank"],
                      "key": bp.head_sort_key(t["name"])})
    units = [u for u in units if ok(u["hw"])]
    units.sort(key=lambda u: u["key"])
    for u in units:
        u["L"] = bp.ru_letter(u["hw"])
        del u["key"]
    return {"flat": flat, "inv": inv, "nests": units, "letters": list(RU_LETTERS), "required": list(RU_REQUIRED)}


def inverted(s: dict) -> str:
    return (s["rh"] + " " + s["rd"]).strip() if s["rd"] and s["rd"] != s["rh"] else s["rh"]


# ---------------------------------------------------------------- English index
def en_index(sp, families) -> dict:
    names = [s for s in sp if s["en"]]

    def ok(word: str) -> bool:
        return bp.en_letter(word) in EN_LETTERS

    def rec(s):
        r = num_rec(s)
        r.update({"x": s["x"], "ru": s["ru"]})
        return r

    fams = [{"t": f["en"], "rng": f["rng"], "sci": f["sci"], "kind": "taxon"} for f in families.values() if f["en"]]

    def split(s):
        head = s["eh"] if s["eh"] and s["en"].endswith(s["eh"]) else s["en"].split()[-1]
        return head, s["en"][: -len(head)].strip()

    flat = [{"t": s["en"], "h": split(s)[0], "nums": [rec(s)], "kind": "sp"} for s in names] + \
        [dict(f, h=f["t"]) for f in fams]
    flat = [e for e in flat if ok(e["t"])]
    flat.sort(key=lambda e: bp.en_key(e["t"]))
    for e in flat:
        e["L"] = bp.en_letter(e["t"])

    inv = []
    for s in names:
        h, d = split(s)
        inv.append({"h": h, "d": d, "nums": [rec(s)], "kind": "sp"})
    for f in fams:
        inv.append({"h": f["t"], "d": "", "rng": f["rng"], "sci": f["sci"], "kind": "taxon"})
    inv = [e for e in inv if ok(e["h"])]
    inv.sort(key=lambda e: (bp.en_key(e["h"]), bp.en_key(e["d"])))
    for e in inv:
        e["L"] = bp.en_letter(e["h"])

    nests: dict[str, dict] = {}
    for s in names:
        h, d = split(s)
        nest = nests.setdefault(h, {"nums": [], "items": []})
        if d:
            nest["items"].append({"d": d, "nums": [rec(s)]})
        else:
            nest["nums"].append(rec(s))
    heads = set(nests)
    units = []
    for hw, nest in nests.items():
        items = sorted(nest["items"], key=lambda it: bp.en_key(it["d"]))
        # two-level tree: items sharing the word next to the head («Bean» in
        # «Taiga Bean Goose», «Tundra Bean Goose») form a sub-nest
        by_last: dict[str, list] = {}
        for it in items:
            by_last.setdefault(it["d"].split()[-1], []).append(it)
        tree, seen = [], set()
        for it in items:
            w = it["d"].split()[-1]
            grp = by_last[w]
            if len(grp) >= 2 and any(g["d"] != w for g in grp):
                if w in seen:
                    continue
                seen.add(w)
                own = [n for g in grp if g["d"] == w for n in g["nums"]]
                subs = [{"d": g["d"][: -len(w)].strip(), "nums": g["nums"]} for g in grp if g["d"] != w]
                tree.append({"sub": w, "nums": own, "items": subs})
            else:
                tree.append(it)
        tree.sort(key=lambda t: bp.en_key(t.get("sub") or t["d"]))
        also = sorted([h for h in heads if h != hw and hw.lower() in h.lower()], key=bp.en_key)
        units.append({"kind": "nest", "hw": hw, "nums": nest["nums"], "items": items, "tree": tree,
                      "also": also, "key": bp.en_key(hw)})
    for f in fams:
        units.append({"kind": "taxon", "hw": f["t"], "rng": f["rng"], "sci": f["sci"], "key": bp.en_key(f["t"])})
    units = [u for u in units if ok(u["hw"])]
    units.sort(key=lambda u: u["key"])
    for u in units:
        u["L"] = bp.en_letter(u["hw"])
        del u["key"]
    return {"flat": flat, "inv": inv, "nests": units, "letters": list(EN_LETTERS), "required": list(EN_REQUIRED)}


# ---------------------------------------------------------------- compile & check
PAGE_RE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)
WORD_RE = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
TOL, PUNCT_TOL = 0.4, 2.5
PUNCT = tuple(".,;:!?»)—–-\u00ad")


def first_page_words(pdf: Path):
    out = subprocess.run(["pdftotext", "-f", "1", "-l", "1", "-bbox", str(pdf), "-"],
                         capture_output=True, text=True, check=True).stdout
    m = PAGE_RE.search(out)
    return [(float(a), float(b), float(c), float(d), html.unescape(t)) for a, b, c, d, t in WORD_RE.findall(m.group(3))]


def check_page(pdf: Path, geoms: list[dict]) -> list[str]:
    """geoms: regions {x0, x1, y0, y1} (pt); a word starting inside a region's
    vertical span must lie within one of the regions horizontally."""
    problems = []
    for x0, y0, x1, y1, t in first_page_words(pdf):
        tol_r = PUNCT_TOL if t.endswith(PUNCT) else TOL
        yc = (y0 + y1) / 2
        rows = [g for g in geoms if g["y0"] <= yc <= g["y1"] + TOL]
        if not rows:
            continue
        if not any(g["x0"] - TOL <= x0 and x1 <= g["x1"] + tol_r for g in rows):
            problems.append(f"«{t}» x {x0:.1f}–{x1:.1f}, y {y0:.1f}")
        if any(y1 > g["y1"] + 1.0 for g in rows if g.get("bottom")):
            problems.append(f"«{t}» ниже полосы (y {y1:.1f})")
    return problems


def compile_one(kind: str, v: int, data_rel: str) -> tuple[Path, list, list, list]:
    pdf = PARTS / f"{kind}{v:02d}.pdf"
    inputs = {"data": data_rel, "kind": kind, "v": str(v)}
    typst.compile(str(HERE / "catalog.typ"), output=str(pdf), root=str(HERE), font_paths=FONTS, sys_inputs=inputs)
    q = lambda label: json.loads(typst.query(str(HERE / "catalog.typ"), label, field="value", root=str(HERE),
                                             font_paths=FONTS, sys_inputs=inputs))
    return pdf, q("<geom>"), q("<hw>"), q("<sp>")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="comma list like list3,ru5,en12")
    ap.add_argument("--no-png", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    PARTS.mkdir(exist_ok=True)
    PNG.mkdir(exist_ok=True)
    t0 = time.time()
    data = prepare()
    data["meta"] = VARIANTS
    data["kind_ru"] = KIND_RU
    (OUT / "catalog_data.json").write_text(json.dumps(data, ensure_ascii=False, indent=0), encoding="utf-8")
    data_rel = "/out/catalog_data.json"
    only = {s.strip() for s in args.only.split(",") if s.strip()}

    jobs = [(k, v) for k in ("list", "ru", "en") for v in range(1, 16)]
    if only:
        jobs = [(k, v) for k, v in jobs if f"{k}{v}" in only]
    bad = 0
    for kind, v in jobs:
        try:
            pdf, geom, hws, sps = compile_one(kind, v, data_rel)
        except typst.TypstError as e:
            print(f"{kind}{v}: ОШИБКА\n{getattr(e, 'diagnostic', e)}")
            bad += 1
            continue
        probs = check_page(pdf, geom[0]["regions"]) if geom else ["нет <geom>"]
        msg = []
        if kind != "list":
            on1 = {h["nest"] for h in hws if h["page"] == 1}
            req = RU_REQUIRED if kind == "ru" else EN_REQUIRED
            miss = [r for r in req if r not in on1]
            if miss:
                probs.append("нет гнёзд: " + ", ".join(miss))
            p1 = [h["hw"] for h in hws if h["page"] == 1]
            msg.append(f"{p1[0]} … {p1[-1]} ({len(p1)} входов)" if p1 else "пусто")
        else:
            p1 = [s["n"] for s in sps if s["page"] == 1]
            msg.append(f"№ {min(p1)}–{max(p1)} ({len(p1)} видов)" if p1 else "пусто")
        status = "OK" if not probs else f"{len(probs)} нарушений"
        print(f"{kind}{v:>2}: {status:14} {'; '.join(msg)}")
        for p in probs[:12]:
            print("      " + p)
        bad += bool(probs)
        if not args.no_png:
            subprocess.run(["pdftoppm", "-png", "-r", "100", "-f", "1", "-l", "1", "-singlefile",
                            str(pdf), str(PNG / f"{kind}{v:02d}")], check=True)

    if not only:
        toc = PARTS / "toc.pdf"
        typst.compile(str(HERE / "toc.typ"), output=str(toc), root=str(HERE), font_paths=FONTS,
                      sys_inputs={"data": data_rel})
        n_toc = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(toc)], capture_output=True,
                                                                text=True).stdout).group(1))
        if n_toc != 1:
            print(f"ОГЛАВЛЕНИЕ: {n_toc} полос вместо одной")
            bad += 1
        singles = [toc]
        for kind, v in jobs:
            src = PARTS / f"{kind}{v:02d}.pdf"
            one = PARTS / f"{kind}{v:02d}_p1.pdf"
            subprocess.run(["pdfseparate", "-f", "1", "-l", "1", str(src), str(one)], check=True)
            singles.append(one)
        final = OUT / "catalog.pdf"
        subprocess.run(["pdfunite", *map(str, singles), str(final)], check=True)
        if not args.no_png:
            subprocess.run(["pdftoppm", "-png", "-r", "100", "-f", "1", "-l", "1", "-singlefile",
                            str(final), str(PNG / "00_toc")], check=True)
        print(f"→ {final.relative_to(REPO)}  ({len(singles)} полос)")
    print(f"{time.time() - t0:.1f} s; страниц с дефектами: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
