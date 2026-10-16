// 15 variants of one page of the English index (fragment A–G of the sample;
// the nests «Duck» and «Goose» must be on the page).
#import "lib.typ": *

#let E = D.en
#let foot-o = context { set text(size: 7.5pt); align(right, folio()) }
#let label = [Указатель английских названий]
#let enums(ns, bold: false, latin: false, ru: false, pad: false) = ns.map(r => {
  let t = if pad { pad5(r.n) } else { str(r.n) }
  if bold { t = strong(t) }
  if latin { t = [#t#nbsp#text(size: 0.84em, emph(r.abbr))] }
  if ru and r.ru != none { t = [#t#h(0.5em)#text(size: 0.9em, fill: luma(25%), r.ru)] }
  t
}).join(", ")
#let nh(s) = s.replace("-", "-\u{2060}")   // no line break after a hyphen
#let xs(r) = if r.x != none [#ext-sign(r.x)#thin] else []
#let letter-c(size: 10pt, above: 6pt, below: 3pt, fill: black, align-to: center) = L => (
  body: block(spacing: 0pt, inset: (top: above, bottom: below), width: 100%, align(align-to, text(size: size, weight: "bold", fill: fill, L))),
  top: block(spacing: 0pt, inset: (bottom: below), width: 100%, align(align-to, text(size: size, weight: "bold", fill: fill, L))),
  keep: true)

// nest with dash lines (one level)
#let en-nest(u, head: none, dash: [—], d-fmt: d => d, nums: ns => enums(ns), indent: 0em, hang: 2em, cont: none,
  taxon: none, also: none) = {
  if u.kind == "taxon" { return ((body: iline(taxon(u), hang: hang), hw: u.hw),) }
  let out = ((body: iline(head(u), hang: hang), hw: u.hw, keep: u.items.len() > 0),)
  for it in u.items {
    out.push((body: iline([#h(indent)#dash#if dash != [] { nbsp }#d-fmt(it.d)#nbsp#nums(it.nums)], hang: indent + hang),
      cont: if cont != none { cont(u) } else { none }))
  }
  if also != none and u.also.len() > 0 { out.push((body: iline([#h(indent)#also(u.also)], hang: indent + hang))) }
  out
}

// ================================================================ 1. flat, direct
#let E1() = {
  show: typeset.with(font: "PT Serif", size: 8.3pt, step: 10pt)
  let items = with-letters(E.flat, letter-c(size: 8.3pt, above: 7pt, below: 2pt), e => {
    let b = if e.kind == "taxon" [#emph(e.t) #e.rng] else [#xs(e.nums.first())#e.t#nbsp#enums(e.nums)]
    ((body: iline(b, hang: 1.5em), hw: e.t, nest: e.h),)
  }, from: "Comb Duck")
  idx-page(items, n: 2, gutter: 8mm, footer: foot-o,
    head: (a, b) => block(width: 100%, stroke: (bottom: 0.4pt), inset: (bottom: 3pt),
      text(size: 7.5pt, top-edge: "cap-height", bottom-edge: "baseline", grid(columns: (1fr, auto), smallcaps[Index of English Names], [#a — #b]))))
}

// ================================================================ 2. inverted, no nests
#let E2() = {
  show: typeset.with(font: "STIX Two Text", size: 7.8pt, step: 9.3pt)
  let items = with-letters(E.inv, letter-c(size: 9pt, above: 6pt, below: 2pt, align-to: left), e => {
    let b = if e.kind == "taxon" [#smallcaps(e.h) #e.rng] else [#xs(e.nums.first())#e.h#if e.d != "" [, #e.d]#nbsp#enums(e.nums)]
    ((body: iline(b, hang: 1.5em), hw: if e.d != "" { e.h + ", " + e.d } else { e.h }, nest: e.h),)
  }, from: "Duck")
  idx-page(items, n: 3, gutter: 5mm, head: idx-head-std(label))
}

// ================================================================ 3. C2 / H&M: run-in
#let E3() = {
  show: typeset.with(font: "Gentium Book Plus", size: 7.5pt, step: 8.6pt)
  let items = with-letters(E.nests, letter-c(size: 10pt, above: 8pt, below: 3pt), u => {
    if u.kind == "taxon" { return ((body: iline([#u.hw #u.rng], hang: 2em), hw: u.hw),) }
    let parts = u.items.map(it => [#xs(it.nums.first())#nh(it.d)#nbsp#enums(it.nums)])
    let b = [#strong(u.hw)#if u.nums.len() > 0 [#nbsp#enums(u.nums)]#if parts.len() > 0 [ #parts.join(", ")]]
    ((body: block(spacing: 0pt, par(hanging-indent: 2em, b)), hw: u.hw),)
  })
  idx-page(items, n: 4, gutter: 4mm, head: idx-head-std(label))
}

// ================================================================ 4. nests with dash
#let E4() = {
  show: typeset.with(font: "Source Serif 4", size: 7.6pt, step: 9pt)
  let items = with-letters(E.nests, letter-c(size: 9.5pt, above: 7pt, below: 2pt), u => en-nest(u,
    head: u => [#strong(u.hw)#if u.nums.len() > 0 [#nbsp#enums(u.nums)]],
    d-fmt: d => d, hang: 2em, cont: u => iline[#strong(u.hw) (cont.)],
    taxon: u => [#emph(u.hw) #u.rng]), from: "Capercaillie")
  idx-page(items, n: 3, gutter: 5mm, head: idx-head-std(label))
}

// ================================================================ 5. two levels: nest → sub-nest
#let E5() = {
  show: typeset.with(font: "Literata", size: 7.4pt, step: 9pt)
  let items = with-letters(E.nests, letter-c(size: 9pt, above: 6pt, below: 2pt), u => {
    if u.kind == "taxon" { return ((body: iline([#emph(u.hw) #u.rng], hang: 2em), hw: u.hw),) }
    let out = ((body: iline([#strong(u.hw)#if u.nums.len() > 0 [#nbsp#enums(u.nums)]], hang: 2em), hw: u.hw, keep: u.tree.len() > 0),)
    let cont = iline[#strong(u.hw) (cont.)]
    for t in u.tree {
      if "sub" in t {
        out.push((body: iline([#h(0.9em)— #text(weight: "semibold", t.sub)#if t.nums.len() > 0 [#nbsp#enums(t.nums)]], hang: 2.9em), cont: cont, keep: true))
        for (k, it) in t.items.enumerate() {
          out.push((body: iline([#h(1.8em)— #xs(it.nums.first())#it.d#nbsp#enums(it.nums)], hang: 3.8em),
            cont: iline[#strong(u.hw) — #t.sub (cont.)], keep: false))
        }
      } else {
        out.push((body: iline([#h(0.9em)— #xs(t.nums.first())#t.d#nbsp#enums(t.nums)], hang: 2.9em), cont: cont))
      }
    }
    out
  }, from: "Curassow")
  idx-page(items, n: 3, gutter: 5mm, head: idx-head-std(label))
}

// ================================================================ 6. dot leaders
#let E6() = {
  show: typeset.with(font: "Libertinus Serif", size: 7.8pt, step: 9.2pt)
  set text(number-width: "tabular")
  let lead(body, nums) = [#body#h(0.3em)#box(width: 1fr, repeat(gap: 0.15em)[.])#h(0.3em)#nums]
  let items2 = with-letters(E.nests, letter-c(size: 9pt, above: 6pt, below: 2pt), u => {
    if u.kind == "taxon" { return ((body: iline(lead(smallcaps(u.hw), u.rng), hang: 2em), hw: u.hw),) }
    let out = ((body: iline(if u.nums.len() > 0 { lead(strong(u.hw), enums(u.nums)) } else { strong(u.hw) }, hang: 2em), hw: u.hw, keep: u.items.len() > 0),)
    for it in u.items { out.push((body: iline(lead([— #xs(it.nums.first())#it.d], enums(it.nums)), hang: 2em))) }
    out
  }, from: "Curassow")
  idx-page(items2, n: 3, gutter: 6mm, head: idx-head-std(label))
}

// ================================================================ 7. Latin bridge (direct)
#let E7() = {
  show: typeset.with(font: "IBM Plex Serif", size: 7.4pt, step: 9pt)
  let items = with-letters(E.flat, letter-c(size: 8.5pt, above: 6pt, below: 2pt), e => {
    let b = if e.kind == "taxon" [#text(weight: "semibold", e.t) #e.rng #text(size: 0.84em, smallcaps(lower(e.sci)))] else [#text(weight: "semibold")[#xs(e.nums.first())#e.t]#nbsp#enums(e.nums) #text(size: 0.9em, emph(e.nums.first().sci))]
    ((body: iline(b, hang: 1.5em), hw: e.t, nest: e.h),)
  }, from: "Crested Duck")
  idx-page(items, n: 2, gutter: 8mm, head: idx-head-std(label))
}

// ================================================================ 8. Russian bridge (inverted)
#let E8() = {
  show: typeset.with(font: "Noto Serif", size: 7.3pt, step: 8.9pt)
  let items = with-letters(E.inv, letter-c(size: 8.5pt, above: 6pt, below: 2pt), e => {
    let b = if e.kind == "taxon" [#emph(e.h) #e.rng] else [#xs(e.nums.first())#e.h#if e.d != "" [, #e.d]#nbsp#enums(e.nums)#h(0.6em)#text(size: 0.92em, fill: luma(28%), e.nums.first().ru)]
    ((body: iline(b, hang: 1.5em), hw: if e.d != "" { e.h + ", " + e.d } else { e.h }, nest: e.h),)
  }, from: "Duck")
  idx-page(items, n: 2, gutter: 8mm, head: idx-head-std(label))
}

// ================================================================ 9. five columns, no letters
#let E9() = {
  show: typeset.with(font: "Fira Sans", stretch: 75%, size: 6.6pt, step: 7.7pt)
  let items = with-letters(E.nests, none, u => en-nest(u,
    head: u => [#text(weight: "bold", u.hw)#if u.nums.len() > 0 [#nbsp#enums(u.nums)]],
    dash: [–], hang: 1.5em, taxon: u => text(weight: "medium")[#upper(u.hw) #u.rng]))
  idx-page(items, n: 5, gutter: 3mm, head: idx-head-std(label, size: 7pt))
}

// ================================================================ 10. small-caps heads, run-in with middle dots
#let E10() = {
  show: typeset.with(font: "Spectral", size: 7.6pt, step: 9.2pt)
  let items = with-letters(E.nests, L => (body: v(5pt), top: [], keep: true), u => {
    if u.kind == "taxon" { return ((body: iline([#emph(u.hw) #u.rng], hang: 1em), hw: u.hw),) }
    let parts = u.items.map(it => [#xs(it.nums.first())#nh(it.d)#nbsp#text(weight: "semibold", enums(it.nums))])
    let b = [#text(tracking: 0.04em, smallcaps(lower(u.hw)))#if u.nums.len() > 0 [#nbsp#text(weight: "semibold", enums(u.nums))]#if parts.len() > 0 [#h(0.4em)#parts.join[~· ]]]
    ((body: block(spacing: 0pt, below: 2pt, par(hanging-indent: 1em, b)), hw: u.hw),)
  }, from: "Chachalaca")
  idx-page(items, n: 3, gutter: 5mm, head: idx-head-std(label))
}

// ================================================================ 11. dictionary with thumb index
#let E11() = {
  show: typeset.with(font: "Vollkorn", size: 8.2pt, step: 9.8pt)
  let hs(it) = text(font: "Fira Sans", weight: "bold", size: 8.4pt, it)
  let items = with-letters(E.nests, L => none, u => en-nest(u,
    head: u => [#hs(u.hw)#if u.nums.len() > 0 [#nbsp#enums(u.nums)]],
    dash: [], d-fmt: d => d, indent: 1em, hang: 1.5em, also: xs => [► see also #xs.join(", ")],
    taxon: u => [#emph(u.hw) #u.rng]), from: "Duck")
  let letters = "ABCDEFGHIJKLMNOPQRSTUVWYZ".clusters()
  let tab-h = 6.8mm
  idx-page(items, n: 2, gutter: 7mm,
    footer: context { set text(size: 8pt); align(right, folio()) },
    head: (a, b) => block(width: 100%, stroke: (bottom: 0.8pt), inset: (bottom: 3pt),
      grid(columns: (1fr, auto), hs(a), hs(b))),
    extra: ((PW - 9mm, PW, M-TOP, PH - M-BOT),),
    deco: g => {
      let j0 = E.nests.position(u => u.hw == g.first)
      let j1 = E.nests.position(u => u.hw == g.last)
      let on = E.nests.slice(j0, j1 + 1).map(u => u.L).dedup()
      for (i, L) in letters.enumerate() {
        if L in on {
          place(top + left, dx: TW + M-OUT - 8mm, dy: -M-TOP + 20mm + i * tab-h,
            block(width: 8mm, height: tab-h - 0.6mm, fill: black, inset: (left: 2.2mm),
              align(horizon + left, text(font: "Fira Sans", weight: "bold", size: 9pt, fill: white, top-edge: "cap-height", bottom-edge: "baseline", L))))
        }
      }
    })
}

// ================================================================ 12. second colour
#let E12() = {
  show: typeset.with(font: "Alegreya", size: 7.8pt, step: 8.9pt)
  let C = SPOT-RED
  let items = with-letters(E.nests, L => (
    body: block(spacing: 0pt, inset: (top: 6pt, bottom: 1pt), text(size: 15pt, weight: "bold", fill: C, top-edge: "cap-height", L)),
    top: block(spacing: 0pt, inset: (bottom: 1pt), text(size: 15pt, weight: "bold", fill: C, top-edge: "cap-height", L)), keep: true),
    u => en-nest(u,
    head: u => [#text(weight: "bold", fill: C, u.hw)#if u.nums.len() > 0 [#nbsp#enums(u.nums)]],
    dash: text(fill: C)[—], hang: 2em, cont: u => iline[#text(weight: "bold", fill: C, u.hw) (cont.)],
    taxon: u => [#text(fill: C, emph(u.hw)) #u.rng]), from: "Bobwhite")
  idx-page(items, n: 4, gutter: 4mm,
    head: (a, b) => block(width: 100%, stroke: (bottom: 0.5pt + C), inset: (bottom: 3pt),
      text(size: 7.5pt, top-edge: "cap-height", bottom-edge: "baseline", grid(columns: (1fr, auto), label, text(fill: C)[*#a — #b*#h(1.2em)*#folio()*]))))
}

// ================================================================ 13. Gaudin: tiny, 5-digit numbers, direct
#let E13() = {
  show: typeset.with(font: "Fira Sans", size: 6.1pt, step: 7.3pt)
  let items = with-letters(E.flat, L => (body: v(7.3pt), top: [], keep: true), e => {
    let b = if e.kind == "taxon" [#e.t #e.rng] else [#e.t #enums(e.nums, pad: true)]
    ((body: iline(b, hang: 1em), hw: e.t, nest: e.h),)
  })
  idx-page(items, n: 3, gutter: 5mm, footer: context { set text(size: 7pt); align(left, folio()) },
    title: block(width: 100%, inset: (bottom: 6mm), prose({
      text(size: 10pt, weight: "bold")[Указатель английских названий · Index of English Names]
      v(1mm)
      text(size: 6.8pt)[Номер вида — пятизначный, с ведущими нулями; семейства — с диапазоном.]
    })))
}

// ================================================================ 14. head word in its own column
#let E14() = {
  show: typeset.with(font: "Noto Serif", size: 7.4pt, step: 9pt)
  let HW = 21mm
  let items = with-letters(E.nests, letter-c(size: 9pt, above: 6pt, below: 2pt), u => {
    if u.kind == "taxon" {
      return ((body: block(spacing: 0pt, inset: (top: 2.5pt), par(hanging-indent: HW + 2mm)[#emph(u.hw) #u.rng]), hw: u.hw),)
    }
    let rows = ()
    if u.nums.len() > 0 { rows.push([#text(fill: luma(45%))[—]#nbsp#enums(u.nums)]) }
    for it in u.items { rows.push(par(hanging-indent: 1em)[#xs(it.nums.first())#it.d#nbsp#enums(it.nums)]) }
    let out = ()
    for (i, r) in rows.enumerate() {
      out.push((body: block(spacing: 0pt, above: if i == 0 { 2.5pt } else { 0pt },
        grid(columns: (HW, 1fr), column-gutter: 2mm,
          if i == 0 { align(right, text(weight: "bold", u.hw)) } else { [] }, r)),
        hw: if i == 0 { u.hw } else { none }, nest: u.hw,
        cont: if i > 0 { grid(columns: (HW, 1fr), column-gutter: 2mm, align(right, text(weight: "bold", fill: luma(45%), u.hw)), []) } else { none }))
    }
    out
  }, from: "Duck")
  idx-page(items, n: 2, gutter: 8mm, head: idx-head-std(label), colrule: 0.3pt + luma(60%))
}

// ================================================================ 15. inverted + see also, families as entries
#let E15() = {
  show: typeset.with(font: "EB Garamond", size: 8.6pt, step: 9.8pt)
  let hang-L(L) = (body: block(spacing: 0pt, height: 4pt, place(top + left, dx: -6.5mm, dy: 4pt + 1.4pt,
      text(size: 19pt, weight: "bold", top-edge: "cap-height", bottom-edge: "baseline", fill: luma(25%), L))),
    top: block(spacing: 0pt, height: 0pt, place(top + left, dx: -6.5mm, dy: 1.4pt,
      text(size: 19pt, weight: "bold", top-edge: "cap-height", bottom-edge: "baseline", fill: luma(25%), L))), keep: true)
  let items = with-letters(E.nests, hang-L, u => {
    if u.kind == "taxon" { return ((body: iline([#smallcaps(u.hw) #u.rng], hang: 1.5em), hw: u.hw),) }
    let out = ()
    for n in u.nums { out.push((body: iline([#u.hw#nbsp#enums((n,))], hang: 1.5em), hw: u.hw)) }
    for (i, it) in u.items.enumerate() {
      out.push((body: iline([#u.hw, #xs(it.nums.first())#it.d#nbsp#enums(it.nums)], hang: 1.5em), hw: if i == 0 { u.hw } else { none }, nest: u.hw))
    }
    if u.also.len() > 0 { out.push((body: iline([#u.hw, _see also_ #u.also.join(", ")], hang: 1.5em))) }
    out
  }, from: "Duck")
  let g = 8mm
  let cw = (TW - 2 * g) / 3
  idx-page(items, n: 3, gutter: g, head: idx-head-std(label),
    extra: range(3).map(i => (M-IN + i * (cw + g) - 7mm, M-IN + i * (cw + g), M-TOP, PH - M-BOT)))
}

#let EN = (E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15)
