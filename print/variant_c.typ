// Variant C — «Компактный справочник» (after the HBW/BirdLife Illustrated
// Checklist and Wolters). 145 × 215 mm, three narrow columns, Gentium Book Plus.
// Entry: number + Russian name (bold); Latin + author (indented); English (8 pt, indented).
#import "common.typ": *

#let body-size = 8.6pt
#let en-size = 8pt

#set document(title: "Птицы мира. Трёхъязычный указатель видов — вариант C", author: "birds-index")
#set text(font: "Gentium Book Plus", size: body-size, lang: "ru", hyphenate: false, number-type: "lining")
#set par(justify: false, leading: 0.42em, spacing: 0.42em)
#set page(width: 145mm, height: 215mm,
  margin: (inside: 17mm, outside: 12mm, top: 16mm, bottom: 16mm),
  header-ascent: 35%, footer: none)

#let ind = 0.9em
#let entry(sp) = block(breakable: false, above: 0.42em, below: 0.42em, width: 100%, {
  par(hanging-indent: ind)[#sp-mark(sp)#text(weight: "bold")[#sp.n#sym.space.nobreak#sym.space.nobreak.narrow#ru-name(sp)]]
  pad(left: ind, par(hanging-indent: 0.6em, sci-auth(sp, brk: 24)))
  pad(left: ind, par(hanging-indent: 0.6em, text(size: en-size, en-name(sp))))
})

#let order-head(o) = block(sticky: true, width: 100%, above: 1.4em, below: 0.9em,
  stroke: (top: 0.8pt, bottom: 0.8pt), inset: (y: 0.45em), {
  set align(center)
  text(size: 10.5pt, tracking: 0.04em, smallcaps(lower(o)))
  let r = order-ru(o)
  if r != none { linebreak(); text(size: 9.5pt, r) }
})

#let family-head(f) = block(sticky: true, width: 100%, above: 1.1em, below: 0.6em,
  stroke: (top: 0.4pt), inset: (top: 0.4em), {
  let d = fam(f)
  set par(leading: 0.35em)
  text(weight: "bold", size: 9pt, upper(f))
  if d.ru != none { linebreak(); text(weight: "bold", size: 9pt, d.ru) }
  if d.en != none { linebreak(); text(size: 7.6pt, style: "italic", d.en) }
})

// ---------------------------------------------------------------- front matter
#title-page(title-size: 21pt, rule-width: 45%)
#imprint-page()
#howto-page(sample: block(width: 36mm, entry(data.species.at(calc.min(11, data.species.len() - 1)))),
  size: 8.6pt)

// ---------------------------------------------------------------- systematic list
#set page(columns: 3, header: list-header(size: 7.5pt, caps: true), footer: pgend-footer)
#set columns(gutter: 4mm)
#pagebreak(to: "odd", weak: true)
#mark("list-start")
#{
  let po = none
  let pf = none
  let k = 0
  for sp in data.species {
    if sp.order != po {
      k += 1
      mark("order-" + str(k))
      order-head(sp.order)
      po = sp.order
      pf = none
    }
    if sp.family != pf { family-head(sp.family); pf = sp.family }
    entry(sp)
  }
}
#mark("list-end")

// ---------------------------------------------------------------- indexes
#all-indexes(cols: 3, size: 7.6pt, gutter: 4mm, title-size: 11.5pt)
