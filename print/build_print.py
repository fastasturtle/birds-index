"""Print (book) layout prototype for the trilingual bird index.

Reads data/species.json + data/taxa.json, prepares a print data file
(numbering, non-breaking spaces, pre-sorted alphabetical indexes) and
compiles three Typst templates (variants A, B, C) into PDF.

    uv run --with typst python print/build_print.py            # sample: Anseriformes + Galliformes
    uv run --with typst python print/build_print.py --full     # whole list (11 131 species)
    uv run --with typst python print/build_print.py --preview  # also render PNG previews
    uv run --with typst python print/build_print.py --variants C2 [--full]  # only variant C2

Variant C2 (iteration 2, variant_c2.typ) has its own data file (prepare_c2):
its alphabetical indexes are measured by Typst and paginated here; the PDF is
then checked for overflowing lines (check_overflow.py, non-zero exit code).

The templates read their data via json(sys.inputs.data) and contain no
sample-specific logic: the same .typ files typeset the full list.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

import typst

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUT = HERE / "out"
FONTS = HERE / "fonts"

SAMPLE_ORDERS = ("Anseriformes", "Galliformes")
VARIANTS = {
    "A": ("variant_a.typ", "birds_A_dictionary"),
    "B": ("variant_b.typ", "birds_B_checklist"),
    "C": ("variant_c.typ", "birds_C_compact"),
}
NBSP = " "
MM = 72 / 25.4

RU_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RU_RANK = {c: i + 1 for i, c in enumerate(RU_ALPHABET)}
EXT_CODE = {"extinct": "x", "possibly_extinct": "p", "extinct_in_wild": "w"}


# ---------------------------------------------------------------- sort keys
def ru_key(name: str):
    """Russian alphabet order (ё after е), word by word (space/hyphen first)."""
    key = []
    for ch in name.lower():
        if ch in RU_RANK:
            key.append(RU_RANK[ch])
        elif ch in " -":
            key.append(0)
        elif ch.isalpha():  # stray Latin letters: after Cyrillic
            key.append(100 + ord(ch))
        # punctuation ignored
    return key, name


def latin_fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))


def en_key(name: str):
    s = latin_fold(name).lower().replace("'", "").replace("’", "")
    key = [0 if ch in " -" else ord(ch) for ch in s if ch.isalnum() or ch in " -"]
    return key, name


def ru_letter(name: str) -> str:
    c = name[0].upper()
    return "Е" if c == "Ё" else c


def en_letter(name: str) -> str:
    return latin_fold(name[0]).upper()


# ---------------------------------------------------------------- data prep
def nb_auth(auth: str | None) -> str | None:
    """Keep "Linnaeus, 1758" and "& Gadow" together on one line."""
    if not auth:
        return None
    head, sep, year = auth.rpartition(", ")
    if sep and year.rstrip(")").isdigit():
        auth = head + "," + NBSP + year
    return auth.replace(" & ", NBSP + "& ").replace("von ", "von" + NBSP).replace("de ", "de" + NBSP)


def prepare(full: bool) -> dict:
    species = json.loads((REPO / "data/species.json").read_text(encoding="utf-8"))
    taxa = json.loads((REPO / "data/taxa.json").read_text(encoding="utf-8"))
    species.sort(key=lambda r: r["seq"])
    sel = species if full else [r for r in species if r["order"] in SAMPLE_ORDERS]

    out_sp = []
    for n, r in enumerate(sel, 1):
        gen, ep = r["sci"].split(" ", 1)
        out_sp.append({
            "n": n,
            "order": r["order"],
            "family": r["family"],
            "gen": gen,
            "ep": ep,
            "sci": gen + NBSP + ep,
            "auth": nb_auth(r.get("auth")),
            "en": r["en"].replace("'", "\u2019") if r.get("en") else None,
            "ru": r.get("ru"),
            "ext": EXT_CODE.get(r.get("extinct")) if r.get("extinct") else None,
            "iucn": r.get("iucn"),
        })

    orders_used = {s["order"] for s in out_sp}
    fams_used = {s["family"] for s in out_sp}
    orders = {o["sci"]: {"ru": o.get("ru")} for o in taxa["orders"] if o["sci"] in orders_used}
    families = {
        f["sci"]: {"ru": f.get("ru"), "en": f.get("en")}
        for f in taxa["families"] if f["sci"] in fams_used
    }
    # families missing from taxa.json still get a (Latin-only) heading
    for s in out_sp:
        orders.setdefault(s["order"], {"ru": None})
        families.setdefault(s["family"], {"ru": None, "en": None})

    def grouped(items, letter_fn):
        # identical names (homonyms in the data) -> one line with several numbers
        merged: list[dict] = []
        for it in items:
            if merged and merged[-1]["name"] == it["name"]:
                merged[-1]["ns"].append(it["n"])
                merged[-1]["ext"] = merged[-1]["ext"] and it["ext"]
            else:
                merged.append({"name": it["name"], "ns": [it["n"]], "ext": it["ext"]})
        groups: list[dict] = []
        for it in merged:
            L = letter_fn(it["name"])
            if not groups or groups[-1]["letter"] != L:
                groups.append({"letter": L, "items": []})
            groups[-1]["items"].append(it)
        return groups

    ru_items = sorted(
        ({"name": s["ru"], "n": s["n"], "ext": s["ext"]} for s in out_sp if s["ru"]),
        key=lambda it: (ru_key(it["name"]), it["n"]),
    )
    en_items = sorted(
        ({"name": s["en"], "n": s["n"], "ext": s["ext"]} for s in out_sp if s["en"]),
        key=lambda it: (en_key(it["name"]), it["n"]),
    )
    genera: dict[str, list] = {}
    for s in out_sp:
        genera.setdefault(s["gen"], []).append({"ep": s["ep"], "n": s["n"], "ext": s["ext"]})
    sci_groups: list[dict] = []
    for g in sorted(genera):
        L = g[0].upper()
        if not sci_groups or sci_groups[-1]["letter"] != L:
            sci_groups.append({"letter": L, "genera": []})
        sci_groups[-1]["genera"].append(
            {"genus": g, "items": sorted(genera[g], key=lambda it: (it["ep"], it["n"]))}
        )

    return {
        "meta": {
            "full": full,
            "count": len(out_sp),
            "count_fmt": f"{len(out_sp):,}".replace(",", "\u202f"),
            "total_fmt": f"{len(species):,}".replace(",", "\u202f"),
            "total": len(species),
            "orders": len(orders),
            "families": len(families),
            "genera": len(genera),
            "avilist": "v2025b",
            "iucn": "1",
        },
        "orders": orders,
        "families": families,
        "species": out_sp,
        "idx_ru": grouped(ru_items, ru_letter),
        "idx_en": grouped(en_items, en_letter),
        "idx_sci": sci_groups,
    }


# ================================================================ variant C2
# Iteration 2 of variant C («компактный справочник», 170×240 мм). The list is
# typeset by Typst from prepared records; the three alphabetical indexes are
# laid out here: entries are measured by Typst (print/c2_measure.typ), then
# split into pages and columns in Python. That gives exact column breaks with
# «(продолж.)» lines for nests continued in a new column, balanced columns on
# the last page of an index and running heads «first — last nest of the page».

sys.path.insert(0, str(REPO / "scripts"))
from build import ru_book as ru_book_fn, ru_head as ru_head_fn  # noqa: E402

C2_TPL = "variant_c2.typ"
C2_STEM = "birds_C2_compact"
EXT_SIGN = {"x": "†", "p": "†?", "w": "‡"}

# index grid (must match c2_index.typ): 4 columns × 31 mm, 7.5/8.6 pt
IDX_STEP = 8.6               # pt, line step of the indexes
IDX_COL_W = 31 * MM          # pt
IDX_SIZE = 7.5               # pt
IDX_BODY_H = (240 - 14 - 20) * MM
IDX_LINES = int(IDX_BODY_H // IDX_STEP)   # lines per column on a full page
IDX_TITLE_LINES = 9          # height of the index title block on its first page
IDX_COLS = 4
LETTER_LINES, LETTER_TOP_LINES = 3, 2     # letter separator: in a column / at its top


def plural(n: int, one: str, few: str, many: str) -> str:
    """Russian agreement: 1 вид, 2 вида, 5 видов, 11 видов, 21 вид."""
    n = abs(n)
    if 11 <= n % 100 <= 14:
        return many
    if n % 10 == 1:
        return one
    if 2 <= n % 10 <= 4:
        return few
    return many


def fmt_int(n: int) -> str:
    """11 131 with a narrow no-break space (only for 5+ digits, as in Russian practice)."""
    return f"{n:,}".replace(",", " ") if n >= 10000 else str(n)


def count_txt(n: int, forms: tuple[str, str, str]) -> str:
    return f"{fmt_int(n)}{NBSP}{plural(n, *forms)}"


VID = ("вид", "вида", "видов")
ROD = ("род", "рода", "родов")
SEM = ("семейство", "семейства", "семейств")
OTR = ("отряд", "отряда", "отрядов")


def ru_sort_key(s: str):
    """Russian alphabet with ё = е (е before ё on a tie), word by word."""
    base, tie = [], []
    for ch in s.lower():
        if ch == "ё":
            base.append(RU_RANK["е"]); tie.append(1)
        elif ch in RU_RANK:
            base.append(RU_RANK[ch]); tie.append(0)
        elif ch in " - ":
            base.append(0); tie.append(0)
        elif ch.isalpha():
            base.append(100 + ord(latin_fold(ch)[0])); tie.append(0)
    return base, tie, s


def head_sort_key(head: str):
    """Nest order: a hyphenated head («утка-пароход») right after the nest of its
    first component («утка»)."""
    first = head.split("-")[0]
    return ru_sort_key(first), 1 if "-" in head else 0, ru_sort_key(head)


def lat_key(s: str):
    return latin_fold(s).lower()


def apos(t: str | None) -> str | None:
    """Typographic apostrophe: d'Orbigny -> d’Orbigny, Grauer's -> Grauer’s."""
    return t.replace("'", "\u2019") if t else t


AUTH_LONG = 22   # characters: a chunk longer than this may break between its words


def auth_chunks(auth: str | None) -> list[str]:
    """Author + year as chunks that the template sets as unbreakable boxes,
    separated by breakable spaces. A line may break only before «&» and after
    the comma between co-authors; the last surname, its comma and the year are
    always glued with no-break spaces («Gill, 2003)»). Only a single surname
    too long for a line (> AUTH_LONG characters: «Geoffroy Saint-Hilaire, 1832»,
    «(Du Bus de Gisignies, 1847)») may also break between its own words."""
    if not auth:
        return []
    auth = apos(auth)
    chunks: list[str] = []
    for i, part in enumerate(auth.split(" & ")):
        names = part.split(", ")
        if len(names) > 1 and names[-1].rstrip(")").isdigit():
            names[-2:] = [names[-2] + "," + NBSP + names[-1]]
        for j, nm in enumerate(names):
            nm = ("& " if i and j == 0 else "") + nm + ("," if j < len(names) - 1 else "")
            if len(nm) > AUTH_LONG:
                chunks += nm.split(" ")          # NBSP before the year survives
            else:
                chunks.append(nm)
    return [c.replace(" ", NBSP) for c in chunks]


RDASH = "\u2060–\u2060"   # en dash of a number range, glued to both numbers


def num_range(ns: list[int]) -> str:
    """[36, 37, 38, 40] -> «36–38, 40»."""
    ns = sorted(ns)
    out, start, prev = [], ns[0], ns[0]
    for n in ns[1:] + [None]:
        if n is not None and n == prev + 1:
            prev = n
            continue
        out.append(str(start) if start == prev else f"{start}{RDASH}{prev}")
        if n is not None:
            start = prev = n
    return ", ".join(out)


def sci_abbr(sci: str) -> str:
    g, e = sci.split(" ", 1)
    return f"{g[0]}.{NBSP}{e}"


def runs_merge(runs: list) -> list:
    out: list[list] = []
    for t, st in runs:
        if out and out[-1][1] == st:
            out[-1][0] += t
        else:
            out.append([t, st])
    return out


def nums_runs(nums: list[tuple[int, bool, str]]) -> list:
    """Numbers of one index line: main entries bold, alternative names light;
    homonyms (several species) get the Latin name in small italics."""
    runs: list = []
    homonyms = len(nums) > 1
    for i, (n, main, sci) in enumerate(nums):
        if i:
            runs.append([", ", ""])
        runs.append([str(n), "b" if main else ""])
        if homonyms:
            runs.append([" (", "s"])
            runs.append([sci_abbr(sci), "si"])
            runs.append([")", "s"])
    return runs


def ru_definition(book: str, head: str) -> str:
    """«лесной белолобый перепел», head «перепел» -> «белолобый лесной»: the head
    is removed, the words before it go in reverse order (Коблик: «дятел пёстрый
    большой»), words after it (genitives: «гусь Росса») follow."""
    words = book.split()
    for i, w in enumerate(words):
        if w[:1].lower() + w[1:] == head:
            return " ".join(words[:i][::-1] + words[i + 1:])
    return book


def c2_species(sel: list[dict]) -> list[dict]:
    out = []
    for n, r in enumerate(sel, 1):
        gen, ep = r["sci"].split(" ", 1)
        alts = [ru_book_fn(a, r.get("en"))[0] for a in r.get("ru_alt") or []]
        out.append({
            "n": n, "o": r["order"], "f": r["family"], "g": gen, "e": ep,
            "a": auth_chunks(r.get("auth")),
            "en": r["en"].replace("'", "’") if r.get("en") else None,
            "ru": r.get("ru_book"),
            "st": r.get("ru_status") == "ok_fallback",
            "alt": alts,
            "x": EXT_CODE.get(r.get("extinct")) if r.get("extinct") else None,
        })
    return out


def c2_idx_ru(sel, sp, orders, families) -> list[dict]:
    """Russian index: nests by ru_head. Returns sorted "nests" (dicts with
    head, sort key and lines of runs)."""
    nests: dict[str, dict] = {}
    for r, s in zip(sel, sp):
        if not r.get("ru"):
            continue
        names = [(r["ru_book"], r["ru_head"], True)]
        for alt, book in zip(r.get("ru_alt") or [], s["alt"]):
            names.append((book, ru_head_fn(alt)[0], False))
        for book, head, main in names:
            nest = nests.setdefault(head, {"nums": [], "defs": {}})
            d = ru_definition(book, head)
            if d == head or not d:
                nest["nums"].append((s["n"], main, r["sci"]))
            else:
                nest["defs"].setdefault((d, not main), []).append((s["n"], main, r["sci"]))
    units = []
    for head, nest in nests.items():
        defs = sorted(nest["defs"].items(), key=lambda kv: (ru_sort_key(kv[0][0]), kv[0][1]))
        head_runs = [[head, "b"]]
        if nest["nums"] and not defs:
            lines = [head_runs + [[NBSP, ""]] + nums_runs(nest["nums"])]
        elif not nest["nums"] and len(defs) == 1:
            (d, alt), nums = defs[0]
            lines = [head_runs + [[" ", ""], [d, "i" if alt else ""], [NBSP, ""]] + nums_runs(nums)]
        else:
            first = head_runs + ([[NBSP, ""]] + nums_runs(nest["nums"]) if nest["nums"] else [])
            lines = [first] + [
                [["—" + NBSP, ""], [d, "i" if alt else ""], [NBSP, ""]] + nums_runs(nums)
                for (d, alt), nums in defs]
        units.append({"key": head_sort_key(head), "hw": head, "lines": lines, "nest": len(lines) > 1})
    for o in orders:
        if o["ru"]:
            name = o["ru"].lower()
            units.append({"key": head_sort_key(name), "hw": name, "nest": False,
                          "lines": [[[name, ""], [" " + (f"{o['a']}{RDASH}{o['b']}" if o['a'] != o['b'] else str(o['a'])), ""]]]})
    for f in families.values():
        if f["ru"]:
            name = f["ru"].lower()
            rng = f"{f['a']}{RDASH}{f['b']}" if f["a"] != f["b"] else str(f["a"])
            units.append({"key": head_sort_key(name), "hw": name, "nest": False,
                          "lines": [[[name, ""], [" " + rng, ""]]]})
    units.sort(key=lambda u: u["key"])
    for u in units:
        u["letter"] = ru_letter(u["hw"])
    return units


def c2_idx_en(sel, sp, families) -> list[dict]:
    """English index, H&M style: «Goose Bar-headed 42, Emperor 43» run in.
    Lines are made later (needs measured widths): each unit carries tokens."""
    nests: dict[str, dict] = {}
    for r, s in zip(sel, sp):
        if not s["en"]:
            continue
        head = s["en"].split()[-1]
        d = s["en"][: -len(head)].strip()
        nest = nests.setdefault(head, {"nums": [], "items": []})
        if d:
            nest["items"].append((d, s["n"]))
        else:
            nest["nums"].append(s["n"])
    units = []
    for head, nest in nests.items():
        items = sorted(nest["items"], key=lambda it: (en_key(it[0]), it[1]))
        units.append({"key": en_key(head), "hw": head, "kind": "run",
                      "head": head, "nums": nest["nums"], "items": items})
    for f in families.values():
        if f["en"]:
            rng = f"{f['a']}{RDASH}{f['b']}" if f["a"] != f["b"] else str(f["a"])
            units.append({"key": en_key(f["en"]), "hw": f["en"].split()[0].rstrip(","), "kind": "plain",
                          "lines": [[[f["en"], ""], [" " + rng, ""]]], "nest": False})
    units.sort(key=lambda u: u["key"])
    for u in units:
        u["letter"] = en_letter(u["hw"])
    return units


def c2_idx_sci(sel, sp, orders, families) -> list[dict]:
    """Latin index: «epithet, Genus 37» inverted; genera bold italic with their
    numbers; families and orders in capitals with a range; former combinations
    (ioc_sci ≠ sci) in italics with an arrow."""
    units = []
    genera: dict[str, list[int]] = {}
    for r, s in zip(sel, sp):
        genera.setdefault(s["g"], []).append(s["n"])
        units.append({"key": (lat_key(s["e"]), 1, lat_key(s["g"])), "hw": s["e"], "nest": False,
                      "lines": [[[s["e"], "i"], ["," + NBSP, ""], [s["g"], "i"], [NBSP + str(s["n"]), ""]]]})
        old = r.get("ioc_sci")
        if old and old != r["sci"] and " " in old:
            og, oe = old.split(" ", 1)
            units.append({"key": (lat_key(oe), 2, lat_key(og)), "hw": oe, "nest": False,
                          "lines": [[[oe, "i"], [", ", ""], [og, "i"], [" → ", ""],
                                     [s["g"] + NBSP + s["e"], "i"], [NBSP + str(s["n"]), ""]]]})
    for g, ns in genera.items():
        units.append({"key": (lat_key(g), 0, ""), "hw": g, "nest": False,
                      "lines": [[[g, "bi"], [" " + num_range(ns), ""]]]})
    for o in orders:
        units.append({"key": (lat_key(o["sci"]), 0, "~"), "hw": o["sci"], "nest": False,
                      "lines": [[[o["sci"].upper(), ""], [" " + num_range(list(range(o["a"], o["b"] + 1))), ""]]]})
    for f in families.values():
        units.append({"key": (lat_key(f["sci"]), 0, "~"), "hw": f["sci"], "nest": False,
                      "lines": [[[f["sci"].upper(), ""], [" " + num_range(list(range(f["a"], f["b"] + 1))), ""]]]})
    units.sort(key=lambda u: u["key"])
    for u in units:
        u["letter"] = en_letter(u["hw"])
    return units


def c2_measure(items: list[dict], tokens: list[list] | None = None) -> tuple[list[int], list[float]]:
    """Heights (in index lines) of index lines set in a 31 mm column and widths
    (pt) of English run-in tokens, measured by Typst with the same renderer
    (c2_index.typ). `items`: {"r": runs, optional "ru": true, "c": 1}."""
    payload = {"items": items, "tokens": tokens or []}
    path = OUT / "c2_measure_in.json"
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    res = json.loads(typst.query(str(HERE / "c2_measure.typ"), "<m>", field="value", root=str(HERE),
                                 font_paths=[str(FONTS)], sys_inputs={"data": "/out/" + path.name}))[0]
    path.unlink()
    heights = [max(1, round(h / IDX_STEP)) for h in res["h"]]
    c2_measure.natural = res["nw"]        # natural (unbroken) widths of the items, pt
    return heights, res["w"]


def en_run_lines(unit: dict, width: dict) -> list[tuple[list, int]]:
    """Break an English nest into lines (greedy, like H&M). A line breaks only
    between names (after the comma); a name too long for a continuation line
    starts a new line and breaks between its words. Returns (runs, flag): flag 0
    for the first line, 1 for a line that starts a new name (indent 2 em),
    2 for the rest of a broken name (indent 3 em)."""
    tokens = en_tokens(unit)
    sp_w = width["\x00space"]
    full = IDX_COL_W - 1.5                 # safety margin, pt
    cont = full - 2 * IDX_SIZE             # hanging indent 2 em
    cont2 = full - 3 * IDX_SIZE            # inside a broken name: 3 em
    lines: list[tuple[list, int]] = []
    cur: list = []
    cur_w = 0.0
    flag = 0

    def join(item):                        # words of one name, no-break spaces
        return [r for t in item for r in t + [[NBSP, ""]]][:-1]

    def lim():
        return full if not lines else (cont2 if flag == 2 else cont)

    for item in tokens:                    # item = list of word tokens
        ws = [width[json.dumps(t, ensure_ascii=False)] for t in item]
        item_w = sum(ws) + sp_w * (len(ws) - 1)
        if cur and cur_w + sp_w + item_w <= lim():
            cur += [[" ", ""]] + join(item)
            cur_w += sp_w + item_w
            continue
        if cur:                            # the name goes to a new line
            lines.append((cur, flag))
            cur, cur_w, flag = [], 0.0, 1
        if item_w <= lim():
            cur, cur_w = join(item), item_w
            continue
        for t, w in zip(item, ws):         # a name longer than a line
            if cur and cur_w + sp_w + w > lim():
                lines.append((cur, flag))
                cur, cur_w, flag = [], 0.0, 2
            cur = cur + ([[NBSP, ""]] if cur else []) + t
            cur_w += (sp_w if cur_w else 0) + w
    if cur:
        lines.append((cur, flag))
    return [(runs_merge(l), f) for l, f in lines]


def en_tokens(unit: dict) -> list[list]:
    """Word tokens of a run-in English nest, grouped by name. The last word of a
    name carries its number and the comma (no-break space before the number)."""
    items = []
    head = [[unit["head"], "b"]]
    if unit["nums"]:
        head.append([NBSP + ", ".join(map(str, unit["nums"])), ""])
    if unit["items"]:
        head[-1] = [head[-1][0] + ("," if unit["nums"] else ""), head[-1][1]]
    items.append([head])
    for i, (d, n) in enumerate(unit["items"]):
        words = d.split(" ")
        tail = NBSP + str(n) + ("," if i < len(unit["items"]) - 1 else "")
        toks = [[[w, ""]] for w in words[:-1]] + [[[words[-1] + tail, ""]]]
        items.append(toks)
    return items


CONT_RU, CONT_EN = "(продолж.)", "(cont.)"


def cont_runs(head: str, word: str) -> list:
    return [[head, "b"], [" " + word, ""]]


def c2_paginate(units: list[dict], cont) -> list[dict]:
    """Fill columns and pages. A unit = lines that stay together (a nest head
    with its first line; a letter with the following unit). A unit continuing
    a nest at the top of a column gets the line «head (продолж.)»."""
    def fill(units, caps, maxcols=None, offset=0):
        cols, col, used = [], [], 0
        ci = 0

        def cap():
            return caps(ci // IDX_COLS)
        for i, u in enumerate(units):
            items = u["items"]
            h = sum(it["h"] for it in items)
            if col and used + h > cap():
                cols.append(col)
                ci += 1
                if maxcols is not None and ci >= maxcols:
                    return None
                col, used = [], 0
            if not col:
                items = [dict(it) for it in items]
                if "L" in items[0]:
                    items[0]["h"] = LETTER_TOP_LINES
                elif u.get("cont"):
                    runs, ch = cont(u["cont"])
                    items = [{"r": runs, "h": ch, "cont": 1,
                              **({"ru": True} if items[0].get("ru") else {})}] + items
                h = sum(it["h"] for it in items)
            if h > cap():
                raise RuntimeError(f"index unit taller than a column: {u}")
            col += [dict(it, _u=offset + i, nest=u["hw"]) for it in items]
            used += h
        cols.append(col)
        return cols

    first_cap = IDX_LINES - IDX_TITLE_LINES
    cols = fill(units, lambda page: first_cap if page == 0 else IDX_LINES)
    pages = [cols[i:i + IDX_COLS] for i in range(0, len(cols), IDX_COLS)]
    # balance the last page: the smallest equal column height that still fits
    last = pages[-1]
    start = last[0][0]["_u"]
    rest = units[start:]
    page_cap = first_cap if len(pages) == 1 else IDX_LINES
    total = sum(it["h"] for c in last for it in c)
    for c in range(max(1, math.ceil(total / IDX_COLS)), page_cap + 1):
        try:
            bal = fill(rest, lambda page, c=c: c, maxcols=IDX_COLS, offset=start)
        except RuntimeError:
            continue
        if bal is not None:
            pages[-1] = bal
            break
    out = []
    for pg in pages:
        us = [units[it["_u"]] for c in pg for it in c]
        out.append({
            "first": us[0]["hw"], "last": us[-1]["hw"],
            "cols": [[{k: v for k, v in it.items() if k != "_u"} for it in c] for c in pg],
        })
    return out


def c2_units(raw: list[dict], heights: dict, ru: bool = False) -> list[dict]:
    """Turn index entries into pagination units with letter separators."""
    units, letter = [], None
    for u in raw:
        flags = u.get("flags") or [0] * len(u["lines"])
        lines = [{"r": l, "h": heights[id(l)], **({"c": flags[j]} if flags[j] else {}),
                  **({"ru": True} if ru else {})}
                 for j, l in enumerate(u["lines"])]
        # a nest may break between columns, but never so that one line stays
        # behind or goes ahead alone: its first two and last two lines stay together
        if u.get("nest") and len(lines) > 3:
            groups = [lines[:2]] + [[l] for l in lines[2:-2]] + [lines[-2:]]
        else:
            groups = [lines]
        for j, g in enumerate(groups):
            unit = {"items": g, "hw": u["hw"]}
            if j:
                unit["cont"] = u["hw"]
            units.append(unit)
            if j == 0 and u["letter"] != letter:
                letter = u["letter"]
                unit["items"] = [{"L": letter, "h": LETTER_LINES}] + unit["items"]
    return units


SHY = "\u00ad"
RU_WORD = re.compile(r"[А-Яа-яЁё-]+")
LIST_WORD_MAX = (42 - 7.8) * MM - 8.5    # pt: continuation line of a list entry, bold 8.5 pt
IDX_WORD_MAX = IDX_COL_W - 2 * IDX_SIZE  # pt: continuation line of an index entry, 7.5 pt


def soft_hyphen_maps(names: list[str]) -> tuple[dict, dict]:
    """Russian words too wide for a line get soft hyphens (pyphen, at least 3
    letters on each side); all other words are never broken. Hyphenated words
    («колибри-отшельник») break only at their own hyphen. Returns word maps for
    the list (bold 8.5 pt) and for the Russian index (7.5 pt)."""
    words = sorted({w for n in names for w in RU_WORD.findall(n) if "-" not in w and len(w) >= 12})
    if not words:
        return {}, {}
    _, ws = c2_measure([], [[[w, "b"]] for w in words])   # bold, 7.5 pt
    try:
        import pyphen
        dic = pyphen.Pyphen(lang="ru_RU", left=3, right=3)
    except ImportError:
        print("  C2: pyphen не установлен (uv run --with pyphen …): сверхдлинные слова без переносов")
        return {}, {}
    lst, idx = {}, {}
    for w, wd in zip(words, ws):
        hy = dic.inserted(w, hyphen=SHY)
        if wd * 8.5 / 7.5 > LIST_WORD_MAX:
            lst[w] = hy
        if wd > IDX_WORD_MAX:
            idx[w] = hy
    return lst, idx


def apply_shy(text: str | None, m: dict) -> str | None:
    if not text or not m:
        return text
    return RU_WORD.sub(lambda g: m.get(g.group(), g.group()), text)


def prepare_c2(full: bool) -> dict:
    species = json.loads((REPO / "data/species.json").read_text(encoding="utf-8"))
    taxa = json.loads((REPO / "data/taxa.json").read_text(encoding="utf-8"))
    species.sort(key=lambda r: r["seq"])
    sel = species if full else [r for r in species if r["order"] in SAMPLE_ORDERS]
    sp = c2_species(sel)

    tx_o = {o["sci"]: o for o in taxa["orders"]}
    tx_f = {f["sci"]: f for f in taxa["families"]}
    orders: list[dict] = []
    families: dict[str, dict] = {}
    for s, r in zip(sp, sel):
        if not orders or orders[-1]["sci"] != s["o"]:
            orders.append({"sci": s["o"], "ru": tx_o.get(s["o"], {}).get("ru"), "a": s["n"], "b": s["n"]})
        orders[-1]["b"] = s["n"]
        f = families.setdefault(s["f"], {"sci": s["f"], "ru": tx_f.get(s["f"], {}).get("ru"),
                                         "en": apos(tx_f.get(s["f"], {}).get("en") or r.get("family_en")),
                                         "a": s["n"], "b": s["n"]})
        f["b"] = s["n"]
    for t in orders + list(families.values()):
        t["cnt"] = count_txt(t["b"] - t["a"] + 1, VID)
    n_gen = len({s["g"] for s in sp})

    # ---- indexes: entries -> measure -> lines -> units -> pages
    raw = {"ru": c2_idx_ru(sel, sp, orders, families),
           "en": c2_idx_en(sel, sp, families),
           "sci": c2_idx_sci(sel, sp, orders, families)}
    # soft hyphens only in Russian words too long for a line
    shy_list, shy_idx = soft_hyphen_maps([s["ru"] for s in sp if s["ru"]] + [a for s in sp for a in s["alt"]])
    for s in sp:
        s["ru"] = apply_shy(s["ru"], shy_list)
        s["alt"] = [apply_shy(a, shy_list) for a in s["alt"]]
    for u in raw["ru"]:
        for l in u["lines"]:
            for r in l:
                r[0] = apply_shy(r[0], shy_idx)
    measure_lines, measure_ru = [], []
    for key, units in raw.items():
        for u in units:
            for l in u.get("lines", []):
                measure_lines.append(l)
                measure_ru.append(key == "ru")
    tok_list, tok_seen = [], {}
    for u in raw["en"]:
        if u["kind"] == "run":
            for item in en_tokens(u):
                for t in item:
                    k = json.dumps(t, ensure_ascii=False)
                    if k not in tok_seen:
                        tok_seen[k] = len(tok_list)
                        tok_list.append(t)
    tok_list.append([["x x", ""]])
    tok_list.append([["xx", ""]])
    hs, ws = c2_measure([{"r": l, **({"ru": True} if r else {})} for l, r in zip(measure_lines, measure_ru)], tok_list)
    heights = {id(l): h for l, h in zip(measure_lines, hs)}
    # Latin index: «epithet, Genus 37» is one unbreakable entry; only an entry
    # wider than the column may break after its comma (remeasured below)
    # Russian index: the number may leave its word only when the line is
    # wider than the column («— южноамериканский | 1499»)
    sci_ids = {id(l) for u in raw["sci"] for l in u["lines"]}
    ru_ids = {id(l) for u in raw["ru"] for l in u["lines"]}
    relaxed = []
    for l, nw in zip(measure_lines, c2_measure.natural):
        if nw <= IDX_COL_W - 2:
            continue
        if id(l) in sci_ids:
            for r in l:
                r[0] = r[0].replace("," + NBSP, ", ")
                if r[0].startswith(NBSP) and r[0][1:].isdigit() and len(l[2][0]) >= 15:
                    r[0] = " " + r[0][1:]        # «Catamblyrhynchus | 10990»
            relaxed.append(l)
        elif id(l) in ru_ids:
            for r in l:
                if r[0] == NBSP:
                    r[0] = " "
            relaxed.append(l)
    width = {json.dumps(t, ensure_ascii=False): w for t, w in zip(tok_list, ws)}
    width["\x00space"] = width[json.dumps([["x x", ""]])] - width[json.dumps([["xx", ""]])]
    for u in raw["en"]:
        if u["kind"] == "run":
            res = en_run_lines(u, width)
            u["lines"], u["flags"] = [l for l, _ in res], [f for _, f in res]
            u["nest"] = len(u["lines"]) > 1
    # second pass: the English lines as broken here (a single long word may
    # still wrap at its hyphen) and the «(продолж.)» lines of every nest
    en_lines = [(l, f) for u in raw["en"] if u["kind"] == "run" for l, f in zip(u["lines"], u["flags"])]
    conts = {k: {u["hw"]: cont_runs(u["hw"], word) for u in raw[k] if u.get("nest")}
             for k, word in (("ru", CONT_RU), ("en", CONT_EN))}
    batch = [{"r": l, **({"c": f} if f else {})} for l, f in en_lines]
    batch += [{"r": l, **({"ru": True} if id(l) in ru_ids else {})} for l in relaxed]
    batch += [{"r": r, "ru": k == "ru"} for k in conts for r in conts[k].values()]
    hs2, _ = c2_measure(batch)
    for (l, _), h in zip(en_lines, hs2):
        heights[id(l)] = h
    for l, h in zip(relaxed, hs2[len(en_lines):]):
        heights[id(l)] = h
    cont_h = {}
    off = len(en_lines) + len(relaxed)
    for (k, hw), h in zip([(k, hw) for k in conts for hw in conts[k]], hs2[off:]):
        cont_h[(k, hw)] = h
    idx = {
        "ru": c2_paginate(c2_units(raw["ru"], heights, ru=True), lambda hw: (cont_runs(hw, CONT_RU), cont_h[("ru", hw)])),
        "en": c2_paginate(c2_units(raw["en"], heights), lambda hw: (cont_runs(hw, CONT_EN), cont_h[("en", hw)])),
        "sci": c2_paginate(c2_units(raw["sci"], heights), None),
    }
    n = len(sp)
    meta = {
        "full": full,
        "count": n,
        "count_fmt": fmt_int(n),
        "total_fmt": fmt_int(len(species)),
        "species_txt": count_txt(n, VID),
        "total_txt": count_txt(len(species), VID),
        "genera_txt": count_txt(n_gen, ROD),
        "families_txt": count_txt(len(families), SEM),
        "orders_txt": count_txt(len(orders), OTR),
        "ru_count": fmt_int(sum(1 for r in sel if r.get("ru"))),
        "ru_missing": fmt_int(sum(1 for r in sel if not r.get("ru"))),
        "ru_fallback": fmt_int(sum(1 for r in sel if r.get("ru_status") == "ok_fallback")),
        "max_n_digits": len(str(len(species))),
        "avilist": "v2025b",
        "ioc": "15.2",
        "year": "2026",
        "sample_orders": " и ".join(f"{(o['ru'] or o['sci']).lower()} ({o['sci']})" for o in orders),
    }
    meta["stats"] = c2_stats(species, taxa)
    meta["sample_orders_ru"] = " и ".join((o["ru"] or o["sci"]).lower() for o in orders)
    meta["n_orders_word"] = {1: "одного отряда", 2: "двух отрядов", 3: "трёх отрядов"}.get(len(orders), f"{len(orders)} отрядов")
    data_tables = c2_tables(species, taxa, sp, sel, full)
    return {"meta": meta, "orders": orders, "families": families, "species": sp, "idx": idx,
            "tables": data_tables}
    return {"meta": meta, "orders": orders, "families": families, "species": sp, "idx": idx}


# Russian wording of the reasons in data/overrides.csv (its notes are in English).
OVERRIDE_REASON_RU = {
    "Melanitta deglandi": "в IOC 15.2 (Волков и Коблик) «горбоносый турпан» дан для M. deglandi в широком "
                          "объёме, до выделения M. stejnegeri; принято по eBird (горбоносый — азиатский "
                          "M. stejnegeri). Требует подтверждения С. В. Волковым",
    "Rhytipterna holerythra": "опечатка в IOC 15.2; мужской род, как у других видов рода",
    "Megalaimidae": "в Wikidata «Азиатские дятлы» — неудачное название",
}


def override_reason(sci: str, note: str) -> str:
    if sci in OVERRIDE_REASON_RU:
        return OVERRIDE_REASON_RU[sci]
    if "Latin" in note:
        return "в IOC 15.2 латинская буква внутри русского слова"
    if "typo" in note:
        return "опечатка в IOC 15.2"
    if "missing in Wikidata" in note:
        return "названия нет ни в Wikidata, ни в таблицах ЗММУ"
    return note


def override_before(value: str, note: str) -> str:
    """The name before the correction, recovered from the quoted text of the note."""
    import difflib
    quoted = re.findall(r'"([^"]+)"', note.replace('""', '"'))
    for q in quoted:
        if " " in q:
            return q
    if quoted:
        q = quoted[0]
        words = value.split()
        best = difflib.get_close_matches(q, words, n=1, cutoff=0.3)
        if best:
            return value.replace(best[0], q, 1)
        return q
    return "—"


def c2_tables(species, taxa, sp, sel, full) -> dict:
    """Working tables for the temporary appendix (not part of the edition)."""
    import csv
    from collections import defaultdict
    num = {r["sci"]: s["n"] for r, s in zip(sel, sp)}
    by_sci = {r["sci"]: r for r in species}
    with open(REPO / "data/overrides.csv", encoding="utf-8") as fh:
        ov = list(csv.DictReader(fh))
    lat_c = re.compile(r"[A-Za-z]")
    fixes, taxa_fixes, taxa_formed = [], [], []
    for o in ov:
        if o["field"] != "ru":
            continue
        before = override_before(o["value"], o["note"])
        row = {"n": num.get(o["sci"]), "sci": o["sci"], "before": before, "after": o["value"],
               "latin": bool(lat_c.search(before)), "why": override_reason(o["sci"], o["note"])}
        if o["sci"] in by_sci:
            fixes.append(row)
        elif "Formed by compiler" in o["note"] or "ru.wikipedia" in o["note"]:
            # names of orders / families formed or chosen by the compiler: the
            # note (in English, from overrides.csv) is shown as is, without URLs
            note = re.sub(r"\s*\(?https?://\S+?\)?(?=[\s;,)]|$)", "", o["note"]).replace("(: ", "(")
            note = re.sub(r"ru\.wikipedia:\s*(?=[,;)])", "ru.wikipedia", note)
            taxa_formed.append({"sci": o["sci"], "after": o["value"], "why": note.strip()})
        else:
            taxa_fixes.append(row)
    groups = defaultdict(list)
    for r in species:
        if r.get("ru"):
            groups[r["ru"]].append(r)
    src_ru = {"ioc": "IOC", "ebird": "eBird", "wikidata": "Wikidata", "manual": "правка"}
    dups = [{"ru": nm, "sp": [{"n": num.get(r["sci"]), "sci": r["sci"], "en": apos(r.get("en")),
                               "src": src_ru.get(r.get("ru_source"), r.get("ru_source"))} for r in rs]}
            for nm, rs in groups.items() if len(rs) > 1]
    pool = sel
    fam_ru = {f["sci"]: f.get("ru") for f in taxa["families"]}
    fallback = [{"n": num.get(r["sci"]), "sci": r["sci"], "ru": r["ru"], "en": apos(r.get("en")),
                 "src": src_ru.get(r["ru_source"], r["ru_source"])}
                for r in pool if r.get("ru_status") == "ok_fallback"]
    missing = [{"n": num.get(r["sci"]), "sci": r["sci"], "en": apos(r.get("en")),
                "fam": r["family"], "fam_ru": fam_ru.get(r["family"])}
               for r in pool if not r.get("ru")]
    syn = [{"n": num.get(r["sci"]), "ru": r["ru"], "alt": ", ".join(r["ru_alt"])}
           for r in pool if r.get("ru_alt")]
    return {
        "fixes": fixes, "taxa_fixes": taxa_fixes, "taxa_formed": taxa_formed, "dups": dups,
        "fallback": fallback, "missing": missing, "syn": syn,
        "full_fallback": sum(1 for r in species if r.get("ru_status") == "ok_fallback"),
        "full_missing": sum(1 for r in species if not r.get("ru")),
        "full_syn": sum(1 for r in species if r.get("ru_alt")),
    }


NUM_WORDS = {1: "Одно", 2: "Два", 3: "Три", 4: "Четыре", 5: "Пять", 6: "Шесть", 7: "Семь",
             8: "Восемь", 9: "Девять", 10: "Десять"}


def c2_stats(species: list[dict], taxa: dict) -> dict:
    """Numbers for the introduction and the technical note (whole list, not the sample)."""
    from collections import Counter
    import csv
    src = Counter(r.get("ru_source") for r in species if r.get("ru"))
    names = Counter(r["ru"] for r in species if r.get("ru"))
    dups = [nm for nm, c in names.items() if c > 1]
    examples = []
    for nm in dups[:5]:
        sps = [r for r in species if r.get("ru") == nm]
        examples.append({"ru": ru_book_fn(nm, None)[0],
                         "sci": [r["sci"] for r in sps], "en": [r["en"] for r in sps]})
    with open(REPO / "data/overrides.csv", encoding="utf-8") as fh:
        ov = list(csv.DictReader(fh))
    sci_species = {r["sci"] for r in species}
    taxa_no_ru = [t for t in taxa["orders"] + taxa["families"] if not t.get("ru")]
    return {
        "total": fmt_int(len(species)),
        "total_txt": count_txt(len(species), VID),
        "ru": fmt_int(sum(src.values())),
        "ioc": fmt_int(src.get("ioc", 0)),
        "ebird": src.get("ebird", 0),
        "wikidata": src.get("wikidata", 0),
        "manual": sum(1 for o in ov if o["sci"] in sci_species and o["field"] == "ru"),
        "manual_word": NUM_WORDS.get(sum(1 for o in ov if o["sci"] in sci_species and o["field"] == "ru"), ""),
        "taxa_manual": sum(1 for o in ov if o["sci"] not in sci_species and o["field"] == "ru"),
        "fallback": sum(1 for r in species if r.get("ru_status") == "ok_fallback"),
        "missing": sum(1 for r in species if not r.get("ru")),
        "dups": len(dups),
        "dup_examples": examples,
        "alt": sum(1 for r in species if r.get("ru_alt")),
        "extinct": sum(1 for r in species if r.get("extinct") == "extinct"),
        "possibly": sum(1 for r in species if r.get("extinct") == "possibly_extinct"),
        "ew": sum(1 for r in species if r.get("extinct") == "extinct_in_wild"),
        "orders": len(taxa["orders"]), "families": len(taxa["families"]),
        "orders_no_ru": sum(1 for t in taxa["orders"] if not t.get("ru")),
        "families_no_ru": sum(1 for t in taxa["families"] if not t.get("ru")),
        "taxa_no_ru": len(taxa_no_ru),
        "genera": fmt_int(len({r["sci"].split()[0] for r in species})),
    }


def run_c2(full: bool, preview: bool) -> tuple[Path, int, dict, dict]:
    t0 = time.time()
    data = prepare_c2(full)
    name = "c2_full.json" if full else "c2_sample.json"
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    data_rel = f"/out/{name}"
    pdf = OUT / f"{C2_STEM}{'_full' if full else ''}.pdf"
    try:
        typst.compile(str(HERE / C2_TPL), output=str(pdf), root=str(HERE),
                      font_paths=[str(FONTS)], sys_inputs={"data": data_rel})
    except typst.TypstError as e:
        sys.exit(getattr(e, "diagnostic", str(e)))
    marks = {m["name"]: m for m in json.loads(typst.query(
        str(HERE / C2_TPL), "<sec>", field="value", root=str(HERE),
        font_paths=[str(FONTS)], sys_inputs={"data": data_rel}))}
    total = pdf_pages(pdf)
    sp = c2_spans(marks, data, total)
    print(f"  C2: {pdf.relative_to(REPO)}  {total} pp  {sp}  ({time.time() - t0:.1f}s)")
    # overflow check
    layout = c2_layout(marks, total)
    (OUT / (name.replace(".json", "_layout.json"))).write_text(json.dumps(layout), encoding="utf-8")
    import check_overflow
    problems = check_overflow.check(pdf, layout)
    if problems:
        print(f"  C2: ПЕРЕПОЛНЕНИЕ — {len(problems)} нарушений:")
        for p in problems[:60]:
            print("    " + p)
    else:
        print("  C2: проверка переполнения — нарушений нет")
    import check_layout
    counts, ex = check_layout.check(pdf, json.loads(json.dumps(layout)), data)
    print("  C2: проверки вёрстки:")
    for line in check_layout.report(counts, ex, show=5):
        print("    " + line)
    bad = sum(v for k, v in counts.items() if k != "soft")
    problems = problems + [f"layout: {k} = {v}" for k, v in counts.items() if v and k != "soft"]
    if preview:
        for p in c2_previews(pdf, marks, full):
            print(f"     preview {p.relative_to(REPO)}")
    return pdf, total, sp, {"problems": len(problems), "marks": marks, "checks": counts}


def c2_spans(marks: dict, data: dict, total: int) -> dict:
    """Pages per section of C2 (whole pages; the list's last page counted whole)."""
    def pages(a, b):
        return marks[b]["page"] - marks[a]["page"] + 1
    out = {
        "front": marks["list-start"]["page"] - 1,
        "list": pages("list-start", "list-end"),
        "idx_ru": len(data["idx"]["ru"]),
        "idx_en": len(data["idx"]["en"]),
        "idx_sci": len(data["idx"]["sci"]),
    }
    for k in ("ru", "en", "sci"):
        real = pages(f"idx-{k}-start", f"idx-{k}-end")
        if real != out[f"idx_{k}"]:
            # a page of the index overflowed into an extra page: pagination bug
            raise SystemExit(f"C2: указатель {k}: сверстано {real} полос вместо {out[f'idx_{k}']} "
                             "(переполнение полосы указателя)")
    out["back"] = marks["colophon"]["page"] - marks["idx-sci-end"]["page"]
    out["apparatus"] = out["front"] + out["back"]
    out["book"] = marks["colophon"]["page"]
    out["temp"] = total - marks["colophon"]["page"]
    return out


def c2_layout(marks: dict, total: int) -> dict:
    """Page geometry for the overflow check: kind of every page."""
    kinds = {}
    for p in range(1, total + 1):
        kinds[p] = "single"
    for p in range(marks["list-start"]["page"], marks["list-end"]["page"] + 1):
        kinds[p] = "list"
    for k in ("ru", "en", "sci"):
        first = marks[f"idx-{k}-start"]["page"]
        for p in range(first, marks[f"idx-{k}-end"]["page"] + 1):
            kinds[p] = "index-first" if p == first else "index"
    return {
        "page_mm": [170, 240], "inside": 20, "outside": 14, "top": 14, "bottom": 20,
        "cols": {"list": [3, 5], "index": [4, 4], "index-first": [4, 4], "single": [1, 0]},
        # full-width title block above the columns on the first page of an index
        "skip_top_pt": {"index-first": IDX_TITLE_LINES * IDX_STEP},
        "kinds": kinds,
    }


def c2_previews(pdf: Path, marks: dict, full: bool) -> list[Path]:
    prev = OUT / "preview"
    prev.mkdir(parents=True, exist_ok=True)
    tag = "C2full" if full else "C2"
    for old in prev.glob(f"{tag}_*.png"):
        old.unlink()
    pg = {k: v["page"] for k, v in marks.items()}
    ls = pg["list-start"]
    if full:
        # passerines: a spread around Pomatorhinus montanus and the index pages
        picks = {"spread": [pg.get("probe", ls) - (pg.get("probe", ls) % 2), pg.get("probe", ls) - (pg.get("probe", ls) % 2) + 1],
                 "idx-ru": [pg["idx-ru-start"] + 20], "idx-en": [pg["idx-en-start"] + 10],
                 "idx-sci": [pg["idx-sci-start"] + 10]}
    else:
        picks = {
            "title": [pg["title"]], "imprint": [pg["imprint"]], "contr": [pg["contr"]],
            "toc": [pg["toc"]], "intro": [pg["intro"]], "howto": [pg["howto"]],
            "spread": [ls + 1, ls + 2], "order2": [pg.get("order-2", ls)],
            "idx-ru": [pg["idx-ru-start"]], "idx-en": [pg["idx-en-start"]],
            "idx-sci": [pg["idx-sci-start"]], "sources": [pg["sources"]], "colophon": [pg["colophon"]],
            "about": [pg["about"]], "tables": [pg["tables"], pg["tables"] + 1],
        }
    made = []
    for name, pages in picks.items():
        for p in pages:
            base = prev / f"{tag}_{name}_p{p:03d}"
            subprocess.run(["pdftoppm", "-png", "-r", "110", "-f", str(p), "-l", str(p), "-singlefile",
                            str(pdf), str(base)], check=True)
            made.append(base.with_suffix(".png"))
    return made


# ---------------------------------------------------------------- compile
def compile_variant(key: str, data_rel: str, suffix: str, iucn: bool = True) -> Path:
    tpl, stem = VARIANTS[key]
    pdf = OUT / f"{stem}{suffix}.pdf"
    typst.compile(
        str(HERE / tpl),
        output=str(pdf),
        root=str(HERE),
        font_paths=[str(FONTS)],
        sys_inputs={"data": data_rel, "iucn": "1" if iucn else "0"},
    )
    return pdf


def section_pages(key: str, data_rel: str) -> dict:
    """Section marks (metadata <sec> emitted by the templates): page and x/y in pt."""
    tpl, _ = VARIANTS[key]
    res = typst.query(
        str(HERE / tpl), "<sec>", field="value", root=str(HERE),
        font_paths=[str(FONTS)], sys_inputs={"data": data_rel},
    )
    return {m["name"]: m for m in json.loads(res)}


def pdf_pages(pdf: Path) -> int:
    try:
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
        return int(next(l.split()[-1] for l in out.splitlines() if l.startswith("Pages:")))
    except Exception:
        return -1


# page geometry (mm): width, height, inside, outside, top, bottom; columns of list / indexes
GEOMETRY = {
    "A": (170, 240, 20, 15, 18, 20, 2, 3),
    "B": (170, 240, 20, 15, 18, 20, 1, 3),
    "C": (145, 215, 17, 12, 16, 16, 3, 3),
}


def fill_fraction(key: str, mk: dict, cols: int) -> float:
    """How much of its page a section has used when its end mark is reached."""
    w, h, inside, outside, top, bottom, _, _ = GEOMETRY[key]
    left = inside if mk["page"] % 2 else outside
    tw = (w - inside - outside) * MM
    x = mk["x"] - left * MM
    y = (mk["y"] - top * MM) / ((h - top - bottom) * MM)
    col = min(max(int(x / (tw / cols)), 0), cols - 1)
    return min(max((col + min(max(y, 0), 1)) / cols, 0.02), 1.0)


def spans(key: str, marks: dict) -> dict:
    """Pages per section: whole pages plus the used fraction of the last one."""
    g = GEOMETRY[key]
    out = {}
    for sec, mk, cols in (("list", "list", g[6]), ("idx_ru", "idx-ru", g[7]),
                          ("idx_en", "idx-en", g[7]), ("idx_sci", "idx-sci", g[7])):
        st, en = marks[mk + "-start"], marks[mk + "-end"]
        out[sec] = round(en["page"] - st["page"] + fill_fraction(key, en, cols), 2)
    out["front"] = marks["list-start"]["page"] - 1
    return out


def full_counts() -> dict:
    sp = json.loads((REPO / "data/species.json").read_text(encoding="utf-8"))
    return {
        "species": len(sp),
        "ru": sum(1 for r in sp if r.get("ru")),
        "en": sum(1 for r in sp if r.get("en")),
        "genera": len({r["sci"].split()[0] for r in sp}),
        "orders": len({r["order"] for r in sp}),
        "families": len({r["family"] for r in sp}),
    }


def render_previews(key: str, pdf: Path, marks: dict) -> list[Path]:
    prev = OUT / "preview"
    prev.mkdir(parents=True, exist_ok=True)
    for old in prev.glob(f"{key}_*.png"):
        old.unlink()
    marks = {k: v["page"] for k, v in marks.items()}
    ls = marks["list-start"]
    picks = {
        "title": [1],
        "howto": [marks["howto"]],
        # a spread: list start (recto) is odd -> take the following even+odd pair
        "spread": [ls + 1, ls + 2],
        "order2": [marks.get("order-2", ls)],
        "idx-ru": [marks["idx-ru-start"]],
        "idx-sci": [marks["idx-sci-start"]],
    }
    made = []
    for name, pages in picks.items():
        for p in pages:
            base = prev / f"{key}_{name}_p{p:03d}"
            subprocess.run(
                ["pdftoppm", "-png", "-r", "150", "-f", str(p), "-l", str(p), "-singlefile",
                 str(pdf), str(base)], check=True)
            made.append(base.with_suffix(".png"))
    return made


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", action="store_true", help="typeset all species instead of the sample")
    ap.add_argument("--preview", action="store_true", help="render PNG previews (needs pdftoppm)")
    ap.add_argument("--variants", default="ABCC2", help="any of A, B, C, C2, e.g. ABC or C2")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    data = prepare(args.full)
    name = "full.json" if args.full else "sample.json"
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    data_rel = f"/out/{name}"
    suffix = "_full" if args.full else ""
    m = data["meta"]
    print(f"{name}: {m['count']} species, {m['orders']} orders, {m['families']} families, {m['genera']} genera")

    fc = full_counts()
    results = {}
    keys = re.findall(r"C2|[ABC]", args.variants.upper())
    status = 0
    for key in keys:
        if key == "C2":
            pdf, total, sp, info = run_c2(args.full, args.preview)
            results["C2"] = (pdf, total, sp, info)
            status = 1 if info["problems"] else status
            continue
        t0 = time.time()
        pdf = compile_variant(key, data_rel, suffix)
        marks = section_pages(key, data_rel)
        sp = spans(key, marks)
        results[key] = (pdf, pdf_pages(pdf), sp, marks)
        print(f"  {key}: {pdf.relative_to(REPO)}  {results[key][1]} pp  {sp}  ({time.time() - t0:.1f}s)")
        if args.preview:
            for p in render_previews(key, pdf, marks):
                print(f"     preview {p.relative_to(REPO)}")

    c2 = results.pop("C2", None)
    if args.full:
        actual = {k: {"pages": r[1], **r[2]} for k, r in results.items()}
        if c2:
            actual["C2"] = {"pages": c2[1], **c2[2]}
        prev = json.loads((OUT / "full_pages.json").read_text()) if (OUT / "full_pages.json").exists() else {}
        prev.update(actual)
        (OUT / "full_pages.json").write_text(json.dumps(prev, indent=1), encoding="utf-8")
    elif results:
        write_estimate(data, results, fc)
    if c2:
        write_estimate_c2(c2, args.full, fc)
    return status


def write_estimate(data: dict, results: dict, fc: dict) -> None:
    m = data["meta"]
    n = m["count"]
    n_ru = sum(len(it["ns"]) for g in data["idx_ru"] for it in g["items"])
    n_en = sum(len(it["ns"]) for g in data["idx_en"] for it in g["items"])
    n_sci_lines = n + m["genera"]
    full_sci_lines = fc["species"] + fc["genera"]
    names = {"A": "A «Словарь» (170×240, 2 кол.)",
             "B": "B «Чеклист» (170×240, таблица)",
             "C": "C «Компактный» (145×215, 3 кол.)"}
    lines = [
        "# Оценка объёма книги по макету",
        "",
        f"Выборка: {n} видов ({m['orders']} отряда, {m['families']} семейств, {m['genera']} родов). "
        f"Полный список: {fc['species']} видов, {fc['orders']} отрядов, {fc['families']} семейств, "
        f"{fc['genera']} родов; русских названий {fc['ru']}.",
        "",
        "Экстраполяция линейная: страницы раздела выборки × (элементов в полном списке / элементов в выборке). "
        "Для списка — по числу видов; для русского и английского указателей — по числу названий; "
        "для латинского — по числу строк (виды + заголовки родов). "
        "В варианте A каждый отряд начинается с новой полосы: добавлено ≈0,5 полосы на отряд "
        f"(в полном списке {fc['orders']} отрядов). Ещё +6 полос на титул, оборот, «Как пользоваться» "
        "и выравнивание разделов на нечётную полосу.",
        "",
        "| Вариант | PDF выборки, с. | Список (выборка) | Указатели рус./англ./лат. (выборка) | Список → 11 131 | Указатели → 11 131 | Книга ≈ (кратно 16) | Факт, `--full` |",
        "|---|---|---|---|---|---|---|---|",
    ]
    actual = {}
    if (OUT / "full_pages.json").exists():
        actual = json.loads((OUT / "full_pages.json").read_text())
    print("\nОценка объёма на полный список (экстраполяция по выборке):")
    for key, (pdf, total, sp, marks) in results.items():
        est_list = sp["list"] * fc["species"] / n
        if key == "A":
            est_list += 0.5 * (fc["orders"] - m["orders"])
        est_ru = sp["idx_ru"] * fc["ru"] / n_ru
        est_en = sp["idx_en"] * fc["en"] / n_en
        est_sci = sp["idx_sci"] * full_sci_lines / n_sci_lines
        est_idx = est_ru + est_en + est_sci
        book = est_list + est_idx + 6
        r = math.ceil
        row = (f"| {names[key]} | {total} | {sp['list']:.1f} | {sp['idx_ru']:.1f} / {sp['idx_en']:.1f} / {sp['idx_sci']:.1f} | "
               f"≈ {r(est_list)} | ≈ {r(est_idx)} ({r(est_ru)} + {r(est_en)} + {r(est_sci)}) | "
               f"≈ {r(book)} (≈ {r(book / 16) * 16}) |")
        a = actual.get(key)
        if a:
            row += (f" {a['pages']}: список {a['list']:.0f}, указатели {a['idx_ru'] + a['idx_en'] + a['idx_sci']:.0f} "
                    f"({a['idx_ru']:.0f} + {a['idx_en']:.0f} + {a['idx_sci']:.0f}) |")
        else:
            row += " — |"
        lines.append(row)
        msg = (f"  {names[key]}: выборка {total} с.; список ≈ {r(est_list)} с., указатели ≈ {r(est_idx)} с. "
               f"(рус {r(est_ru)}, англ {r(est_en)}, лат {r(est_sci)}), книга ≈ {r(book)} с. "
               f"(≈ {r(book / 16) * 16} с., кратно 16)")
        if a:
            msg += f"; фактически при --full: {a['pages']} с."
        print(msg)
    lines += [
        "",
        "Числа по выборке — полосы раздела с дробной долей последней полосы (по положению конца раздела "
        "в колонке). Столбец «Факт» заполняется, если запускался `build_print.py --full`: те же шаблоны "
        "сверстали весь список (11 131 вид), это точный объём при текущих настройках.",
        "",
        "Расхождение экстраполяции с фактом объясняется тем, что выборка (гусеобразные и курообразные) "
        "не вполне типична: в полном списке 46 отрядов и 252 семейства (больше заголовков и неполных "
        "полос в варианте A), иные длины названий у воробьиных.",
        "",
    ]
    old = (OUT / "estimate.md").read_text(encoding="utf-8") if (OUT / "estimate.md").exists() else ""
    if C2_BEGIN in old:  # keep the C2 section
        lines += ["", old[old.index(C2_BEGIN):old.index(C2_END) + len(C2_END)], ""]
    (OUT / "estimate.md").write_text("\n".join(lines), encoding="utf-8")

C2_BEGIN, C2_END = "<!-- C2 begin -->", "<!-- C2 end -->"


def write_estimate_c2(c2: tuple, full: bool, fc: dict) -> None:
    """Section «C2» of estimate.md (between markers; rows A/B/C are kept)."""
    pdf, total, sp, info = c2
    store = OUT / "full_pages.json"
    saved = json.loads(store.read_text()) if store.exists() else {}
    key = "C2" if full else "C2_sample"
    saved[key] = {"pages": total, **sp}
    store.write_text(json.dumps(saved, indent=1), encoding="utf-8")
    smp, fl = saved.get("C2_sample"), saved.get("C2")

    def row(label, d):
        if not d:
            return f"| {label} | — | — | — | — | — | — | — |"
        return (f"| {label} | {d.get('book', d['pages'])} | {d['list']} | {d['idx_ru']} / {d['idx_en']} / {d['idx_sci']} "
                f"| {d['idx_ru'] + d['idx_en'] + d['idx_sci']} | {d['front']} + {d['back']} = {d['apparatus']} "
                f"| {d.get('temp', 0)} | {d['pages']} |")
    lines = [
        C2_BEGIN,
        "## C2 «Компактный справочник», итерация 2 (170×240, 3 кол.; указатели 4 кол.)",
        "",
        "Полосы по разделам: список — от первой до последней полосы списка; указатели — число полос, "
        "сверстанных build_print.py (последняя полоса сбалансирована); аппарат — до списка (титул, оборот, "
        "контртитул, оглавление, введение, «Как пользоваться книгой», пустые полосы выравнивания) и после "
        "указателей (источники, колофон); временные страницы (записка «О подготовке этого макета» и рабочие "
        "таблицы) идут после колофона и в объём книги не входят.",
        "",
        "| Прогон | Книга, полос (по колофон) | Список | Указатели рус. / англ. / лат. | Указатели всего | Аппарат (до + после) | Временные (записка, таблицы) | PDF всего |",
        "|---|---|---|---|---|---|---|---|",
        row(f"выборка (гусеобразные + курообразные)", smp),
        row(f"полный список ({count_txt(fc['species'], VID)}, `--full`)", fl),
        "",
    ]
    if smp:
        n_s = json.loads((OUT / "c2_sample.json").read_text())["meta"]["count"]
        est = math.ceil(smp["list"] * fc["species"] / n_s)
        lines.append(f"Линейная экстраполяция списка по выборке: ≈ {est} полос "
                     f"(факт полного прогона: {fl['list'] if fl else '—'}).")
        lines.append("")
    lines.append(C2_END)
    path = OUT / "estimate.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if C2_BEGIN in text:
        a, b = text.index(C2_BEGIN), text.index(C2_END) + len(C2_END)
        text = text[:a] + "\n".join(lines) + text[b:]
    else:
        text = text.rstrip("\n") + "\n\n" + "\n".join(lines) + "\n"
    path.write_text(text, encoding="utf-8")
    print("\n".join(l for l in lines if l.startswith("|")))


if __name__ == "__main__":
    sys.exit(main())
