# Build report

## Sources

- **AviList v2025b**: `data/raw/AviList-v2025b-extended.xlsx`
- **IOC Multilingual 15.2**: `data/raw/IOC-Multiling-15.2.xlsx`
- **eBird taxonomy (ru)**: `data/cache/ebird-taxonomy-ru.json`, 10366 species with Cyrillic names
- **Wikidata P1843 (ru)**: `data/cache/wikidata-ru-p1843.json`, 10700 taxa
- **IOC 15.2 vs other lists (former names)**: `data/raw/IOC_15.2_vs_other_lists.xlsx`, 5087 species with names
- **eBird taxonomies 2015–2024 (former names)**: 9 of 9 versions
- **ZMMU passerine list (family names)**: `data/raw/Birds_rus_names_passerine.xlsx`, 142 families
- **Wikidata orders/families (ru)**: `data/cache/wikidata-taxa-ru.json`, 231 taxa

## Counts

| Metric | Count |
|---|---|
| Total species (AviList) | 11131 |
| Russian name present | 10727 |
| — from IOC | 10636 |
| — from eBird | 68 |
| — from Wikidata | 4 |
| — manual override | 19 |
| Russian name missing | 404 |
| Extinct | 151 |
| Extinct in the wild | 5 |
| Possibly extinct | 46 |
| AviList species not in IOC (exact name) | 42 |
| IOC species not in AviList (exact name) | 138 |
| IOC vs eBird Russian name differs | 164 |
| `ru_ebird` set (eBird name differs from `ru`) | 108 |
| `ru_ebird` suppressed by override | 19 |
| `auth` with leftover initials | 0 |
| Species with `sci_prev` (former scientific names) | 5146 |
| Species with `sci_book_prev` | 3160 |
| Names with mixed Cyrillic/Latin words | 0 |
| Russian names shared by several species | 42 |
| `ru` split into `ru` + `ru_alt` | 41 |
| Species with `ru_alt` | 41 |
| `ru_alt` names in total | 41 |
| `ru_alt` equal to another species' `ru` | 0 |
| Distinct `ru_head` | 1225 |
| `ru_head` doubtful (auto) | 15 |
| `ru_head` manual | 0 |
| `ru_book` with the capital kept | 69 |

## Russian names: checks and index fields


### Words mixing Cyrillic and Latin letters (0)

Look-alike letters (e.g. Latin C in "Cкоморох"); fix in `data/overrides.csv`.

| Scientific name | Name |
|---|---|

### Russian names shared by several species (42)

Not fixed automatically; resolve in `data/overrides.csv` when the right name is known.

| Russian name | Species (English, source) |
|---|---|
| Чатемский тайфунник | *Pterodroma magentae* (Magenta Petrel, ioc); *Pterodroma axillaris* (Chatham Islands Petrel, ioc) |
| Синегрудый зимородок | *Alcedo euryzona* (Javan Blue-banded Kingfisher, ioc); *Halcyon malimbica* (Blue-breasted Kingfisher, ioc) |
| Рябой дятел | *Meiglyptes grammithorax* (Buff-rumped Woodpecker, ebird); *Meiglyptes tristis* (Zebra Woodpecker, ioc) |
| Туи | *Brotogeris sanctithomae* (Tui Parakeet, ioc); *Prosthemadera novaeseelandiae* (Tui, ioc) |
| Черноголовый лорито | *Pyrilia caica* (Caica Parrot, ioc); *Pionites melanocephalus* (Black-headed Parrot, ioc) |
| Синеспинный попугай | *Tanygnathus everetti* (Blue-backed Parrot, ebird); *Tanygnathus sumatranus* (Azure-rumped Parrot, ioc) |
| Крошечный лорикет | *Charminetta wilhelminae* (Pygmy Lorikeet, ioc); *Parvipsitta pusilla* (Little Lorikeet, ioc) |
| Сероголовый тоди-мухолов | *Todirostrum poliocephalum* (Yellow-lored Tody-Flycatcher, ioc); *Poecilotriccus sylvia* (Slaty-headed Tody-Flycatcher, ioc) |
| Боливийский москитолов | *Zimmerius bolivianus* (Bolivian Tyrannulet, ioc); *Mecocerculus hellmayri* (Buff-banded Tyrannulet, ioc) |
| Рыжекрылый бентеви | *Myiozetetes cayanensis* (Rusty-margined Flycatcher, ioc); *Myiodynastes bairdii* (Baird's Flycatcher, ioc) |
| Белогорлый бентеви | *Conopias albovittatus* (White-ringed Flycatcher, ioc); *Phelpsia inornata* (White-bearded Flycatcher, ioc) |
| Рыжебрюхая гевара | *Neoxolmis rufiventris* (Chocolate-vented Tyrant, ioc); *Myiotheretes fuscorufus* (Rufous-bellied Bush Tyrant, ioc) |
| Пестроголовый древолаз | *Dendrocolaptes hoffmannsi* (Hoffmanns's Woodcreeper, ioc); *Lepidocolaptes souleyetii* (Streak-headed Woodcreeper, ioc) |
| Короткохвостая иглохвостка | *Hellmayrea gularis* (White-browed Spinetail, ioc); *Synallaxis brachyura* (Slaty Spinetail, ioc) |
| Тёмная медовка | *Vosea whitemanensis* (Gilliard's Honeyeater, ioc); *Myzomela obscura* (Dusky Myzomela, ioc) |
| Индокитайская птерутия | *Pteruthius aeralatus* (White-browed Shrike-babbler, ioc); *Pteruthius intermedius* (Clicking Shrike-babbler, ioc) |
| Пестрогрудая веерохвостка | *Rhipidura threnothorax* (Sooty Thicket Fantail, ioc); *Rhipidura dedemi* (Streak-breasted Fantail, ioc) |
| Большая лофорина | *Lophorina superba* (Vogelkop Lophorina, ioc); *Lophorina latipennis* (Greater Lophorina, ebird) |
| Белохвостая эльминия | *Elminia albicauda* (White-tailed Blue Flycatcher, ioc); *Elminia albonotata* (White-tailed Crested Flycatcher, ioc) |
| Ошейниковый апалис | *Oreolais ruwenzorii* (Rwenzori Apalis, ioc); *Apalis thoracica* (Bar-throated Apalis, ioc) |
| Тиморская клинохвостка | *Cincloramphus bivittatus* (Buff-banded Thicketbird, ioc); *Cincloramphus timoriensis* (Tawny Grassbird, ioc) |
| Вануатская клинохвостка | *Cincloramphus whitneyi* (Santo Thicketbird, ioc); *Cincloramphus turipavae* (Guadalcanal Thicketbird, ebird) |
| Домовая ласточка | *Hirundo javanica* (Pacific Swallow, ebird); *Hirundo tahitica* (Tahiti Swallow, ioc) |
| Рыжепоясничная ласточка | *Cecropis rufula* (European Red-rumped Swallow, ebird); *Cecropis daurica* (Eastern Red-rumped Swallow, ioc) |
| Сулавесская пеночка | *Phylloscopus sarasinorum* (Lompobattang Leaf Warbler, ioc); *Phylloscopus nesophilus* (Sulawesi Leaf Warbler, ebird) |
| Бирманский бюльбюль | *Pycnonotus blanfordi* (Ayeyarwady Bulbul, ioc); *Iole viridescens* (Olive Bulbul, ioc) |
| Белоголовый бюльбюль | *Hypsipetes thompsoni* (White-headed Bulbul, ioc); *Hypsipetes leucocephalus* (Black Bulbul, ioc) |
| Марианская белоглазка | *Zosterops semiflavus* (Marianne White-eye, ioc); *Zosterops conspicillatus* (Bridled White-eye, ioc) |
| Желтоклювая белоглазка | *Zosterops lacertosus* (Sanford's White-eye, ioc); *Zosterops luteirostris* (Gizo White-eye, ioc) |
| Белогорлая дроздовка | *Argya gularis* (White-throated Babbler, ioc); *Turdoides gilberti* (White-throated Mountain Babbler, ioc) |
| Пятнистый крапивник | *Campylorhynchus gularis* (Spotted Wren, ioc); *Pheugopedius maculipectus* (Spot-breasted Wren, ioc) |
| Рыжеспинный дрозд | *Geokichla erythronota* (Red-backed Thrush, ioc); *Turdus rufopalliatus* (Rufous-backed Thrush, ioc) |
| Суматранская нильтава | *Niltava sumatrana* (Rufous-vented Niltava, ioc); *Cyornis herioti* (Blue-breasted Blue Flycatcher, ioc) |
| Рыжещёкий заряночник | *Sheppardia poensis* (Short-tailed Akalat, ebird); *Sheppardia bocagei* (Bocage's Akalat, ioc) |
| Ангольская нектарница | *Cinnyris ludovicensis* (Ludwig's Double-collared Sunbird, ioc); *Cinnyris oustaleti* (Oustalet's Sunbird, ioc) |
| Голубокрылая листовка | *Chloropsis moluccensis* (Blue-winged Leafbird, ebird); *Chloropsis cochinchinensis* (Javan Leafbird, ioc) |
| Гольцовый конёк | *Anthus japonicus* (Siberian Pipit, ebird); *Anthus rubescens* (American Pipit, ioc) |
| Китайская чечевица | *Carpodacus davidianus* (Chinese Beautiful Rosefinch, ioc); *Carpodacus dubius* (Chinese White-browed Rosefinch, ioc) |
| Трёхполосая корольковка | *Basileuterus tristriatus* (Three-striped Warbler, ioc); *Basileuterus trifasciatus* (Three-banded Warbler, ioc) |
| Желтогорлая танагра | *Hemithraupis flavicollis* (Yellow-backed Tanager, ioc); *Iridosornis analis* (Yellow-throated Tanager, ioc) |
| Толстоклювый просяночник | *Sporophila simplex* (Drab Seedeater, ioc); *Sporophila funerea* (Thick-billed Seed Finch, ioc) |
| Желтоголовая танагра | *Iridosornis jelskii* (Golden-collared Tanager, ioc); *Tangara xanthocephala* (Saffron-crowned Tanager, ioc) |

### Synonyms split out of `ru` (41)

Separators: comma, " / ", " или ", parentheses. The first part stays in `ru`, the rest go to `ru_alt` (first letter capitalised).

| Scientific name | Source name | ru | ru_alt | ru_source |
|---|---|---|---|---|
| Anser fabalis | Гуменник (лесной гуменник) | Гуменник | Лесной гуменник | ioc |
| Cyrtonyx montezumae | Плачущий перепел, перепел Монтесумы | Плачущий перепел | Перепел Монтесумы | ioc |
| Catreus wallichii | Хохлатый фазан, чир | Хохлатый фазан | Чир | ioc |
| Coua cursor | Желтогорлая тивука, тивука-бегун | Желтогорлая тивука | Тивука-бегун | ioc |
| Hirundapus caudacutus | Колючехвост, колючехвостый стриж | Колючехвост | Колючехвостый стриж | ioc |
| Sarcoramphus papa | Королевская катарта, королевский гриф | Королевская катарта | Королевский гриф | ioc |
| Cathartes aura | Катарта-индейка, гриф-индейка | Катарта-индейка | Гриф-индейка | ioc |
| Buceros bicornis | Двурогий калао, гомрай | Двурогий калао | Гомрай | ioc |
| Caracara plancus | Равнинная каракара, каранчо | Равнинная каракара | Каранчо | ioc |
| Strigops habroptilus | Какапо, совиный попугай | Какапо | Совиный попугай | ioc |
| Loriculus galgulus | Малайский лорикулюс, серендак | Малайский лорикулюс | Серендак | ioc |
| Pitangus sulphuratus | Большой бентеви, кискади | Большой бентеви | Кискади | ioc |
| Gymnorhina tibicen | Буругонг, ворона-свистун | Буругонг | Ворона-свистун | ioc |
| Erpornis zantholeuca | Эрпорнис, зелёная ложноюхина | Эрпорнис | Зелёная ложноюхина | ioc |
| Lanius tigrinus | Тигровый жулан, тигровый сорокопут | Тигровый жулан | Тигровый сорокопут | ioc |
| Lanius phoenicuroides | Туркестанский жулан, рыжехвостый жулан | Туркестанский жулан | Рыжехвостый жулан | ioc |
| Lanius schach | Длиннохвостый сорокопут, сорокопут-шах | Длиннохвостый сорокопут | Сорокопут-шах | ioc |
| Pyrrhocorax graculus | Альпийская галка, альпийская клушица | Альпийская галка | Альпийская клушица | ioc |
| Nucifraga caryocatactes | Кедровка, ореховка | Кедровка | Ореховка | ioc |
| Heteralocha acutirostris | Гуйя, разноклювая гуйя | Гуйя | Разноклювая гуйя | ioc |
| Cyanistes cyanus | Князёк, белая лазоревка | Князёк | Белая лазоревка | ioc |
| Pseudopodoces humilis | Тибетская ложносойка, земляная синица | Тибетская ложносойка | Земляная синица | ioc |
| Lophophanes cristatus | Хохлатая синица, гренадерка | Хохлатая синица | Гренадерка | ioc |
| Panurus biarmicus | Усатка, усатая синица | Усатка | Усатая синица | ioc |
| Lullula arborea | Лесной жаворонок, юла | Лесной жаворонок | Юла | ioc |
| Eremophila alpestris | Рогатый жаворонок, рюм | Рогатый жаворонок | Рюм | ioc |
| Hirundo rustica | Деревенская ласточка, ласточка-касатка | Деревенская ласточка | Ласточка-касатка | ioc |
| Delichon urbicum | Воронок, городская ласточка | Воронок | Городская ласточка | ioc |
| Phylloscopus proregulus | Корольковая пеночка, корольковая зарничка | Корольковая пеночка | Корольковая зарничка | ioc |
| Phylloscopus schwarzi | Толстоклювая пеночка, голосистая пеночка | Толстоклювая пеночка | Голосистая пеночка | ioc |
| Myzornis pyrrhoura | Зелёная огнехвостка, мизорнис | Зелёная огнехвостка | Мизорнис | ioc |
| Leiothrix lutea | Красноклювый лиотрикс, пекинский соловей | Красноклювый лиотрикс | Пекинский соловей | ioc |
| Garrulax canorus | Очковая кустарница, хуамей | Очковая кустарница | Хуамей | ioc |
| Grandala coelicolor | Лазоревая птица, грандала | Лазоревая птица | Грандала | ioc |
| Carpodacus puniceus | Красная чечевица, красный вьюрок | Красная чечевица | Красный вьюрок | ioc |
| Serinus canaria | Канарский вьюрок, дикая канарейка | Канарский вьюрок | Дикая канарейка | ioc |
| Serinus serinus | Канареечный вьюрок, европейский вьюрок | Канареечный вьюрок | Европейский вьюрок | ioc |
| Emberiza schoeniclus | Камышовая овсянка, стренатка | Камышовая овсянка | Стренатка | ioc |
| Emberiza citrinella | Овсянка, обыкновенная овсянка | Овсянка | Обыкновенная овсянка | ioc |
| Molothrus ater | Коровий трупиал, буроголовый желтушник | Коровий трупиал | Буроголовый желтушник | ioc |
| Coereba flaveola | Банановая кареба, сахарная цветочница | Банановая кареба | Сахарная цветочница | ioc |

### Parentheses left in `ru` (0)

The parenthesis does not look like a name (comment, Latin, digits); not split.

| Scientific name | ru |
|---|---|

### `ru_alt` equal to another species' `ru` (0)

| Scientific name | ru_alt | is `ru` of |
|---|---|---|

### Top 50 `ru_head` (index nests)

| ru_head | Species |
|---|---|
| голубь | 196 |
| дятел | 158 |
| дрозд | 149 |
| бюльбюль | 142 |
| танагра | 127 |
| нектарница | 123 |
| мухоловка | 105 |
| белоглазка | 100 |
| горлица | 96 |
| козодой | 92 |
| жаворонок | 92 |
| крапивник | 86 |
| ласточка | 78 |
| овсянка | 76 |
| зимородок | 73 |
| муравьеловка | 72 |
| кустарница | 71 |
| скворец | 69 |
| ткач | 68 |
| кукушка | 66 |
| пеночка | 62 |
| попугай | 58 |
| совка | 56 |
| тапакуло | 56 |
| трупиал | 53 |
| веерохвостка | 50 |
| сова | 49 |
| цистикола | 49 |
| колибри | 48 |
| медосос | 48 |
| свистун | 48 |
| древолаз | 47 |
| сойка | 47 |
| цветоед | 47 |
| астрильд | 47 |
| перепел | 46 |
| чайка | 46 |
| древесница | 46 |
| буревестник | 45 |
| вьюрок | 45 |
| конёк | 45 |
| крачка | 42 |
| воробей | 42 |
| мухолов | 41 |
| иглохвостка | 41 |
| монарх | 41 |
| куропатка | 40 |
| тайфунник | 40 |
| камышовка | 40 |
| просяночник | 40 |

### Doubtful `ru_head` (15)

All-adjective names, a lower-case word after the head (apposition such as "конёк пуны" or a typo), or a capitalised head after other words. Fix systematic errors in `ru_head()`, single ones with `field = ru_head` in overrides.

| Scientific name | ru | ru_head |
|---|---|---|
| Tinamotis pentlandii | Тинаму пуны | тинаму |
| Crypturellus tataupa | Скрытохвост татаупа | скрытохвост |
| Spatula puna | Чирок пуны | чирок |
| Syrmaticus mikado | Фазан микадо | фазан |
| Gallinago andina | Бекас пуны | бекас |
| Cacatua leadbeateri | Какаду инка | какаду |
| Scytalopus opacus | Тапакуло парамо | тапакуло |
| Geositta punensis | Землекоп пуны | землекоп |
| Asthenes helleri | Чертополошник пуны | чертополошник |
| Vireo chivi | Виреон чиви | виреон |
| Zosterops flavissimus | Белоглазка вакатоби | белоглазка |
| Anthus brevirostris | Конёк пуны | конёк |
| Anthus bogotensis | Конёк парамо | конёк |
| Catamenia homochroa | Семеноед парамо | семеноед |
| Sporophila beltoni | Просяночник серрадо | просяночник |

### `ru_book` with the capital kept (69)

First word is a possessive adjective from a proper name.

| Scientific name | ru | English | English has 's |
|---|---|---|---|
| Rhea pennata | Дарвинов нанду | Lesser Rhea |  |
| Nothura darwinii | Дарвинова нотура | Darwin's Nothura | yes |
| Crypturellus bartletti | Бартлеттов скрытохвост | Bartlett's Tinamou | yes |
| Chloephaga picta | Магелланов гусь | Upland Goose |  |
| Aythya baeri | Бэров нырок | Baer's Pochard | yes |
| Tachyeres pteneres | Магелланова утка-пароход | Fuegian Steamer Duck |  |
| Penelope ortoni | Ортонова пенелопа | Baudo Guan |  |
| Mitu salvini | Сальвинов гокко | Salvin's Curassow | yes |
| Pternistis swainsonii | Свенсонов франколин | Swainson's Spurfowl | yes |
| Podiceps major | Магелланова поганка | Great Grebe |  |
| Rallus antarcticus | Магелланов пастушок | Austral Rail |  |
| Pluvianellus socialis | Магелланова ржанка | Magellanic Plover |  |
| Haematopus leucopodus | Магелланов кулик-сорока | Magellanic Oystercatcher |  |
| Anarhynchus wilsonia | Вильсонов зуёк | Wilson's Plover | yes |
| Attagis malouinus | Магелланов зобатый бегунок | White-bellied Seedsnipe |  |
| Calidris bairdii | Бэрдов песочник | Baird's Sandpiper | yes |
| Calidris fuscicollis | Бонапартов песочник | White-rumped Sandpiper |  |
| Chroicocephalus philadelphia | Бонапартова чайка | Bonaparte's Gull | yes |
| Leucophaeus scoresbii | Магелланова чайка | Dolphin Gull |  |
| Leucophaeus pipixcan | Франклинова чайка | Franklin's Gull | yes |
| Ichthyaetus audouinii | Одуэнова чайка | Audouin's Gull | yes |
| Larus belcheri | Бельчерова чайка | Belcher's Gull | yes |
| Spheniscus humboldti | Гумбольдтов пингвин | Humboldt Penguin |  |
| Spheniscus magellanicus | Магелланов пингвин | Magellanic Penguin |  |
| Diomedea antipodensis | Антиподов альбатрос | Antipodean Albatross |  |
| Thalassarche bulleri | Буллеров альбатрос | Buller's Albatross | yes |
| Oceanites oceanicus | Вильсонова океанида | Wilson's Storm Petrel | yes |
| Bulweria bulwerii | Бульверов штормовик | Bulwer's Petrel | yes |
| Ardenna bulleri | Буллеров буревестник | Buller's Shearwater | yes |
| Puffinus boydi | Бойдов буревестник | Boyd's Shearwater | yes |
| Pelecanoides magellani | Магелланов ныряющий буревестник | Magellanic Diving Petrel |  |
| Pachyptila salvini | Сальвинов прион | Salvin's Prion | yes |
| Pterodroma gouldi | Гульдов тайфунник | Grey-faced Petrel |  |
| Pterodroma solandri | Соландров тайфунник | Providence Petrel |  |
| Leucocarbo magellanicus | Магелланов баклан | Rock Shag |  |
| Urile pelagicus | Берингов баклан | Pelagic Cormorant |  |
| Urile perspicillatus | Стеллеров баклан | Spectacled Cormorant |  |
| Caprimulgus concretus | Бонапартов козодой | Bonaparte's Nightjar | yes |
| Cypseloides rothschildi | Ротшильдов стриж | Rothschild's Swift | yes |
| Neafrapus cassini | Кассинов колючехвост | Cassin's Spinetail | yes |
| Lophornis gouldii | Гульдова кокетка | Dot-eared Coquette |  |
| Archilochus alexandri | Александров колибри | Black-chinned Hummingbird |  |
| Selasphorus sasin | Алленов колибри | Allen's Hummingbird | yes |
| Thaumasius baeri | Бэров левкипп | Tumbes Hummingbird |  |
| Chrysuronia humboldtii | Гумбольдтов сапфир | Humboldt's Sapphire | yes |
| Bubo magellanicus | Магелланов филин | Lesser Horned Owl |  |
| Astur cooperii | Куперов ястреб | Cooper's Hawk | yes |
| Buteo swainsoni | Свенсонов канюк | Swainson's Hawk | yes |
| Buteo ventralis | Магелланов канюк | Rufous-tailed Hawk |  |
| Ceyx wallacii | Уоллесов зимородок | Sula Dwarf Kingfisher |  |
| Tanysiptera ellioti | Эллиотов райский зимородок | Kofiau Paradise Kingfisher |  |
| Selenidera gouldii | Гульдов туканчик | Gould's Toucanet | yes |
| Campephilus magellanicus | Магелланов дятел | Magellanic Woodpecker |  |
| Dendropicos elliotii | Эллиотов дятел | Elliot's Woodpecker | yes |
| Enicognathus ferrugineus | Магелланова которра | Austral Parakeet |  |
| Cyanoramphus unicolor | Антиподов какарики | Antipodes Parakeet |  |
| Trichoglossus johnstoniae | Джонстонов лорикет | Mindanao Lorikeet |  |
| Scytalopus magellanicus | Магелланов тапакуло | Magellanic Tapaculo |  |
| Xiphorhynchus spixii | Спиксов древолаз | Spix's Woodcreeper | yes |
| Menura alberti | Альбертов лирохвост | Albert's Lyrebird | yes |
| Cyanocitta stelleri | Стеллерова сойка | Steller's Jay | yes |
| Onychognathus tristramii | Тристрамов скворец | Tristram's Starling | yes |
| Catharus ustulatus | Свэнсонов дрозд | Swainson's Thrush | yes |
| Turdus falcklandii | Магелланов дрозд | Austral Thrush |  |
| Niltava davidi | Давидова нильтава | Fujian Niltava |  |
| Aethopyga gouldiae | Гульдова нектарница | Mrs. Gould's Sunbird | yes |
| Vidua wilsoni | Вильсонова вдовушка | Wilson's Indigobird | yes |
| Chloebia gouldiae | Гульдова амадина | Gouldian Finch |  |
| Spinus magellanicus | Магелланов чиж | Hooded Siskin |  |

## Orders and families: Russian names

Sources: ZMMU passerine list family headers (`zmmu`), Wikidata (`wikidata`), `data/overrides.csv` (`manual`). Written to `data/taxa.json`.

| Rank | Total | zmmu | wikidata | manual | missing |
|---|---|---|---|---|---|
| orders | 46 | 0 | 39 | 7 | 0 |
| families | 252 | 142 | 96 | 14 | 0 |

### Taxon name warnings

- ZMMU header 'Scleruridae' (Тенелюбовые) not used (majority AviList family of its species: Furnariidae)
- ZMMU header 'Dendrocolaptidae' (Древолазовые) not used (majority AviList family of its species: Furnariidae)
- ZMMU header 'Pityriaseidae' (Щетинкоголовы) lists Pityriasidae species; used for Pityriasidae
- ZMMU header 'Eulacestomatidae' (Сителлы) lists Neosittidae species; used for Neosittidae
- ZMMU header 'Pteruthiusidae' (Птерутии) not used (majority AviList family of its species: Vireonidae)
- ZMMU header 'Lamproliidae' (Шелкохвостковые) not used (majority AviList family of its species: Rhipiduridae)
- ZMMU header 'Ptilogonatidae' (Шелкохвосты) lists Ptiliogonatidae species; used for Ptiliogonatidae
- ZMMU header 'Scotocercidae' (Скотоцерки) not used (majority AviList family of its species: Cettiidae)
- ZMMU header 'Chamaeidae' (Чапаральницы) not used (majority AviList family of its species: Paradoxornithidae)
- ZMMU header 'Rhabdornithidae' (Пищуховые скворцы) not used (majority AviList family of its species: Sturnidae)
- ZMMU header 'Drepanididae' (Гавайские цветочницы) not used (majority AviList family of its species: Fringillidae)
- ZMMU header 'Zeleddoniidae' (Зеледонии) lists Zeledoniidae species; used for Zeledoniidae
- ZMMU header 'Icteriidae' (Иктерии) not used (majority AviList family of its species: Icteridae)

### Orders and families without a Russian name (0)

| Rank | Scientific name | English | Species |
|---|---|---|---|

## AviList species not found in IOC (42)

| Scientific name | English | ru_source |
|---|---|---|
| Tachyspiza haplochrous | White-bellied Goshawk | — |
| Rhinopomastus castaneiceps | Forest Wood Hoopoe | ebird |
| Charmosyna multistriata | Striated Lorikeet | ebird |
| Vini margarethae | Duchess Lorikeet | ebird |
| Chalcopsitta fuscata | Dusky Lory | ebird |
| Chalcopsitta cardinalis | Cardinal Lory | ebird |
| Trichoglossus concinnus | Musk Lorikeet | ebird |
| Trichoglossus johnstoniae | Mindanao Lorikeet | ebird |
| Trichoglossus iris | Iris Lorikeet | ebird |
| Trichoglossus ornatus | Ornate Lorikeet | ebird |
| Trichoglossus meyeri | Yellow-cheeked Lorikeet | — |
| Trichoglossus flavoviridis | Sula Lorikeet | wikidata |
| Trichoglossus reticulatus | Blue-streaked Lory | ebird |
| Trichoglossus semilarvatus | Blue-eared Lory | ebird |
| Trichoglossus borneus | Red Lory | ebird |
| Trichoglossus cyanogenius | Black-winged Lory | ebird |
| Trichoglossus histrio | Red-and-blue Lory | ebird |
| Trichoglossus squamatus | Violet-necked Lory | ebird |
| Elaenia cherriei | Hispaniolan Elaenia | — |
| Empidonomus aurantioatrocristatus | Crowned Slaty Flycatcher | ebird |
| Ochthoeca salvini | Tumbes Tyrant | ebird |
| Lichmera lombokia | Scaly-crowned Honeyeater | ebird |
| Meliphaga reticulata | Streak-breasted Honeyeater | ebird |
| Meliphaga fordiana | Kimberley Honeyeater | ebird |
| Meliphaga albilineata | White-lined Honeyeater | ebird |
| Meliphaga chrysogenys | Orange-cheeked Honeyeater | ebird |
| Meliphaga montana | Forest Honeyeater | ebird |
| Meliphaga mimikae | Mottle-breasted Honeyeater | ebird |
| Meliphaga flavirictus | Yellow-gaped Honeyeater | ebird |
| Meliphaga orientalis | Mountain Honeyeater | ebird |
| Meliphaga albonotata | Scrub Honeyeater | ebird |
| Meliphaga analoga | Mimic Honeyeater | ebird |
| Meliphaga vicina | Tagula Honeyeater | ebird |
| Meliphaga gracilis | Graceful Honeyeater | ebird |
| Meliphaga imitatrix | Cryptic Honeyeater | ebird |
| Meliphaga cinereifrons | Elegant Honeyeater | ebird |
| Microtarsus eutilotus | Puff-backed Bulbul | ebird |
| Rubigula erythropthalmos | Spectacled Bulbul | ebird |
| Rubigula cyaniventris | Grey-bellied Bulbul | ebird |
| Rubigula squamata | Scaly-breasted Bulbul | ebird |
| Stiphrornis mabirae | Yellow-breasted Forest Robin | — |
| Emblema modestum | Plum-headed Finch | ebird |

## Species with no Russian name anywhere (404)

| Scientific name | English |
|---|---|
| Pipile grayi | White-throated Piping Guan |
| Penelope bridgesi | Yungas Guan |
| Guttera verreauxi | Western Crested Guineafowl |
| Guttera edouardi | Southern Crested Guineafowl |
| Lagopus scotica | Red Grouse |
| Lophura pyronota | Bornean Crestless Fireback |
| Lophura rufa | Malayan Crested Fireback |
| Rheinardia nigrescens | Malayan Crested Argus |
| Tropicoperdix graydoni | Sabah Partridge |
| Scleroptila elgonensis | Elgon Francolin |
| Scleroptila whytei | Whyte's Francolin |
| Coua olivaceiceps | Olive-capped Coua |
| Phaenicophaeus oeneicaudus | Mentawai Malkoha |
| Piaya mexicana | Mexican Squirrel Cuckoo |
| Chalcites crassirostris | Pied Bronze Cuckoo |
| Cacomantis virescens | Sulawesi Brush Cuckoo |
| Cacomantis addendus | Solomons Brush Cuckoo |
| Cacomantis blandus | Manus Brush Cuckoo |
| Streptopelia dusumieri | Philippine Collared Dove |
| Streptopelia xanthocycla | Burmese Collared Dove |
| Ducula oenothorax | Enggano Imperial Pigeon |
| Ducula geelvinkiana | Geelvink Imperial Pigeon |
| Ducula cuprea | Malabar Imperial Pigeon |
| Ptilinopus chrysogaster | Raiatea Fruit Dove |
| Ptilinopus speciosus | Geelvink Fruit Dove |
| Anarhynchus dealbatus | White-faced Plover |
| Gallinago magellanica | Magellanic Snipe |
| Turnix novaecaledoniae | New Caledonian Buttonquail |
| Gygis candida | Blue-billed White Tern |
| Gygis microrhyncha | Little White Tern |
| Gelochelidon macrotarsa | Australian Tern |
| Thalasseus albididorsalis | West African Crested Tern |
| Larus brachyrhynchus | Short-billed Gull |
| Eudyptes filholi | Eastern Rockhopper Penguin |
| Fregetta lineata | New Caledonian Storm Petrel |
| Pachyptila macgillivrayi | MacGillivray's Prion |
| Sula brewsteri | Cocos Booby |
| Butorides atricapilla | Little Heron |
| Ardea brachyrhyncha | Yellow-billed Egret |
| Ardea plumifera | Plumed Egret |
| Caprimulgus ritae | Timor Nightjar |
| Caprimulgus griseatus | Chirruping Nightjar |
| Aegotheles terborghi | Karimui Owlet-nightjar |
| Cypsiurus gracilis | Malagasy Palm Swift |
| Anthracothorax aurulentus | Puerto Rican Mango |
| Coeligena conradii | Green Inca |
| Coeligena inca | Gould's Inca |
| Coeligena consita | Perija Starfrontlet |
| Coeligena eos | Golden-tailed Starfrontlet |
| Ocreatus peruanus | Peruvian Racket-tail |
| Ocreatus addae | Rufous-booted Racket-tail |
| Cynanthus lawrencei | Tres Marias Hummingbird |
| Campylopterus calcirupicola | Outcrop Sabrewing |
| Campylopterus diamantinensis | Diamantina Sabrewing |
| Saucerottia hoffmanni | Blue-vented Hummingbird |
| Saucerottia cupreicauda | Copper-tailed Hummingbird |
| Tyto javanica | Eastern Barn Owl |
| Tyto furcata | American Barn Owl |
| Ninox rotiensis | Rote Boobook |
| Ninox fusca | Timor Boobook |
| Ninox plesseni | Alor Boobook |
| Ninox leucopsis | Tasmanian Boobook |
| Ninox hantu | Buru Boobook |
| Taenioptynx sylvaticus | Sunda Owlet |
| Aegolius gradyi | Bermuda Saw-whet Owl |
| Athene granti | Guadalcanal Owl |
| Athene malaitae | Malaita Owl |
| Athene roseoaxillaris | Makira Owl |
| Otus tempestatis | Wetar Scops Owl |
| Otus mendeni | Banggai Scops Owl |
| Otus bikegila | Principe Scops Owl |
| Bubo milesi | Arabian Eagle-Owl |
| Tachyspiza haplochrous | White-bellied Goshawk |
| Astur atricapillus | American Goshawk |
| Bermuteo avivorus | Bermuda Hawk |
| Trogon tenellus | Graceful Black-throated Trogon |
| Trogon cupreicauda | Choco Black-throated Trogon |
| Trogon chrysochloros | Atlantic Black-throated Trogon |
| Trogon ambiguus | Coppery-tailed Trogon |
| Lophoceros semifasciatus | West African Pied Hornbill |
| Horizocerus cassini | Eastern Long-tailed Hornbill |
| Horizocerus granti | Eastern Dwarf Hornbill |
| Merops lafresnayii | Ethiopian Bee-eater |
| Merops americanus | Rufous-crowned Bee-eater |
| Alcedo peninsulae | Malaysian Blue-banded Kingfisher |
| Ceyx sangirensis | Sangihe Dwarf Kingfisher |
| Halcyon gularis | Brown-breasted Kingfisher |
| Cittura sanghirensis | Sangihe Lilac Kingfisher |
| Psilopogon cyanotis | Blue-eared Barbet |
| Psilopogon auricularis | Necklaced Barbet |
| Psilopogon chersonesus | Turquoise-throated Barbet |
| Pogoniulus uropygialis | Northern Red-fronted Tinkerbird |
| Campethera taeniolaema | Fine-banded Woodpecker |
| Mulleripicus fuliginosus | Southern Sooty Woodpecker |
| Colaptes oceanicus | Bermuda Flicker |
| Campephilus splendens | Splendid Woodpecker |
| Chrysocolaptes socialis | Malabar Flameback |
| Dryobates pernyii | Necklaced Woodpecker |
| Cacatua citrinocristata | Citron-crested Cockatoo |
| Forpus spengeli | Turquoise-winged Parrotlet |
| Forpus crassirostris | Riparian Parrotlet |
| Amazona lilacina | Lilacine Amazon |
| Pyrrhura subandina | Subandean Parakeet |
| Pyrrhura caeruleiceps | Perija Parakeet |
| Psittacara frontatus | Cordilleran Parakeet |
| Psittacara maugei | Puerto Rican Parakeet |
| Coracopsis sibilans | Comoro Black Parrot |
| Eclectus cornelia | Sumba Eclectus |
| Eclectus riedeli | Tanimbar Eclectus |
| Eclectus polychloros | Papuan Eclectus |
| Eclectus infectus | Oceanic Eclectus |
| Psittinus abbotti | Simeulue Parrot |
| Northiella narethae | Naretha Bluebonnet |
| Loriculus bonapartei | Black-billed Hanging Parrot |
| Nannopsittacus melanogenia | Dusky-cheeked Fig Parrot |
| Nannopsittacus nigrifrons | Black-fronted Fig Parrot |
| Charmosyna stellae | Stella's Lorikeet |
| Trichoglossus meyeri | Yellow-cheeked Lorikeet |
| Serilophus rubropygius | Grey-lored Broadbill |
| Pitta abbotti | Nicobar Hooded Pitta |
| Pitta forsteni | Minahasa Hooded Pitta |
| Pitta novaeguineae | Eastern Hooded Pitta |
| Pitta rosenbergii | Biak Hooded Pitta |
| Pitta concinna | Ornate Pitta |
| Pitta vigorsii | Banda Sea Pitta |
| Cryptopipo litae | Choco Manakin |
| Lepidothrix velutina | Velvety Manakin |
| Tityra leucura | White-tailed Tityra |
| Pachyramphus salvini | Cryptic Becard |
| Rhynchocyclus aequinoctialis | Western Olivaceous Flatbill |
| Stigmatura bahiae | Bahia Wagtail-Tyrant |
| Euscarthmus fulviceps | Fulvous-faced Scrub Tyrant |
| Myiopagis parambae | Choco Elaenia |
| Myiopagis cinerea | Amazonian Elaenia |
| Elaenia cherriei | Hispaniolan Elaenia |
| Nesotriccus maranonicus | Maranon Tyrannulet |
| Myiophobus crypterythrus | Mouse-grey Flycatcher |
| Myiophobus rufescens | Rufescent Flycatcher |
| Ochthoeca superciliosa | Rufous-browed Chat-Tyrant |
| Contopus bogotensis | Northern Tropical Pewee |
| Conopophaga snethlageae | Black-breasted Gnateater |
| Herpsilochmus frater | Rusty-winged Antwren |
| Sakesphorus pulchellus | Streak-fronted Antshrike |
| Thamnophilus shumbae | Maranon Antshrike |
| Grallaria spatiator | Sierra Nevada Antpitta |
| Grallaria saltuensis | Perija Antpitta |
| Grallaria centralis | Oxapampa Antpitta |
| Grallaria ayacuchensis | Ayacucho Antpitta |
| Grallaria occabambae | Urubamba Antpitta |
| Grallaria sinaensis | Puno Antpitta |
| Grallaria cochabambae | Bolivian Antpitta |
| Grallaria alvarezi | Chami Antpitta |
| Grallaria saturata | Equatorial Antpitta |
| Grallaria cajamarcae | Cajamarca Antpitta |
| Grallaria gravesi | Chachapoyas Antpitta |
| Grallaria oneilli | Panao Antpitta |
| Grallaria obscura | Junin Antpitta |
| Grallaria alticola | Boyaca Antpitta |
| Grallaria atuensis | Atuen Antpitta |
| Deconychura typica | Piping Long-tailed Woodcreeper |
| Deconychura pallida | Mournful Long-tailed Woodcreeper |
| Campylorhamphus probatus | Tapajos Scythebill |
| Campylorhamphus multostriatus | Xingu Scythebill |
| Xenops mexicanus | Northern Plain Xenops |
| Xenops genibarbis | Amazonian Plain Xenops |
| Automolus cervinigularis | Fawn-throated Foliage-gleaner |
| Cranioleuca weskei | Vilcabamba Spinetail |
| Synallaxis simoni | Araguaia Spinetail |
| Synallaxis chinchipensis | Chinchipe Spinetail |
| Amytornis oweni | Sandhill Grasswren |
| Gerygone citrina | Rennell Gerygone |
| Myzomela simplex | Moluccan Myzomela |
| Myzomela rubrotincta | Red-tinged Myzomela |
| Myzomela rubrobrunnea | Biak Myzomela |
| Myzomela erythrina | Reddish Myzomela |
| Myzomela batjanensis | Bacan Myzomela |
| Myzomela nigriventris | Samoan Myzomela |
| Myzomela longirostris | Long-billed Myzomela |
| Coracina larutensis | Malayan Cuckooshrike |
| Coracina mindorensis | Mindoro Cuckooshrike |
| Coracina panayensis | Visayan Cuckooshrike |
| Coracina kochii | Mindanao Cuckooshrike |
| Coracina guillemardi | Sulu Cuckooshrike |
| Lalage leucoptera | Biak Triller |
| Edolisoma timoriense | Timor Cicadabird |
| Edolisoma tricolor | Malaita Cicadabird |
| Edolisoma salvadorii | Sangihe Cicadabird |
| Edolisoma erythropygium | Central Melanesian Cicadabird |
| Edolisoma meyerii | Geelvink Cicadabird |
| Edolisoma pelingi | Banggai Cicadabird |
| Edolisoma obiense | Obi Cicadabird |
| Edolisoma grayi | North Moluccan Cicadabird |
| Edolisoma rostratum | Rossel Cicadabird |
| Edolisoma amboinense | South Moluccan Cicadabird |
| Batis dimorpha | Malawi Batis |
| Batis occulta | West African Batis |
| Cyanolanius comorensis | Comoro Blue Vanga |
| Falcunculus leucogaster | Western Shriketit |
| Falcunculus whitei | Northern Shriketit |
| Paramythia olivacea | Western Crested Berrypecker |
| Tunchiornis ferrugineifrons | Rufous-fronted Greenlet |
| Tunchiornis luteifrons | Guianan Greenlet |
| Tunchiornis rubrifrons | Para Greenlet |
| Oriolus finschi | Wetar Oriole |
| Oriolus consobrinus | Ventriloquial Oriole |
| Oriolus consanguineus | Black-and-crimson Oriole |
| Pachycephala graeffii | Yellow-throated Fiji Whistler |
| Pachycephala ornata | Nendo Whistler |
| Pachycephala utupuae | Utupua Whistler |
| Pachycephala calliope | Tenggara Whistler |
| Pachycephala teysmanni | Selayar Whistler |
| Pachycephala sharpei | Babar Whistler |
| Rhipidura coultasi | White-gorgeted Fantail |
| Rhipidura semicollaris | Supertramp Fantail |
| Rhipidura torrida | Gilolo Fantail |
| Rhipidura louisiadensis | Louisiade Fantail |
| Rhipidura melanolaema | Santa Cruz Fantail |
| Rhipidura versicolor | Micronesian Rufous Fantail |
| Rhipidura rufofronta | Solomons Rufous Fantail |
| Rhipidura ocularis | Guadalcanal Fantail |
| Rhipidura spilodera | Vanuatu Streaked Fantail |
| Rhipidura layardi | Fiji Streaked Fantail |
| Dicrurus striatus | Short-tailed Drongo |
| Terpsiphone floris | Tenggara Paradise Flycatcher |
| Myiagra eichhorni | Velvet Flycatcher |
| Symposiachrus melanopterus | Louisiade Monarch |
| Symposiachrus malaitae | Malaita Monarch |
| Symposiachrus nigrotectus | Vella Lavella Monarch |
| Carterornis castus | Tanimbar Monarch |
| Lycocorax obiensis | Obi Paradise-crow |
| Lanius giganteus | Giant Grey Shrike |
| Corvus philippinus | Philippine Jungle Crow |
| Corvus sierramadrensis | Sierra Madre Crow |
| Corvus samarensis | Samar Crow |
| Corvus celebensis | Sulawesi Crow |
| Corvus pusillus | Palawan Crow |
| Melanocharis citreola | Satin Berrypecker |
| Melanocharis piperata | Spotted Berrypecker |
| Heteromyias armiti | Black-capped Robin |
| Corypha kurrae | Highland Lark |
| Corypha kabalii | Plains Lark |
| Corypha nigrescens | Plateau Lark |
| Corypha athi | Sentinel Lark |
| Corypha sharpii | Russet Lark |
| Corypha kidepoensis | Kidepo Lark |
| Apalis stronachi | Maasai Apalis |
| Prinia khasiana | Rufous-crowned Prinia |
| Prinia lepida | Delicate Prinia |
| Cisticola bakerorum | Kilombero Cisticola |
| Cisticola bailunduensis | Huambo Cisticola |
| Cisticola anderseni | White-tailed Cisticola |
| Acrocephalus nijoi | Aguiguan Reed Warbler |
| Riparia cowani | Madagascar Martin |
| Ptyonoprogne rufigula | Red-throated Rock Martin |
| Cecropis melanocrissus | African Red-rumped Swallow |
| Atimastillas flavigula | Pale-throated Greenbul |
| Phyllastrephus viridiceps | Angola Greenbul |
| Pycnonotus davisoni | Pale-eyed Bulbul |
| Ixos sumatranus | Sumatran Bulbul |
| Hypsipetes platenae | Sangihe Golden Bulbul |
| Hypsipetes aureus | Togian Golden Bulbul |
| Hypsipetes harterti | Banggai Golden Bulbul |
| Hypsipetes chloris | Halmahera Golden Bulbul |
| Hypsipetes lucasi | Obi Golden Bulbul |
| Hypsipetes catarmanensis | Camiguin Bulbul |
| Suthora ricketti | Eye-ringed Parrotbill |
| Sterrhoptilus affinis | Calabarzon Babbler |
| Zosterops kaffensis | Kafa White-eye |
| Zosterops kasaicus | Angola White-eye |
| Zosterops meratusensis | Meratus White-eye |
| Zosterops paruhbesar | Wangi-wangi White-eye |
| Zosterops hamlini | Bougainville White-eye |
| Zosterops oblitus | Guadalcanal White-eye |
| Zosterops ponapensis | Grey-brown White-eye |
| Mixornis prillwitzi | Kangean Tit-Babbler |
| Cyanoderma bicolor | Bicolored Babbler |
| Pomatorhinus phayrei | Brown-crowned Scimitar Babbler |
| Pomatorhinus bornensis | Sunda Scimitar Babbler |
| Erythrogenys imberbis | Red-eyed Scimitar Babbler |
| Pellorneum nigrocapitatum | Malayan Black-capped Babbler |
| Pellorneum capistratoides | Bornean Black-capped Babbler |
| Illadopsis distans | Tanzanian Illadopsis |
| Gypsophila annamensis | Annam Limestone Babbler |
| Gypsophila calcicola | Rufous Limestone Babbler |
| Sitta insularis | Bahama Nuthatch |
| Polioptila maior | Maranon Gnatcatcher |
| Polioptila bilineata | White-browed Gnatcatcher |
| Troglodytes beani | Cozumel Wren |
| Troglodytes martinicensis | Kalinago Wren |
| Troglodytes mesoleucus | St. Lucia Wren |
| Troglodytes musicus | St. Vincent Wren |
| Troglodytes grenadensis | Grenada Wren |
| Troglodytes musculus | Southern House Wren |
| Pheugopedius schulenbergi | Grey-browed Wren |
| Cyphorhinus dichrous | Northern Chestnut-breasted Wren |
| Ramphocinclus sanctaeluciae | St. Lucia Thrasher |
| Rhabdornis rabori | Visayan Rhabdornis |
| Gracula venerata | Tenggara Hill Myna |
| Gracupica floweri | Siamese Pied Myna |
| Gracupica jalla | Javan Pied Myna |
| Acridotheres leucocephalus | Vinous-breasted Myna |
| Myadestes woahensis | Amaui |
| Zoothera atrigena | Bougainville Thrush |
| Turdus simensis | Ethiopian Thrush |
| Turdus mindorensis | Mindoro Island Thrush |
| Turdus thomassoni | Luzon Island Thrush |
| Turdus nigrorum | Negros Island Thrush |
| Turdus erythropleurus | Christmas Island Thrush |
| Turdus schlegelii | Sulawesi Island Thrush |
| Turdus javanicus | Sunda Island Thrush |
| Turdus deningeri | Sula Island Thrush |
| Turdus papuensis | Papuan Island Thrush |
| Turdus heinrothi | Bismarck Island Thrush |
| Turdus bougainvillei | Bougainville Island Thrush |
| Turdus kulambangrae | Guadalcanal Island Thrush |
| Turdus vanikorensis | Vanuatu Island Thrush |
| Turdus pritzbueri | Loyalty Island Thrush |
| Turdus xanthopus | New Caledonian Island Thrush |
| Turdus samoensis | Samoan Island Thrush |
| Turdus ruficeps | Fiji Island Thrush |
| Turdus ardosiaceus | Eastern Red-legged Thrush |
| Copsychus leggei | Sri Lanka Shama |
| Copsychus barbouri | Maratua Shama |
| Copsychus nigricauda | Kangean Shama |
| Copsychus omissus | Larwo Shama |
| Copsychus superciliaris | Visayan Shama |
| Niltava oatesi | Chinese Vivid Niltava |
| Eumyias stresemanni | Sumba Jungle Flycatcher |
| Cyornis camarinensis | Rufous-breasted Blue Flycatcher |
| Cyornis montanus | Dayak Blue Flycatcher |
| Cyornis kadayangensis | Meratus Blue Flycatcher |
| Cyornis kalaoensis | Kalao Blue Flycatcher |
| Cyornis ocularis | Sulu Jungle Flycatcher |
| Cyornis ruficrissa | Crocker Jungle Flycatcher |
| Stiphrornis pyrrholaemus | Olive-backed Forest Robin |
| Stiphrornis mabirae | Yellow-breasted Forest Robin |
| Myiomela sumatrana | Sumatran Blue Robin |
| Larvivora tanensis | Izu Robin |
| Larvivora namiyei | Okinawa Robin |
| Brachypteryx poliogyna | Philippine Shortwing |
| Brachypteryx erythrogyna | Bornean Shortwing |
| Brachypteryx saturata | Sumatran Shortwing |
| Brachypteryx floris | Flores Shortwing |
| Ficedula owstoni | Ryukyu Flycatcher |
| Tarsiger albocoeruleus | Qilian Bluetail |
| Tarsiger formosanus | Taiwan Bush Robin |
| Monticola erythronotus | Amber Mountain Rock Thrush |
| Oenanthe seebohmi | Atlas Wheatear |
| Oenanthe frenata | Rusty-breasted Wheatear |
| Dicaeum kampalili | Flame-crowned Flowerpecker |
| Dicaeum cambodianum | Cambodian Flowerpecker |
| Dicaeum luzoniense | Fire-throated Flowerpecker |
| Dicaeum beccarii | Sumatran Flowerpecker |
| Dicaeum rhodopygiale | Flores Flowerpecker |
| Dicaeum wilhelminae | Sumba Flowerpecker |
| Dicaeum hanieli | Timor Flowerpecker |
| Dicaeum keiense | Pink-breasted Flowerpecker |
| Anthreptes tephrolaemus | Grey-chinned Sunbird |
| Aethopyga tibolii | Tboli Sunbird |
| Cinnyris melanogastrus | Gorgeous Sunbird |
| Cinnyris hellmayri | Arabian Sunbird |
| Cinnyris ornatus | Ornate Sunbird |
| Cinnyris infrenatus | Tukangbesi Sunbird |
| Cinnyris frenatus | Sahul Sunbird |
| Cinnyris aurora | Palawan Sunbird |
| Cinnyris clementiae | South Moluccan Sunbird |
| Cinnyris teysmanni | Flores Sea Sunbird |
| Cinnyris idenburgi | Mamberamo Sunbird |
| Irena tweeddalii | Palawan Fairy-bluebird |
| Ploceus brachypterus | Olive-naped Weaver |
| Ploceus holoxanthus | Ruvu Weaver |
| Ploceus castaneofuscus | Chestnut-and-black Weaver |
| Euplectes laticauda | Red-cowled Widowbird |
| Anaplectes jubaensis | Red Weaver |
| Lonchura nigerrima | New Hanover Mannikin |
| Fringilla spodiogenys | African Chaffinch |
| Fringilla moreletti | Azores Chaffinch |
| Fringilla maderensis | Madeira Chaffinch |
| Fringilla canariensis | Canary Islands Chaffinch |
| Chlorophonia sclateri | Puerto Rican Euphonia |
| Chlorophonia flavifrons | Lesser Antillean Euphonia |
| Euphonia godmani | West Mexican Euphonia |
| Pyrrhula owstoni | Taiwan Bullfinch |
| Crithagra striatipectus | Stripe-breasted Seedeater |
| Chrysocorythus mindanensis | Mindanao Serin |
| Arremon nigriceps | Maranon Sparrow |
| Arremon axillaris | Yellow-mandibled Sparrow |
| Arremon dorbignii | Moss-backed Sparrow |
| Melozone occipitalis | Grey-crowned Ground Sparrow |
| Pipilo naufragus | Bermuda Towhee |
| Atlapetes taczanowskii | Taczanowski's Brushfinch |
| Sturnella lilianae | Chihuahuan Meadowlark |
| Basileuterus delattrii | Chestnut-capped Warbler |
| Granatellus paraensis | Rose-bellied Chat |
| Heliothraupis oneilli | Inti Tanager |
| Xenodacnis petersi | Streaked Dacnis |
| Saltator olivascens | Olive-grey Saltator |
| Saltator grandis | Cinnamon-bellied Saltator |
| Sporophila iberaensis | Ibera Seedeater |
| Melopyrrha grandis | St. Kitts Bullfinch |
| Melopyrrha taylori | Grand Cayman Bullfinch |
| Dubusia carrikeri | Carriker's Mountain Tanager |
| Dubusia stictocephala | Streak-crowned Mountain Tanager |
| Tangara brasiliensis | White-bellied Tanager |

## IOC species not found in AviList (138)

| IOC scientific name | English (IOC) | Russian (IOC) |
|---|---|---|
| Accipiter chionogaster | White-breasted Hawk | Белогрудый ястреб |
| Accipiter erythronemius | Rufous-thighed Hawk | Рыжебёдрый ястреб |
| Accipiter ventralis | Plain-breasted Hawk | Светлобрюхий ястреб |
| Aegithalos bonvaloti | Black-browed Bushtit | Чернобровый ополовник |
| Aerodramus ocistus | Marquesan Swiftlet | Маркизская салангана |
| Amblyornis germanus | Huon Bowerbird |  |
| Anas carolinensis | Green-winged Teal | Зеленокрылый чирок |
| Apalis flavocincta | Brown-tailed Apalis |  |
| Apus cooki | Cook's Swift | Индокитайский стриж |
| Apus leuconyx | Blyth's Swift | Гималайский стриж |
| Bubo nacurutu | Tropical Horned Owl |  |
| Bubo nigrescens | Paramo Horned Owl |  |
| Buteo bannermani | Cape Verde Buzzard | Кабовердский канюк |
| Camaroptera brevicaudata | Grey-backed Camaroptera | Короткохвостая терновница |
| Carpodacus lepidus | Chinese Long-tailed Rosefinch |  |
| Centropus spilopterus | Kai Coucal | Кайский кукаль |
| Charmosynoides margarethae | Duchess Lorikeet | Лорикет Маргариты |
| Chloris kittlitzi | Bonin Greenfinch |  |
| Cinnyris whytei | Whyte's Double-collared Sunbird | Малавийская нектарница |
| Cnemoscopus chrysogaster | Black-billed Cnemoscopus |  |
| Colaptes aeruginosus | Bronze-winged Woodpecker | Бронзовокрылый дятел |
| Corvus cornix | Hooded Crow | Серая ворона |
| Corvus culminatus | Indian Jungle Crow | Индийская ворона |
| Corvus levaillantii | Eastern Jungle Crow | Джунглевая ворона |
| Cyanoramphus hochstetteri | Reischek's Parakeet | Береговой какарики |
| Cyanoramphus subflavescens | Lord Howe Parakeet | Желтоватый какарики |
| Dacnis egregia | Yellow-tufted Dacnis | Желтоплечий дакнис |
| Diglossa melanopis | Whistling Masked Flowerpiercer |  |
| Elaenia cherrei | Hispaniolan Elaenia |  |
| Elaenia chilensis | Chilean Elaenia | Чилийская эления |
| Emblema modesta | Plum-headed Finch | Полосатая амадина |
| Eos bornea | Red Lory | Красный лори |
| Eos cyanogenia | Black-winged Lory | Чернокрылый лори |
| Eos histrio | Red-and-blue Lory | Сине-красный лори |
| Eos reticulata | Blue-streaked Lory | Пёстрый лори |
| Eos semilarvata | Blue-eared Lory | Синеухий лори |
| Eos squamata | Violet-necked Lory | Чешуйчатый лори |
| Erythrura regia | Royal Parrotfinch | Попугайная амадина |
| Euptilotus eutilotus | Puff-backed Bulbul | Серохохлый бюльбюль |
| Geothlypis chiriquensis | Chiriqui Yellowthroat | Панамская желтогрудка |
| Glaucidium californicum | Northern Pygmy Owl | Западный сычик |
| Glaucidium cobanense | Guatemalan Pygmy Owl | Гватемальский сычик |
| Glaucidium hoskinsii | Baja Pygmy Owl | Калифорнийский сычик |
| Glossopsitta concinna | Musk Lorikeet | Мускусный лорикет |
| Gracula robusta | Nias Hill Myna | Большая майна |
| Griseotyrannus aurantioatrocristatus | Crowned Slaty Flycatcher | Аргентинский тиранн |
| Himantopus melanurus | White-backed Stilt | Южноамериканский ходулочник |
| Ixodia cyaniventris | Grey-bellied Bulbul | Серобрюхий бюльбюль |
| Ixodia erythropthalmos | Spectacled Bulbul | Красноглазый бюльбюль |
| Ixodia squamata | Scaly-breasted Bulbul | Чешуйчатый бюльбюль |
| Kleinothraupis auricularis | White-browed Hemispingus | Белобровая пипира |
| Leptotila battyi | Azuero Dove | Панамская голубка |
| Manucodia alter | Tagula Manucode |  |
| Microptilotis albonotatus | Scrub Honeyeater | Кустарниковый медосос |
| Microptilotis analogus | Mimic Honeyeater | Медосос-пересмешник |
| Microptilotis cinereifrons | Elegant Honeyeater | Элегантный медосос |
| Microptilotis flavirictus | Yellow-gaped Honeyeater | Желтоусый медосос |
| Microptilotis gracilis | Graceful Honeyeater | Изящный медосос |
| Microptilotis imitatrix | Cryptic Honeyeater | Кэрнский медосос |
| Microptilotis mimikae | Mottle-breasted Honeyeater | Пестрогрудый медосос |
| Microptilotis montanus | Forest Honeyeater | Горный медосос |
| Microptilotis orientalis | Mountain Honeyeater | Тонкоклювый медосос |
| Microptilotis vicina | Tagula Honeyeater | Тагуланский медосос |
| Mionectes galbinus | Olive-striped Flycatcher |  |
| Muscicapa tyrrhenica | Mediterranean Flycatcher | Средиземноморская мухоловка |
| Myiarchus flavidior | Salvadoran Flycatcher |  |
| Myiothlypis roraimae | Roraiman Warbler | Рораймский певун |
| Myrmecocichla collaris | Ruaha Chat | Белоголовая термитница |
| Myrmotherula luctuosa | Silvery-flanked Antwren | Серобокий муравьелов |
| Nesillas longicaudata | Anjouan Brush Warbler | Анжуанский рогозник |
| Oreornis chrysogenys | Orange-cheeked Honeyeater | Золотощёкий медосос |
| Otus feae | Annobon Scops Owl |  |
| Otus madagascariensis | Torotoroka Scops Owl | Мадагаскарская совка |
| Oxyura ferruginea | Andean Duck | Андская савка |
| Pachycephala fuliginosa | Western Whistler |  |
| Pachycephala johni | Cinnamon-breasted Whistler | Коричневогрудый свистун |
| Pampa pampa | Wedge-tailed Sabrewing | Клинохвостый саблекрыл |
| Passerella megarhyncha | Thick-billed Fox Sparrow | Большеклювая овсянка |
| Passerella schistacea | Slate-colored Fox Sparrow | Тёмная овсянка |
| Passerella unalaschcensis | Sooty Fox Sparrow | Пестрогрудая овсянка |
| Patagona peruviana | Northern Giant Hummingbird |  |
| Pellorneum poliogene | Leaflitter Babbler |  |
| Pellorneum saturatum | Glissando Babbler |  |
| Pericrocotus speciosus | Scarlet Minivet | Огненный личинкоед |
| Phibalura boliviana | Palkachupa Cotinga | Боливийская ласточковая котинга |
| Phoeniculus castaneiceps | Forest Wood Hoopoe | Каштановоголовый древесный удод |
| Phyllastrephus alfredi | Sharpe's Greenbul | Малавийский бюльбюль |
| Phylloscopus floresianus | Flores Leaf Warbler |  |
| Picus dedemi | Sumatran Woodpecker |  |
| Pionus seniloides | White-capped Parrot | Седоголовый амазонет |
| Piranga hepatica | Hepatic Tanager | Солнечная пиранга |
| Piranga lutea | Tooth-billed Tanager | Горная пиранга |
| Polioptila attenboroughi | Inambari Gnatcatcher | Инамбарская комароловка |
| Polioptila facilis | Rio Negro Gnatcatcher | Рионегросская комароловка |
| Porphyrio indicus | Black-backed Swamphen | Черноспинная султанка |
| Porphyrio madagascariensis | African Swamphen | Африканская султанка |
| Porphyrio melanotus | Australasian Swamphen | Австралийская султанка |
| Porphyrio poliocephalus | Grey-headed Swamphen | Сероголовая султанка |
| Porphyrio pulverulentus | Philippine Swamphen | Филиппинская султанка |
| Pseudeos cardinalis | Cardinal Lory | Кардиналовый лори |
| Pseudeos fuscata | Dusky Lory | Тёмный лори |
| Pterodroma occulta | Vanuatu Petrel | Вануатский тайфунник |
| Puffinus mauretanicus | Balearic Shearwater | Балеарский буревестник |
| Ramosomyia wagneri | Cinnamon-sided Hummingbird | Рыжебокая амазилия |
| Ramphastos citreolaemus | Citron-throated Toucan | Лимонногорлый тукан |
| Rhipidura kordensis | Biak Fantail |  |
| Saudareos flavoviridis | Sula Lorikeet | Жёлто-зелёный лорикет |
| Saudareos iris | Iris Lorikeet | Синебровый лорикет |
| Saudareos johnstoniae | Mindanao Lorikeet | Джонстонов лорикет |
| Saudareos meyeri | Yellow-cheeked Lorikeet |  |
| Saudareos ornata | Ornate Lorikeet | Украшенный лорикет |
| Saxicola stejnegeri | Amur Stonechat | Восточный черноголовый чекан |
| Setophaga auduboni | Audubon's Warbler | Одюбонова древесница |
| Setophaga goldmani | Goldman's Warbler | Желтоспинная древесница |
| Stiphrornis xanthogaster | Yellow-breasted Forest Robin |  |
| Strix mauritanica | Maghreb Owl |  |
| Sturnia blythii | Malabar Starling | Малабарский скворец |
| Sugomel lombokium | Scaly-crowned Honeyeater | Ломбокский медолюб |
| Synorhacma multistriata | Striated Lorikeet | Полосатый лорикет |
| Tachyspiza haplochroa | White-bellied Goshawk | Белобрюхий ястреб |
| Taeniopygia castanotis | Australian Zebra Finch |  |
| Territornis albilineata | White-lined Honeyeater | Белоусый медосос |
| Territornis fordiana | Kimberley Honeyeater | Скальный медосос |
| Territornis reticulata | Streak-breasted Honeyeater | Тиморский медосос |
| Thalassarche impavida | Campbell Albatross | Желтоглазый альбатрос |
| Thalasseus acuflavidus | Cabot's Tern | Карибская крачка |
| Trachyphonus usambiro | Usambiro Barbet | Масайская чубатка |
| Treron permagnus | Ryukyu Green Pigeon |  |
| Tumbezia salvini | Tumbes Tyrant | Тумбезия |
| Turdus phaeopygus | Grey-flanked Thrush |  |
| Tyto manusi | Manus Masked Owl | Манусская сипуха |
| Tyto multipunctata | Lesser Sooty Owl | Пёстрая сипуха |
| Tyto sororcula | Moluccan Masked Owl | Молуккская сипуха |
| Vireo swainsoni | Western Warbling Vireo |  |
| Zosterops aldabrensis | Aldabra White-eye | Альдабранская белоглазка |
| Zosterops anjuanensis | Anjouan White-eye |  |
| Zosterops chrysolaemus | Black-fronted White-eye |  |
| Zosterops comorensis | Moheli White-eye |  |

## IOC and eBird Russian names differ (164)

Case-insensitive comparison of the raw names. `ru` always prefers IOC; the eBird name is kept in `ru_ebird` when it still differs from the final `ru` after normalisation (ё = е, spaces and hyphens ignored, part before a comma), unless suppressed with `field = ru_ebird`, value `-` in `data/overrides.csv` (column «подавлено»).

| Scientific name | IOC | eBird | ru_ebird | подавлено |
|---|---|---|---|---|
| Anser canagicus | Белошей | Гусь-белошей | Гусь-белошей |  |
| Anser fabalis | Гуменник (лесной гуменник) | Лесной гуменник | Лесной гуменник |  |
| Melanitta deglandi | Горбоносый турпан | Белокрылый турпан |  |  |
| Cyrtonyx montezumae | Плачущий перепел, перепел Монтесумы | Плачущий перепел |  |  |
| Catreus wallichii | Хохлатый фазан, чир | Хохлатый фазан |  |  |
| Coua cursor | Желтогорлая тивука, тивука-бегун | Желтогорлая тивука |  |  |
| Fulica newtonii | Маскаренская лысуха | Маврикийская лысуха | Маврикийская лысуха |  |
| Ardea coromanda | Коровья цапля | Восточная египетская цапля | Восточная египетская цапля |  |
| Hirundapus caudacutus | Колючехвост, колючехвостый стриж | Колючехвост |  |  |
| Cynanthus doubledayi | Мексиканский колибри | Мексиканский изумруд | Мексиканский изумруд |  |
| Sarcoramphus papa | Королевская катарта, королевский гриф | Королевская катарта |  |  |
| Cathartes aura | Катарта-индейка, гриф-индейка | Катарта-индейка |  |  |
| Buceros bicornis | Двурогий калао, гомрай | Двурогий калао |  |  |
| Campethera maculosa | Гвинейский дятел | Зеленоспинный дятел | Зеленоспинный дятел |  |
| Caracara plancus | Равнинная каракара, каранчо | Равнинная каракара |  |  |
| Strigops habroptilus | Какапо, совиный попугай | Какапо |  |  |
| Loriculus galgulus | Малайский лорикулюс, серендак | Малайский лорикулюс |  |  |
| Limnoctites rectirostris | Болотный прямоклюв | Прямоклюв | Прямоклюв |  |
| Limnoctites sulphuriferus | Желтобородый прямоклюв | Желтобородая курутия | Желтобородая курутия |  |
| Aethomyias nigrorufus | Рыжебрюхая кустовка | Чёрно-рыжая мышевидка | Чёрно-рыжая мышевидка |  |
| Oriolus oriolus | Иволга | Обыкновенная иволга | Обыкновенная иволга |  |
| Dicrurus hottentottus | Лирохвостый дронго | Индийский дронго | Индийский дронго |  |
| Dicrurus macrocercus | Чёрный дронго | Черный дронго |  |  |
| Terpsiphone atrocaudata | Чёрная райская мухоловка | Черная райская мухоловка |  |  |
| Lophorina superba | Большая лофорина | Арфакская лофорина | Арфакская лофорина |  |
| Platylophus galericulatus | Сорокопутовая сойка | Хохлатая малайская сойка | Хохлатая малайская сойка |  |
| Lanius meridionalis | Иберийский сорокопут | Пиренейский сорокопут | Пиренейский сорокопут |  |
| Lanius tigrinus | Тигровый жулан, тигровый сорокопут | Тигровый сорокопут | Тигровый сорокопут |  |
| Lanius isabellinus | Буланый жулан | Рыжехвостый жулан | Рыжехвостый жулан |  |
| Lanius collurio | Жулан | Обыкновенный жулан | Обыкновенный жулан |  |
| Lanius phoenicuroides | Туркестанский жулан, рыжехвостый жулан | Туркестанский жулан |  |  |
| Lanius schach | Длиннохвостый сорокопут, сорокопут-шах | Длиннохвостый сорокопут |  |  |
| Pyrrhocorax graculus | Альпийская галка, альпийская клушица | Альпийская галка |  |  |
| Podoces hendersoni | Монгольская пустынная сойка | Монгольская сойка | Монгольская сойка |  |
| Nucifraga caryocatactes | Кедровка, ореховка | Кедровка |  |  |
| Culicicapa ceylonensis | Сероголовый комаролов | Сероголовая комароловка | Сероголовая комароловка |  |
| Remiz pendulinus | Ремез | Обыкновенный ремез | Обыкновенный ремез |  |
| Cyanistes cyanus | Князёк, белая лазоревка | Белая лазоревка | Белая лазоревка |  |
| Periparus venustulus | Короткохвостая синица | Желтобрюхая синица | Желтобрюхая синица |  |
| Lophophanes cristatus | Хохлатая синица, гренадерка | Хохлатая синица |  |  |
| Panurus biarmicus | Усатка, усатая синица | Усатая синица | Усатая синица |  |
| Lullula arborea | Лесной жаворонок, юла | Лесной жаворонок |  |  |
| Galerida theklae | Короткохохлый жаворонок | Короткопалый хохлатый жаворонок | Короткопалый хохлатый жаворонок |  |
| Eremophila alpestris | Рогатый жаворонок, рюм | Рогатый жаворонок |  |  |
| Calandrella cinerea | Красноголовый жаворонок | Африканский малый жаворонок | Африканский малый жаворонок |  |
| Cisticola juncidis | Веерохвостая цистикола | Золотистая цистикола | Золотистая цистикола |  |
| Arundinax aedon | Толстоклювая камышовка | Толстоклювая камышевка |  |  |
| Iduna pallida | Бледная бормотушка | Бледная пересмешка | Бледная пересмешка |  |
| Acrocephalus schoenobaenus | камышовка-барсучок | Камышевка-барсучок |  |  |
| Acrocephalus bistrigiceps | Чернобровая камышовка | Пестроголовая камышевка | Пестроголовая камышовка |  |
| Acrocephalus sorghophilus | Просяная камышовка | Просяная камышевка |  |  |
| Acrocephalus paludicola | Вертлявая камышовка | Вертлявая камышевка |  |  |
| Acrocephalus melanopogon | Тонкоклювая камышовка | Тонкоклювая камышевка |  |  |
| Acrocephalus agricola | Индийская камышовка | Индийская камышевка |  |  |
| Acrocephalus tangorum | Маньчжурская камышовка | Маньчжурская камышевка |  |  |
| Acrocephalus dumetorum | Садовая камышовка | Садовая камышевка |  |  |
| Acrocephalus orinus | Большеклювая камышовка | Большеклювая камышевка |  |  |
| Acrocephalus palustris | Болотная камышовка | Болотная камышевка |  |  |
| Acrocephalus scirpaceus | Тростниковая камышовка | Тростниковая камышевка |  |  |
| Acrocephalus arundinaceus | Дроздовидная камышовка | Дроздовидная камышевка |  |  |
| Acrocephalus orientalis | Восточная камышовка | Восточная дроздовидная камышевка | Восточная дроздовидная камышовка |  |
| Acrocephalus stentoreus | Голосистая камышовка | Южная дроздовидная камышевка | Южная дроздовидная камышовка |  |
| Helopsaltes fasciolatus | Таёжный сверчок | Таежный сверчок |  |  |
| Progne subis | Пурпурная ласточка | Большая ласточка | Большая ласточка |  |
| Hirundo rustica | Деревенская ласточка, ласточка-касатка | Деревенская ласточка |  |  |
| Delichon urbicum | Воронок, городская ласточка | Воронок |  |  |
| Cecropis daurica | Рыжепоясничная ласточка | Восточная рыжепоясничная ласточка | Восточная рыжепоясничная ласточка |  |
| Petrochelidon pyrrhonota | Светлолобая ласточка | Белолобая ласточка | Белолобая ласточка |  |
| Leptopoecile elegans | Элегантная синичка | Хохлатая расписная синичка | Хохлатая расписная синичка |  |
| Horornis diphone | Бамбуковая широкохвостка | Бамбуковая камышевка | Бамбуковая камышовка |  |
| Horornis canturians | Короткокрылая широкохвостка | Короткокрылая камышевка | Короткокрылая камышовка |  |
| Phylloscopus humei | Тусклая зарничка | Тусклая пеночка | Тусклая пеночка |  |
| Phylloscopus subviridis | Кашмирская зарничка | Пеночка гималайская | Пеночка гималайская |  |
| Phylloscopus proregulus | Корольковая пеночка, корольковая зарничка | Корольковая пеночка |  |  |
| Phylloscopus schwarzi | Толстоклювая пеночка, голосистая пеночка | Толстоклювая пеночка |  |  |
| Phylloscopus armandii | Субальпийская пеночка | Пеночка Арманда | Пеночка Арманда |  |
| Phylloscopus reguloides | Рододендровая пеночка | Корольковидная пеночка | Корольковидная пеночка |  |
| Phylloscopus poliocephalus | Папуанская пеночка | Нумфорская пеночка | Нумфорская пеночка |  |
| Pycnonotus leucogenys | Белощёкий бюльбюль | Белощекий бюль-бюль |  |  |
| Hypsipetes amaurotis | Рыжеухий бюльбюль | Короткопалый бюль-бюль | Короткопалый бюль-бюль |  |
| Hypsipetes leucocephalus | Белоголовый бюльбюль | Черный бюль-бюль | Черный бюль-бюль |  |
| Sylvia atricapilla | Славка-черноголовка | Черноголовая славка | Черноголовая славка |  |
| Curruca curruca | Славка-мельничек | Славка-завирушка | Славка-завирушка |  |
| Curruca hortensis | Славка-орфей | Певчая славка | Певчая славка |  |
| Curruca crassirostris | Певчая славка | Восточноорфейская славка | Восточноорфейская славка |  |
| Trochalopteron lineatum | Полосатая кустарница | Полосатая тимелия | Полосатая тимелия |  |
| Argya squamiceps | Аравийская дроздовка | Ававийская дроздовка |  | yes |
| Garrulax canorus | Очковая кустарница, хуамей | Очковая кустарница |  |  |
| Bombycilla japonica | Амурский свиристель | Японский свиристель | Японский свиристель |  |
| Hypocolius ampelinus | Сорокопутовый свиристель | Свиристелевый сорокопут | Свиристелевый сорокопут |  |
| Corthylio calendula | Рубиновоголовый королёк | Рубиноголовый королёк | Рубиноголовый королёк |  |
| Tichodroma muraria | Краснокрылый стенолаз | Стенолаз | Стенолаз |  |
| Sitta krueperi | Рыжегрудый поползень | Черноголовый поползень | Черноголовый поползень |  |
| Sitta europaea | Поползень | Обыкновенный поползень | Обыкновенный поползень |  |
| Certhia hodgsoni | Кашмирская пищуха | Кашмирская пищуху |  | yes |
| Certhia familiaris | Пищуха | Обыкновенная пищуха | Обыкновенная пищуха |  |
| Mimus polyglottos | Многоголосый пересмешинк | Многоголосый пересмешник |  |  |
| Sturnus vulgaris | Скворец | Обыкновенный скворец | Обыкновенный скворец |  |
| Agropsar philippensis | Красноухий скворец | Японский скворец | Японский скворец |  |
| Spodiopsar sericeus | Шелковистый скворец | Красноклювый скворец | Красноклювый скворец |  |
| Catharus ustulatus | Свэнсонов дрозд | Дрозд Свэнсона | Дрозд Свэнсона |  |
| Turdus naumanni | Рыжий дрозд | Дрозд Науманна | Дрозд Науманна |  |
| Luscinia luscinia | Восточный соловей | Обыкновенный соловей | Обыкновенный соловей |  |
| Ficedula zanthopygia | Желтоспинная мухоловка | Даурская желтоспинная мухоловка | Даурская желтоспинная мухоловка |  |
| Ficedula narcissina | Японская мухоловка | Японская желтоспинная мухоловка | Японская желтоспинная мухоловка |  |
| Ficedula mugimaki | Таёжная мухоловка | Таежная мухоловка |  |  |
| Ficedula albicilla | Восточная мухоловка | Восточная малая мухоловка | Восточная малая мухоловка |  |
| Phoenicurus ochruros | Горихвостка-чернушка | Черная горихвостка | Черная горихвостка |  |
| Phoenicurus phoenicurus | Горихвостка-лысушка | Обыкновенная горихвостка | Обыкновенная горихвостка |  |
| Monticola gularis | Белогорлый каменный дрозд | Белогорлый дрозд | Белогорлый дрозд |  |
| Saxicola caprata | Чёрный чекан | Черный чекан |  |  |
| Saxicola maurus | Азиатский черноголовый чекан | Сибирский черноголовый чекан | Сибирский черноголовый чекан |  |
| Saxicola rubicola | Западный черноголовый чекан | Черноголовый чекан | Черноголовый чекан |  |
| Oenanthe oenanthe | Каменка | Обыкновенная каменка | Обыкновенная каменка |  |
| Oenanthe picata | Чёрная каменка | Черная каменка |  |  |
| Oenanthe lugens | Траурная каменка | Черноспинная каменка | Черноспинная каменка |  |
| Oenanthe xanthoprymna | Курдская каменка | Курдистанская каменка | Курдистанская каменка |  |
| Leptocoma sperata | Пурпурногорлая нектарница | Пурпурногорлая нектраница |  | yes |
| Nectarinia bocagii | Сверкающая нектарница | Сверкающая нектраница |  | yes |
| Cinnyris manoensis | Миомбская нектарница | Миомбская нектраница |  | yes |
| Cinnyris reichenowi | Желтоплечая нектарница | Желтоплечая нектраница |  | yes |
| Cinnyris afer | Серобрюхая нектарница | Серобрюхая нектраница |  | yes |
| Cinnyris osea | Палестинская нектарница | Палестинская некатарница |  | yes |
| Lonchura flaviprymna | Желтопоясничная муния | Жёлтопоясничная муния |  |  |
| Prunella ocularis | Пёстрая завирушка | Йеменская завирушка | Йеменская завирушка |  |
| Prunella koslowi | Монгольская завирушка | Завирушка Козлова | Завирушка Козлова |  |
| Montifringilla nivalis | Снежный воробей | Снежный вьюрок | Снежный вьюрок |  |
| Passer zarudnyi | Пустынный воробей | Воробей пустынный | Воробей пустынный |  |
| Anthus godlewskii | Конёк Годлевского | Забайкальский конёк | Забайкальский конёк |  |
| Anthus rufulus | Рисовый конёк | Рисовой конёк |  | yes |
| Anthus rubescens | Гольцовый конёк | Американский конёк | Американский конёк |  |
| Fringilla montifringilla | Юрок | Вьюрок | Вьюрок |  |
| Mycerobas affinis | Ошейниковый дубонос | Ошейниковый горный дубонос | Ошейниковый горный дубонос |  |
| Mycerobas melanozanthos | Пестрокрылый дубонос | Пестрокрылый горный дубонос | Пестрокрылый горный дубонос |  |
| Mycerobas carnipes | Арчовый дубонос | Арчевый горный дубонос | Арчевый горный дубонос |  |
| Coccothraustes coccothraustes | Дубонос | Обыкновенный дубонос | Обыкновенный дубонос |  |
| Carpodacus erythrinus | Чечевица | Обыкновенная чечевица | Обыкновенная чечевица |  |
| Carpodacus puniceus | Красная чечевица, красный вьюрок | Красный вьюрок | Красный вьюрок |  |
| Bucanetes mongolicus | Монгольский вьюрок | Монгольский пустынный вьюрок | Монгольский пустынный вьюрок |  |
| Bucanetes githagineus | Пустынный вьюрок | Толстоклювый пустынный вьюрок | Толстоклювый пустынный вьюрок |  |
| Leucosticte arctoa | Сибирский горный вьюрок | Сибирский вьюрок | Сибирский вьюрок |  |
| Leucosticte tephrocotis | Американский горный вьюрок | Американский вьюрок | Американский вьюрок |  |
| Chloris chloris | Зеленушка | Обыкновенная зеленушка | Обыкновенная зеленушка |  |
| Linaria flavirostris | Горная коноплянка | Горная чечётка | Горная чечётка |  |
| Serinus serinus | Канареечный вьюрок, европейский вьюрок | Европейский вьюрок | Европейский вьюрок |  |
| Plectrophenax hyperboreus | Островная пуночка | Белая пуночка | Белая пуночка |  |
| Emberiza schoeniclus | Камышовая овсянка, стренатка | Тростниковая овсянка | Тростниковая овсянка |  |
| Emberiza tristrami | Таёжная овсянка | Таежная овсянка |  |  |
| Emberiza sulphurata | Японская овсянка | Японская желтая овсянка | Японская желтая овсянка |  |
| Emberiza buchanani | Скальная овсянка | Скалистая овсянка | Скалистая овсянка |  |
| Emberiza caesia | Красноклювая овсянка | Овсянка Крешмара | Овсянка Крешмара |  |
| Emberiza citrinella | Овсянка, обыкновенная овсянка | Обыкновенная овсянка | Обыкновенная овсянка |  |
| Spizella passerina | Воробьиная овсянка | Малая воробьиная овсянка | Малая воробьиная овсянка |  |
| Arremon phygas | Париайский тохи | Париайский дромник | Париайский дромник |  |
| Spizelloides arborea | Древесная овсянка | Воробьиная овсянка | Воробьиная овсянка |  |
| Passerella iliaca | Лисья овсянка | Пестрогрудая овсянка | Пестрогрудая овсянка |  |
| Junco hyemalis | Темноглазый юнко | Серый юнко | Серый юнко |  |
| Zonotrichia atricapilla | Чернобровая зонотрихия | Чернобровая овсянка | Чернобровая овсянка |  |
| Zonotrichia leucophrys | Белобровая зонотрихия | Белобровая овсянка | Белобровая овсянка |  |
| Melospiza georgiana | Болотная овсянка | Болотная зонотрихия | Болотная зонотрихия |  |
| Atlapetes personatus | Капюшоновая атлапета | Капюшоновая ая атлапета |  | yes |
| Spindalis dominicensis | Гаитянская зена | Каитянская зена |  | yes |
| Sturnella neglecta | Жаворонковый луговой трупиал | Западный луговой трупиал | Западный луговой трупиал |  |
| Setophaga coronata | Миртовая древесница | Миртовый певун | Миртовый певун |  |

## Former scientific names (`sci_prev`): 5146 species

Former combinations from `data/raw/IOC_15.2_vs_other_lists.xlsx` (IOC 15.2, IOC 15.1, Clements 2025, BirdLife v10, H&M 4.1, HBW, Peters, S&M 1993; rows joined on the AviList column) and historical eBird taxonomies (`ebirdYYYY`, joined on the species code), plus `field = sci_prev` overrides. AviList protonyms are not included. `sci_book_prev` is the first name of kind genus / genus_ending / epithet (the list is sorted by the most recent source, then by name). eBird versions are read from the public API without a key; there is no 2020 version.

- eBird 2024: `data/cache/ebird-taxonomy-2024.json`, 11145 species, 11090 AviList species joined
- eBird 2023: `data/cache/ebird-taxonomy-2023.json`, 11017 species, 10949 AviList species joined
- eBird 2022: `data/cache/ebird-taxonomy-2022.json`, 10906 species, 10826 AviList species joined
- eBird 2021: `data/cache/ebird-taxonomy-2021.json`, 10824 species, 10704 AviList species joined
- eBird 2019: `data/cache/ebird-taxonomy-2019.json`, 10721 species, 10597 AviList species joined
- eBird 2018: `data/cache/ebird-taxonomy-2018.json`, 10585 species, 10455 AviList species joined
- eBird 2017: `data/cache/ebird-taxonomy-2017.json`, 10550 species, 10414 AviList species joined
- eBird 2016: `data/cache/ebird-taxonomy-2016.json`, 10514 species, 10366 AviList species joined
- eBird 2015: `data/cache/ebird-taxonomy-2015.json`, 10473 species, 10319 AviList species joined
- current names of another species -> concept: 25
- eBird names of another species kept under a reused code -> concept: 8
- ebird2015: code not found, joined by the newer name: 364
- ebird2016: code not found, joined by the newer name: 352
- ebird2017: code not found, joined by the newer name: 342
- ebird2018: code not found, joined by the newer name: 319
- ebird2019: code not found, joined by the newer name: 249
- ebird2021: code not found, joined by the newer name: 223
- ebird2022: code not found, joined by the newer name: 158
- ebird2023: code not found, joined by the newer name: 102
- ebird2024: code not found, joined by the newer name: 51
- linked directly: 11131
- linked through subspecies: 1280
- names that are a concept in one source, a synonym in another -> concept: 5
- unlinked species rows: 107

### By kind

| kind | species | names |
|---|---|---|
| genus | 2662 | 3027 |
| genus_ending | 546 | 582 |
| epithet | 136 | 145 |
| spelling | 531 | 553 |
| concept | 2025 | 2563 |

### By source

| source | species | names |
|---|---|---|
| ioc15.2 | 117 | 137 |
| ioc15.1 | 241 | 276 |
| clements2025 | 39 | 50 |
| birdlife10 | 931 | 1001 |
| ebird2024 | 53 | 53 |
| ebird2023 | 279 | 279 |
| ebird2022 | 452 | 452 |
| ebird2021 | 524 | 524 |
| ebird2019 | 783 | 783 |
| ebird2018 | 862 | 862 |
| ebird2017 | 932 | 932 |
| ebird2016 | 1046 | 1046 |
| ebird2015 | 1137 | 1137 |
| hm4 | 1594 | 1605 |
| hbw | 2813 | 2862 |
| sm93 | 2623 | 2683 |
| peters | 4107 | 4181 |

Species with `sci_book_prev`: 3160.

### Examples (30)

| Scientific name | sci_book_prev | sci_prev |
|---|---|---|
| Sibirionetta formosa | Anas formosa | Anas formosa (genus: ebird2016, ebird2015, hbw, sm93, peters) |
| Spinus spinus | Carduelis spinus | Carduelis spinus (genus: hbw, sm93, peters) |
| Calidris pugnax | Philomachus pugnax | Philomachus pugnax (genus: hbw, sm93, peters) |
| Astur gentilis | Accipiter gentilis | Accipiter gentilis (genus: birdlife10, ebird2023, ebird2022, ebird2021, ebird2019, ebird2018, ebird2017, ebird2016, ebird2015, hm4, hbw, sm93, peters) |
| Corvus corone |  | Corvus cornix (concept: ioc15.2, ioc15.1, clements2025, hbw) |
| Apteryx maxima | Apteryx haastii | Apteryx haastii (epithet: birdlife10, ebird2023, ebird2022, ebird2021, ebird2019, ebird2018, ebird2017, ebird2016, ebird2015, hm4, hbw, sm93, peters) |
| Bubo scandiacus | Nyctea scandiaca | Nyctea scandiaca (genus_ending: hbw, sm93, peters) |
| Setophaga petechia | Dendroica petechia | Dendroica petechia (genus: hbw, sm93, peters) |
| Phaenicophaeus sumatranus | Rhopodytes sumatranus | Rhopodytes sumatranus (genus: peters) |
| Grus virgo | Anthropoides virgo | Anthropoides virgo (genus: birdlife10, ebird2024, ebird2023, ebird2022, ebird2021, ebird2019, ebird2018, ebird2017, ebird2016, ebird2015, hbw, peters) |
| Gallinago jamesoni | Chubbia jamesoni | Chubbia jamesoni (genus: peters) |
| Microcarbo melanoleucos | Phalacrocorax melanoleucos | Phalacrocorax melanoleucos (genus: ebird2015, hbw, sm93, peters) |
| Heliodoxa rubricauda | Clytolaema rubricauda | Clytolaema rubricauda (genus: birdlife10, ebird2021, ebird2019, ebird2018, ebird2017, ebird2016, ebird2015, hm4, hbw, sm93, peters) |
| Strix woodfordii | Ciccaba woodfordii | Ciccaba woodfordii (genus: peters) |
| Merops hirundineus | Dicrocercus hirundineus | Dicrocercus hirundineus (genus: peters) |
| Dryobates cathpharius | Dendrocopos cathpharius | Dendrocopos cathpharius (genus: hm4, hbw, sm93, peters) |
| Glossoptilus goldiei | Psitteuteles goldiei | Psitteuteles goldiei (genus: birdlife10, ebird2019, ebird2018, ebird2017, ebird2016, ebird2015, hm4, hbw, sm93, peters); Glossoptila goldiei (spelling: ebird2021) |
| Thamnophilus bernardi | Sakesphorus bernardi | Sakesphorus bernardi (genus: hbw, sm93, peters) |
| Trichodere cockerelli | Lichmera cockerelli | Lichmera cockerelli (genus: peters) |
| Carterornis chrysomela | Monarcha chrysomela | Monarcha chrysomela (genus: hbw, sm93, peters) |
| Alaudala raytal | Calandrella raytal | Calandrella raytal (genus: ebird2015, hbw, sm93, peters) |
| Phylloscopus olivaceus | Seicercus olivaceus | Seicercus olivaceus (genus: hm4) |
| Fulvetta ludlowi | Alcippe ludlowi | Alcippe ludlowi (genus: ebird2018, ebird2017, ebird2016, ebird2015, sm93); Alcippe cinereiceps ludlowi (concept: peters) |
| Heterophasia gracilis | Malacias gracilis | Malacias gracilis (genus: hbw) |
| Cichlopsis leucogenys | Myadestes leucogenys | Cichlopsis chubbi (concept: birdlife10); Cichlopsis gularis (concept: birdlife10); Cichlopsis peruviana (concept: birdlife10); Myadestes leucogenys (genus: peters) |
| Larvivora akahige | Luscinia akahige | Luscinia akahige (genus: hbw); Erithacus akahige (genus: sm93, peters) |
| Spermestes cucullata | Lonchura cucullata | Lonchura cucullata (genus: sm93, peters) |
| Spinus cucullatus | Carduelis cucullata | Carduelis cucullata (genus_ending: hbw, sm93, peters) |
| Setophaga virens | Dendroica virens | Dendroica virens (genus: hbw, sm93, peters) |
| Stilpnia cyanoptera | Tangara argentea | Tangara argentea (epithet: birdlife10, hm4); Tangara cyanoptera (genus: hbw, sm93, peters) |

### Rows of the comparison file not joined to AviList (107)

Species rows with no AviList name of their own and no AviList subspecies under them (hybrids, doubtful and extinct forms, lumps noted only in the Notes column). Join by hand with `field = sci_prev` if needed.

| IOC 15.2 seq. | names | why | notes (shortened) |
|---|---|---|---|
| 360 | clements2025: Chenonetta finschi; birdlife10: Chenonetta finschi | no AviList species |  |
| 464 | tif: Anas chathamica | no AviList species | John H. Boyd III: The extinct Chatham Duck, usually placed in its own genus Pachyanas, actually belongs with the brown … |
| 672 | peters: Ortalis spixi | no AviList species | H&M4: superciliaris includes Ortalis spixi |
| 1373 | sm93: Lophura hatinhensis | no AviList species | H&M4: Lophura edwardsi includes L. hatinhensis |
| 1406 | hbw: Lophura imperialis; peters: Hierophasis imperialis; sm93: Lophura imperialis | no AviList species | H&M4: Lophura imperialis is considered a hybrid |
| 2094 | peters: Caprimulgus ludovicianus | no AviList species | H&M4: inornatus includes vinaceabrunneus, ludovicianus and malbranti |
| 2219 | birdlife10: Aegotheles archboldi; hm4: Aegotheles archboldi; hbw: Aegotheles archboldi; sm93: Aegotheles archboldi; tif: Aegotheles archboldi | no AviList species | IOC7.2: Treat Mountain Owlet-nightjar as monotypic including Archbold's Owlet-nightjar A. archboldi and Salvadori's Owl… |
| 2223 | hm4: Aegotheles salvadorii; tif: Aegotheles salvadorii | no AviList species |  |
| 2226 | tif: Aegotheles novaezealandiae | no AviList species |  |
| 2482 | peters: Hirund-apus ernsti | no AviList species | H&M4: cochinchinensis includes ernsti, formosana and rupchandi |
| 2651 | peters: Apus toulsoni; sm93: Apus toulsoni | no AviList species | H&M4: Apus horus: The name toulsoni may refer to a local colour morph. |
| 2711 | gaudin: Pygmornis maranhaoensis | no AviList species |  |
| 2873 | peters: Heliangelus squamigularis | no AviList species | HBW: Heliangelus strophianus: Other forms known mainly or exclusively from Bogotá trade skins include “H. squamigularis… |
| 2874 | peters: Heliangelus speciosa | no AviList species | HBW: Heliangelus strophianus: Other forms known mainly or exclusively from Bogotá trade skins include “H. squamigularis… |
| 2875 | peters: Heliangelus rothschildi | no AviList species | HBW: Heliangelus strophianus: Other forms known mainly or exclusively from Bogotá trade skins include “H. squamigularis… |
| 2876 | peters: Heliangelus luminosus | no AviList species | HBW: Heliangelus strophianus: Other forms known mainly or exclusively from Bogotá trade skins include “H. squamigularis… |
| 2883 | hbw: Heliangelus splendidus | no AviList species | H&M4: viola includes pyropus and splendidus |
| 2886 | hm4: Heliangelus zusii; hbw: Heliangelus zusii | no AviList species | IOC7.3: Hybrid Long-tailed Sylph Aglaiocercus kingii X ??? Pérez-Emán et al. 2017; see also Kirchman et al. 2010 |
| 2910 | peters: Lithiophanes insignibarbis | no AviList species | HBW: “L. insignibarbis”, known from a single Bogotá trade skin and sometimes awarded monospecific genus Lithiophanes, m… |
| 2934 | peters: Neolesbia nehrkorni | no AviList species | HBW: “Neolesbia nehrkorni” is known from only two specimens and appears to be a hybrid of present species [Aglaiocercus… |
| 3056 | peters: Eriocnemis söderströmi | no AviList species | H&M4: Eriocnemis nigrivestis: "Eriocnemis soderstromi" is considered a hybrid between this and E. luciani |
| 3075 | peters: Eriocnemis isaacsonii | no AviList species | H&M4: "Eriocnemis isaacsonii" is now treated as a hybrid |
| 3282 | peters: Acestrura decorata | no AviList species | H&M4: "Chaetocercus decorata" is a hybrid between C. mulsant and C. heliodor |
| 3290 | peters: Acestrura harterti | no AviList species | H&M4: "Chaetocercus harterti" is now considered a hybrid |
| 3345 | birdlife10: Riccordia elegans; hm4: Chlorostilbon elegans; tif: Cynanthus elegans | no AviList species | IOC13.1: The extinct Gould's Emerald Riccordia elegans, formerly included in this genus, is known solely from the uniqu… |
| 3393 | peters: Ptochoptera iolaima | no AviList species | HBW: Chlorostilbon poortmani: “Ptochoptera iolaima”, known from a specimen taken at Ypanema, São Paulo (Brazil), is pro… |
| 3395 | peters: Chlorostilbon inexpectatus | no AviList species | H&M4: Chlorostilbon poortmani includes C. inexpectatus |
| 3577 | birdlife10: Amazilia alfaroana; gaudin: Saucerottia alfaroana | no AviList species |  |
| 3604 | gaudin: Amazilia saturata | no AviList species |  |
| 3693 | peters: Amazilia cyaneotincta | no AviList species | H&M4: "Amazilia cyaneotincta" is probably an aberrant A. fimbriata or A. amabilis |
| 4507 | clements2025: Columba thiriouxi; birdlife10: Columba thiriouxi | no AviList species |  |
| 4585 | peters: Columba chiriquensis | no AviList species | H&M4: nigrirostris includes chiriquensis |
| 4596 | clements2025: Nesoenas cicur; birdlife10: Nesoenas cicur; hm4: Streptopelia cicur | no AviList species |  |
| 5465 | clements2025: Alectroenas payandeei; birdlife10: Alectroenas payandeei | no AviList species |  |
| 5588 | peters: Ducula melanura | no AviList species |  |
| 5592 | sm93: Ducula constans | no AviList species | H&M4: spilorrhoa includes constans |
| 5870 | peters: Tricholimnas conditicius; sm93: Gallirallus conditicius | no AviList species | H&M4: sylvestris includes conditicius |
| 5887 | clements2025: Tribonyx hodgenorum; birdlife10: Tribonyx hodgenorum | no AviList species |  |
| 5935 | hm4: Fulica caribaea; hbw: Fulica caribaea; peters: Fulica caribaea; sm93: Fulica caribaea | no AviList species | IOC6.3: Caribbean Coot is a white shield color morph of American Coot (HBW Alive, Donegan et al. 2015, NACC 2016-A-9) |
| 5978 | clements2025: Porphyrio kukwiedei; birdlife10: Porphyrio kukwiedei | no AviList species | Extinct |
| 5979 | clements2025: Porphyrio caerulescens; birdlife10: Porphyrio caerulescens; gaudin: Porphyrio coerulescens | no AviList species | Extinct. Original spelling is Apterornis cœrulescens. |
| 6072 | peters: Pennula millsi | no AviList species | H&M4: Zapornia sandwichensis: Pennula millsi is a synonym |
| 7433 | tif: Thalobata cryptoleucura | no AviList species | John H. Boyd III: I treat the Pacific populations of band-rumped storm-petrels as a single species, T. cryptoleucura, i… |
| 7668 | gaudin: Fregata rothschildi | no AviList species |  |
| 8565 | tif: Accipiter fringilloides; gaudin: Accipiter fringilloides | no AviList species |  |
| 9686 | gaudin: Megascops stangiae | no AviList species |  |
| 9687 | gaudin: Megascops alagoensis | no AviList species |  |
| 9688 | gaudin: Megascops ater | no AviList species |  |
| 9867 | gaudin: Heterotrogon camerunense | no AviList species |  |
| 10541 | hm4: Todiramphus miyakoensis; peters: Halcyon miyakoensis | no AviList species | TOC12.1: Delete subspecies miyakoensis. Treat [cinnamominus] as monotypic. Includes previously accepted, extinct race m… |
| 10684 | peters: Ceyx goodfellowi | no AviList species | H&M4: margarethae includes goodfellowi and virgicapitus |
| 11012 | gaudin: Bucco dugandi | no AviList species |  |
| 11208 | peters: Pteroglossus mariae; sm93: Pteroglossus mariae | no AviList species |  |
| 11369 | peters: Megalaima robustirostris | no AviList species | HBW: Form described from Assam as “robustirostris” long considered a separate species, but apparently matched by specim… |
| 11500 | tif: Pogoniulus makawai | no AviList species | IOC13.2: P. makawai, known only from the unique type specimen, was previously treated as a species based on its distinc… |
| 11734 | peters: Picumnus guttifer | no AviList species |  |
| 11804 | peters: Melanerpes rubrifrons | no AviList species | H&M4: cruentatus includes extensus and rubrifrons |
| 13161 | peters: Touit emmae | no AviList species | H&M4: T. emmae was described from the female of Touit stictopterus |
| 13310 | clements2025: Amazona martinicana; birdlife10: Amazona martinicana | no AviList species | Extinct |
| 13311 | clements2025: Amazona violacea; birdlife10: Amazona violacea | no AviList species | Extinct |
| 13525 | peters: Ara caninde | no AviList species | H&M4: Ara ararauna includes some aberrant birds named caninde. |
| 13532 | sm93: Ara cubensis | no AviList species | H&M4: tricolor includes cubensis |
| 13590 | clements2025: Psittacara labati; birdlife10: Psittacara labati | no AviList species | Extinct |
| 13763 | hbw: Psittacula intermedia; peters: Psittacula intermedia; sm93: Psittacula intermedia | no AviList species | H&M4: The name intermedia has been shown to relate to hybrids. / Penhallurick: Rasmussen & Collar, 1999, Bulletin of th… |
| 14001 | peters: Domicella tibialis | no AviList species | H&M4: L. tibialis might have been applied to aberrant specimens of L. domicella |
| 15118 | peters: Syndactyla mirandae | no AviList species | H&M4: Syndactyla mirandae was shown to be a synonym of S. dimidiata / HBW: The taxon S. mirandae, described from C Braz… |
| 15119 | peters: Philydor baeri | no AviList species |  |
| 15601 | peters: Synallaxis poliophrys | no AviList species | H&M4: Includes S. poliophrys / HBW: Proposed taxon S. poliophrys was based on a misidentified specimen of present speci… |
| 15927 | tif: Herpsilochmus scapularis | no AviList species |  |
| 16189 | sm93: Phlegopsis barringeri | no AviList species | H&M4: Phlegopsis barringeri is considered a hybrid between P. erythroptera and P. nigromaculata / HBW: Phlegopsis nigro… |
| 16281 | gaudin: Cercomacroides hypomelaena | no AviList species |  |
| 16359 | peters: Sipia rosenbergi | no AviList species | H&M4: Sipia rosenbergi is a synonym of this species [Sipia nigricauda] / HBW: Myrmeciza nigricauda: Forms a superspecie… |
| 16753 | hm4: Scytalopus notorius; gaudin: Scytalopus notorius | no AviList species | H&M4: For arguments that this is a synonym of S. speluncae, see Maurício (2005, 2010); but see also Raposo et al. (2012) |
| 16912 | peters: Serpophaga araguayae | no AviList species | H&M4: [caniceps] includes Serpophaga araguayae / HBW: Described taxon Serpophaga araguayae, based on a single specimen … |
| 17005 | gaudin: Camptostoma thyellophilum | no AviList species |  |
| 17277 | tif: Leptopogon transandinus | no AviList species |  |
| 17447 | peters: Poecilotriccus tricolor | no AviList species | H&M4: P. tricolor is a synonym [of P. capitalis] / HBW: Described taxon P. tricolor, from SW Brazil (Rondônia), has rec… |
| 18539 | gaudin: Schiffornis intercedens | no AviList species |  |
| 18546 | gaudin: Schiffornis cracrafti | no AviList species |  |
| 20255 | gaudin: Laniarius somaliensis | no AviList species |  |
| 21088 | tif: Pachycephala arthuri; gaudin: Pachycephala arthuri | no AviList species |  |
| 21153 | gaudin: Pachycephala efatensis | no AviList species |  |
| 21733 | gaudin: Oriolus alleni | no AviList species |  |
| 22440 | gaudin: Arses lauterbachi | no AviList species |  |
| 23162 | gaudin: Melampitta rostrata | no AviList species |  |
| 23164 | gaudin: Melampitta longicauda | no AviList species |  |
| 24128 | hbw: Heteromirafra sidamoensis; sm93: Heteromirafra sidamoensis | no AviList species | H&M4: For treatment [sidamoensis] as a subspecies of H. archeri, see Spottiswoode et al. (2013). |
| 24134 | peters: Mirafra candida | no AviList species | H&M4: pulpa includes candida / HBW: Birds from R Nyiro, in NE Kenya, described as species “M. candida”, but type specim… |
| 24620 | sm93: Andropadus hallae | no AviList species | H&M4: zombensis includes marwitzi and hallae / HBW: Described taxon A. hallae, known only from the single type specimen… |
| 24653 | hm4: Phyllastrephus leucolepis; hbw: Phyllastrephus leucolepis; sm93: Phyllastrephus leucolepis; tif: Phyllastrephus leucolepis | no AviList species | IOC8.1: Enigmatic Liberian Greenbul [Phyllastrephus leucolepis] is deemed a plumage variant of Icterine Greenbul P. ict… |
| 25082 | peters: Psalidoprocne petiti; sm93: Psalidoprocne petiti; gaudin: Psalidoprocne petiti | no AviList species |  |
| 26798 | ioc15.2: Apalis flavocincta; ioc15.1: Apalis flavocincta; birdlife10: Apalis flavocincta; gaudin: Apalis flavocincta | no AviList species |  |
| 27154 | hm4: Curruca inornata; tif: Melizophilus inornatus | no AviList species | IOC10.2: Western Subalpine Warbler is split from (Eastern) Subalpine Warbler C. cantillans following Zuccon et al. (202… |
| 27685 | hm4: Zosterops rendovae; peters: Zosterops rendovae; gaudin: Zosterops rendovae | no AviList species |  |
| 27853 | peters: Stachyris rodolphei; sm93: Stachyris rodolphei | no AviList species | H&M4: [rufifrons] considered to include rodolphei, IOC10.1: Variant of Rufous-fronted Babbler with no known population … |
| 30293 | gaudin: Catharus berlepschi | no AviList species |  |
| 30295 | gaudin: Catharus arcanus | no AviList species |  |
| 30690 | clements2025: Aplonis ulietensis; birdlife10: Aplonis ulietensis; hbw: Turdus ulietensis; gaudin: Aplonis ulietensis | no AviList species | HBW: This is another of those species known today only from a painting by Georg Forster. This painting, now in the Fors… |
| 32341 | peters: Anthreptes pujoli | no AviList species | H&M4: rectirostris includes pujoli / HBW: description of pujoli (from Guinea) is based on a juvenile specimen of nomina… |
| 33076 | sm93: Ploceus victoriae | no AviList species | H&M4: We have not listed P. victoriae Ash, 1986. It remains best considered a species inquirenda / HBW: Ploceus castano… |
| 33233 | peters: Foudia bruante | no AviList species | Wikipedia: A type of fody on Réunion was previously mentioned as Foudia bruante by Philipp Ludwig Statius Müller in the… |
| 33244 | clements2025: Foudia delloni; birdlife10: Foudia delloni | no AviList species |  |
| 34514 | peters: Neospiza concolor | no AviList species | Neospiza concolor is listed twice in Peters et al. checklist |
| 35084 | peters: Chlorospingus zeledoni | no AviList species | H&M4: C. zeledoni is considered to be a colour morph [of C. pileatus] / HBW: The form “zeledoni”, originally described … |
| 36130 | peters: Icterus xantholemus | no AviList species | H&M4: [Xanthopsar flavus] includes Icterus xantholemus / HBW: Form Icterus xantholemus, based on a single speciment fro… |
| 37294 | peters: Sporophila insulata; sm93: Sporophila insulata | no AviList species | H&M4: [S. telasco] includes S. insulata / HBW: Taxonomic status of “S. insulata” (known only from Tumaco I, off Nariño,… |
| 37314 | sm93: Sporophila zelichi | no AviList species | H&M4: [S. palustris] includes S. zelichi / HBW: form described as S. zelichi (from Entre Ríos, in NE Argentina) conside… |
