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

## 5. Manual overrides

- **File:** `data/overrides.csv` (`sci,field,value,note`), applied last.
  An override of `ru` sets `ru_source = "manual"`.
