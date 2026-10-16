"""Layout checks of the C2 book (proofreading findings turned into tests).

    python print/check_layout.py print/out/birds_C2_compact_full.pdf print/out/c2_full_layout.json print/out/c2_full.json

Counts, on the systematic list (and the Russian index for hyphens):
  hyphen      lines of a Russian name ending in an automatic hyphenation
              (a hyphen that is not part of a hyphenated name) — must be 0;
  soft        breaks at a soft hyphen (only overlong words get them) — reported;
  hanging     columns of the list that start with anything but an entry
              (number) or an order / family heading — e.g. a stray English line;
  year        lines of the list that start with a lone year («, | 1832») ;
  cont1       index columns starting with «head (продолж.)» followed by a
              single line of that nest (from the pagination data);
  apostrophe  straight apostrophes ' anywhere in the PDF.
Exit code 1 if any count except `soft` is non-zero.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from check_overflow import MM, words

SHY = "­"
CYR = re.compile(r"[А-Яа-яЁё]")
YEAR_START = re.compile(r"^\d{4}\)?[,.;]?$")


def columns(ws, left, cw, gutter, ncols, top):
    cols = defaultdict(list)
    for w in ws:
        x0, y0, x1, y1, t = w
        if y1 < top - 3:
            continue          # running head (sits above the type area)
        c = min(ncols - 1, max(0, int((x0 - left + gutter / 2) // (cw + gutter))))
        cols[c].append(w)
    out = {}
    for c, cw_ in cols.items():
        lines: list[list] = []
        for w in sorted(cw_, key=lambda w: (round(w[3], 1), w[0])):
            if lines and abs(w[3] - lines[-1][-1][3]) < 2.0:
                lines[-1].append(w)
            else:
                lines.append([w])
        out[c] = [sorted(l, key=lambda w: w[0]) for l in lines]
    return out


def check(pdf: Path, layout: dict, data: dict) -> tuple[dict, dict]:
    W, H = (v * MM for v in layout["page_mm"])
    inside, outside, top = layout["inside"] * MM, layout["outside"] * MM, layout["top"] * MM
    # names with a real hyphen, to tell it from a hyphenation
    hyph_words = set()
    for s in data["species"]:
        for n in [s["ru"] or ""] + s["alt"]:
            for w in n.replace(SHY, "").split():
                if "-" in w:
                    hyph_words.add(w.strip("(),*").lower())
    heads = set()
    for o in data["orders"]:
        heads.add((o["ru"] or o["sci"]).upper())
        heads.add(o["sci"].upper())
    for f in data["families"].values():
        heads.add(f["sci"])
        if f["ru"]:
            heads.add(f["ru"].split()[0])
    counts = {k: 0 for k in ("hyphen", "soft", "hanging", "year", "cont1", "apostrophe")}
    ex = defaultdict(list)
    for pno, ws in words(pdf):
        for w in ws:
            if "'" in w[4]:
                counts["apostrophe"] += 1
                ex["apostrophe"].append(f"с. {pno}: {w[4]}")
        kind = layout["kinds"].get(str(pno), "single")
        if kind not in ("list", "index", "index-first"):
            continue
        ncols, gutter = layout["cols"][kind]
        gutter *= MM
        left = inside if pno % 2 else outside
        right = W - (outside if pno % 2 else inside)
        cw = (right - left - gutter * (ncols - 1)) / ncols
        col_top = top + layout.get("skip_top_pt", {}).get(kind, 0)
        cols = columns(ws, left, cw, gutter, ncols, col_top)
        for c, lines in cols.items():
            texts = [" ".join(w[4] for w in l) for l in lines]
            for i, l in enumerate(lines[:-1]):
                last = l[-1][4]
                if not CYR.search(last):
                    continue
                if last.endswith(SHY):
                    counts["soft"] += 1
                    ex["soft"].append(f"с. {pno}: {last.rstrip(SHY)}-|{lines[i + 1][0][4]}")
                elif last.endswith("-") and not last.startswith("—"):
                    joined = (last + lines[i + 1][0][4]).strip("(),*").lower()
                    if joined.rstrip(".,") not in hyph_words and not any(joined in h for h in hyph_words):
                        counts["hyphen"] += 1
                        ex["hyphen"].append(f"с. {pno}: {last}|{lines[i + 1][0][4]}")
            if kind != "list":
                continue
            if texts:
                first = texts[0]
                if not (first[:1].isdigit() or any(first.startswith(h) for h in heads)):
                    counts["hanging"] += 1
                    ex["hanging"].append(f"с. {pno}, кол. {c + 1}: «{first}»")
            for l in lines:
                if len(l) == 1 and YEAR_START.match(l[0][4]):
                    counts["year"] += 1
                    ex["year"].append(f"с. {pno}: «{' '.join(w[4] for w in l)}»")
    for key in ("ru", "en", "sci"):
        for pi, pg in enumerate(data["idx"][key]):
            for ci, col in enumerate(pg["cols"]):
                if col and col[0].get("cont"):
                    nest = col[0]["nest"]
                    n = sum(it["h"] for it in col[1:] if it.get("nest") == nest and "L" not in it)
                    # count only lines that follow directly
                    k = 0
                    for it in col[1:]:
                        if it.get("nest") != nest:
                            break
                        k += it["h"]
                    if k < 2:
                        counts["cont1"] += 1
                        ex["cont1"].append(f"{key}, полоса {pi + 1}, кол. {ci + 1}: {nest}")
    return counts, ex


NAMES = {"hyphen": "автоматические переносы в русских строках",
         "soft": "переносы по мягкому дефису (сверхдлинные слова)",
         "hanging": "колонки списка, начинающиеся не со статьи и не с рубрики",
         "year": "строки, начинающиеся с года («, | год»)",
         "cont1": "продолжения гнезда из одной строки",
         "apostrophe": "прямые апострофы"}


def report(counts: dict, ex: dict, show: int = 8) -> list[str]:
    out = []
    for k, n in counts.items():
        out.append(f"{NAMES[k]}: {n}")
        for e in ex.get(k, [])[:show]:
            out.append("    " + e)
    return out


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    counts, ex = check(Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()),
                       json.loads(Path(sys.argv[3]).read_text()))
    print("\n".join(report(counts, ex)))
    return 1 if any(v for k, v in counts.items() if k != "soft") else 0


if __name__ == "__main__":
    sys.exit(main())
