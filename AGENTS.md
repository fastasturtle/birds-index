# AGENTS.md

The main agent never does concrete work itself. It acts as **orchestrator**, **reviewer** and **guru**; every concrete task goes to a subagent.

## Project

- Trilingual (Russian / English / Latin) index of all world bird species, including recently extinct ones (post-1500).
- Taxonomic backbone: AviList (currently v2025b). Species only, no subspecies.
- Russian names cascade: IOC World Bird List 15.2 multilingual (names originate from Волков & Коблик, ZMMU) → eBird → Wikidata → `data/overrides.csv` (manual layer, applied last; never edit generated data by hand, put fixes in overrides).
- Pipeline: `uv run scripts/build.py` regenerates `data/species.json`, `data/taxa.json` (orders and families with Russian names: ZMMU passerine family headers → Wikidata → overrides), `data/report.md` and their copies `docs/data/species.json`, `docs/data/taxa.json` from scratch. Raw AviList/IOC/ZMMU files live in `data/raw/`; eBird/Wikidata are cached in `data/cache/` (gitignored).
- Site: static `docs/index.html` (the index), `docs/missing.html` (species without a Russian name or with a fallback name, CSV download), shared `docs/style.css`, data in `docs/data/species.json` + `docs/data/taxa.json` (optional for the pages), deployed to GitHub Pages from `docs/` on push to main. No build step, no framework.
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
