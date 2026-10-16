// Variant B — «Чеклист» (after Howard & Moore / IOC World Bird List).
// 170 × 240 mm, one table across the text block, Source Serif 4, 9 pt.
// Orders and families are full-width subheader rows (table.header level 2/3):
// Typst never leaves them orphaned at a page foot, and the family row repeats
// at the top of the next page together with the column heads.
#import "common.typ": *

#let body-size = 9pt

#set document(title: "Птицы мира. Трёхъязычный указатель видов — вариант B", author: "birds-index")
#set text(font: "Source Serif 4", size: body-size, lang: "ru", hyphenate: false, number-type: "lining")
#set par(justify: false, leading: 0.5em, spacing: 0.5em)
#set page(width: 170mm, height: 240mm,
  margin: (inside: 20mm, outside: 15mm, top: 18mm, bottom: 20mm),
  header-ascent: 35%, footer: none)

#let ncols = if show-iucn { 5 } else { 4 }
// small IUCN code on the baseline of the 9 pt row (cells are top-aligned)
#let small(x) = text(size: 7pt, top-edge: 0.67 * body-size, x)

#let iucn-cell(c) = if c == none { [] } else { small(c.replace(" ", sym.space.nobreak)) }

#let row(sp) = {
  let cells = (
    { sp-mark(sp); str(sp.n) },
    par(hanging-indent: 0.8em, ru-name(sp)),
    par(hanging-indent: 0.8em, sci-auth(sp)),
    par(hanging-indent: 0.8em, en-name(sp)),
  )
  if show-iucn { cells.push(iucn-cell(sp.iucn)) }
  cells
}

#let order-row(o) = {
  let r = order-ru(o)
  table.header(level: 2, repeat: false,
    table.cell(colspan: ncols, inset: (top: 9pt, bottom: 5pt), align: center,
      text(size: 11pt, tracking: 0.08em)[#upper(o)#if r != none [ — #r]]))
}

#let family-row(f) = {
  let d = fam(f)
  table.header(level: 3,
    table.cell(colspan: ncols, inset: (top: 6pt, bottom: 2.5pt, x: 3pt),
      stroke: (bottom: 0.4pt), align: left,
      [#text(weight: "bold", f)#if d.ru != none [ — #text(weight: "bold", d.ru)]#if d.en != none [ — #d.en]]))
}

#let col-heads = {
  let h(x) = text(size: 7.5pt, style: "italic", x)
  let cs = (h[№], h[Русское название], h[Научное название, автор], h[English name])
  if show-iucn { cs.push(h[МСОП]) }
  table.header(level: 1, ..cs.map(c => table.cell(stroke: (top: 0.8pt, bottom: 0.4pt), inset: (y: 3pt, x: 3pt), c)))
}

// ---------------------------------------------------------------- front matter
#title-page(title-size: 24pt)
#imprint-page()
#howto-page(sample: {
  set text(size: body-size)
  let sp = data.species.at(calc.min(11, data.species.len() - 1))
  table(columns: (auto, 36fr, 50fr, 34fr) + if show-iucn { (auto,) } else { () },
    stroke: none, inset: (x: 3pt, y: 1.5pt), ..row(sp))
}, size: body-size, iucn-note: show-iucn)

// ---------------------------------------------------------------- systematic list
#set page(header: list-header(), footer: pgend-footer)
#pagebreak(to: "odd", weak: true)
#mark("list-start")
#{
  set par(leading: 0.36em)
  let cells = ()
  let po = none
  let pf = none
  let k = 0
  for sp in data.species {
    if sp.order != po {
      k += 1
      cells.push(table.cell(colspan: ncols, inset: 0pt, mark("order-" + str(k))))
      cells.push(order-row(sp.order))
      po = sp.order
      pf = none
    }
    if sp.family != pf { cells.push(family-row(sp.family)); pf = sp.family }
    cells += row(sp)
  }
  table(
    columns: (auto, 36fr, 50fr, 34fr) + if show-iucn { (auto,) } else { () },
    align: (col, _) => if col == 0 { right } else { left },
    stroke: none,
    inset: (x: 2.5pt, y: 2pt),
    col-heads,
    ..cells,
  )
}
#mark("list-end")

// ---------------------------------------------------------------- indexes
#all-indexes(cols: 3, size: 8pt)
