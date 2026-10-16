"""Print (book) layout prototype for the trilingual bird index.

Reads data/species.json + data/taxa.json, prepares a print data file
(numbering, non-breaking spaces, pre-sorted alphabetical indexes) and
compiles three Typst templates (variants A, B, C) into PDF.

    uv run --with typst python print/build_print.py            # sample: Anseriformes + Galliformes
    uv run --with typst python print/build_print.py --full     # whole list (11 131 species)
    uv run --with typst python print/build_print.py --preview  # also render PNG previews

The templates read their data via json(sys.inputs.data) and contain no
sample-specific logic: the same .typ files typeset the full list.
"""

from __future__ import annotations

import argparse
import json
import math
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


MM = 72 / 25.4
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
    ap.add_argument("--variants", default="ABC")
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
    for key in args.variants:
        t0 = time.time()
        pdf = compile_variant(key, data_rel, suffix)
        marks = section_pages(key, data_rel)
        sp = spans(key, marks)
        results[key] = (pdf, pdf_pages(pdf), sp, marks)
        print(f"  {key}: {pdf.relative_to(REPO)}  {results[key][1]} pp  {sp}  ({time.time() - t0:.1f}s)")
        if args.preview:
            for p in render_previews(key, pdf, marks):
                print(f"     preview {p.relative_to(REPO)}")

    if args.full:
        actual = {k: {"pages": r[1], **r[2]} for k, r in results.items()}
        prev = json.loads((OUT / "full_pages.json").read_text()) if (OUT / "full_pages.json").exists() else {}
        prev.update(actual)
        (OUT / "full_pages.json").write_text(json.dumps(prev, indent=1), encoding="utf-8")
    else:
        write_estimate(data, results, fc)
    return 0


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
    (OUT / "estimate.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
