// 15 variants of one page of the Russian index (fragment А–К of the sample;
// a variant with a small page capacity starts later, so that the nests «гусь»,
// «казарка» and «куропатка» are on the page).
#import "lib.typ": *

#let R = D.ru
#let foot-c = context { set text(size: 7.5pt); align(center, folio()) }
#let foot-o = context { set text(size: 7.5pt); align(right, folio()) }
#let label = [Указатель русских названий]

// ---- shared item builders
// nest with dash lines: head line, «— def nums» lines; style dict:
//   head(u) -> content of the head line (with its numbers), dash: "—" or "~",
//   def(d) -> content of a definition, nums(ns) -> numbers, sep: between def and numbers,
//   indent: indent of dash lines, cont: content of a continuation line or none
#let nest-items(u, head: none, dash: [—], def: none, nums: none, sep: nbsp, indent: 0em, hang: 2em,
  cont: none, also: none, taxon: none) = {
  if u.kind == "taxon" {
    return ((body: iline(taxon(u), hang: hang), hw: u.hw),)
  }
  let out = ((body: iline(head(u), hang: hang), hw: u.hw, keep: u.defs.len() > 0),)
  for d in u.defs {
    out.push((body: iline([#h(indent)#dash#nbsp#def(d)#sep#nums(d.nums)], hang: indent + hang),
      cont: if cont != none { cont(u) } else { none }))
  }
  if also != none and u.also.len() > 0 {
    out.push((body: iline([#h(indent)#also(u.also)], hang: indent + hang)))
  }
  out
}
#let defn(d) = if d.alt { emph(d.d) } else { d.d }
#let ref-also(xs) = [_см. также_ #xs.join(", ")]

// letter header: centred bold, `lines` of space (top variant without space above)
#let letter-c(size: 10pt, above: 6pt, below: 3pt, fill: black) = L => (
  body: block(spacing: 0pt, inset: (top: above, bottom: below), width: 100%, align(center, text(size: size, weight: "bold", fill: fill, L))),
  top: block(spacing: 0pt, inset: (bottom: below), width: 100%, align(center, text(size: size, weight: "bold", fill: fill, L))),
  keep: true)

// ================================================================ 1. flat, direct
#let R1() = {
  show: typeset.with(font: "IBM Plex Serif", size: 8.2pt, step: 10pt)
  let items = with-letters(R.flat, letter-c(size: 8.2pt, above: 7pt, below: 2pt), e => {
    let body = if e.kind == "taxon" [#cap(e.t), #e.rng] else if e.alt [#emph(cap(e.t)) #inums(e.nums, bold: false)] else [#cap(e.t)#nbsp#inums(e.nums, bold: false)]
    ((body: iline(body, hang: 1.5em), hw: cap(e.t), nest: e.h),)
  })
  idx-page(items, n: 2, gutter: 8mm, footer: foot-o,
    head: (a, b) => block(width: 100%, stroke: (bottom: 0.4pt), inset: (bottom: 3pt),
      text(size: 7.5pt, top-edge: "cap-height", bottom-edge: "baseline", grid(columns: (1fr, auto), smallcaps[Алфавитный указатель русских названий], [#a — #b]))),
    title: block(width: 100%, inset: (bottom: 5mm), align(center, prose({
      text(size: 10pt, weight: "bold", upper[Алфавитный указатель русских названий])
      v(2mm)
      block(width: 80%, text(size: 7.4pt, style: "italic")[Названия в прямом порядке, как они стоят в списке. Номер — номер вида. Отряды и семейства — с диапазоном номеров; альтернативные названия — курсивом.])
    }))))
}

// ================================================================ 2. C2: nests with dash, 4 columns
#let R2() = {
  show: typeset.with(font: "Gentium Book Plus", size: 7.5pt, step: 8.6pt)
  let items = with-letters(R.nests, letter-c(size: 10pt, above: 8pt, below: 3pt), u => nest-items(u,
    head: u => [#strong(u.hw)#if u.nums.len() > 0 [#nbsp#inums(u.nums)]],
    def: defn, nums: ns => inums(ns), hang: 2em,
    cont: u => iline[#strong(u.hw) (продолж.)],
    taxon: u => [#u.hw #u.rng]))
  idx-page(items, n: 4, gutter: 4mm, head: idx-head-std(label),
    title: block(width: 100%, height: 9 * 8.6pt, align(center, prose({
      text(size: 12pt, weight: "bold")[Алфавитный указатель русских названий]
      v(0.3em)
      text(size: 9pt, style: "italic")[Index of Russian Names]
      v(2mm)
      block(width: 88%, par(leading: 0.45em, text(size: 7.5pt, style: "italic")[Названия собраны в гнёзда по ведущему слову (полужирным); тире заменяет его повтор, определения внутри гнезда — в обратном порядке. Номера основных статей — полужирным; альтернативные названия набраны курсивом, их номера — светлым.]))
    }))))
}

// ================================================================ 3. Павлинов
#let R3() = {
  show: typeset.with(font: "STIX Two Text", size: 8.4pt, step: 10pt)
  let items = with-letters(R.nests, L => (body: v(10pt), top: [], keep: true), u => {
    if u.kind == "taxon" {
      return ((body: iline([#cap(u.hw), #u.rng], hang: 1.5em), hw: cap(u.hw), nest: u.hw),)
    }
    let out = ((body: iline([#cap(u.hw)#if u.nums.len() > 0 [, #inums(u.nums)]], hang: 1.5em), hw: cap(u.hw), nest: u.hw, keep: u.defs.len() > 0),)
    for d in u.defs {
      out.push((body: iline(if d.alt [#h(1.5em)— #emph(d.d). #emph[См.] #cap(d.ref)] else [#h(1.5em)— #d.d, #inums(d.nums)], hang: 3em)))
    }
    if u.also.len() > 0 { out.push((body: iline([#h(1.5em)#emph[См. также] #u.also.map(cap).join(", ")], hang: 3em))) }
    out
  }, from: "гуменник")
  idx-page(items, n: 2, gutter: 9mm, footer: foot-o,
    head: (a, b) => block(width: 100%, stroke: (bottom: 0.5pt), inset: (bottom: 3pt),
      align(center, text(size: 8pt, style: "italic", top-edge: "cap-height", bottom-edge: "baseline")[Птицы мира — указатель названий таксонов])))
}

// ================================================================ 4. Стриганова: tilde, huge letters
#let R4() = {
  show: typeset.with(font: "Old Standard TT", size: 7.3pt, step: 8.3pt)
  let big(L) = (body: block(spacing: 0pt, inset: (top: 10pt, bottom: 6pt), text(size: 20pt, weight: "bold", top-edge: "cap-height", L)),
    top: block(spacing: 0pt, inset: (bottom: 6pt), text(size: 20pt, weight: "bold", top-edge: "cap-height", L)), keep: true)
  let items = with-letters(R.nests, big, u => nest-items(u,
    head: u => [#u.hw#if u.nums.len() > 0 [ #inums(u.nums, bold: false)]],
    dash: [\~], def: defn, nums: ns => inums(ns, bold: false), sep: [ ], hang: 1.2em,
    taxon: u => [#u.hw #u.rng]))
  idx-page(items, n: 3, gutter: 5mm, footer: foot-o, gap: 2mm,
    head: (a, b) => align(right, text(size: 12pt, weight: "bold", top-edge: "cap-height", bottom-edge: "baseline")[РУССКИЙ]))
}

// ================================================================ 5. run-in nests (H&M)
#let R5() = {
  show: typeset.with(font: "Source Serif 4", size: 7.4pt, step: 8.8pt)
  let items = with-letters(R.nests, letter-c(size: 9.5pt, above: 7pt, below: 2pt), u => {
    if u.kind == "taxon" { return ((body: iline([#u.hw #u.rng], hang: 1em), hw: u.hw),) }
    let parts = u.defs.map(d => [#defn(d)#nbsp#inums(d.nums)])
    let body = [#strong(u.hw)#if u.nums.len() > 0 [#nbsp#inums(u.nums)]#if parts.len() > 0 [#h(0.35em)#parts.join(", ")]]
    ((body: block(spacing: 0pt, below: 1.6pt, par(hanging-indent: 1em, ru-hy(body))), hw: u.hw),)
  })
  idx-page(items, n: 3, gutter: 5mm, head: idx-head-std(label))
}

// ================================================================ 6. Коблик: inversion, no nests
#let R6() = {
  show: typeset.with(font: "PT Serif", size: 8.6pt, step: 10.4pt)
  let big(L) = (body: block(spacing: 0pt, inset: (top: 10pt, bottom: 4pt), text(size: 17pt, top-edge: "cap-height", L)),
    top: block(spacing: 0pt, inset: (bottom: 4pt), text(size: 17pt, top-edge: "cap-height", L)), keep: true)
  let items = with-letters(R.inv, big, e => {
    let t = if e.kind == "taxon" [#e.t – #e.rng] else if e.alt [#emph(e.t) – #emph(inums(e.nums, bold: false))] else [#e.t – #emph(inums(e.nums, bold: false))]
    ((body: iline(t, hang: 1.5em), hw: e.t, nest: e.h),)
  }, from: "гусь")
  idx-page(items, n: 2, gutter: 9mm,
    head: (a, b) => block(width: 100%, stroke: (bottom: 0.4pt), inset: (bottom: 3pt),
      text(size: 8.5pt, style: "italic", top-edge: "cap-height", bottom-edge: "baseline", grid(columns: (1fr, auto), [Птицы мира], folio()))))
}

// ================================================================ 7. ЗИН: dot leaders, numbers flush right
#let R7() = {
  show: typeset.with(font: "Libertinus Serif", size: 7.8pt, step: 9.2pt)
  set text(number-width: "tabular")
  let lead(body, nums) = [#body#h(0.3em)#box(width: 1fr, repeat(gap: 0.15em)[.])#h(0.3em)#nums]
  let items = with-letters(R.nests, letter-c(size: 9pt, above: 6pt, below: 2pt), u => nest-items(u,
    head: u => if u.nums.len() > 0 { lead(strong(u.hw), inums(u.nums, bold: false)) } else { strong(u.hw) },
    dash: [], def: d => lead([— #defn(d)], inums(d.nums, bold: false)), nums: ns => [], sep: [], indent: 0em, hang: 2em,
    taxon: u => lead(smallcaps(u.hw), u.rng)))
  idx-page(items, n: 3, gutter: 6mm, head: idx-head-std(label))
}

// ================================================================ 8. Latin after every number
#let R8() = {
  show: typeset.with(font: "Literata", size: 7.2pt, step: 8.8pt)
  let items = with-letters(R.nests, letter-c(size: 9pt, above: 6pt, below: 2pt), u => nest-items(u,
    head: u => [#strong(u.hw)#if u.nums.len() > 0 [ #inums(u.nums, latin: true)]],
    def: defn, nums: ns => inums(ns, latin: true), sep: [ ], hang: 2em,
    taxon: u => [#u.hw #u.rng #text(size: 0.82em, smallcaps(lower(u.sci)))]), from: "гага")
  idx-page(items, n: 3, gutter: 5mm, head: idx-head-std(label))
}

// ================================================================ 9. five columns, no letters
#let R9() = {
  show: typeset.with(font: "Fira Sans", stretch: 75%, size: 6.6pt, step: 7.7pt)
  let items = with-letters(R.nests, none, u => nest-items(u,
    head: u => [#text(weight: "bold", u.hw)#if u.nums.len() > 0 [#nbsp#inums(u.nums, bold: false)]],
    dash: [–], def: defn, nums: ns => inums(ns, bold: false), hang: 1.5em,
    taxon: u => text(weight: "medium")[#upper(u.hw) #u.rng]))
  idx-page(items, n: 5, gutter: 3mm, head: idx-head-std(label, size: 7pt))
}

// ================================================================ 10. letter in a rule, light numbers
#let R10() = {
  show: typeset.with(font: "Spectral", size: 7.7pt, step: 9.3pt)
  let rl(L) = grid(columns: (1fr, auto, 1fr), column-gutter: 0.6em, align: horizon,
    line(length: 100%, stroke: 0.4pt), text(size: 8.5pt, weight: "bold", tracking: 0.1em, L), line(length: 100%, stroke: 0.4pt))
  let items = with-letters(R.nests, L => (body: block(spacing: 0pt, inset: (top: 7pt, bottom: 3pt), rl(L)),
    top: block(spacing: 0pt, inset: (bottom: 3pt), rl(L)), keep: true), u => nest-items(u,
    head: u => [#text(weight: "semibold", u.hw)#if u.nums.len() > 0 [#nbsp#inums(u.nums, bold: false)]],
    def: defn, nums: ns => inums(ns, bold: false), indent: 0.8em, hang: 1.6em,
    cont: u => iline[#text(weight: "semibold", u.hw) #emph[(продолж.)]],
    taxon: u => [#emph(u.hw) #u.rng]), from: "белошей")
  idx-page(items, n: 3, gutter: 5mm, head: idx-head-std(label))
}

// ================================================================ 11. dictionary with thumb index
#let R11() = {
  show: typeset.with(font: "Vollkorn", size: 8.2pt, step: 9.8pt)
  let hs = (sz) => (it) => text(font: "Fira Sans", weight: "bold", size: sz, it)
  let items = with-letters(R.nests, L => none, u => nest-items(u,
    head: u => [#hs(8.4pt)(u.hw)#if u.nums.len() > 0 [#nbsp#inums(u.nums, bold: false)]],
    def: defn, nums: ns => inums(ns, bold: false), indent: 1em, hang: 1.5em,
    also: xs => [► #xs.join(", ")],
    taxon: u => [#hs(8.4pt)(u.hw) #u.rng]), from: "гусь")
  let letters = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЭЮЯ".clusters()
  let tab-h = 7.6mm
  idx-page(items, n: 2, gutter: 7mm,
    footer: context { set text(size: 8pt); align(right, folio()) },
    head: (a, b) => block(width: 100%, stroke: (bottom: 0.8pt), inset: (bottom: 3pt),
      grid(columns: (1fr, auto), text(font: "Fira Sans", weight: "bold", size: 9pt, top-edge: "cap-height", bottom-edge: "baseline", a),
        text(font: "Fira Sans", weight: "bold", size: 9pt, top-edge: "cap-height", bottom-edge: "baseline", b))),
    extra: ((PW - 9mm, PW, M-TOP, PH - M-BOT),),
    deco: g => {
      // thumb tabs of the letters on this page, at their place in the alphabet
      let j0 = R.nests.position(u => u.hw == g.first)
      let j1 = R.nests.position(u => u.hw == g.last)
      let on = R.nests.slice(j0, j1 + 1).map(u => u.L).dedup()
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
#let R12() = {
  show: typeset.with(font: "Alegreya", size: 7.8pt, step: 8.9pt)
  let C = SPOT-BLUE
  let items = with-letters(R.nests, L => (
    body: block(spacing: 0pt, inset: (top: 6pt, bottom: 1pt), text(size: 15pt, weight: "bold", fill: C, top-edge: "cap-height", L)),
    top: block(spacing: 0pt, inset: (bottom: 1pt), text(size: 15pt, weight: "bold", fill: C, top-edge: "cap-height", L)), keep: true),
    u => nest-items(u,
    head: u => [#text(weight: "bold", fill: C, u.hw)#if u.nums.len() > 0 [#nbsp#inums(u.nums)]],
    dash: text(fill: C)[—], def: defn, nums: ns => inums(ns), hang: 2em,
    cont: u => iline[#text(weight: "bold", fill: C, u.hw) (продолж.)],
    taxon: u => [#text(fill: C, smallcaps(u.hw)) #u.rng]))
  idx-page(items, n: 4, gutter: 4mm,
    head: (a, b) => block(width: 100%, stroke: (bottom: 0.5pt + C), inset: (bottom: 3pt),
      text(size: 7.5pt, top-edge: "cap-height", bottom-edge: "baseline", grid(columns: (1fr, auto), label, text(fill: C)[*#a — #b*#h(1.2em)*#folio()*]))))
}

// ================================================================ 13. hanging letters in the gutter
#let R13() = {
  show: typeset.with(font: "EB Garamond", size: 8.8pt, step: 9.9pt)
  let hang-L(L) = (body: block(spacing: 0pt, height: 4pt, place(top + left, dx: -6.5mm, dy: 4pt + 1.4pt,
      text(size: 19pt, weight: "bold", top-edge: "cap-height", bottom-edge: "baseline", fill: luma(25%), L))),
    top: block(spacing: 0pt, height: 0pt, place(top + left, dx: -6.5mm, dy: 1.4pt,
      text(size: 19pt, weight: "bold", top-edge: "cap-height", bottom-edge: "baseline", fill: luma(25%), L))), keep: true)
  let items = with-letters(R.nests, hang-L, u => nest-items(u,
    head: u => [#text(weight: "semibold", u.hw)#if u.nums.len() > 0 [#nbsp#inums(u.nums)]],
    def: defn, nums: ns => inums(ns), indent: 0.6em, hang: 1.6em,
    taxon: u => [#smallcaps(u.hw) #u.rng]), from: "белошей")
  let g = 8mm
  let cw = (TW - 2 * g) / 3
  idx-page(items, n: 3, gutter: g, head: idx-head-std(label),
    extra: range(3).map(i => (M-IN + i * (cw + g) - 7mm, M-IN + i * (cw + g), M-TOP, PH - M-BOT)))
}

// ================================================================ 14. head word in its own column
#let R14() = {
  show: typeset.with(font: "Noto Serif", size: 7.5pt, step: 9.1pt)
  let HW = 19mm
  let items = with-letters(R.nests, letter-c(size: 9pt, above: 6pt, below: 2pt), u => {
    if u.kind == "taxon" {
      return ((body: block(spacing: 0pt, inset: (top: 2.5pt), par(hanging-indent: HW + 2mm)[#emph(u.hw) #u.rng]), hw: u.hw),)
    }
    let rows = ()
    if u.nums.len() > 0 { rows.push([#text(fill: luma(45%))[—]#nbsp#inums(u.nums)]) }
    for d in u.defs { rows.push(par(hanging-indent: 1em)[#defn(d)#nbsp#inums(d.nums)]) }
    if rows.len() == 0 { rows.push([]) }
    let out = ()
    for (i, r) in rows.enumerate() {
      out.push((body: block(spacing: 0pt, above: if i == 0 { 2.5pt } else { 0pt },
        grid(columns: (HW, 1fr), column-gutter: 2mm,
          if i == 0 { align(right, ru-hy(text(weight: "bold", u.hw))) } else { [] }, r)),
        hw: if i == 0 { u.hw } else { none }, nest: u.hw,
        cont: if i > 0 { grid(columns: (HW, 1fr), column-gutter: 2mm, align(right, text(weight: "bold", fill: luma(45%), u.hw)), []) } else { none }))
    }
    out
  }, from: "гусь")
  idx-page(items, n: 2, gutter: 8mm, head: idx-head-std(label), colrule: 0.3pt + luma(60%))
}

// ================================================================ 15. bridge: inverted + English
#let R15() = {
  show: typeset.with(font: "Source Serif 4", size: 7.6pt, step: 9.2pt)
  let items = with-letters(R.inv, letter-c(size: 9pt, above: 6pt, below: 2pt), e => {
    let b = if e.kind == "taxon" [#text(weight: "semibold", e.t) #e.rng] else [#text(weight: "semibold", if e.alt { emph(e.t) } else { e.t })#nbsp#inums(e.nums, bold: false)#h(0.6em)#text(size: 6.9pt, fill: luma(30%), e.nums.first().en)]
    ((body: iline(b, hang: 1.5em), hw: e.t, nest: e.h),)
  }, from: "гусь")
  idx-page(items, n: 2, gutter: 8mm, head: idx-head-std(label))
}

#let RU = (R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15)
