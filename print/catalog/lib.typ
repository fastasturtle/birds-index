// Catalogue of layout ideas: shared pieces — data, the catalogue plaque in the
// top margin, book-page geometry, geometry metadata for the overflow check,
// manual column layout of index pages, small helpers.

#let D = json(sys.inputs.at("data", default: "/out/catalog_data.json"))
#let KIND = sys.inputs.at("kind", default: "list")
#let V = int(sys.inputs.at("v", default: "1"))

// ------------------------------------------------------------ geometry
#let PW = 170mm
#let PH = 240mm
#let M-IN = 20mm        // inside (left: every catalogue page is a recto)
#let M-OUT = 14mm
#let M-TOP = 25mm       // 14 mm of the book + room for the catalogue plaque
#let M-BOT = 18mm
#let TW = PW - M-IN - M-OUT   // 136 mm
#let PLAQUE-H = 16.5mm

#let PLAQUE-FILL = rgb("#efe9da")
#let PLAQUE-LINE = rgb("#b9ab86")
#let SPOT-RED = rgb("#9e1b22")
#let SPOT-BLUE = rgb("#1d3f74")

// ------------------------------------------------------------ helpers
#let ext-sign(x) = if x == "x" { "†" } else if x == "p" { "†?" } else if x == "w" { "‡" } else { none }
#let nbsp = sym.space.nobreak
#let thin = sym.space.nobreak.narrow
#let author(s) = if s.a.len() > 0 { s.a.map(c => box(c)).join(" ") } else { none }
#let pad5(n) = { let s = str(n); "0" * (5 - s.len()) + s }
#let rng(a, b) = if a == b { str(a) } else { str(a) + "\u{2060}–\u{2060}" + str(b) }
#let cap(s) = if s == none { none } else { upper(s.first()) + s.slice(s.first().len()) }
#let SP = D.species
#let sp-range(a, b) = SP.filter(s => s.n >= a and s.n <= b)
#let fam(f) = D.families.at(f)
#let order(o) = D.orders.find(x => x.sci == o)

// number in a box of fixed width, flush right, `gap` before the text
#let numbox(w, body, gap: 1.1mm) = box(width: w, inset: (right: gap), align(right, body))

// Russian text with hyphenation (only Russian lines may hyphenate)
#let ru-hy(body) = text(lang: "ru", hyphenate: true, costs: (hyphenation: 200%), body)

// ------------------------------------------------------------ catalogue plaque
#let plaque-font = "Fira Sans"
#let plural(n, one, few, many) = {
  let m10 = calc.rem(n, 10)
  let m100 = calc.rem(n, 100)
  if m100 >= 11 and m100 <= 14 { many } else if m10 == 1 { one } else if m10 >= 2 and m10 <= 4 { few } else { many }
}
#let plaque() = context {
  let m = D.meta.at(KIND).at(V - 1)
  let kr = D.kind_ru.at(KIND)
  // what is on page 1: species range (+ estimate of the whole list) or first … last headword
  let info = if KIND == "list" {
    let ns = query(<sp>).filter(q => q.value.page == 1).map(q => q.value.n)
    if ns.len() > 0 {
      let pages = calc.ceil(11131 / ns.len())
      [№ #calc.min(..ns)–#calc.max(..ns): #ns.len() #plural(ns.len(), "вид", "вида", "видов") на полосе → ≈ #pages #plural(pages, "полоса", "полосы", "полос") на 11#thin\131 видов]
    }
  } else {
    let hs = query(<hw>).map(q => q.value)
    if hs.len() > 0 [на полосе «#hs.first().hw» … «#hs.last().hw»: #hs.len() #plural(hs.len(), "вход", "входа", "входов")]
  }
  set text(font: plaque-font, stretch: 75%, size: 6.5pt, lang: "ru", hyphenate: false, fill: rgb("#2b2b2b"),
    top-edge: "cap-height", bottom-edge: "baseline", number-type: "lining")
  set par(leading: 0.42em, spacing: 0.42em, justify: false, first-line-indent: 0pt, hanging-indent: 0pt)
  place(top + left, block(width: PW, height: PLAQUE-H, fill: PLAQUE-FILL,
    stroke: (bottom: 0.6pt + PLAQUE-LINE), inset: (x: 7mm, top: 2.3mm, bottom: 1.5mm), {
    par(text(size: 7.4pt)[#text(weight: "bold")[#kr · вариант #V из 15 · «#m.title»]#h(0.5em)·#h(0.5em)#m.spec])
    v(0.3em)
    par[#m.desc]
    par[#text(fill: rgb("#2e6b2e"), weight: "bold")[+]#h(0.25em)#m.pro#h(0.8em)#text(fill: rgb("#9e1b22"), weight: "bold")[−]#h(0.25em)#m.con]
  }))
  // measured facts of this page: a strip at the very bottom, outside the book page
  place(bottom + left, block(width: PW, height: 5mm, fill: PLAQUE-FILL, stroke: (top: 0.6pt + PLAQUE-LINE),
    inset: (x: 7mm), align(horizon, text(size: 6.8pt, fill: rgb("#5b4d2a"))[Каталог вёрстки · #kr, вариант #V · #info])))
}

// ------------------------------------------------------------ geometry metadata
// Regions of the type area (pt from the page's top-left corner) in which every
// word must lie entirely; build_catalog.py checks page 1 with pdftotext -bbox.
#let geom(regions) = [#metadata((regions: regions.map(r => (
  x0: r.at(0).pt(), x1: r.at(1).pt(), y0: r.at(2).pt(), y1: r.at(3).pt(), bottom: r.at(4, default: true))))) <geom>]
#let geom-cols(n, gutter, top: M-TOP, bottom: M-BOT, left: M-IN, width: TW, from: none) = {
  let cw = (width - gutter * (n - 1)) / n
  let y0 = if from == none { top } else { from }
  geom(range(n).map(i => (left + i * (cw + gutter), left + i * (cw + gutter) + cw, y0, PH - bottom)))
}

// ------------------------------------------------------------ book page
// cfg: columns, gutter, top, bottom, header, footer, font settings are set by
// the caller inside `body`.
#let book-page(cols: 1, gutter: 5mm, top: M-TOP, bottom: M-BOT, header: none, footer: none,
  header-ascent: 3mm, footer-descent: 5mm, folio: 9, body) = {
  set page(width: PW, height: PH, margin: (left: M-IN, right: M-OUT, top: top, bottom: bottom),
    columns: cols, header: header, footer: footer, header-ascent: header-ascent,
    footer-descent: footer-descent, background: plaque())
  set columns(gutter: gutter)
  counter(page).update(folio)
  body
}

// folio of the current page: the variant's folio (variants.py) + page offset
#let FOLIO = D.meta.at(KIND).at(V - 1).at("folio", default: 9)
#let folio() = context str(FOLIO + here().page() - 1)

// marks for the plaque / checker
#let sp-mark(s) = context [#metadata((n: s.n, page: here().page())) <sp>]
#let hw-mark(hw) = [#metadata((hw: hw, page: 1)) <hw>]

// fixed line step: every line box is exactly `step` high (as in C2)
#let typeset(font: "Gentium Book Plus", size: 8.5pt, step: 9.6pt, stretch: 100%, body) = {
  set text(font: font, stretch: stretch, size: size, lang: "ru", hyphenate: false, top-edge: step * 0.74,
    bottom-edge: -step * 0.26, number-type: "lining")
  set par(leading: 0pt, spacing: 0pt, justify: false, first-line-indent: 0pt)
  body
}

// ------------------------------------------------------------ index: manual columns
// items: array of dicts
//   body: content (one entry line or a header block), hw: headword shown in the
//   running head / plaque (marked <hw>), nest: nest word for the obligatory-nest check,
//   keep: true = must stay with the next item (letter headers),
//   top: alternative body when the item opens a column (letter without space above),
//   cont: content repeated at the top of a column when this item lands there
//         (e.g. «гусь (продолж.)» before a «— белолобый 49» line).
// Columns are filled up to `avail`; what does not fit is dropped (the catalogue
// shows page 1 only); if everything fits, the columns are balanced.
#let idx-layout(items, n, colw, avail) = {
  let H(b) = measure(block(width: colw, b)).height
  let hs = items.map(it => H(it.body))
  let tops = items.map(it => if "top" in it { H(it.top) } else { none })
  let conts = items.map(it => if it.at("cont", default: none) != none { H(it.cont) } else { 0pt })
  let fill(T) = {
    let cols = ()
    let cur = ()
    let h = 0pt
    let i = 0
    while i < items.len() {
      let j = i
      while j < items.len() - 1 and items.at(j).at("keep", default: false) { j += 1 }
      let at-top = cur.len() == 0
      let gh = 0pt
      for k in range(i, j + 1) {
        gh += if k == i and at-top and tops.at(k) != none { tops.at(k) } else { hs.at(k) }
      }
      if at-top { gh += conts.at(i) }
      if not at-top and h + gh > T {
        cols.push(cur)
        cur = ()
        h = 0pt
        if cols.len() >= n { break }
        continue
      }
      for k in range(i, j + 1) { cur.push((k, k == i and at-top)) }
      h += gh
      i = j + 1
    }
    if cur.len() > 0 and cols.len() < n { cols.push(cur) }
    (cols: cols, done: i >= items.len() and cols.len() <= n)
  }
  let res = fill(avail)
  if res.done {
    let T = hs.sum(default: 0pt) / n
    let r2 = fill(T)
    while not r2.done and T < avail { T += 1pt; r2 = fill(T) }
    if r2.done { res = r2 }
  }
  let placed = res.cols.flatten().chunks(2).map(c => c.at(0))
  let hws = placed.map(k => items.at(k).at("hw", default: none)).filter(x => x != none)
  let render(col) = {
    let out = ()
    for (pos, (k, at-top)) in col.enumerate() {
      let it = items.at(k)
      if pos == 0 and it.at("cont", default: none) != none { out.push(it.cont) }
      out.push(if at-top and "top" in it { it.top } else { it.body })
      if it.at("hw", default: none) != none {
        out.push([#metadata((hw: it.hw, nest: it.at("nest", default: it.hw), page: 1)) <hw>])
      }
    }
    block(width: colw, spacing: 0pt, out.join())
  }
  (cols: res.cols.map(render), first: hws.at(0, default: ""), last: hws.at(-1, default: ""), done: res.done)
}

// One index page. `head(first, last)` — running head (inside the type area, top);
// `title` — optional title block (first page of an index); `deco(geo)` — extra
// decoration placed on the page (thumb tabs etc.), gets (top: y of columns);
// `extra` — extra allowed regions for the overflow check.
#let idx-page(items, n: 4, gutter: 4mm, head: none, title: none, colrule: none, footer: none,
  deco: none, extra: (), gap: 2.5mm) = book-page(footer: footer, context {
  let colw = (TW - gutter * (n - 1)) / n
  let hh = if head != none { measure(block(width: TW, head("Ag", "Ag"))).height + gap } else { 0pt }
  let th = if title != none { measure(block(width: TW, title)).height } else { 0pt }
  let avail = PH - M-TOP - M-BOT - hh - th
  let L = idx-layout(items, n, colw, avail)
  let y0 = M-TOP + hh + th
  geom(range(n).map(i => (M-IN + i * (colw + gutter), M-IN + i * (colw + gutter) + colw, y0, PH - M-BOT)) + extra.map(r => (r.at(0), r.at(1), y0, r.at(3))))
  if head != none { block(spacing: 0pt, width: 100%, head(L.first, L.last)); v(gap) }
  if title != none { block(spacing: 0pt, title) }
  let cells = L.cols
  while cells.len() < n { cells.push([]) }
  grid(columns: (colw,) * n, column-gutter: gutter, ..cells)
  if colrule != none {
    for i in range(1, n) {
      place(top + left, dx: i * (colw + gutter) - gutter / 2, dy: hh + th,
        line(length: avail, angle: 90deg, stroke: colrule))
    }
  }
  if deco != none { deco((top: y0, first: L.first, last: L.last)) }
})

// prose inside a fixed-step page (titles, notes): normal line boxes and leading
#let prose(body, lead: 0.5em) = {
  set text(top-edge: "cap-height", bottom-edge: "baseline")
  set par(leading: lead, spacing: lead + 0.2em)
  body
}

// ------------------------------------------------------------ index: entry helpers
#let iline(body, hang: 1em) = block(spacing: 0pt, width: 100%, par(hanging-indent: hang, body))
// numbers of one entry; main entries bold if `bold`; `latin`: abbreviated binomial after each
#let inums(ns, bold: true, latin: false, sep: ", ", style: none) = ns.map(r => {
  let t = str(r.n)
  if bold and r.main { t = strong(t) }
  if style == "italic" { t = emph(t) }
  if latin [#t#nbsp#text(size: 0.82em, emph(r.abbr))] else { t }
}).join(sep)
// sequence of items with letter separators: letter(L) -> item dict or none
#let with-letters(units, letter, unit-items, from: none) = {
  let items = ()
  let prev = none
  let on = from == none
  for u in units {
    if not on and (u.at("hw", default: none) == from or u.at("t", default: none) == from or u.at("h", default: none) == from) { on = true }
    if not on { continue }
    if letter != none and u.L != prev {
      let it = letter(u.L)
      if it != none { items.push(it) }
    }
    prev = u.L
    items += unit-items(u)
  }
  items
}

// standard running head of an index page: folio and first — last at the outer edge
#let idx-head-std(label, size: 7.5pt, rule: 0.3pt) = (a, b) => {
  set text(size: size, top-edge: "cap-height", bottom-edge: "baseline")
  block(width: 100%, spacing: 0pt, stroke: if rule != none { (bottom: rule) } else { none }, inset: (bottom: 3pt),
    grid(columns: (1fr, auto), label, [*#a — #b*#h(1.2em)*#folio()*]))
}
