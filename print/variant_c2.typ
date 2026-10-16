// Variant C2 — «компактный справочник», iteration 2 (spec: research critique,
// §3.1–3.7). 170 × 240 mm (70×100/16), margins inside 20 / outside 14 / top 14 /
// bottom 20 mm; list in 3 columns, indexes in 4 × 31 mm; Gentium Book Plus.
// Data: prepared by build_print.py (prepare_c2): species records, order and
// family ranges, and the alphabetical indexes already split into pages and
// columns (this template only sets them).
#import "c2_index.typ": *

#let data = json(sys.inputs.at("data", default: "/out/c2_sample.json"))
#let meta = data.meta
#let st = meta.stats
#let SP = data.species

// ------------------------------------------------------------ grid
#let NB = 7.8mm          // number box: 5 bold tabular digits (6.85 mm) + 0.95 mm
#let GAP = 0.95mm
#let STEP = 9.6pt        // line step of the list
#let HANG = NB + 1em     // continuation lines of any entry line

#set document(title: "Птицы мира: русские, латинские и английские названия видов", author: "birds-index")
#set text(font: "Gentium Book Plus", size: 8.5pt, lang: "ru", hyphenate: false,
  number-type: "lining", top-edge: 7pt, bottom-edge: -2.6pt)
#set par(leading: 0pt, spacing: 0pt, justify: false, first-line-indent: 0pt)
#set page(width: 170mm, height: 240mm,
  margin: (inside: 20mm, outside: 14mm, top: 14mm, bottom: 20mm),
  header-ascent: 2.5mm, footer: none, header: none)

// Prose (front and back matter): normal line boxes, leading in em.
#let prose(size: 9pt, lead: 0.62em, sp: 0.62em, body) = {
  set text(size: size, top-edge: "cap-height", bottom-edge: "baseline")
  set par(leading: lead, spacing: sp, justify: true)
  body
}

// ------------------------------------------------------------ marks
// build_print.py queries <sec> (page and position of section marks).
#let mark(name) = context {
  let pos = here().position()
  [#metadata((name: name, page: pos.page, x: pos.x.pt(), y: pos.y.pt())) <sec>]
}
#let page-of(name) = {
  let ms = query(<sec>).filter(m => m.value.name == name)
  if ms.len() > 0 { str(ms.first().value.page) } else { "?" }
}

// ------------------------------------------------------------ helpers
#let ext-sign(x) = if x == "x" { "†" } else if x == "p" { "†?" } else if x == "w" { "‡" } else { none }
#let rng(a, b) = if a == b { str(a) } else { str(a) + "\u{2060}–\u{2060}" + str(b) }
#let ord-ru(o) = if o.ru != none { o.ru } else { o.sci }

// Running head: folio and `outer` at the outer edge (bold), `inner` at the spine.
#let head-row(outer, inner) = context {
  let p = here().page()
  set text(size: 7.5pt, top-edge: "cap-height", bottom-edge: "baseline")
  let folio = strong(counter(page).display())
  let o = if outer != none { strong(outer) } else { none }
  block(width: 100%, stroke: (bottom: 0.3pt), inset: (bottom: 3pt),
    if calc.even(p) {
      grid(columns: (auto, 1fr), column-gutter: 1em, [#folio#h(1.2em)#o], align(right, inner))
    } else {
      grid(columns: (1fr, auto), column-gutter: 1em, inner, [#o#h(1.2em)#folio])
    })
}
#let plain-head(title) = head-row(none, title)

// ------------------------------------------------------------ list: running heads
// Counter `spc` is stepped by every entry; the page foot records its value
// (<pgend>), the head reads it at the page top: first and last species of the page.
#let spc = counter("species")
#let pgend = context [#metadata((page: here().page(), n: spc.get().first())) <pgend>]
// Left page: the order of the first entry of the page; right page: the family
// of the first entry. If a new order begins on the page, both name it instead
// (its first family on the right page).
#let list-head = context {
  let p = here().page()
  let top = spc.get().first()
  let ends = query(<pgend>).filter(m => m.value.page == p)
  if ends.len() == 0 { return }
  let last = ends.first().value.n
  if last <= top or last > SP.len() { return }
  let a = SP.at(top)
  let b = SP.at(last - 1)
  let range = [#a.n–#b.n]
  let new-ord = data.orders.find(o => o.a > a.n and o.a <= b.n)
  if calc.even(p) {
    let o = if new-ord != none { new-ord } else { data.orders.find(o => o.sci == a.o) }
    head-row(range, [#ord-ru(o) · #o.sci])
  } else {
    let f = data.families.at(if new-ord != none { SP.at(new-ord.a - 1).f } else { a.f })
    head-row(range, if f.ru != none [#f.ru · #f.sci] else [#f.sci])
  }
}

// ------------------------------------------------------------ list: entry
#let nbox(body) = box(width: NB, inset: (right: GAP), align(right, body))
#let num(n) = text(size: 7.5pt, weight: "bold", str(n))
#let author(s) = s.a.map(c => box(c)).join(" ")
#let binomial(s) = emph(s.g + " " + s.e)
#let lat-auth(s, bold: false) = {
  if bold { text(weight: "bold", binomial(s)) } else { binomial(s) }
  if s.a.len() > 0 { [ ]; author(s) }
}
// No automatic hyphenation: words too long for a line carry soft hyphens
// (build_print.py, pyphen); a line breaks between words otherwise.
#let ru-text(body) = text(lang: "ru", hyphenate: false, body)
// Simple first-fit breaking: a binomial or a name breaks only when it cannot fit.
#let line-par(body) = par(hanging-indent: HANG, linebreaks: "simple", body)

// The entry is unbreakable as a whole: it never splits between columns.
#let entry(s) = block(above: 2pt, below: 2pt, width: 100%, breakable: false, {
  let sign = ext-sign(s.x)
  block(breakable: false, spacing: 0pt, width: 100%, {
    if s.ru != none {
      line-par[#spc.step()#nbox(num(s.n))#ru-text[#strong(s.ru)#if s.st { strong("*") }#if s.alt.len() > 0 [ (#s.alt.join(", "))]]]
      line-par[#nbox(if sign != none { sign })#lat-auth(s)]
    } else {
      // no Russian name: the Latin name moves up into the name line
      line-par[#spc.step()#nbox(num(s.n))#if sign != none [#sign ]#lat-auth(s, bold: true)]
    }
    // former combination by another world list, no author: «= Anas formosa»
    if s.p != none { line-par[#box(width: NB)#text(size: 7.5pt)[=#sym.space.nobreak#emph(s.p)]] }
  })
  if s.en != none {
    block(breakable: false, spacing: 0pt, line-par[#box(width: NB)#text(size: 7.5pt, s.en)])
  }
})

// ------------------------------------------------------------ list: headings
#let order-head(o, k) = {
  colbreak(weak: true)
  block(sticky: true, above: 8pt, below: 6pt, width: 100%,
    stroke: (top: 0.6pt, bottom: 0.6pt), inset: (y: 4.5pt), {
    mark("order-" + str(k))
    set align(center)
    // 9.5 pt bold capitals with 5 % letter-spacing; a name too long for the
    // column (БУРЕВЕСТНИКООБРАЗНЫЕ) is set smaller to fit
    context {
      let t(sz, tr) = text(size: sz, weight: "bold", tracking: tr, upper(ord-ru(o)))
      let w = measure(t(9.5pt, 0.05em)).width
      let avail = 41.5mm
      par(if w <= avail { t(9.5pt, 0.05em) } else { t(9.5pt * (avail / w), 0.05em) })
    }
    if o.ru != none { par(text(size: 8.5pt, o.sci)) }
  })
}

#let family-head(f, first, specimen: false) = block(sticky: true, above: if first { 0pt } else { 7pt }, below: 4pt,
  width: 100%, stroke: if first { none } else { (top: 0.3pt) }, inset: (top: if first { 0pt } else { 3.5pt }), {
  if not specimen { mark("fam-" + f.sci) }
  set par(hanging-indent: 1em)
  if f.ru != none {
    par[#text(size: 9pt, weight: "bold", f.ru)#h(0.6em)#text(size: 8.5pt, f.sci)]
  } else {
    par(text(size: 9pt, weight: "bold", f.sci))
  }
  if f.en != none { par(text(size: 7.5pt, f.en)) }
  par(text(size: 7pt)[№#sym.space.nobreak.narrow#rng(f.a, f.b) · #f.cnt])
})

// ================================================================ FRONT MATTER
// p. 1 — title
#page[
  #mark("title")
  #prose(size: 10pt)[
    #set align(center)
    #set par(justify: false)
    #v(4mm)
    #text(size: 9pt, tracking: 0.08em)[\[АВТОРЫ\]]
    #v(1fr)
    #text(size: 26pt, weight: "bold")[Птицы мира]
    #v(5mm)
    #text(size: 13pt)[Русские, латинские и английские\ названия видов]
    #v(7mm)
    #line(length: 30%, stroke: 0.5pt)
    #v(5mm)
    #text(size: 10.5pt)[Систематический список по AviList #meta.avilist\ с алфавитными указателями]
    #v(1fr)
    #if not meta.full {
      block(stroke: 0.4pt, inset: (x: 1em, y: 0.7em))[
        #set text(size: 8.5pt)
        Макет, выборка: #meta.sample_orders —\ #meta.species_txt из #meta.total_fmt
      ]
      v(6mm)
    }
    #text(size: 9.5pt)[Москва · \[Издательство\] · #meta.year]
    #v(3mm)
  ]
]

// p. 2 — verso of the title (ГОСТ Р 7.0.4-2020)
#page[
  #mark("imprint")
  #prose(size: 8pt, lead: 0.55em, sp: 0.8em)[
    #grid(columns: (auto, auto), column-gutter: 1.5em, row-gutter: 0.55em,
      [УДК], [\[598.2\]],
      [ББК], [\[28.693.35\]],
      [], [\[...\]])
    #v(1fr)
    *Птицы мира: русские, латинские и английские названия видов* : справочник /
    \[сост.: …\] ; под ред. \[…\]. — Москва : \[Издательство\], #meta.year. — \[…\] с. —
    ISBN \[…\]. — Текст : непосредственный.

    Справочник содержит систематический список всех #st.total видов птиц современной мировой фауны,
    включая вымершие после 1500 г., с латинскими названиями, авторами и годами описания, русскими
    и английскими названиями. Систематика и латинские названия приняты по AviList (версия 2025b),
    русские названия — по рекомендованному списку С. В. Волкова и Е. А. Коблика (Зоологический музей
    МГУ) в редакции IOC World Bird List 15.2. Три алфавитных указателя (русских, английских
    и латинских названий) отсылают к сквозному номеру вида. Для зоологов, переводчиков, редакторов,
    преподавателей и любителей птиц.

    _Birds of the World: Russian, Scientific and English Names of Species._ A checklist of all
    #st.total bird species of the world (AviList v2025b) with Russian names after S. V. Volkov
    and E. A. Koblik (Zoological Museum of Moscow University) and indexes of Russian, English and
    scientific names.

    #v(0.6em)
    #align(center)[Рецензенты: \[…\]]
    #v(0.4em)
    #align(center)[\[Утверждено к печати …\]]
    #v(1fr)
    #grid(columns: (1fr, 1fr), column-gutter: 2em,
      align(bottom)[ISBN \[978-5-…\]],
      [© \[Авторы\], #meta.year\ © AviList Core Team, 2026 (CC BY 4.0), систематика\ © \[Издательство\], оформление, #meta.year])
    #v(3mm)
  ]
]

// p. 3 — counter-title (English)
#page[
  #mark("contr")
  #prose(size: 10pt)[
    #set align(center)
    #set par(justify: false)
    #v(4mm)
    #text(size: 9pt, tracking: 0.08em)[\[AUTHORS\]]
    #v(1fr)
    #text(size: 24pt, weight: "bold", style: "italic")[Birds of the World]
    #v(5mm)
    #text(size: 12.5pt, style: "italic")[Russian, Scientific and English\ Names of Species]
    #v(7mm)
    #line(length: 30%, stroke: 0.5pt)
    #v(5mm)
    #text(size: 10pt)[A checklist following AviList #meta.avilist\ with alphabetical indexes]
    #v(1fr)
    #text(size: 9.5pt)[Moscow · \[Publisher\] · #meta.year]
    #v(3mm)
  ]
]

// p. 4 — contents: orders and their families with ranges of species numbers
// and pages, dot leaders; 8/10 pt in two columns
#page(header: plain-head[Оглавление])[
  #mark("toc")
  #prose(size: 8pt)[
    #align(center, text(size: 12pt, weight: "bold")[Оглавление])
    #v(4mm)
  ]
  #set text(size: 8pt, top-edge: 7.5pt, bottom-edge: -2.5pt)
  #set par(leading: 0pt, spacing: 0pt, justify: false)
  #context {
    let pages = query(<sec>).fold((:), (acc, m) => { if m.value.name not in acc { acc.insert(m.value.name, m.value.page) }; acc })
    let pg(name) = str(pages.at(name, default: "?"))
    // One paragraph: the name wraps with a hanging indent; the leader dots,
    // the range of numbers and the page always end the last line. The space
    // before the name's last word is no-break-glued to the leaders via a
    // word joiner, so the tail never starts a line on its own.
    let line(body, r, p, ind: 0pt, bold: false, above: 0pt) = block(above: above, below: 0pt, breakable: false,
      pad(left: ind, par(hanging-indent: 1em, linebreaks: "simple")[#if bold { strong(body) } else { body }#sym.wj#box(width: 1fr, repeat(gap: 1pt)[.])#sym.wj#if r != [] { box[#h(2.5pt)#text(size: 7pt, r)] }#sym.wj#box(width: 5.5mm, align(right, p))]))
    columns(2, gutter: 5mm, {
      line([Введение], [], pg("intro"))
      line([Как пользоваться книгой], [], pg("howto"))
      line([Систематический список], [№ #rng(1, meta.count_fmt)], pg("list-start"), bold: true, above: 4pt)
      for (k, o) in data.orders.enumerate() {
        block(sticky: true, above: 2.5pt, below: 0pt,
          line([#ord-ru(o)#if o.ru != none [ · #o.sci]], rng(o.a, o.b), pg("order-" + str(k + 1)), bold: true))
        for f in data.families.values().filter(f => f.a >= o.a and f.b <= o.b) {
          line([#if f.ru != none [#f.ru · ]#f.sci], rng(f.a, f.b), pg("fam-" + f.sci), ind: 1em)
        }
      }
      line([Алфавитный указатель русских названий], [], pg("idx-ru-start"), bold: true, above: 6pt)
      line([Алфавитный указатель английских названий], [], pg("idx-en-start"), bold: true)
      line([Алфавитный указатель латинских названий], [], pg("idx-sci-start"), bold: true)
      line([Источники], [], pg("sources"))
    })
  }
]

// p. 5 — introduction
#page(header: plain-head[Введение])[
  #mark("intro")
  #prose(size: 8.6pt, lead: 0.56em, sp: 0.62em)[
    #align(center, text(size: 12pt, weight: "bold")[Введение])
    #v(3mm)
    #set par(first-line-indent: (amount: 1.2em, all: false))

    Справочник содержит систематический список птиц мировой фауны — #st.total_txt, включая
    виды, вымершие после 1500 г., — с латинскими (научными), русскими и английскими названиями,
    и три алфавитных указателя к нему. Его назначение — дать в одном томе согласованные названия
    на трёх языках: найти русское название по латинскому или английскому и обратно, увидеть место
    вида в системе и проверить, как вид называется в современном мировом списке.

    *Таксономическая основа.* Состав видов, их последовательность, деление на отряды
    и семейства, латинские названия с авторами и годами описания и английские названия приняты
    по AviList — единому мировому списку птиц (AviList: The Global Avian Checklist, версия 2025b).
    В нём #st.total_txt из #st.genera родов, #st.families семейств и #st.orders отрядов.
    Подвиды не приводятся. Номер вида сквозной и не несёт систематического смысла: он нужен для
    ссылок из указателей.

    *Русские названия.* Основа русской номенклатуры — рекомендованные названия С. В. Волкова
    и Е. А. Коблика (Зоологический музей МГУ), в том виде, в каком они вошли в многоязычный
    список IOC World Bird List, версия 15.2; отсюда взяты названия #st.ioc видов. Названия
    сопоставлены с AviList по точному совпадению латинского названия. Если вид в этом списке
    отсутствует (чаще всего это виды, выделенные в последние годы), название взято из русской
    версии таксономии eBird/Clements (#st.ebird) или из Wikidata (#st.wikidata); такие названия,
    всего #st.fallback, помечены звёздочкой «\*» и должны считаться предварительными до утверждения
    авторами номенклатуры. #st.manual_word названий исправлено вручную (опечатки и пропущенные «ё» в источнике, одно
    совпадение названий у двух видов). У #st.missing видов русского названия нет; в списке на его
    месте стоит латинское название полужирным курсивом. Русские названия отрядов и семейств
    взяты из таблиц ЗММУ и Wikidata.

    *Орфография.* Русские названия видов даны со строчной буквы, как принято в отечественной
    зоологической литературе. Прописная сохраняется у имён собственных и у притяжательных
    прилагательных от них: «гусь Росса», «Магелланов гусь». Названия отрядов и семейств пишутся
    с прописной. Альтернативные русские названия, приведённые в источнике, даны после основного
    в скобках светлым шрифтом.

    *Знаки статуса.* Крестом «†» отмечены виды, вымершие после 1500 г. (#st.extinct), знаком
    «†?» — возможно вымершие (#st.possibly), знаком «‡» — исчезнувшие в дикой природе и сохраняющиеся
    только в неволе (#st.ew). Статус принят по AviList.

    *Указатели* отсылают к номеру вида, а не к странице. В русском указателе названия собраны
    в гнёзда по ведущему слову, как правило существительному: «*гусь* — белолобый», «— серый».
    Определения внутри гнезда стоят в обратном порядке: «большой пёстрый дятел» ищите как
    «*дятел* — пёстрый большой». Английский указатель устроен так же, гнёзда набраны в подбор.
    В латинском указателе вид приведён в инверсии «эпитет, Род»: так его можно найти и после
    переноса в другой род. Отряды, семейства и роды включены в указатели с диапазонами номеров.
    Прежние комбинации латинских названий по другим мировым спискам (IOC, Clements, BirdLife,
    Howard & Moore, HBW, Peters, Sibley & Monroe, eBird) приведены в статье вида строкой «= …»
    и включены в латинский указатель со стрелкой к принятому названию.

    *Предшественники.* Ближайший отечественный предшественник — «Пятиязычный словарь
    названий животных. Птицы» Р. Л. Бёме и В. Е. Флинта (1994): 11 060 названий видов и надвидовых
    таксонов на пяти языках. Настоящий справочник отличается от него современной систематикой
    (тридцать лет описаний новых видов и пересмотров объёма видов), тремя языками вместо пяти,
    включением видов, вымерших в историческое время, пометой происхождения русских названий
    и гнездовым русским указателем. Образцом для вёрстки послужили также «Список птиц Российской
    Федерации» Е. А. Коблика, Я. А. Редькина и В. Ю. Архипова (2006) и «Howard and Moore Complete
    Checklist of the Birds of the World».
  ]
]

// p. 6 — how to use the book, symbols
#let specimen = {
  let s = SP.find(s => s.g == "Anser" and s.e == "fabalis")
  if s == none { s = SP.at(calc.min(10, SP.len() - 1)) }
  s
}
#page(header: plain-head[Как пользоваться книгой])[
  #mark("howto")
  #prose(size: 8.6pt, lead: 0.55em, sp: 0.6em)[
    #align(center, text(size: 12pt, weight: "bold")[Как пользоваться книгой])
    #v(3mm)
    Виды расположены в *систематическом порядке* AviList: отряд, внутри него семейства, внутри
    семейств виды. Каждый отряд начинается с новой колонки. Статья вида состоит из трёх строк:
    русское название (полужирным), латинское название с автором и годом описания и английское
    название; если в других мировых списках вид назывался иначе, между латинским и английским
    названием стоит строка «= _Anas formosa_». Все строки начинаются от одной вертикали; номер
    вида стоит слева от неё.

    #v(2mm)
    #grid(columns: (44mm, 1fr), column-gutter: 7mm,
      // specimen in the real column width
      block(width: 42mm, stroke: (top: 0.3pt, bottom: 0.3pt), inset: (y: 4pt), {
        set text(size: 8.5pt, top-edge: 7pt, bottom-edge: -2.6pt)
        set par(leading: 0pt, spacing: 0pt, justify: false, first-line-indent: 0pt)
        let f = data.families.at(specimen.f)
        family-head(f, true, specimen: true)
        entry(specimen)
        spc.update(0)
      }),
      {
        set par(justify: false)
        [*#specimen.n* — номер вида, сквозной по всей книге (1–#meta.total_fmt).
        На него, а не на страницу, ссылаются указатели. \
        *#specimen.ru* — русское название, со строчной буквы; в скобках — альтернативное название. \
        #emph[#specimen.g #specimen.e] — латинское (научное) название: род и видовой эпитет. \
        #specimen.a.join(" ") — автор и год описания. Скобки означают, что вид описан
        в другом роде (МКЗН, ст. 51.3). \
        #specimen.en — английское название (AviList).]
      })
    #v(2mm)
    Над статьями семейства стоит рубрика: русское и латинское название семейства, английское
    название и строка «№ … · … видов» — диапазон номеров и число видов в семействе. Колонтитул
    левой полосы называет отряд, правой — семейство; у внешнего края рядом с номером страницы
    полужирным дан диапазон номеров видов на полосе.

    #v(3mm)
    #align(center, text(size: 10.5pt, weight: "bold")[Условные обозначения])
    #v(2mm)
    #let item(k, body) = (align(right, k), body)
    #set par(justify: false)
    #grid(columns: (24mm, 1fr), column-gutter: 4mm, row-gutter: 0.62em,
      ..item([*гусь*\*], [звёздочка после русского названия: название взято из запасного источника
        (eBird или Wikidata), рекомендованного названия нет; предварительное.]),
      ..item(text(weight: "bold", emph[Genus species]), [латинское название полужирным курсивом на месте
        русского: русское название отсутствует.]),
      ..item([(серый гусь)], [альтернативное русское название.]),
      ..item([†], [вид вымер после 1500 г. (категория МСОП EX «исчезнувшие»). Знаки статуса стоят
        в графе номера, слева от латинского названия.]),
      ..item([†?], [вид, возможно, вымер: давно не отмечался, но вымирание не подтверждено
        (категория МСОП CR(PE) «находящиеся на грани полного исчезновения (возможно, исчезнувшие)»).]),
      ..item([‡], [вид исчез в дикой природе и сохраняется только в неволе (категория МСОП EW
        «исчезнувшие в дикой природе»).]),
      ..item([Linnaeus, 1758], [автор и год описания вида; «&» соединяет соавторов.]),
      ..item([\= _Anas formosa_], [прежняя комбинация: так вид назывался в других мировых списках
        (IOC, Clements, BirdLife, Howard & Moore, HBW, Peters, Sibley & Monroe, eBird 2015–2024),
        до переноса в другой род или изменения эпитета; без автора.]),
      ..item([Harrison et al., 2013], [у описаний четырёх и более авторов назван только первый.]),
      ..item([*52*, 52], [в указателях: номер основной статьи — полужирным; номер при альтернативном
        названии (набранном курсивом) — светлым.]),
      ..item([_серая_~52~#text(size: 6.5pt)[eBird]], [в русском указателе: название вида по eBird,
        отличное от принятого в книге; ведёт на тот же номер.]),
      ..item([*гусь* — серый], [в русском указателе: ведущее слово гнезда полужирным, тире заменяет его
        повтор; «(продолж.)» — гнездо продолжается с предыдущей колонки.]),
      ..item([(_M. deglandi_)], [в указателях: уточнение латинским названием, если одно русское название
        относится к двум видам.]),
      ..item([1–176], [у отрядов, семейств и родов в указателях: диапазон номеров видов.]),
      ..item([_formosa_, _Anas_ →], [в латинском указателе: прежняя комбинация, стрелка ведёт
        к принятому названию и номеру вида.]),
    )
  ]
]

// ================================================================ LIST
#pagebreak(to: "odd", weak: true)
#set page(columns: 3, header: list-head, footer: pgend)
#set columns(gutter: 5mm)
#mark("list-start")
#{
  let po = none
  let pf = none
  let k = 0
  let probe = SP.find(s => s.g == "Pomatorhinus" and s.e == "montanus")
  for s in SP {
    if s.o != po {
      k += 1
      order-head(data.orders.at(k - 1), k)
      po = s.o
      pf = none
    }
    if s.f != pf { family-head(data.families.at(s.f), pf == none); pf = s.f }
    if probe != none and s.n == probe.n { mark("probe") }
    entry(s)
  }
}
#mark("list-end")

// ================================================================ INDEXES
#set page(columns: 1, footer: none)
#let letter(it) = block(spacing: 0pt, width: 100%, height: it.h * i-step,
  inset: (top: (it.h - 1.5) * i-step),
  i-text(align(center, text(size: 10pt, weight: "bold", it.L))))
#let idx-item(it) = if "L" in it { letter(it) } else { idx-line(it) }

#let index-section(key, title-ru, title-en, short, note) = {
  let pages = data.idx.at(key)
  for (i, pg) in pages.enumerate() {
    let heads = if pg.first == pg.last { pg.first } else [#pg.first — #pg.last]
    page(header: head-row(heads, short))[
      #if i == 0 {
        mark("idx-" + key + "-start")
        block(spacing: 0pt, width: 100%, height: 9 * i-step, prose(size: 8pt)[
          #set align(center)
          #set par(justify: false, leading: 0.45em)
          #text(size: 12pt, weight: "bold", title-ru)\
          #v(-1pt)#text(size: 9pt, style: "italic", title-en)
          #v(2.5mm)
          #block(width: 88%, text(size: 7.5pt, style: "italic", note))
        ])
      }
      #grid(columns: (i-col,) * 4, column-gutter: i-gutter,
        ..range(4).map(c => if c < pg.cols.len() { pg.cols.at(c).map(idx-item).join() } else { [] }))
      #if i == pages.len() - 1 { mark("idx-" + key + "-end") }
    ]
  }
}

#pagebreak(to: "odd", weak: true)
#index-section("ru", [Алфавитный указатель русских названий], [Index of Russian Names],
  [Указатель русских названий],
  [Названия собраны в гнёзда по ведущему слову (полужирным); тире заменяет его повтор, определения
   внутри гнезда — в обратном порядке. Номера основных статей — полужирным; альтернативные названия
   набраны курсивом, их номера — светлым. Названия по eBird, отличные от принятых, — тоже курсивом,
   после номера помета #text(size: 6.5pt)[eBird]. Отряды и семейства — прямым шрифтом с диапазоном номеров.
   Буква ё приравнена к е.])
#index-section("en", [Алфавитный указатель английских названий], [Index of English Names],
  [Указатель английских названий],
  [Названия собраны в гнёзда по последнему слову (полужирным) и набраны в подбор: «*Goose* Greylag»
   означает Greylag Goose. Названия семейств — прямым шрифтом с диапазоном номеров.
   Names are grouped under the last word; families are given with the range of species numbers.])
#index-section("sci", [Алфавитный указатель латинских названий], [Index of Scientific Names],
  [Указатель латинских названий],
  [Виды — в инверсии: _эпитет, Род_. Прежние комбинации по другим мировым спискам — со стрелкой
   к принятому названию: «_formosa_, _Anas_ → _Sibirionetta formosa_»; если сменился только род, после
   стрелки стоит один род: «_bonariensis_, _Pipraeidea_ → _Rauenia_». Роды — полужирным курсивом
   с номерами всех видов рода; семейства и отряды — прописными с диапазоном номеров.])

// ================================================================ BACK MATTER
#page(header: plain-head[Источники])[
  #mark("sources")
  #prose(size: 8.6pt, lead: 0.55em, sp: 0.75em)[
    #align(center, text(size: 12pt, weight: "bold")[Источники])
    #v(4mm)
    #set par(justify: false, hanging-indent: 1.5em)
    #let refs = (
      [Бёме, Р. Л. Пятиязычный словарь названий животных. Птицы. Латинский, русский, английский,
       немецкий, французский / Р. Л. Бёме, В. Е. Флинт ; под общ. ред. В. Е. Соколова. — Москва :
       Русский язык : РУССО, 1994. — 845 с. — ISBN 5-200-00643-0. — Текст : непосредственный.],
      [Волков, С. В. Птицы мира: рекомендуемые русские названия видов / С. В. Волков, Е. А. Коблик ;
       Зоологический музей МГУ. — Москва, \[б. г.\]. — URL: #"https://zmmu.msu.ru/files/publications/Birds_rus_names_passerine.xlsx"
       (дата обращения: 13.10.2026). — Текст : электронный.],
      [Коблик, Е. А. Список птиц Российской Федерации / Е. А. Коблик, Я. А. Редькин, В. Ю. Архипов. —
       Москва : Товарищество научных изданий КМК, 2006. — 256 с. — Текст : непосредственный.],
      [AviList Core Team. AviList: The Global Avian Checklist, v2025b / AviList Core Team. — 2026. —
       DOI 10.2173/avilist.v2025b. — URL: #"https://www.avilist.org" (дата обращения: 13.10.2026). —
       Текст : электронный.],
      [Clements, J. F. The eBird/Clements Checklist of Birds of the World: v2025 / J. F. Clements
       \[et al.\]. — Ithaca : Cornell Lab of Ornithology, 2025. — URL: #"https://www.birds.cornell.edu/clementschecklist/"
       (дата обращения: 13.10.2026). — Текст : электронный.],
      [eBird Taxonomy : versions 2015–2019, 2021–2024 / Cornell Lab of Ornithology. — Ithaca, 2015–2024. —
       URL: #"https://api.ebird.org/v2/ref/taxonomy/ebird" (дата обращения: 16.10.2026). —
       Текст : электронный.],
      [Gill, F. IOC World Bird List (v15.2) / F. Gill, D. Donsker, P. Rasmussen (eds.). — 2026. —
       DOI 10.14344/IOC.ML.15.2. — URL: #"https://worldbirdnames.org" (дата обращения: 13.10.2026). —
       Текст : электронный.],
      [Kovalik, P. IOC 15.2 vs other lists / P. Kovalik \/\/ IOC World Bird List (v15.2) / F. Gill,
       D. Donsker, P. Rasmussen (eds.). — 2026. — URL: #"https://www.worldbirdnames.org/IOC_15.2_vs_other_lists.xlsx"
       (дата обращения: 16.10.2026). — Текст : электронный.],
      [Wikidata : свободная база знаний. — URL: #"https://www.wikidata.org" (дата обращения: 13.10.2026). —
       Текст : электронный.],
    )
    #for (i, r) in refs.enumerate() [#(i + 1). #r\ #parbreak()]
  ]
]

#pagebreak(to: "even", weak: true)
#page[
  #mark("colophon")
  #prose(size: 8pt, lead: 0.5em, sp: 0.5em)[
    #set align(center)
    #set par(justify: false)
    #v(1fr)
    _Научное издание_
    #v(2mm)
    #text(size: 9.5pt, weight: "bold")[Птицы мира]\
    #text(size: 9pt)[Русские, латинские и английские названия видов]
    #v(2mm)
    Авторы \[…\]\
    Редактор \[…\] · Корректор \[…\]\
    Компьютерная вёрстка \[…\]
    #v(3mm)
    #context {
      let total = query(<sec>).filter(m => m.value.name == "colophon").first().value.page
      let usl = calc.round(total / 16 * 7000 / 5400, digits: 2)
      [Подписано в печать \[…\]. Формат 70×100/16. Бумага офсетная.\
       Гарнитура Gentium Book Plus. Печать офсетная.\
       Усл. печ. л. #str(usl).replace(".", ","). Уч.-изд. л. \[…\]. Тираж \[…\] экз. Заказ № \[…\]]
    }
    #v(3mm)
    \[Издательство, адрес\]\
    \[Типография, адрес\]
    #v(8mm)
  ]
]

// ================================================================ TEMPORARY
// Not part of the edition: a note for the editor (text in about_draft.typ)
// and working tables prepared by build_print.py (c2_tables).
#let temp-head = plain-head[Временные страницы — в издание не входят]
#page(header: temp-head)[
  #mark("about")
  #include "about_draft.typ"
]

#let T = data.tables
#let tnum(n) = if n == none { "—" } else { str(n) }
#let tsci(s) = emph(s)
#let ttable(cols, head, rows, al: auto) = table(
  columns: cols, align: al, stroke: none, inset: (x: 3pt, y: 1.6pt),
  table.header(repeat: true, ..head.map(h => text(weight: "bold", h)), table.hline(stroke: 0.4pt)),
  ..rows)
#let tsection(title, note: none, body) = {
  block(sticky: true, above: 7mm, below: 2.5mm, {
    text(size: 10pt, weight: "bold", title)
    if note != none { linebreak(); text(size: 8pt, style: "italic", note) }
  })
  body
}
#let in-full(n, shown) = if not meta.full and n != shown [Показаны виды выборки (#shown); в полной книге: #n.] else [Всего: #n.]

#page(header: temp-head)[
  #set text(size: 8pt, top-edge: 7.5pt, bottom-edge: -2.5pt, hyphenate: false)
  #set par(leading: 0pt, spacing: 0pt, justify: false)
  #mark("tables")
  #align(center, text(size: 12pt, weight: "bold")[Рабочие таблицы])
  #align(center, emph[Временно, в издание не входят.])
  #if not meta.full {
    align(center, text(size: 8pt)[№ — номер вида в этом макете; «—» — вида нет в выборке.])
  }

  #tsection([а) Ручные исправления названий], note: [Строки файла правок; «было» — название в исходном источнике
    (латинские буквы внутри русских слов отмечены «лат.»).])[
    #ttable((9mm, 30mm, 29mm, 29mm, 1fr), ([№], [Латинское название], [Было], [Стало], [Причина]),
      T.fixes.map(r => (tnum(r.n), tsci(r.sci), [#r.before#if r.latin [ (лат.)]], r.after, r.why)).flatten(),
      al: (right, left, left, left, left))
    #v(2mm)
    _Названия отрядов и семейств, внесённые вручную:_
    #v(1mm)
    #ttable((32mm, 30mm, 32mm, 1fr), ([Таксон], [Было], [Стало], [Причина]),
      T.taxa_fixes.map(r => (r.sci, r.before, r.after, r.why)).flatten())
    #if T.taxa_formed.len() > 0 {
      v(2mm)
      emph[Названия отрядов и семейств, образованные агентом (обоснование — из файла правок):]
      v(1mm)
      ttable((32mm, 34mm, 1fr), ([Таксон], [Название], [Обоснование]),
        T.taxa_formed.map(r => (r.sci, r.after, r.why)).flatten())
    }
  ]

  #tsection([б) Одно русское название у нескольких видов], note: [Всего: #T.dups.len(). Ждут решения авторов номенклатуры.])[
    #ttable((auto, auto, auto, 1fr, auto), ([Русское название], [№], [Латинское название], [Английское], [Источник]),
      T.dups.map(d => d.sp.enumerate().map(((i, s)) => (
        if i == 0 { d.ru } else { [] }, tnum(s.n), tsci(s.sci), s.en, s.src))).flatten(),
      al: (left, right, left, left, left))
  ]

  #tsection([в) Названия из запасных источников (помечены «\*»)], note: in-full(T.full_fallback, T.fallback.len()))[
    #ttable((auto, auto, auto, 1fr, auto), ([№], [Латинское название], [Русское], [Английское], [Источник]),
      T.fallback.map(r => (tnum(r.n), tsci(r.sci), r.ru, r.en, r.src)).flatten(),
      al: (right, left, left, left, left))
  ]

  #tsection([г) Виды без русского названия], note: in-full(T.full_missing, T.missing.len()))[
    // grouped by family (a spanning row), two columns, no hyphenation
    #let rows = ()
    #let pf = none
    #for r in T.missing {
      if r.fam != pf {
        rows.push(table.cell(colspan: 3, align: left, inset: (top: 4pt, bottom: 1.6pt, x: 3pt),
          text(weight: "bold", [#r.fam#if r.fam_ru != none [ · #r.fam_ru]])))
        pf = r.fam
      }
      rows += (tnum(r.n), tsci(r.sci), text(lang: "en", r.en))
    }
    #set text(size: 7.5pt, hyphenate: false)
    #columns(2, gutter: 5mm, ttable((8mm, 30mm, 1fr), ([№], [Латинское название], [Английское]),
      rows, al: (right, left, left)))
  ]

  #tsection([д) Вторые названия, записанные в источнике через запятую], note: [В списке Волкова и Коблика у этих видов указано два названия; первое принято основным, второе попадает только в алфавитный указатель. #in-full(T.full_syn, T.syn.len())])[
    #ttable((auto, auto, 1fr), ([№], [Основное название], [Альтернативное]),
      T.syn.map(r => (tnum(r.n), r.ru, r.alt)).flatten(), al: (right, left, left))
  ]

  #tsection([е) Расхождения с eBird], note: [Названия eBird попадают в алфавитный указатель как дополнительные входы; явные опечатки eBird (19) подавлены и в таблицу не входят. #in-full(T.full_ebird, T.ebird.len())])[
    #ttable((auto, auto, 1fr, 1fr), ([№], [Латинское название], [Принятое (IOC/ЗММУ)], [Название eBird]),
      T.ebird.map(r => (tnum(r.n), tsci(r.sci), r.ru, r.eb)).flatten(), al: (right, left, left, left))
  ]
]
