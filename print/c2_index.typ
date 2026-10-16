// Variant C2: renderer of one alphabetical-index line, shared by the book
// (variant_c2.typ) and by the measuring pass (c2_measure.typ), so that the
// heights measured for pagination in build_print.py are exactly those set.
// An index line is a list of runs [text, style]; style letters: b bold,
// i italic, s small (6.5 pt). Fixed line box: 7.5 pt type on an 8.6 pt step.

#let i-size = 7.5pt
#let i-step = 8.6pt
#let i-col = 31mm
#let i-gutter = 4mm

#let i-text(body) = {
  set text(font: "Gentium Book Plus", size: i-size, top-edge: 6.3pt, bottom-edge: -2.3pt,
    lang: "ru", hyphenate: false, number-type: "lining")
  set par(leading: 0pt, spacing: 0pt, justify: false, first-line-indent: 0pt)
  body
}

#let run(r) = {
  let (t, st) = r
  let body = t
  if st.contains("s") { body = text(size: 6.5pt, body) }
  if st.contains("i") { body = emph(body) }
  if st.contains("b") { body = strong(body) }
  body
}

// it.r: runs; it.c: continuation line of an English run-in nest (indent 2 em);
// it.ru: Russian entry (hyphenation allowed, at a high cost).
#let idx-line(it) = i-text({
  let body = it.r.map(run).join()
  if it.at("ru", default: false) {
    body = text(hyphenate: true, costs: (hyphenation: 300%), body)
  }
  if it.at("c", default: 0) == 1 {
    block(spacing: 0pt, pad(left: 2em, par(body)))
  } else {
    block(spacing: 0pt, par(hanging-indent: 2em, body))
  }
})
