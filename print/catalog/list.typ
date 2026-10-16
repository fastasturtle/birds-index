// 15 variants of one page of the systematic list (same data: Anatidae from № 38;
// a few variants start earlier to show their order/family/genus rubrics).
#import "lib.typ": *

// species from `start`, with rubric callbacks at the real start of an order /
// family / genus
#let walk(start, stop: 176, order-head: none, family-head: none, genus-head: none, entry) = {
  for s in SP.filter(s => s.n >= start and s.n <= stop) {
    let o = order(s.o)
    let f = fam(s.f)
    let g = D.genera.at(s.g)
    if order-head != none and o.a == s.n { order-head(o) }
    if family-head != none and f.a == s.n { family-head(f) }
    if genus-head != none and g.a == s.n { genus-head(g) }
    entry(s)
  }
}

// first and last species number on the current page
#let page-ns() = {
  let p = here().page()
  query(<sp>).filter(q => q.location().page() == p).map(q => q.value.n)
}
#let page-range() = {
  let ns = page-ns()
  if ns.len() == 0 { none } else [#calc.min(..ns)–#calc.max(..ns)]
}
#let page-family() = {
  let ns = page-ns()
  if ns.len() == 0 { return none }
  let s = SP.find(x => x.n == calc.max(..ns))
  fam(s.f)
}

// C2 running head: inner — family; outer — range of numbers + folio, both bold
#let head-c2(size: 7.5pt) = context {
  set text(size: size, top-edge: "cap-height", bottom-edge: "baseline")
  let f = page-family()
  block(width: 100%, stroke: (bottom: 0.3pt), inset: (bottom: 3pt),
    grid(columns: (1fr, auto), if f != none [#f.ru · #f.sci], [*#page-range()*#h(1.2em)*#folio()*]))
}

// ================================================================ 1. C2
#let L1() = {
  let NB = 7.8mm
  let HANG = NB + 1em
  let nbox(body) = box(width: NB, inset: (right: 0.95mm), align(right, body))
  let lp(body, opt: false) = par(hanging-indent: HANG, linebreaks: if opt { "optimized" } else { "simple" }, body)
  let entry(s) = block(above: 2pt, below: 2pt, width: 100%, {
    sp-mark(s)
    let sign = ext-sign(s.x)
    block(breakable: false, spacing: 0pt, width: 100%, {
      lp(opt: true)[#nbox(text(size: 7.5pt, weight: "bold", str(s.n)))#ru-hy[#strong(s.ru)#if s.st { strong("*") }#if s.alt.len() > 0 [ (#s.alt.join(", "))]]]
      lp[#nbox(sign)#emph(s.g + " " + s.e) #author(s)]
    })
    block(breakable: false, spacing: 0pt, lp[#box(width: NB)#text(size: 7.5pt, s.en)])
  })
  book-page(cols: 3, gutter: 5mm, header: head-c2(), header-ascent: 3mm)[
    #geom-cols(3, 5mm)
    #show: typeset.with(font: "Gentium Book Plus", size: 8.5pt, step: 9.6pt)
    #walk(38, entry)
  ]
}

// ================================================================ 2. Бёме–Флинт
#let L2() = {
  let first = 38
  let entry(s) = {
    let full = s.n == first or D.genera.at(s.g).a == s.n
    let g = if full { s.g } else { s.g.first() + "." }
    par[#sp-mark(s)#text(weight: "bold")[#s.n]#h(0.4em)#if ext-sign(s.x) != none [#ext-sign(s.x)#thin]#text(weight: "bold")[#g #s.e]#h(0.3em)#emph(s.au.replace("\u{a0}", " "))#h(0.35em)#text(size: 7pt)[1]#h(0.2em)#ru-hy(s.ru)#h(0.35em)#text(size: 7pt)[2]#h(0.2em)#text(lang: "en", hyphenate: true, s.en)]
  }
  let head = context {
    set text(size: 8pt, weight: "bold", top-edge: "cap-height", bottom-edge: "baseline")
    let ns = page-ns()
    align(right, if ns.len() > 0 { str(calc.min(..ns)) })
  }
  let foot = context { set text(size: 8pt); align(left, folio()) }
  book-page(cols: 2, gutter: 6mm, header: head, footer: foot)[
    #geom-cols(2, 6mm)
    #show: typeset.with(font: "Old Standard TT", size: 8pt, step: 9.4pt)
    #set par(justify: true, linebreaks: "optimized", hanging-indent: 0pt, first-line-indent: (amount: 1em, all: true))
    #walk(first, entry)
  ]
}

// ================================================================ 3. Gaudin
#let L3() = {
  let W = (11mm, 55mm, 37mm, 1fr)
  let row(s) = block(breakable: false, spacing: 0pt, {
    sp-mark(s)
    grid(columns: W, column-gutter: 2mm,
      text(number-type: "lining", pad5(s.n)),
      par(hanging-indent: 1em)[#if ext-sign(s.x) != none [#ext-sign(s.x)#thin]#emph(s.g + " " + s.e) #author(s)],
      par(hanging-indent: 1em, ru-hy(s.ru)),
      par(hanging-indent: 1em, s.en))
  })
  let order-head(o) = block(above: 4pt, below: 7pt, text(size: 9pt, tracking: 0.06em)[#upper(o.sci) · #upper(o.ru)])
  let family-head(f) = block(above: 9pt, below: 6pt, sticky: true)[#text(weight: "bold", f.sci) · #f.ru · #f.en]
  let genus-head(g) = v(5.4pt)
  let foot = context { set text(size: 8pt); folio() }
  book-page(cols: 1, footer: foot)[
    #geom(((M-IN, PW - M-OUT, M-TOP, PH - M-BOT),))
    #show: typeset.with(font: "Fira Sans", size: 7.6pt, step: 9.4pt)
    #walk(1, order-head: order-head, family-head: family-head, genus-head: genus-head, row)
  ]
}

// ================================================================ 4. Howard & Moore
#let L4() = {
  let L = 84mm
  let entry(s) = block(above: 1.5pt, below: 0pt, breakable: false, {
    sp-mark(s)
    grid(columns: (7mm, L - 7mm, 1fr), column-gutter: (0mm, 4mm),
      numbox(7mm, text(size: 7pt, str(s.n)), gap: 1.2mm),
      par(hanging-indent: 1.5em)[#if ext-sign(s.x) != none [#ext-sign(s.x)]#text(weight: "bold", emph(s.g + " " + s.e)) #author(s) #smallcaps(s.en)],
      par(hanging-indent: 1em, ru-hy(s.ru)))
  })
  let genus-head(g) = block(above: 9pt, below: 2pt, sticky: true,
    par(hanging-indent: 1.5em)[#text(size: 10pt, weight: "bold", upper(g.g))#h(0.5em)#text(size: 8pt)[№ #g.rng · #g.cnt]])
  let head = context {
    set text(size: 6.8pt, top-edge: "cap-height", bottom-edge: "baseline")
    block(width: 100%, inset: (bottom: 2pt), upper[Птицы мира: систематический список])
  }
  let foot = context { set text(size: 8pt); folio() }
  book-page(cols: 1, header: head, footer: foot)[
    #geom(((M-IN, M-IN + L, M-TOP, PH - M-BOT), (M-IN + L + 4mm, PW - M-OUT, M-TOP, PH - M-BOT)))
    #show: typeset.with(font: "STIX Two Text", size: 8.5pt, step: 10.2pt)
    #walk(36, genus-head: genus-head, entry)
  ]
}

// ================================================================ 5. Коблик 2006
#let L5() = {
  let sans = "PT Sans"
  let entry(s) = block(above: 6pt, below: 0pt, breakable: false, {
    sp-mark(s)
    grid(columns: (10mm, 1fr, 10mm),
      text(weight: "bold", str(s.n) + "."),
      {
        par(hanging-indent: 1em)[#text(weight: "bold", ru-hy(cap(s.ru)))#if s.Ru == none { "" } #h(0.25em)#if ext-sign(s.x) != none [#ext-sign(s.x)#thin]#emph(s.g + " " + s.e) #author(s)]
        text(font: sans, size: 7.5pt, s.en)
      },
      align(right, text(weight: "bold", s.iucn)))
  })
  let plate(fill, size, word, name, sci) = block(width: 100%, fill: fill, stroke: 0.6pt, inset: (y: 5pt),
    above: 14pt, below: 6pt, sticky: true,
    align(center, text(font: sans, size: size, top-edge: "cap-height", bottom-edge: "baseline")[#word #text(weight: "bold")[#name #sci]]))
  let order-head(o) = plate(luma(82%), 13pt, "Отряд", o.ru, o.sci)
  let family-head(f) = plate(luma(93%), 10.5pt, "Семейство", f.ru, f.sci)
  let head = context {
    set text(size: 8.5pt, style: "italic", top-edge: "cap-height", bottom-edge: "baseline")
    block(width: 100%, stroke: (bottom: 0.4pt), inset: (bottom: 3pt),
      grid(columns: (1fr, auto), [Отряд Гусеобразные Anseriformes], folio()))
  }
  book-page(cols: 1, header: head)[
    #geom(((M-IN, PW - M-OUT, M-TOP, PH - M-BOT),))
    #show: typeset.with(font: "PT Serif", size: 9.5pt, step: 12pt)
    #walk(1, order-head: order-head, family-head: family-head, entry)
  ]
}

// ================================================================ 6. table with rules
#let L6() = {
  let W = (7mm, 39.5mm, 49mm, 1fr)
  let hdr = table.header(..([№], [Русское], [Латинское], [Английское]).map(c => text(size: 7pt, weight: "bold", c)))
  let rows = ()
  for s in SP.filter(s => s.n >= 38) {
    rows += (
      [#sp-mark(s)#align(right, text(weight: "bold", str(s.n)))],
      ru-hy(s.ru),
      [#if ext-sign(s.x) != none [#ext-sign(s.x)#thin]#emph(s.g + " " + s.e) #author(s)],
      s.en)
  }
  let head = context {
    set text(size: 7.5pt, top-edge: "cap-height", bottom-edge: "baseline")
    let f = page-family()
    block(width: 100%, inset: (bottom: 3pt), stroke: (bottom: 0.3pt),
      grid(columns: (1fr, auto), if f != none [#f.ru · #f.sci], [*#page-range()*#h(1.2em)*#folio()*]))
  }
  book-page(cols: 1, header: head)[
    #geom(((M-IN, PW - M-OUT, M-TOP, PH - M-BOT),))
    #show: typeset.with(font: "IBM Plex Serif", size: 7.6pt, step: 9.2pt)
    #set par(hanging-indent: 0.8em)
    #table(columns: W, inset: (x: 1.6mm, y: 1.6pt), stroke: 0.25pt + luma(35%), align: left + horizon,
      hdr, ..rows)
  ]
}

// ================================================================ 7. table, zebra
#let L7() = {
  let W = (9mm, 52mm, 38mm, 1fr)
  let hdr = table.header(..([№], [латинское], [русское], [английское]).map(c => smallcaps(text(size: 7.4pt, c))))
  let rows = ()
  for s in SP.filter(s => s.n >= 38) {
    rows += (
      [#sp-mark(s)#align(right, str(s.n))],
      [#if ext-sign(s.x) != none [#ext-sign(s.x)#thin]#emph(s.g + " " + s.e) #text(size: 6.8pt, fill: luma(35%), author(s))],
      text(weight: "semibold", ru-hy(s.ru)),
      s.en)
  }
  let head = context {
    set text(size: 7.5pt, top-edge: "cap-height", bottom-edge: "baseline")
    let f = page-family()
    block(width: 100%, inset: (bottom: 3pt),
      grid(columns: (1fr, auto), if f != none [#smallcaps(lower(f.ru)) · #f.sci], [#page-range()#h(1.2em)*#folio()*]))
  }
  book-page(cols: 1, header: head)[
    #geom(((M-IN, PW - M-OUT, M-TOP, PH - M-BOT),))
    #show: typeset.with(font: "Source Serif 4", size: 7.8pt, step: 9.6pt)
    #set text(number-width: "tabular")
    #set par(hanging-indent: 0.8em)
    #table(columns: W, inset: (x: 1.5mm, y: 2.2pt), stroke: none, align: left + horizon,
      fill: (_, y) => if y > 0 and calc.even(y) { luma(95%) } else { none },
      table.hline(stroke: 0.6pt), hdr, table.hline(stroke: 0.3pt), ..rows)
  ]
}

// ================================================================ 8. genus as subheading, epithets only
#let L8() = {
  let NB = 6.5mm
  let entry(s) = block(above: 3.2pt, below: 0pt, breakable: false, {
    sp-mark(s)
    par(hanging-indent: NB + 1em)[#numbox(NB, text(size: 7.3pt, weight: "bold", str(s.n)), gap: 1.2mm)#ru-hy(text(weight: "bold", s.ru))#h(0.5em)#text(size: 7.3pt, fill: luma(30%), s.en)]
    par(hanging-indent: NB + 1em)[#h(NB)#if ext-sign(s.x) != none [#ext-sign(s.x)#thin]#emph(s.e) #author(s)]
  })
  let genus-head(g) = block(above: 9pt, below: 3pt, sticky: true, width: 100%, stroke: (bottom: 0.3pt),
    inset: (bottom: 2pt))[#text(size: 9.5pt, weight: "bold", emph(g.g))#h(1fr)#text(size: 7pt)[№ #g.rng · #g.cnt]]
  book-page(cols: 2, gutter: 6mm, header: head-c2())[
    #geom-cols(2, 6mm)
    #show: typeset.with(font: "Spectral", size: 8pt, step: 9.8pt)
    #walk(36, genus-head: genus-head, entry)
  ]
}

// ================================================================ 9. cards
#let L9() = {
  let entry(s) = block(width: 100%, breakable: false, spacing: 0pt, inset: (y: 3.2pt),
    stroke: (bottom: 0.3pt + luma(55%)), {
    sp-mark(s)
    grid(columns: (1fr, auto), ru-hy(text(weight: "bold", s.ru)), text(size: 7.5pt, weight: "bold", str(s.n)))
    par(hanging-indent: 1em)[#if ext-sign(s.x) != none [#ext-sign(s.x)#thin]#emph(s.g + " " + s.e) #author(s)]
    text(size: 7.6pt, s.en)
  })
  book-page(cols: 2, gutter: 8mm, header: head-c2())[
    #geom-cols(2, 8mm)
    #show: typeset.with(font: "Vollkorn", size: 8.5pt, step: 10.2pt)
    #walk(38, entry)
  ]
}

// ================================================================ 10. magazine
#let L10() = {
  let entry(s) = block(above: 5.5pt, below: 0pt, breakable: false, {
    sp-mark(s)
    par(hanging-indent: 1em)[#text(number-type: "old-style", weight: "semibold", str(s.n))#h(0.45em)#smallcaps(ru-hy(s.ru))]
    par(hanging-indent: 1em)[#if ext-sign(s.x) != none [#ext-sign(s.x)#thin]#emph(s.g + " " + s.e)#text(size: 7pt)[ #author(s)]]
    par(hanging-indent: 1em, text(fill: luma(50%), weight: "light", s.en))
  })
  let head = context {
    set text(size: 7pt, top-edge: "cap-height", bottom-edge: "baseline", tracking: 0.08em)
    let f = page-family()
    block(width: 100%, inset: (bottom: 3pt),
      grid(columns: (1fr, auto), if f != none [#smallcaps(lower(f.ru))#h(0.6em)#text(tracking: 0pt, style: "italic", f.sci)], [#page-range()#h(1.4em)#folio()]))
  }
  book-page(cols: 3, gutter: 5mm, header: head)[
    #geom-cols(3, 5mm)
    #show: typeset.with(font: "Literata", size: 7.8pt, step: 9.4pt)
    #walk(38, entry)
  ]
}

// ================================================================ 11. second colour
#let L11() = {
  let C = SPOT-RED
  let NB = 7.2mm
  let HANG = NB + 1em
  let nbox(body) = box(width: NB, inset: (right: 0.9mm), align(right, body))
  let lp(body) = par(hanging-indent: HANG, body)
  let entry(s) = block(above: 2.2pt, below: 2.2pt, breakable: false, width: 100%, {
    sp-mark(s)
    lp[#nbox(text(size: 7.5pt, weight: "bold", fill: C, str(s.n)))#ru-hy(strong(s.ru))]
    lp[#nbox(text(fill: C, ext-sign(s.x)))#emph(s.g + " " + s.e) #author(s)]
    lp[#box(width: NB)#text(size: 7.5pt, s.en)]
  })
  let order-head(o) = block(width: 100%, above: 2pt, below: 6pt, sticky: true, inset: (y: 4pt),
    stroke: (top: 1.2pt + C, bottom: 0.4pt + C),
    align(center)[#text(fill: C, size: 9.5pt, weight: "bold", tracking: 0.06em, upper(o.ru))\ #text(size: 8.5pt, o.sci)])
  let family-head(f) = block(width: 100%, above: 8pt, below: 4pt, sticky: true, inset: (top: 3pt),
    stroke: (top: 0.4pt + C), {
    par[#text(fill: C, size: 9pt, weight: "bold", f.ru)#h(0.5em)#f.sci]
    par(text(size: 7.5pt, f.en))
    par(text(size: 7pt, fill: C)[№#thin#f.rng · #f.cnt])
  })
  let head = context {
    set text(size: 7.5pt, top-edge: "cap-height", bottom-edge: "baseline")
    let f = page-family()
    block(width: 100%, stroke: (bottom: 0.4pt + C), inset: (bottom: 3pt),
      grid(columns: (1fr, auto), if f != none [#f.ru · #f.sci], text(fill: C)[*#page-range()*#h(1.2em)*#folio()*]))
  }
  book-page(cols: 3, gutter: 5mm, header: head)[
    #geom-cols(3, 5mm)
    #show: typeset.with(font: "Libertinus Serif", size: 8.6pt, step: 9.6pt)
    #walk(1, order-head: order-head, family-head: family-head, entry)
  ]
}

// ================================================================ 12. staircase
#let L12() = {
  let NB = 7mm
  let row(indent, body, hy: false) = par(hanging-indent: indent + 1em)[#h(NB + indent)#body]
  let entry(s) = block(above: 3pt, below: 0pt, breakable: false, {
    sp-mark(s)
    par(hanging-indent: NB + 1em)[#numbox(NB, text(size: 8pt, weight: "bold", str(s.n)), gap: 1.2mm)#ru-hy(text(weight: "semibold", s.ru))]
    par(hanging-indent: NB + 2em)[#h(NB + 1em)#if ext-sign(s.x) != none [#ext-sign(s.x)#thin]#emph(s.g + " " + s.e) #author(s)]
    par(hanging-indent: NB + 3em)[#h(NB + 2em)#text(size: 8pt, s.en)]
  })
  book-page(cols: 3, gutter: 5mm, header: head-c2(size: 8pt))[
    #geom-cols(3, 5mm)
    #show: typeset.with(font: "EB Garamond", size: 9.2pt, step: 10pt)
    #walk(38, entry)
  ]
}

// ================================================================ 13. gift edition
#let L13() = {
  let NB = 9mm
  let entry(s) = block(above: 9pt, below: 0pt, breakable: false, {
    sp-mark(s)
    par(hanging-indent: NB + 1em)[#numbox(NB, text(size: 9pt, weight: "medium", number-type: "old-style", str(s.n)), gap: 2mm)#ru-hy(text(size: 10.5pt, weight: "bold", s.ru))]
    par(hanging-indent: NB + 1em)[#h(NB)#if ext-sign(s.x) != none [#ext-sign(s.x)#thin]#emph(s.g + " " + s.e)#text(size: 8.5pt)[ #author(s)]]
    par(hanging-indent: NB + 1em)[#h(NB)#text(size: 9pt, smallcaps(s.en))]
  })
  let head = context {
    set text(size: 8.5pt, top-edge: "cap-height", bottom-edge: "baseline")
    let f = page-family()
    block(width: 100%, inset: (bottom: 3pt),
      grid(columns: (1fr, auto), if f != none [#smallcaps(lower(f.ru))#h(0.5em)·#h(0.5em)#emph(f.sci)], folio()))
  }
  book-page(cols: 2, gutter: 9mm, header: head)[
    #geom-cols(2, 9mm)
    #show: typeset.with(font: "Alegreya", size: 10pt, step: 12pt)
    #walk(38, entry)
  ]
}

// ================================================================ 14. pocket
#let L14() = {
  let NB = 5.6mm
  let lp(body) = par(hanging-indent: NB + 0.8em, body)
  let entry(s) = block(above: 1.8pt, below: 0pt, breakable: false, {
    sp-mark(s)
    lp[#numbox(NB, text(weight: "bold", str(s.n)), gap: 0.8mm)#ru-hy(text(weight: "semibold", s.ru))]
    lp[#h(NB)#if ext-sign(s.x) != none [#ext-sign(s.x)#thin]#emph(s.g + " " + s.e) #text(size: 6.2pt, author(s))]
    lp[#h(NB)#text(weight: "light", s.en)]
  })
  book-page(cols: 4, gutter: 3.5mm, header: head-c2(size: 7pt))[
    #geom-cols(4, 3.5mm)
    #show: typeset.with(font: "Fira Sans", stretch: 75%, size: 7pt, step: 8.5pt)
    #walk(38, entry)
  ]
}

// ================================================================ 15. marginal rail
#let L15() = {
  let R = 8.5mm
  let status(s) = {
    let c = s.iucn
    if s.x != none { text(size: 8pt, weight: "bold", ext-sign(s.x)) }
    else if c in ("CR", "EN", "VU") { box(fill: black, inset: (x: 1.2pt, y: 1.4pt), radius: 1pt, text(fill: white, size: 5.6pt, weight: "bold", c)) }
    else if c == "NT" { box(stroke: 0.5pt, inset: (x: 1.2pt, y: 1.2pt), radius: 1pt, text(size: 5.6pt, weight: "bold", c)) }
    else { none }
  }
  let entry(s) = block(above: 0pt, below: 0pt, breakable: false, width: 100%, inset: (y: 2.6pt), {
    sp-mark(s)
    grid(columns: (R, 1fr), column-gutter: 2.2mm,
      align(right, {
        par(text(size: 8pt, weight: "bold", str(s.n)))
        v(1.5pt)
        status(s)
      }),
      {
        par(hanging-indent: 1em, ru-hy(text(weight: "bold", s.ru)))
        par(hanging-indent: 1em)[#emph(s.g + " " + s.e) #author(s)]
        par(hanging-indent: 1em, text(size: 7pt, style: "italic", fill: luma(25%), s.en))
      })
  })
  let colbg = place(top + left, dx: R + 1.1mm, line(start: (0pt, -1mm), end: (0pt, PH - M-TOP - M-BOT + 1mm), stroke: 0.3pt + luma(55%)))
  book-page(cols: 2, gutter: 7mm, header: head-c2())[
    #let cw = (TW - 7mm) / 2
    #geom(((M-IN, M-IN + R, M-TOP, PH - M-BOT), (M-IN + R + 2.2mm, M-IN + cw, M-TOP, PH - M-BOT),
      (M-IN + cw + 7mm, M-IN + cw + 7mm + R, M-TOP, PH - M-BOT), (M-IN + cw + 7mm + R + 2.2mm, PW - M-OUT, M-TOP, PH - M-BOT)))
    #place(top + left, dx: R + 1.1mm, line(start: (0pt, 0pt), end: (0pt, PH - M-TOP - M-BOT), stroke: 0.3pt + luma(60%)))
    #place(top + left, dx: cw + 7mm + R + 1.1mm, line(start: (0pt, 0pt), end: (0pt, PH - M-TOP - M-BOT), stroke: 0.3pt + luma(60%)))
    #show: typeset.with(font: "Noto Serif", size: 7.6pt, step: 9.3pt)
    #walk(38, entry)
  ]
}

#let LIST = (L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12, L13, L14, L15)
