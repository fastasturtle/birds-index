"""Overflow check for the print PDFs: finds words that stick out of their column
or out of the type area (Typst itself never reports an overfull line).

    python print/check_overflow.py print/out/birds_C2_compact.pdf print/out/c2_sample_layout.json

The layout file (written by build_print.py) gives the page size, margins and,
for every page, its kind: "list" (3 columns), "index" (4 columns) or "single".
A word is a violation if
  * on a multi-column page, below the running head, it does not lie entirely
    inside one column (with a 0.3 pt tolerance) — this also catches a line that
    runs into the gutter and merges with the word of the next column;
  * anywhere, it crosses the left/right edge of the type area or the bottom
    margin.
Words are taken from `pdftotext -bbox` (poppler). The labels of the thumb-index
tabs (white text in the black tabs on the outer edge, beyond the type area) are
skipped by their text and position. Exit code 1 if anything is found.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

MM = 72 / 25.4
TOL = 0.3  # pt
# Typst hangs punctuation slightly into the margin (text.overhang, optical
# margin alignment); a word ending in punctuation may stick out this much.
PUNCT_TOL = 2.5  # pt
PUNCT = tuple(".,;:!?»)—–-")

# thumb-index tabs of C2 (variant_c2.typ, TABS / TAB-W): label text and the
# width of the tab inside the page, measured from the outer trim edge
TAB_LABELS = {"СПИСОК", "РУССКИЙ", "ENGLISH", "LATINA"}
TAB_W = 9 * MM

PAGE_RE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)
WORD_RE = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')


def words(pdf: Path):
    out = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    for pno, m in enumerate(PAGE_RE.finditer(out), 1):
        W = float(m.group(1))
        ws = [(float(a), float(b), float(c), float(d), html.unescape(t)) for a, b, c, d, t in WORD_RE.findall(m.group(3))]
        yield pno, [w for w in ws if not is_tab(w, pno, W)]


def is_tab(w, pno: int, W: float) -> bool:
    """A thumb-tab label: known text, entirely inside the tab at the outer edge."""
    x0, _, x1, _, t = w
    if t not in TAB_LABELS:
        return False
    return x0 >= W - TAB_W - TOL if pno % 2 else x1 <= TAB_W + TOL


def check(pdf: Path, layout: dict) -> list[str]:
    W, H = (v * MM for v in layout["page_mm"])
    inside, outside = layout["inside"] * MM, layout["outside"] * MM
    top, bottom = layout["top"] * MM, layout["bottom"] * MM
    problems = []
    for pno, ws in words(pdf):
        kind = layout["kinds"].get(str(pno), layout["kinds"].get(pno, "single"))
        left = inside if pno % 2 else outside
        right = W - (outside if pno % 2 else inside)
        ncols, gutter = layout["cols"][kind]
        gutter *= MM
        cw = (right - left - gutter * (ncols - 1)) / ncols
        col_top = top + layout.get("skip_top_pt", {}).get(kind, 0)
        cols = [(left + i * (cw + gutter), left + i * (cw + gutter) + cw) for i in range(ncols)]
        for x0, y0, x1, y1, t in ws:
            where = None
            tol_r = PUNCT_TOL if t.endswith(PUNCT) else TOL
            if x0 < left - TOL or x1 > right + tol_r:
                where = "за краем полосы"
            elif y1 > H - bottom + TOL:
                where = "ниже нижнего поля"
            elif ncols > 1 and y0 >= col_top - TOL and not any(a - TOL <= x0 and x1 <= b + tol_r for a, b in cols):
                where = "за краем колонки"
            if where:
                problems.append(f"с. {pno}: {where}: «{t}» (x {x0:.1f}–{x1:.1f} pt, y {y0:.1f})")
    return problems


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    pdf, layout = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
    problems = check(pdf, layout)
    for p in problems:
        print(p)
    print(f"{pdf.name}: {len(problems)} нарушений" if problems else f"{pdf.name}: переполнений нет")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
