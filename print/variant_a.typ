// Variant A — «Словарь» (after Böhme & Flint, Five-language dictionary of animal names).
// 170 × 240 mm, two columns, PT Serif 9 pt. Each order starts on a new page with a
// full-width head; families are in-column subheads; dictionary-style running heads.
#import "common.typ": *

#let body-size = 9pt
#let num-w = str(meta.count).len() * 0.52em + 0.45em

#set document(title: "Птицы мира. Трёхъязычный указатель видов — вариант A", author: "birds-index")
#set text(font: "PT Serif", size: body-size, lang: "ru", hyphenate: false, number-type: "lining")
#set par(justify: false, leading: 0.5em, spacing: 0.5em)
#set page(width: 170mm, height: 240mm,
  margin: (inside: 20mm, outside: 15mm, top: 18mm, bottom: 20mm),
  header-ascent: 35%, footer: none)

// ---------------------------------------------------------------- entry
// Russian name never splits across lines unless it is longer than a column.
#let ru-bold(sp) = {
  let r = text(weight: "bold", ru-name(sp))
  if ru-name(sp).clusters().len() <= 30 { box(r) } else { r }
}
#let entry(sp) = block(breakable: false, above: 0.45em, below: 0.45em, width: 100%,
  grid(columns: (num-w, 1fr), column-gutter: 0.35em,
    align(right, text(weight: "bold", str(sp.n))),
    {
      sp-mark(sp)
      par(hanging-indent: 0.9em, sci-auth(sp))
      par(hanging-indent: 0.9em, first-line-indent: 0em)[#h(0.9em)#en-name(sp)#h(0.3em)–#h(0.3em)#ru-bold(sp)]
    }))

#let order-head(o) = place(top + center, float: true, scope: "parent", clearance: 7mm, block(width: 100%, {
  set align(center)
  set text(hyphenate: false)
  v(4mm)
  text(size: 15pt, tracking: 0.12em, upper(o))
  let r = order-ru(o)
  if r != none { v(0.15em); text(size: 13pt, r) }
  v(3mm)
  line(length: 30%, stroke: 0.5pt)
}))

#let family-head(f) = block(sticky: true, above: 1.5em, below: 0.8em, width: 100%, {
  set align(center)
  let d = fam(f)
  text(weight: "bold", size: 10pt, upper(f))
  if d.ru != none { text(weight: "bold", size: 10pt)[ — #d.ru] }
  if d.en != none { linebreak(); text(size: 8.5pt, style: "italic", d.en) }
})

// ---------------------------------------------------------------- front matter
#title-page(title-size: 24pt)
#imprint-page()
#howto-page(sample: {
  set par(leading: 0.5em, spacing: 0.5em)
  block(width: 62mm, entry(data.species.at(calc.min(11, data.species.len() - 1))))
}, size: body-size, heads: [Словарного типа: на каждой странице — номер и научное название первого
  (слева) и последнего (справа) вида на этой странице; номер страницы — во внешнем углу.])

// ---------------------------------------------------------------- systematic list
#let dict-head(sp) = [#text(weight: "bold", str(sp.n))#h(0.35em)#emph(sp.sci)]
#set page(columns: 2, footer: pgend-footer, header: context {
  let sps = page-species()
  if sps.len() == 0 { return }
  head-row(dict-head(sps.first()), dict-head(sps.last()))
})
#set columns(gutter: 6mm)
#pagebreak(to: "odd", weak: true)
#mark("list-start")
#{
  let po = none
  let pf = none
  let k = 0
  for sp in data.species {
    if sp.order != po {
      if po != none { pagebreak(weak: true) }
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
#all-indexes(cols: 3, size: 8pt)
