// One page of the layout catalogue: variant `v` of kind `kind` (list / ru / en).
// Compiled by build_catalog.py once per variant; only page 1 is kept.
#import "lib.typ": *
#import "list.typ": LIST
#import "idx_ru.typ": RU
#import "idx_en.typ": EN

#set document(title: "Каталог идей вёрстки")
#let fns = (list: LIST, ru: RU, en: EN).at(KIND)
#(fns.at(V - 1))()
