// Shared pieces of the three print variants: data loading, name formatting,
// title page, "how to use" page, running heads helpers, alphabetical indexes.
// Data is prepared by build_print.py (numbering, nbsp, pre-sorted indexes).

#let data = json(sys.inputs.at("data", default: "/out/sample.json"))
#let meta = data.meta
#let show-iucn = sys.inputs.at("iucn", default: "1") == "1"

// ------------------------------------------------------------ marks
// Section marks; build_print.py queries <sec> to count pages per section.
#let mark(name) = context {
  let pos = here().position()
  [#metadata((name: name, page: pos.page, x: pos.x.pt(), y: pos.y.pt())) <sec>]
}

// ------------------------------------------------------------ names
#let ext-sign(code) = if code == "x" { "†" } else if code == "p" { "(†)" } else if code == "w" { "‡" } else { none }

// Latin binomial (italic) with extinction sign before it (upright).
// `brk`: binomials longer than this many characters may break between genus
// and epithet (for narrow columns); shorter ones keep their no-break space.
#let sci(sp, brk: 999) = {
  let s = ext-sign(sp.ext)
  if s != none { [#s#sym.space.nobreak.narrow] }
  emph(if sp.sci.clusters().len() > brk { sp.gen + " " + sp.ep } else { sp.sci })
}
#let auth(sp) = if sp.auth != none { sp.auth } else { none }
#let sci-auth(sp, brk: 999) = {
  sci(sp, brk: brk)
  if sp.auth != none { [ #sp.auth] }
}
#let ru-name(sp) = if sp.ru != none { sp.ru } else { "—" }
#let en-name(sp) = if sp.en != none { sp.en } else { "—" }

#let order-ru(o) = data.orders.at(o, default: (ru: none)).ru
#let fam(f) = data.families.at(f, default: (ru: none, en: none))

// ------------------------------------------------------------ running heads
// Every species entry steps counter `spc` (value = its number n). The page
// footer records the counter at the page foot as metadata <pgend>; the header
// reads the counter at the page top. Together they give the first and last
// species of the page without scanning all entries (cheap enough for 11 131).
#let spc = counter("species")
#let sp-mark(sp) = spc.step()
#let pgend-footer = context [#metadata((page: here().page(), n: spc.get().first())) <pgend>]

// (first, last) species records of the current page, or none.
#let page-species() = {
  let p = here().page()
  let top = spc.get().first()
  let ends = query(<pgend>).filter(m => m.value.page == p)
  if ends.len() == 0 { return () }
  let last = ends.first().value.n
  if last <= top or last > data.species.len() { return () }
  (data.species.at(top), data.species.at(last - 1))
}

// Header row with the folio in the outer corner and a hairline below.
#let head-row(inner-left, inner-right, size: 8pt, rule: true) = context {
  let p = here().page()
  let folio = text(size: size + 0.5pt, counter(page).display("1"))
  set text(size: size)
  set text(hyphenate: false)
  let body = if calc.even(p) {
    grid(columns: (auto, 1fr, auto), column-gutter: 1em, align: (left, left, right),
      folio, inner-left, inner-right)
  } else {
    grid(columns: (auto, 1fr, auto), column-gutter: 1em, align: (left, right, right),
      inner-left, inner-right, folio)
  }
  block(width: 100%, inset: (bottom: 2.5pt), stroke: if rule { (bottom: 0.4pt) } else { none }, body)
}

// Page heads for the systematic list: left (verso) — order, right (recto) — family.
// Order = order of the first species on the page, family = of the last one.
#let list-header(size: 8pt, caps: false) = context {
  let sps = page-species()
  if sps.len() == 0 { return }
  let p = here().page()
  let first = sps.first()
  let last = sps.last()
  let ord = {
    let o = first.order
    let r = order-ru(o)
    if caps { smallcaps(lower(o)) } else { upper(o) }
    if r != none { [ — #r] }
  }
  let fm = {
    let f = fam(last.family)
    last.family
    if f.ru != none { [ — #f.ru] }
  }
  let range = [#first.n–#last.n]
  if calc.even(p) { head-row(ord, range, size: size) } else { head-row(range, fm, size: size) }
}

// Index page heads: index title on both pages.
#let index-header(title, size: 8pt) = context {
  let p = here().page()
  if calc.even(p) { head-row(title, none, size: size) } else { head-row(none, title, size: size) }
}

// ------------------------------------------------------------ title page
#let title-page(title-size: 22pt, rule-width: 40%) = {
  page(header: none, footer: none, numbering: none)[
    #set par(justify: false)
    #set align(center)
    #v(18%)
    #text(size: title-size, weight: "bold")[Птицы мира]
    #v(0.2em)
    #text(size: title-size * 0.62)[Трёхъязычный указатель видов]
    #v(1.4em)
    #line(length: rule-width, stroke: 0.5pt)
    #v(1.0em)
    #text(size: title-size * 0.72, style: "italic")[Birds of the World]
    #v(0.2em)
    #text(size: title-size * 0.5, style: "italic")[A Trilingual Index of Species]
    #v(2.6em)
    #text(size: 11pt)[Русские, английские и латинские названия]
    #v(0.3em)
    #text(size: 11pt)[По AviList #meta.avilist]
    #v(1fr)
    #block(stroke: 0.4pt, inset: (x: 1em, y: 0.6em))[
      #set text(size: 9pt)
      Макет. #if meta.full [Полный список: #meta.count_fmt видов] else [Выборка: отряды Anseriformes и Galliformes, #meta.count_fmt видов из #meta.total_fmt]
    ]
    #v(8%)
  ]
}

// Imprint (verso of the title page).
#let imprint-page() = page(header: none, footer: none)[
  #set text(size: 8pt)
  #set par(justify: false, leading: 0.5em, spacing: 0.9em)
  #v(1fr)
  *Птицы мира. Трёхъязычный указатель видов.* Систематика и английские названия — AviList Core Team (2025):
  AviList: The Global Avian Checklist, #meta.avilist. Русские названия — IOC World Bird List 15.2 (многоязычный
  список; русские названия по Волкову и Коблику, Зоологический музей МГУ), дополнения — eBird, Wikidata
  и ручная правка. Категории Красного списка МСОП — по данным AviList.

  Макет вёрстки. Данные: #meta.count_fmt #if meta.full [видов] else [видов (выборка)], #meta.orders отр., #meta.families сем., #meta.genera родов.
]

// ------------------------------------------------------------ how to use
// `sample` is the variant's own entry for a real species, shown as a specimen.
#let heads-default = [В систематическом списке над левой полосой указан отряд, над правой — семейство, а также
  номера первого и последнего вида на странице; номер страницы — во внешнем углу.]
#let howto-page(sample: none, size: 9pt, iucn-note: false, heads: heads-default) = {
  page(header: none)[
    #set text(size: size)
    #set par(justify: false, leading: 0.55em, spacing: 0.75em)
    #mark("howto")
    #align(center, text(size: size * 1.45, weight: "bold")[Как пользоваться указателем])
    #v(0.8em)

    Виды расположены в *систематическом порядке* по AviList #meta.avilist: отряды, внутри них — семейства,
    внутри семейств — виды. Подвиды не приводятся. Для каждого вида даны русское, английское и научное
    (латинское) название с автором и годом описания.

    #if sample != none {
      v(0.3em)
      block(width: 100%, inset: (x: 1em, y: 0.7em), stroke: (top: 0.4pt, bottom: 0.4pt), {
        text(size: size * 0.85, style: "italic")[Образец статьи:]
        v(0.2em)
        sample
      })
      spc.update(0) // the specimen stepped the species counter
      v(0.3em)
    }

    #let item(k, body) = grid(columns: (7.2em, 1fr), column-gutter: 0.8em, row-gutter: 0pt, align(right, k), body)
    #set par(spacing: 0.65em)
    #item[*12*][Порядковый номер вида — сквозной от 1 до #meta.count_fmt. *Все ссылки в алфавитных указателях
      даются на номер вида, а не на страницу*: на одной странице помещается много видов, а номер
      однозначно указывает на статью и не зависит от вёрстки.]
    #item[_Anser anser_][Научное название вида (род и видовой эпитет) — курсивом.]
    #item[Linnaeus, 1758][Автор и год описания — прямым шрифтом.]
    #item[(Latham, 1790)][Автор и год в скобках: вид был описан в другом роде, чем тот, в который он
      помещён сейчас (Международный кодекс зоологической номенклатуры, ст. 51.3).]
    #item[†][Вид вымер (после 1500 г.).]
    #item[(†)][Вид, возможно, вымер (не отмечался много лет, но вымирание не подтверждено).]
    #item[‡][Вид исчез в природе, сохраняется только в неволе.]
    #item[—][Русское название не установлено.]
    #if iucn-note {
      item[LC, NT…][Категория Красного списка МСОП (IUCN): LC — вызывающие наименьшие опасения;
        NT — близкие к уязвимому положению; VU — уязвимые; EN — вымирающие; CR — в критическом
        состоянии; CR (PEW) — возможно, исчез в природе; EW — исчез в природе; EX — вымер;
        DD — недостаточно данных; NE — не оценивался.]
    }

    #v(0.6em)
    *Алфавитные указатели* в конце книги: русских названий, английских названий и научных названий.
    Русские названия упорядочены по полному названию в том виде, как оно дано в списке, без перестановки
    слов: «Серый гусь» следует искать на букву С, а не под словом «гусь»; буква ё при сортировке следует
    за е. Английские названия упорядочены пословно. В указателе научных названий виды сгруппированы по
    родам: под названием рода с отступом перечислены видовые эпитеты.

    #v(0.3em)
    *Колонтитулы.* #heads
  ]
}

// ------------------------------------------------------------ indexes
// Common index settings: `cols` columns, body size `size`.
#let index-letter(L, size) = block(sticky: true, width: 100%, above: 0.9em, below: 0.45em,
  align(center, text(size: size * 1.25, weight: "bold", L)))

#let idx-entry(name, n, ext, size, italic: false, indent: 0em) = {
  let s = ext-sign(ext)
  let nm = if italic { emph(name) } else { name }
  let ns = if type(n) == array { n.map(str).join(", ") } else { str(n) }
  // nbsp keeps the number with the last word of the name
  let p = par(hanging-indent: 1em, first-line-indent: 0em)[#if s != none [#s#sym.space.nobreak.narrow]#nm#sym.space.nobreak#sym.space.nobreak.narrow#ns]
  if indent > 0em { pad(left: indent, p) } else { p }
}

#let index-section(title, mark-name, groups, cols: 3, size: 8pt, gutter: 1.1em, title-size: 13pt, italic: false) = {
  set page(header: index-header(title), columns: cols)
  set columns(gutter: gutter)
  set text(size: size)
  set par(justify: false, leading: 0.38em, spacing: 0.38em)
  place(top + center, float: true, scope: "parent", clearance: 1.6em,
    align(center, text(size: title-size, weight: "bold", title)))
  mark(mark-name + "-start")
  for g in groups {
    index-letter(g.letter, size)
    for it in g.items { idx-entry(it.name, it.ns, it.ext, size, italic: italic) }
  }
  mark(mark-name + "-end")
}

// Scientific index: genus, then epithets indented beneath it.
#let index-sci(title: "Index of scientific names · Указатель научных названий", cols: 3, size: 8pt, gutter: 1.1em, title-size: 13pt) = {
  set page(header: index-header("Index of scientific names"), columns: cols)
  set columns(gutter: gutter)
  set text(size: size)
  set par(justify: false, leading: 0.38em, spacing: 0.38em)
  place(top + center, float: true, scope: "parent", clearance: 1.6em,
    align(center, text(size: title-size, weight: "bold", title)))
  mark("idx-sci-start")
  for g in data.idx_sci {
    index-letter(g.letter, size)
    for gen in g.genera {
      let g = text(style: "italic", weight: "bold", gen.genus)
      if gen.items.len() == 1 {
        // monotypic in this list: run in on one line
        let it = gen.items.first()
        let s = ext-sign(it.ext)
        block(above: 0.55em, below: 0.38em, par(hanging-indent: 1em)[#if s != none [#s#sym.space.nobreak.narrow]#g #emph(it.ep)#sym.space.nobreak#sym.space.nobreak.narrow#str(it.n)])
      } else {
        // genus line sticks to its first epithet
        block(sticky: true, above: 0.55em, below: 0.38em, par(g))
        for it in gen.items { idx-entry(it.ep, it.n, it.ext, size, italic: true, indent: 0.9em) }
      }
    }
  }
  mark("idx-sci-end")
}

#let all-indexes(cols: 3, size: 8pt, gutter: 1.1em, title-size: 13pt) = {
  pagebreak(to: "odd", weak: true)
  index-section("Указатель русских названий", "idx-ru", data.idx_ru, cols: cols, size: size, gutter: gutter, title-size: title-size)
  index-section("Index of English names", "idx-en", data.idx_en, cols: cols, size: size, gutter: gutter, title-size: title-size)
  index-sci(cols: cols, size: size, gutter: gutter, title-size: title-size)
}
