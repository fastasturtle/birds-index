# AGENTS.md

The main agent never does concrete work itself. It acts as **orchestrator**, **reviewer** and **guru**; every concrete task goes to a subagent.

## Project

- Trilingual (Russian / English / Latin) index of all world bird species, including recently extinct ones (post-1500).
- Taxonomic backbone: AviList (currently v2025b). Species only, no subspecies.
- Russian names cascade: IOC World Bird List 15.2 multilingual (names originate from Волков & Коблик, ZMMU) → eBird → Wikidata → `data/overrides.csv` (manual layer, applied last; never edit generated data by hand, put fixes in overrides).
- Pipeline: `uv run scripts/build.py` regenerates `data/species.json`, `data/taxa.json` (orders and families with Russian names: ZMMU passerine family headers → Wikidata → overrides), `data/report.md` and their copies `docs/data/species.json`, `docs/data/taxa.json` from scratch. Raw AviList/IOC/ZMMU files live in `data/raw/`; eBird/Wikidata are cached in `data/cache/` (gitignored).
- Index fields in `species.json` (computed in `build.py`): `ru_alt` (synonyms split out of `ru` by comma / parentheses / « / » / « или », plus overrides `field = ru_alt`, «; »-separated), `ru_head` + `ru_head_source` (leading noun of `ru` for an inverted index; overrides `field = ru_head`), `ru_book` (`ru` with a lower-case first letter except possessives from proper names), `en_head` (last word of `en`), `ru_ebird` (eBird/Clements Russian name when it differs from the final `ru` after normalisation — case, ё/е, spaces, hyphens, part after a comma; null if `ru_source = ebird`; overrides `field = ru_ebird`, value `-` suppresses a wrong eBird name; does not affect `ru` / `ru_alt` / `ru_head`).
- Former scientific names: `sci_prev` (list of `{name, kind, sources}`, kind ∈ genus / genus_ending / epithet / spelling / concept, sorted by the most recent source) from `data/raw/IOC_15.2_vs_other_lists.xlsx` (joined on its AviList column) and eBird taxonomies 2015–2024 (`data/cache/ebird-taxonomy-<year>.json`, joined on species code), overrides `field = sci_prev` («; »-separated, `-Name` removes); `sci_book_prev` = first genus / genus_ending / epithet name, for the book's «= …» line. AviList protonyms are not used.
- Site: static `docs/index.html` (the index), `docs/missing.html` (species without a Russian name or with a fallback name, CSV download), `docs/sources.html` (static sources/licences/citation/related-resources page; the single place for source details — the index footer only links to it), shared `docs/style.css`, data in `docs/data/species.json` + `docs/data/taxa.json` (optional for the pages), deployed to GitHub Pages from `docs/` on push to main. No build step, no framework.
- Print layout: `print/` (Typst). `uv run --with typst --with pyphen python print/build_print.py [--full] [--preview] [--variants C2]` typesets the book from `data/*.json` into `print/out/` (current variant: `variant_c2.typ`, 170×240 mm; indexes are paginated in Python after a Typst measuring pass; `check_overflow.py` and `check_layout.py` must report zero violations; pages after the colophon are temporary — note text in `print/about_draft.typ` and working tables). `*_full.pdf` are not tracked.
- Decisions and their rationale are logged in `DECISIONS.md`; append an entry whenever a decision is made or changed, and update README/AGENTS.md when the pipeline, schema or layout changes.

## Roles

- **Orchestrator** — splits the request into narrow tasks, picks a subagent and model for each, writes a self-contained brief (goal, scope, relevant files, what is already known, expected output), runs independent tasks in parallel, and assembles the results.
- **Reviewer** — checks every subagent result before it reaches the user or the next step: matches the brief, is correct and complete, no out-of-scope changes. Sends it back with concrete notes instead of silently fixing it.
- **Guru** — holds project context and architecture, makes decisions on approach, answers the user's questions, and clarifies ambiguous requests (use the `grilling` skill to stress-test plans).

## Model routing

| Task | Model |
|---|---|
| Coding: implementation, refactoring, fixes, tests | **Opus**, always |
| Research and exploration | **Sonnet** for simple, local lookups; **Opus** for anything complex (unfamiliar architecture, comparing approaches, root-causing bugs, planning). When in doubt, Opus |
| Reviewing another subagent's code | **Opus**, given the code, not the orchestrator's conclusions |

## Rules

- One subagent, one task. Don't mix "explore" and "implement" in one brief.
- Subagents don't commit, push or take irreversible actions unless the brief says so.
- Answer the user in the language they used.
- Keep docs in sync: a change to the data schema, pipeline flags, or site structure updates README.md and AGENTS.md in the same PR.
- Follow-up work and deferred decisions go into GitHub issues in this repository, not into chat or TODO comments.
