# Data sources

All Russian names are matched to the AviList backbone by exact scientific name
(case- and whitespace-normalised). Priority: IOC → eBird → Wikidata → manual
overrides (`data/overrides.csv`). The build script is `scripts/build.py`.

## 1. AviList — taxonomic backbone (committed)

- **Name:** AviList: The Global Avian Checklist, extended version
- **Version:** v2025b (10 June 2026); same 11,131 species concepts as v2025
- **File:** `data/raw/AviList-v2025b-extended.xlsx` (downloaded 2026-10-13)
- **URL:** https://www.avilist.org/wp-content/uploads/2026/06/AviList-v2025b-10Jun2026-extended.xlsx
- **Licence:** CC BY 4.0
- **Citation:** AviList Core Team. 2025. AviList: The Global Avian Checklist, v2025.
  https://doi.org/10.2173/avilist.v2025 — the v2025b release recommends citing
  AviList Core Team. 2026. AviList: The Global Avian Checklist, v2025b.
  https://doi.org/10.2173/avilist.v2025b
- **Used for:** species list, sequence, order, family, scientific and English
  names, authority, extinction status, IUCN Red List category, Avibase ID.

## 2. IOC World Bird List Multilingual — primary Russian names (committed)

- **Name:** Multilingual IOC World Bird List
- **Version:** 15.2 (2026)
- **File:** `data/raw/IOC-Multiling-15.2.xlsx` (downloaded 2026-10-13)
- **URL:** https://worldbirdnames.org/Multiling%20IOC%2015.2.xlsx
- **Licence:** CC BY 3.0
- **Citation:** Gill F, Donsker D & Rasmussen P (Eds). 2026. IOC World Bird List
  (v15.2). doi:10.14344/IOC.ML.15.2
- **Note:** the Russian names in the IOC multilingual list originate from
  Волков С.В., Коблик Е.А. «Птицы мира: рекомендуемые русские названия видов»
  (Зоологический музей МГУ, ЗММУ МГУ).
- **Used for:** `ru` with `ru_source = "ioc"` (sheet "List", columns `IOC_15.2`
  and `Russian`).

## 3. eBird / Clements — fallback Russian names (not redistributed)

- **Name:** eBird taxonomy with Russian common names (eBird/Clements v2025;
  equivalent to the eBird 2025 alternate common names, locale `ru`)
- **Version:** eBird taxonomy 2025
- **URL:** https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json&locale=ru&cat=species
- **Licence / terms:** eBird data terms of use (non-commercial). Used only as a
  fallback for species without an IOC Russian name; the raw file is cached in
  `data/cache/` (gitignored) and is **not** redistributed as a file.
- **Citation:** eBird. 2025. eBird taxonomy v2025, alternate common names.
  Cornell Lab of Ornithology, Ithaca, New York. https://www.birds.cornell.edu/clementschecklist/
- **Used for:** `ru` with `ru_source = "ebird"`. The API falls back to English
  when no Russian name exists; names without Cyrillic are treated as missing.

## 4. Wikidata — second fallback (not redistributed as a file)

- **Name:** Wikidata, property P1843 (taxon common name), language `ru`, for
  items with P105 (taxon rank) = Q7432 (species), joined on P225 (taxon name)
- **Endpoint:** https://query.wikidata.org/sparql (queried at build time,
  cached in `data/cache/`, gitignored)
- **Licence:** CC0 1.0
- **Used for:** `ru` with `ru_source = "wikidata"`. If Wikidata is unreachable
  the build still succeeds and `data/report.md` says it was skipped.

## 5. ZMMU passerine list — Russian family names (committed)

- **Name:** Волков С.В., Коблик Е.А. «Птицы мира: рекомендуемые русские
  названия видов», spreadsheet for Passeriformes
- **File:** `data/raw/Birds_rus_names_passerine.xlsx` (downloaded 2026-10-13)
- **URL:** https://zmmu.msu.ru/files/publications/Birds_rus_names_passerine.xlsx
- **Used for:** Russian family names in `data/taxa.json` (`ru_source = "zmmu"`),
  from family header rows such as `Pittidae - Питтовые` (alternative names in
  parentheses and stress marks dropped). Each header is checked against the
  AviList families of the species listed under it; misspelt headers are
  mapped to the AviList family of their species, and headers for families
  AviList does not recognise are ignored (listed in `data/report.md`).
- **Not used:** the companion non-passerine file
  (https://zmmu.msu.ru/files/publications/Birds_rus_names.xlsx) has family
  header rows with Latin names only, no Russian, so it is not downloaded.
  Neither file has order names.

## 6. Wikidata — Russian order and family names (not redistributed as a file)

- One SPARQL query with a VALUES list of all AviList order and family names:
  items with P225 = name and P105 = Q36602 (order) or Q35409 (family); items
  placed under Aves (Q5113) win over homonyms. Russian P1843 is preferred,
  else the Russian label if it is Cyrillic. Cached in
  `data/cache/wikidata-taxa-ru.json` (gitignored); re-queried only with
  `--fetch` or when the cache lacks a current name.
- **Licence:** CC0 1.0
- **Used for:** `ru_source = "wikidata"` in `data/taxa.json` when ZMMU has no name.

## 7. IOC "vs other lists" — former scientific names (committed)

- **Name:** IOC 15.2 vs other lists (cross reference between IOC 15.2 and
  AviList v2025, Clements v2025, HBW/BirdLife v10 (2025), Howard & Moore 4.1,
  HBW 1992–2013, Peters 1931–1986, TiF 3.10, Gaudin 2025, Sibley & Monroe
  1993, IOC 15.1), compiled by Peter Kovalik
- **Version:** 15.2 (file dated 26 April 2026)
- **File:** `data/raw/IOC_15.2_vs_other_lists.xlsx` (downloaded 2026-10-16)
- **URL:** https://www.worldbirdnames.org/IOC_15.2_vs_other_lists.xlsx
- **Licence:** CC BY 3.0 (published on the IOC World Bird List site, whose
  content is CC BY 3.0)
- **Citation:** Kovalik P. 2026. IOC 15.2 vs other lists. In: Gill F,
  Donsker D & Rasmussen P (Eds). IOC World Bird List (v15.2).
  https://www.worldbirdnames.org/
- **Used for:** `sci_prev` / `sci_book_prev` in `data/species.json`: names by
  IOC 15.2 and 15.1, Clements 2025, BirdLife v10, H&M 4.1, HBW, Peters and
  S&M 1993 that differ from the AviList name; rows are joined on the AviList
  column. TiF and Gaudin columns are not used (alternative, not former,
  classifications).

## 8. eBird taxonomy versions 2015–2024 — former scientific names (not redistributed)

- **URL:** https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json&cat=species&version=YYYY
  (works without an API key; versions 2015–2019 and 2021–2024, there is no 2020)
- **Licence / terms:** eBird data terms of use, as for source 3. Only species
  names and codes are cached in `data/cache/ebird-taxonomy-YYYY.json`
  (gitignored), not redistributed.
- **Used for:** `sci_prev` sources `ebird2015` … `ebird2024`; joined on the
  eBird species code (AviList `Species_code_Cornell_Lab`), or on the name
  from the next newer version when the code changed with a split. If the API
  is unreachable and there is no cache, the version is skipped (noted in
  `data/report.md`).

## 9. Manual overrides

- **File:** `data/overrides.csv` (`sci,field,value,note`), applied last.
  An override of `ru` sets `ru_source = "manual"`.
  `sci` may also be an order or family name (only `field = ru`), which sets
  the name in `data/taxa.json` with `ru_source = "manual"`.
  `field = sci_prev` adds former names (`Genus species; Genus species`,
  source `override`) or removes them (`-Genus species`).
