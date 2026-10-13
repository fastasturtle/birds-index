# Build report

## Sources

- **AviList v2025b**: `data/raw/AviList-v2025b-extended.xlsx`
- **IOC Multilingual 15.2**: `data/raw/IOC-Multiling-15.2.xlsx`
- **eBird taxonomy (ru)**: `data/cache/ebird-taxonomy-ru.json`, 10366 species with Cyrillic names
- **Wikidata P1843 (ru)**: `data/cache/wikidata-ru-p1843.json`, 10701 taxa

## Counts

| Metric | Count |
|---|---|
| Total species (AviList) | 11131 |
| Russian name present | 10728 |
| — from IOC | 10655 |
| — from eBird | 69 |
| — from Wikidata | 4 |
| — manual override | 0 |
| Russian name missing | 403 |
| Extinct | 151 |
| Extinct in the wild | 5 |
| Possibly extinct | 46 |
| AviList species not in IOC (exact name) | 42 |
| IOC species not in AviList (exact name) | 138 |
| IOC vs eBird Russian name differs | 164 |

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

## Species with no Russian name anywhere (403)

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

Report only; the JSON always prefers IOC. First 50 examples:

| Scientific name | IOC | eBird |
|---|---|---|
| Anser canagicus | Белошей | Гусь-белошей |
| Anser fabalis | Гуменник (лесной гуменник) | Лесной гуменник |
| Melanitta deglandi | Горбоносый турпан | Белокрылый турпан |
| Cyrtonyx montezumae | Плачущий перепел, перепел Монтесумы | Плачущий перепел |
| Catreus wallichii | Хохлатый фазан, чир | Хохлатый фазан |
| Coua cursor | Желтогорлая тивука, тивука-бегун | Желтогорлая тивука |
| Fulica newtonii | Маскаренская лысуха | Маврикийская лысуха |
| Ardea coromanda | Коровья цапля | Восточная египетская цапля |
| Hirundapus caudacutus | Колючехвост, колючехвостый стриж | Колючехвост |
| Cynanthus doubledayi | Мексиканский колибри | Мексиканский изумруд |
| Sarcoramphus papa | Королевская катарта, королевский гриф | Королевская катарта |
| Cathartes aura | Катарта-индейка, гриф-индейка | Катарта-индейка |
| Buceros bicornis | Двурогий калао, гомрай | Двурогий калао |
| Campethera maculosa | Гвинейский дятел | Зеленоспинный дятел |
| Caracara plancus | Равнинная каракара, каранчо | Равнинная каракара |
| Strigops habroptilus | Какапо, совиный попугай | Какапо |
| Loriculus galgulus | Малайский лорикулюс, серендак | Малайский лорикулюс |
| Limnoctites rectirostris | Болотный прямоклюв | Прямоклюв |
| Limnoctites sulphuriferus | Желтобородый прямоклюв | Желтобородая курутия |
| Aethomyias nigrorufus | Рыжебрюхая кустовка | Чёрно-рыжая мышевидка |
| Oriolus oriolus | Иволга | Обыкновенная иволга |
| Dicrurus hottentottus | Лирохвостый дронго | Индийский дронго |
| Dicrurus macrocercus | Чёрный дронго | Черный дронго |
| Terpsiphone atrocaudata | Чёрная райская мухоловка | Черная райская мухоловка |
| Lophorina superba | Большая лофорина | Арфакская лофорина |
| Platylophus galericulatus | Сорокопутовая сойка | Хохлатая малайская сойка |
| Lanius meridionalis | Иберийский сорокопут | Пиренейский сорокопут |
| Lanius tigrinus | Тигровый жулан, тигровый сорокопут | Тигровый сорокопут |
| Lanius isabellinus | Буланый жулан | Рыжехвостый жулан |
| Lanius collurio | Жулан | Обыкновенный жулан |
| Lanius phoenicuroides | Туркестанский жулан, рыжехвостый жулан | Туркестанский жулан |
| Lanius schach | Длиннохвостый сорокопут, сорокопут-шах | Длиннохвостый сорокопут |
| Pyrrhocorax graculus | Альпийская галка, альпийская клушица | Альпийская галка |
| Podoces hendersoni | Монгольская пустынная сойка | Монгольская сойка |
| Nucifraga caryocatactes | Кедровка, ореховка | Кедровка |
| Culicicapa ceylonensis | Сероголовый комаролов | Сероголовая комароловка |
| Remiz pendulinus | Ремез | Обыкновенный ремез |
| Cyanistes cyanus | Князёк, белая лазоревка | Белая лазоревка |
| Periparus venustulus | Короткохвостая синица | Желтобрюхая синица |
| Lophophanes cristatus | Хохлатая синица, гренадерка | Хохлатая синица |
| Panurus biarmicus | Усатка, усатая синица | Усатая синица |
| Lullula arborea | Лесной жаворонок, юла | Лесной жаворонок |
| Galerida theklae | Короткохохлый жаворонок | Короткопалый хохлатый жаворонок |
| Eremophila alpestris | Рогатый жаворонок, рюм | Рогатый жаворонок |
| Calandrella cinerea | Красноголовый жаворонок | Африканский малый жаворонок |
| Cisticola juncidis | Веерохвостая цистикола | Золотистая цистикола |
| Arundinax aedon | Толстоклювая камышовка | Толстоклювая камышевка |
| Iduna pallida | Бледная бормотушка | Бледная пересмешка |
| Acrocephalus schoenobaenus | камышовка-барсучок | Камышевка-барсучок |
| Acrocephalus bistrigiceps | Чернобровая камышовка | Пестроголовая камышевка |
