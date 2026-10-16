// Contents page of the layout catalogue.
#import "lib.typ": D, PW, PH, PLAQUE-FILL, PLAQUE-LINE

#set document(title: "Каталог идей вёрстки")
#set page(width: PW, height: PH, margin: (x: 12mm, top: 12mm, bottom: 10mm))
#set text(font: "Fira Sans", stretch: 75%, size: 7.8pt, lang: "ru", hyphenate: false)
#set par(leading: 0.42em, spacing: 0.5em, justify: false)

#block(width: 100%, fill: PLAQUE-FILL, stroke: (bottom: 0.8pt + PLAQUE-LINE), inset: (x: 5mm, y: 4mm), {
  text(size: 15pt, weight: "bold")[«Птицы мира» — каталог идей вёрстки]
  v(1.5mm)
  text(size: 8.6pt)[45 полос 170 × 240 мм: 15 вариантов одной полосы систематического списка, 15 — русского указателя, 15 — английского.
  Все варианты набраны из одних данных — выборки print/out/sample (Anseriformes + Galliformes, 483 вида): список — Anatidae с № 38
  (некоторые варианты начинают раньше, чтобы показать свои рубрики), указатели — фрагменты А–К и A–G (с гнёздами «гусь», «казарка»,
  «куропатка», «Duck», «Goose»; варианты малой ёмкости начинают с середины фрагмента).]
  v(1mm)
  text(size: 7.4pt, fill: rgb("#5b4d2a"))[Плашка вверху каждой полосы — не часть книги: идея, шрифт, кегль/интерлиньяж, колонки, источник, плюсы и минусы.
  Полоска внизу — измеренный результат (сколько видов или входов поместилось, оценка объёма списка). Ради плашки верхнее поле у всех вариантов 25 мм
  вместо 14: полоса набора на ≈ 5 % ниже, чем будет в книге. Колонтитулы, фолио и сама полоса ниже — как в книге.]
})

#let section(kind, title, first-page) = {
  v(3mm)
  block(width: 100%, stroke: (bottom: 0.5pt), inset: (bottom: 2pt), text(size: 10pt, weight: "bold", title))
  v(0.6mm)
  let rows = ()
  for (i, m) in D.meta.at(kind).enumerate() {
    rows += (
      text(fill: luma(45%), [с.#sym.space.nobreak.narrow#(first-page + i)]),
      align(right, text(weight: "bold", str(i + 1))),
      [#text(weight: "bold", m.title) — #m.idea],
    )
  }
  grid(columns: (8mm, 4mm, 1fr), column-gutter: 2mm, row-gutter: 1.25mm, ..rows)
}

#section("list", [Систематический список (с. 2–16)], 2)
#section("ru", [Русский указатель (с. 17–31)], 17)
#section("en", [Английский указатель (с. 32–46)], 32)
