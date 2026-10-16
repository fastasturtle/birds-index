// Measuring pass for variant C2 (called by build_print.py): heights of index
// entries set in a 31 mm column and widths of English run-in tokens.
#import "c2_index.typ": *
#let d = json(sys.inputs.data)
#context {
  let hs = d.items.map(it => measure(block(width: i-col, idx-line(it))).height.pt())
  let ws = d.tokens.map(t => measure(i-text(t.map(run).join())).width.pt())
  [#metadata((h: hs, w: ws)) <m>]
}
