<script setup lang="ts">
interface Beer {
  url: string;
  photo: string;
  icon: string;
  title: string;
  brewery: string;
  style: string;
  newStyle?: boolean;
  newBrewery?: boolean;
}

const ipaBeers: Beer[] = [
  {
    url: "https://untappd.com/b/midnight-project-citra-pre-order/6349012",
    photo:
      "https://assets.untappd.com/photos/2025_11_23/79ef619ae2e5d1d67496c988cee1b163_c_1530618259_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6349012_c92f5_sm.jpeg",
    title: "Citra? Pre-Order!",
    brewery: "Midnight Project × Horror × Red Rocket",
    style: "IPA — American",
  },
  {
    url: "https://untappd.com/b/sigma-brau-sigma-brau-auster-shymkentskij-marakas/6061139",
    photo:
      "https://assets.untappd.com/photos/2025_09_13/2711911f164c991e7272c38e2f8639e9_c_1513123889_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6061139_dff87_sm.jpeg",
    title: "Шымкентский Маракас",
    brewery: "Sigma Bräu",
    style: "IPA — New England / Hazy",
  },
  {
    url: "https://untappd.com/b/velka-morava-dunedin/6127822",
    photo:
      "https://assets.untappd.com/photos/2025_02_05/d81a63a6e9739c4596d0320079056cdc_c_1454596498_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6127822_90729_sm.jpeg",
    title: "Dunedin",
    brewery: "Velka Morava",
    style: "IPA — New Zealand",
  },
  {
    url: "https://untappd.com/b/ostrovica-relict/6171726",
    photo:
      "https://assets.untappd.com/photos/2025_04_26/436c478ee6bf0c721d184988d4d88803_c_1474271153_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6171726_744b7_sm.jpeg",
    title: "RELICT",
    brewery: "OSTROVICA × Big Village",
    style: "IPA — Session",
  },
  {
    url: "https://untappd.com/b/malanka-mlosc-superdelic-and-mosaic/6405405",
    photo:
      "https://assets.untappd.com/photos/2025_09_16/77f8691bf3bd8f1908dd272532f2f78f_c_1514014640_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6405405_dd4a4_hd.jpeg",
    title: "Mlosć",
    brewery: "Malanka",
    style: "Pale Ale — American",
  },
  {
    url: "https://untappd.com/b/big-village-brewery-sunlit-silence/6397612",
    photo:
      "https://assets.untappd.com/photos/2025_09_12/71ca61458b9fceb6bde5477b72483878_c_1512795065_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6397612_84d4c_sm.jpeg",
    title: "SUNLIT SILENCE",
    brewery: "Big Village",
    style: "Pale Ale — New England / Hazy",
  },
  {
    url: "https://untappd.com//b/zagovor-brewery-dogma/6231793",
    photo:
      "https://assets.untappd.com/photos/2025_04_18/0a55d95d3479fdfd2086f181b1a574dd_c_1471873752_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6231793_955d6_hd.jpeg",
    title: "Dogma",
    brewery: "Zagovor",
    style: "IPA — Imperial / Double New England / Hazy",
  },
  {
    url: "https://untappd.com//b/midnight-project-hop-headshot-bru-1/6376078",
    photo:
      "https://assets.untappd.com/photos/2025_10_03/0ac5b22627dacc5ab741b7bb948052dd_c_1518016198_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6376078_ee8bf_sm.jpeg",
    title: "Hop Headshot: BRU-1",
    brewery: "Midnight Project",
    style: "IPA — Triple",
  },
  {
    url: "https://untappd.com/b/rewort-brewery-fasten-seat-belt/5789767",
    photo:
      "https://assets.untappd.com/photos/2025_02_15/3088b62edef9472934c76938171f5517_c_1456770592_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5789767_626f0_sm.jpeg",
    title: "Fasten Seat Belt",
    brewery: "Rewort",
    style: "IPA — Quadruple",
  },
];

const lagerBeers: Beer[] = [
  {
    url: "https://untappd.com/b/big-village-brewery-village-lager/5302067",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5302067_22b97_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_11_29/4469c59bc35edd9a3f84ad226fdda46e_c_1531847616_raw.jpg",
    title: "VILLAGE LAGER",
    brewery: "Big Village",
    style: "Lager — Pale",
  },
  {
    url: "https://untappd.com/b/boxing-wizard-brewery-suckin-diesel-hell/5774322",
    title: "Suckin' Diesel Hell",
    brewery: "Boxing Wizard",
    style: "Lager — Helles",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-5774322_b0e63_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_01_07/9f50b25e91cbd8ce7e776f5af385fcfc_c_1448548349_raw.jpg",
  },

  {
    url: "https://untappd.com/b/velka-morava-humara/6471779",
    title: "Humara",
    brewery: "Velka Morava",
    style: "Lager — Světlé (Czech Pale)",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6471779_20ef8_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_11_02/799cefa97cb0f8d14f5c5d3f4a530fca_c_1525762860_raw.jpg",
  },
  {
    url: "https://untappd.com/b/big-village-brewery-que-pasa/5917687",
    title: "QUÉ PASA",
    brewery: "Big Village",
    style: "Lager — Mexican",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5917687_26254_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_08_22/25f876652eee103ff4372c45db5a61a5_c_1507364608_raw.jpg",
  },
  {
    url: "https://untappd.com/b/stamm-brewing-koinobori/6264963",
    title: "Koinobori",
    brewery: "Stamm",
    style: "Lager — Japanese Rice",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6264963_a909c_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_18/17e519f48b5b6fe87bc1bb07291d7b0f_c_1488656506_raw.jpg",
  },
  {
    url: "https://untappd.com/b/selfmade-brewery-late-night-pizza-club/6282984",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6282984_d45ff_sm.jpeg",
    title: "Late Night Pizza Club",
    brewery: "Selfmade",
    style: "Lager — American Light",
    photo:
      "https://assets.untappd.com/photos/2025_07_27/54ac69a083e3255de8beec48b7be44fe_c_1500082070_raw.jpg",
  },
  {
    url: "https://untappd.com/b/hacker-pschorr-munchner-munich-gold/16313",
    title: "Münchner Gold",
    brewery: "Hacker-Pschorr",
    style: "Lager — Dortmunder / Export",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-16313_60221_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_10_01/82285b04ccecc582ea6a5c34982ef425_c_1517700311_raw.jpg",
  },

  {
    url: "https://untappd.com/b/red-rocket-brewery-bazovye-potrebnosti/6228586",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6228586_ee57c_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_04_27/39a7de6b685fac5eec1da31623e3223c_c_1474683514_raw.jpg",
    title: "БАЗОВЫЕ ПОТРЕБНОСТИ",
    brewery: "Red Rocket Brewery",
    style: "Kölsch",
  },
  {
    url: "https://untappd.com/b/midnight-project-zhigulikkeller/3069407",
    title: "Zhigulikkeller",
    brewery: "Midnight Project × Mikkeller × Selfmade",
    style: "Lager — IPL",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-3069407_c80bd_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_09_09/26158748be2bccc7d398279c3ddb547b_c_1512205127_raw.jpg",
  },
  {
    url: "https://untappd.com/b/velka-morava-marzen/5253759",
    title: "Märzen",
    brewery: "Velka Morava",
    style: "Märzen",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5253759_19abf_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_05_09/22a69eca5d827c292162c5c9712b885b_c_1477554304_raw.jpg",
  },
  {
    url: "https://untappd.com//b/moscow-brewing-company-moskovskaya-pivovarennaya-kompaniya-zhiguli-barnoe-barhatnoe-zhiguli-barnoe-barhatnoe/2204742?filter=you",
    title: "Жигули Барное Бархатное",
    brewery: "Московская Пивоваренная Компания",
    style: "Lager — Dark",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-2204742_a54c5_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_02_21/458c27805f4f99e23d550c4ffb6f74b6_c_1458099927_raw.jpg",
  },
  {
    url: "https://untappd.com/b/ayinger-privatbrauerei-ayinger-altbairisch-dunkel/26091",
    title: "Altbairisch Dunkel",
    brewery: "Ayinger",
    style: "Lager — Munich Dunkel",
    icon: "https://assets.untappd.com/site/beer_logos/beer-26091_19532_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_08/29c12155d5a1ff577fd86b302e26c4c9_c_1486022282_raw.jpg",
  },
  {
    url: "https://untappd.com//b/russian-north-martinek/5156616",
    title: "Martínek",
    brewery: "Russian North",
    style: "Pilsner — Czech / Bohemian",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5156616_54ff7_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_25/5ec2c28b0b6fddff293c4e6c1aa1247e_c_1490671022_raw.jpg",
  },
  {
    url: "https://untappd.com//b/velka-morava-karma-police/6211663",
    title: "Karma Police",
    brewery: "Velka Morava",
    style: "Pilsner — German",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6211663_01bb2_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_04_12/0d8041b8935c66f3721579937c2b01ac_c_1470293549_raw.jpg",
  },
  {
    url: "https://untappd.com/b/zagovor-brewery-recovery-pils/5955289",
    title: "Recovery Pils",
    brewery: "Zagovor",
    style: "Pilsner — New Zealand",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5955289_94893_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_01_19/3720b3ee3f6dfb15d9b98594d6de09b1_c_1451143385_raw.jpg",
  },
  {
    url: "https://untappd.com/b/pivovarnya-odna-tonna-odna-tonna-brewery-elevenactka/6082347",
    title: "Elevenáctka",
    brewery: "Одна тонна",
    style: "Lager — Other",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6082347_8c5a1_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_01_12/c89f8616e6c974b474a13906a2f05337_c_1449660902_raw.jpg",
  },
  {
    url: "https://untappd.com/b/tilsitkrone-krepkij-gustav/5419204",
    title: "Крепкий Густав",
    brewery: "Tilsitkrone",
    style: "Bock — Hell / Maibock / Lentebock",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-5419204_b9ada_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_07/e334dd8662d32490590dc888d17b15c4_c_1485734894_raw.jpg",
  },
  {
    url: "https://untappd.com/b/schneider-weisse-g-schneider-and-sohn-aventinus-eisbock-tap09/67996",
    title: "Aventinus Eisbock (TAP09)",
    brewery: "Schneider",
    style: "Bock — Eisbock",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-67996_bcdd1_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_03_28/2856428ac1a70c2bc49094dc183fe39f_c_1466449083_raw.jpg",
  },
];

const wheatBeers: Beer[] = [
  {
    url: "https://untappd.com/b/jaws-brewery-weizen/839739",
    title: "Weizen",
    brewery: "Jaws",
    style: "Wheat Beer — Hefeweizen",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-839739_bcce0_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_07_06/4a8ce847939f6e11047b40216c79fd25_c_1493954489_raw.jpg",
  },
  {
    url: "https://untappd.com/b/brouwerij-van-steenberge-baptist-wit-blanche/2138256",
    title: "Baptist Wit / Blanche",
    brewery: "Van Steenberge",
    style: "Wheat Beer — Witbier / Blanche",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-2138256_7ed9a_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_09_05/e10a549d893711815edb3f7e83691000_c_1511183287_raw.jpg",
  },
  {
    url: "https://untappd.com/b/68-pauza-tap-68/6069161",
    title: "ТАП 68",
    brewery: "68 Пауза",
    style: "Wheat Beer — Hopfenweisse",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6069161_330bc_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_05_17/1a9fbdfd338ce8e2b9a0961fb467b164_c_1479572811_raw.jpg",
  },
  {
    url: "https://untappd.com/b/horror-brewing-midday-beast/6205422",
    title: "Midday Beast",
    brewery: "Horror",
    style: "Wheat Beer — American Pale Wheat",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6205422_25965_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_04_26/d32f451a044d8bbe278f0ef0f8d2f193_c_1474349113_raw.jpg",
  },
  {
    url: "https://untappd.com/b/horror-brewing-midday-beast/6205422",
    title: "Weihenstephaner Vitus",
    brewery: "Weihenstephan",
    style: "Bock — Weizenbock",
    icon: "https://assets.untappd.com/site/beer_logos/beer-7408_a806b_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_11_14/45f9a295bff9151c5f10ee63889f2ae6_c_1528387008_raw.jpg",
  },
  {
    url: "https://untappd.com/b/brasserie-de-la-senne-witz-bio/6064208",
    title: "Witz Bio",
    brewery: "Brasserie de la Senne",
    style: "Wheat Beer — Other",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6064208_c0211_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_12_03/3a0626b5a3f2a371b1822155e94be152_c_1532740659_raw.jpg",
  },
];

const belgianBeers: Beer[] = [
  {
    url: "https://untappd.com/b/rvyom-kogti-dzhejms-blond/6362060",
    title: "Джеймс Блонд",
    brewery: "РВЁМ КОГТИ",
    newBrewery: true,
    style: "Belgian Blonde",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6362060_d971e_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_08_02/c0c1556bc91779b4b8e8452e7ddc4269_c_1501720691_raw.jpg",
  },
  {
    url: "https://untappd.com/b/brouwerij-der-trappisten-van-westmalle-westmalle-trappist-dubbel/4168",
    title: "Westmalle Trappist Dubbel",
    brewery: "Westmalle",
    style: "Belgian Dubbel",
    icon: "https://assets.untappd.com/site/beer_logos/beer-4168_8fdd0_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_05_21/54ad4e14add6ef96881e1431b53c912a_c_1480674684_raw.jpg",
  },
  {
    url: "https://untappd.com/b/brouwerij-bosteels-tripel-karmeliet/6511",
    title: "Tripel Karmeliet",
    brewery: "Bosteels",
    style: "Belgian Tripel",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6511_cb677_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_11_26/ceb1800827a38ea5e1065c16add3d7de_c_1531083369_raw.jpg",
  },
  {
    url: "https://untappd.com/b/plague-brew-moort/4648542",
    title: "Moort",
    brewery: "Plague Brew",
    style: "Belgian Strong Golden Ale",
    icon: "https://assets.untappd.com/site/beer_logos/beer-4648542_8eaf4_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_07_17/fea794c5739212afb2ade53765b7213f_c_1496864509_raw.jpg",
  },
  {
    url: "",
    title: "",
    brewery: "",
    style: "Belgian Strong Dark Ale",
    icon: "",
    photo: "",
  },
  {
    url: "https://untappd.com/b/kasteel-brouwerij-vanhonsebrouck-kasteel-cuvee/15332",
    title: "Kasteel Cuvée",
    brewery: "Kasteel",
    style: "Belgian Quadrupel",
    icon: "https://assets.untappd.com/site/beer_logos/beer-15332_80a2f_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_12/6ff98381b5b27b501efc3d0749ca4171_c_1486894943_raw.jpg",
  },
];

const sourGoseBeers: Beer[] = [
  {
    url: "https://untappd.com/b/big-village-brewery-winds-of-fear/6348058",
    title: "WINDS OF FEAR",
    brewery: "Big Village Brewery",
    style: "Sour — Fruited",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6348058_8f627_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_08_22/21098f36722a669d02452a389060c375_c_1507350971_raw.jpg",
  },
  {
    url: "https://untappd.com/b/gusi-hoola-hoop-16-black-currant-blueberry-lime/6231642",
    title: "HOOLA HOOP 16",
    brewery: "GUSI",
    style: "Sour — Fruited Berliner Weisse",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6231642_439f1_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_08_28/f4f7b95abe19d8828f6f371168d04769_c_1508999693_raw.jpg",
  },
  {
    url: "https://untappd.com/b/big-pot-serotonin-barrel-aged-strawberry-and-guava/5674933",
    title: "Serotonin: Barrel Aged Strawberry & Guava",
    brewery: "Big Pot",
    style: "Sour — Smoothie / Pastry",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5674933_e6b74_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_02_19/9357a9df79b193ebad30f69275aed7f9_c_1457753828_raw.jpg",
  },
  {
    url: "https://untappd.com/b/pivovarnya-odna-tonna-odna-tonna-brewery-cherrify/6064548",
    title: "Cherrify",
    brewery: "Одна тонна",
    style: "Fruit Beer",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6064548_ad597_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_03_28/dffb9fb9cbf490c1ac71d5712b274b52_c_1466550831_raw.jpg",
  },
  {
    url: "https://untappd.com/b/delirium-huyghe-brewery-floris-passion/70362",
    title: "Floris Passion",
    brewery: "Huyghe",
    style: "Wheat Beer — Fruited",
    icon: "https://assets.untappd.com/site/beer_logos/beer-70362_219a4_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_11_14/a1f060510cf9cac73dfdb3805006aa18_c_1528373254_raw.jpg",
  },
  {
    url: "https://untappd.com/b/plague-brew-perfect-red-2025/6365766",
    title: "Perfect Red 2025",
    brewery: "Plague Brew",
    style: "Sour — Catharina",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6365766_03c9c_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_10_15/6054411cdcd3ec20c8bcc0c3fce69b69_c_1521212508_raw.jpg",
  },
  {
    url: "https://untappd.com/b/dieta-dieta-seven-seas/6290803",
    title: "Seven Seas",
    brewery: "DIETA",
    style: "Sour — Traditional Gose",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6290803_50cda_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_27/2313f60c40f840204a0c922fcbc28145_c_1491218048_raw.jpg",
  },
  {
    url: "https://untappd.com/b/ability-brewing-project-slow-heavy-metal-music-playing/6156502",
    title: "Slow Heavy Metal Music Playing",
    brewery: "Ability",
    style: "Sour — Tomato / Vegetable Gose",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6156502_3135f_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_04_06/072d00fb2c4a379919a70c1608914d6d_c_1469018928_raw.jpg",
  },
  {
    url: "https://untappd.com/b/plague-brew-chile-lima/5818740",
    title: "Chile Lima",
    brewery: "Plague",
    style: "Sour — Other Gose",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5818740_fd4d5_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_04_26/129829df71f5c10ca1bb5d89724f4e2c_c_1474273161_raw.jpg",
  },
  {
    url: "https://untappd.com/b/midnight-project-limonsol/6254724",
    title: "Лимонсоль",
    brewery: "Midnight Project",
    style: "Sour — Fruited Gose",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6254724_52205_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_21/75398141008317298dc7d5751769c52f_c_1489604123_raw.jpg",
  },
  {
    url: "https://untappd.com/b/4brewers-currant-mood/6211467",
    title: "Currant Mood",
    brewery: "4BREWERS",
    style: "Sour — Dark",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6211467_a898a_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_05_23/30072250ceb494c084bbdd91420ddd7c_c_1481146475_raw.jpg",
  },
  {
    url: "https://untappd.com/b/4brewers-harakter-ba-2020/4072488",
    title: "Характер [BA 2020]",
    brewery: "4BREWERS",
    style: "Sour — Other",
    icon: "https://assets.untappd.com/site/beer_logos/beer-4072488_b5d3c_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_01_19/429274fb7442096f9c75474acdddba1b_c_1451094076_raw.jpg",
  },
];

const stoutBeers: Beer[] = [
  {
    url: "https://untappd.com/b/baltika-breweries-baltika-baltika-stout/6071592",
    title: "Baltika Stout",
    brewery: "Балтика",
    style: "Stout - Irish Dry",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6071592_fe8fd_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_03_12/14b237de2d83d50317fff70b42497eb7_c_1462633225_raw.jpg",
  },
  {
    url: "https://untappd.com/b/zagovor-brewery-scratch/823908",
    title: "Scratch",
    brewery: "Zagovor",
    style: "Stout - Oatmeal",
    icon: "https://assets.untappd.com/site/beer_logos/beer-823908_29e2c_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_02_19/5dbf3984dc6015977b95ef98c6822b6b_c_1457766066_raw.jpg",
  },
  {
    url: "https://untappd.com/b/pivoteka-brew-pivoteka-zavtrak-v-kaire/5785656",
    title: "Завтрак в Каире",
    brewery: "Пивотека",
    style: "Stout - Coffee",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5785656_e3b8e_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_09_13/1659ef62eeac8fe93ca55dcd238775a5_c_1513216255_raw.jpg",
  },
  {
    url: "https://untappd.com/b/pivovarnya-odna-tonna-odna-tonna-brewery-temnaya-energiya-kokos-kakao-vanil/6264025",
    title: "Темная энергия: Кокос, Какао, Ваниль",
    brewery: "Одна тонна",
    style: "Stout - Imperial / Double",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6264025_5f603_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_07_26/cfda56a5ea41a1ad36351204e5a60c31_c_1499640055_raw.jpg",
  },
  {
    url: "https://untappd.com/b/4brewers-chary/6198286",
    title: "Чары",
    brewery: "4BREWERS",
    style: "Barleywine",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6198286_6fc72_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_08_06/c73818c68ce618cf0be95e94dc1cd1ff_c_1502973626_raw.jpg",
  },
  {
    url: "https://untappd.com/b/ability-brewing-project-echo-slam/6203343",
    title: "Echo Slam",
    brewery: "Ability",
    style: "Freeze-Distilled Beer",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6203343_1f3f2_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_14/db6eb22805ed4e3de2ecd7c4d73c57b0_c_1487552634_raw.jpg",
  },
];

const wildBeers: Beer[] = [
  {
    title: "Duchesse de Bourgogne",
    brewery: "Verhaeghe",
    url: "https://untappd.com/b/brouwerij-verhaeghe-duchesse-de-bourgogne/3954",
    style: "Sour - Flanders Red Ale",
    icon: "https://assets.untappd.com/site/beer_logos/beer-3954_c81f1_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_01_02/ff84aa560138760871449e5eec5f65e3_c_1447392612_raw.jpg",
  },
  {
    title: "Oud Bruin Raspberry (harvest 2023)",
    brewery: "Verzet",
    url: "https://untappd.com/b/brouwerij-t-verzet-oud-bruin-raspberry-harvest-2023/5970446",
    style: "Sour - Flanders Oud Bruin",
    icon: "https://assets.untappd.com/site/beer_logos/beer-1897631_a59b9_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_10_16/4844cf07b0a6ccbbf78e1d82cff8a1f7_c_1521414232_raw.jpg",
  },
  {
    title: "Bonbon",
    brewery: "Jaws",
    url: "https://untappd.com/b/jaws-brewery-bonbon/5585464",
    style: "Red Ale",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5585464_8116a_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_11_18/b2c7e47142d05e5c5320368b94b96425_c_1529412676_raw.jpg",
  },
  {
    title: "Kriek 100% Lambic Bio (2024)",
    brewery: "Cantillon",
    url: "https://untappd.com/b/brasserie-cantillon-kriek-100-lambic-bio-2024/5685869",
    style: "Lambic - Kriek",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5685869_fb805_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_14/9670c6784854153e2fc3a2f99b5b7aea_c_1487567364_raw.jpg",
  },
  {
    title: "Rosé de Gambrinus",
    brewery: "Cantillon",
    url: "https://untappd.com/b/brasserie-cantillon-rose-de-gambrinus/13142",
    style: "Lambic - Framboise",
    icon: "https://assets.untappd.com/site/beer_logos/beer-RosedeGambrinus_13142.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_12_05/3eb0cc0cea1b516aa18bdf75b12bc86b_c_1533235766_raw.jpg",
  },
  {
    title: "Cassis",
    brewery: "Lindemans",
    url: "https://untappd.com/b/brouwerij-lindemans-cassis/7895",
    style: "Lambic - Fruit",
    icon: "https://assets.untappd.com/site/beer_logos/beer-7895_543a6_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_01_29/5e64d96831ee2245c88beb0ba28b15e1_c_1453056204_raw.jpg",
  },
  {
    title: "Geuze Mariage Parfait",
    brewery: "Boon",
    url: "https://untappd.com/b/brouwerij-boon-geuze-mariage-parfait/29149",
    style: "Lambic - Gueuze",
    icon: "https://assets.untappd.com/site/beer_logos/beer-29149_05088_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_09/d576706d3b97c7e77216ae4ebcddb383_c_1486363755_raw.jpg",
  },
  {
    title: "Полуночница",
    brewery: "Wild Hills",
    url: "https://untappd.com/b/wild-hills-brewery-polunochnica/6323139",
    style: "Wild Ale",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6323139_05200_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_11_24/d5827aac1395a3622911d3b4b2a2c5e7_c_1530785804_raw.jpg",
  },
  {
    title: "Abby Che Brett Ale",
    brewery: "KLAATU BREW",
    url: "https://untappd.com/b/klaatu-brew-abby-che-brett-ale/5441401",
    style: "Farmhouse Ale",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5441401_c20be_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_10_03/fa28e70c680407d3810ab983feace6d1_c_1518136433_raw.jpg",
  },
];

const englishBeers: Beer[] = [
  {
    title: "Dogmatic",
    brewery: "Boxing Wizard × Чаща",
    url: "https://untappd.com/b/boxing-wizard-brewery-dogmatic/6202603",
    style: "Bitter - Best",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6202603_50f13_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_04_19/edd69adeba9d97a5b34e12e79995cbe5_c_1472187660_raw.jpg",
  },
  {
    title: "ESB",
    brewery: "Fuller's Griffin",
    url: "https://assets.untappd.com/site/beer_logos/beer-5455_0a690_sm.jpeg",
    style: "Bitter - Extra Special / Strong (ESB)",
    icon: "https://assets.untappd.com/site/beer_logos/beer-5455_0a690_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_09/e11bb927563881ed5f0a3f0fc52786a6_c_1486366215_raw.jpg",
  },
  {
    title: "Hazelnut Brown Ale",
    brewery: "Rogue Ales",
    url: "https://untappd.com/b/rogue-ales-hazelnut-brown-ale/4179",
    style: "Brown Ale - American",
    icon: "https://assets.untappd.com/site/beer_logos/beer-4179_56c20_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_11_07/85311b92d3a8f1b5e33b6b8eb1425cf5_c_1526667300_raw.jpg",
  },
];

const ciders: Beer[] = [
  {
    title: "Le Shouga Barrel Made",
    brewery: "Заповедник",
    url: "https://untappd.com/b/zapovednik-le-shouga-barrel-made/6315738",
    style: "Cider - Dry",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6315738_c0e27_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_08_02/573e3a3af414581fd649bbef731aba21_c_1501728554_raw.jpg",
  },
  {
    title: "Анархия",
    brewery: "Andreev Ciderworks",
    url: "https://untappd.com/b/andreev-ciderworks-anarhiya/5979131",
    style: "Cider - Traditional / Apfelwein",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-5979131_c05e5_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_03_16/49c1e0c2e166fb5d077d4ba59e026a2b_c_1463871492_raw.jpg",
  },
  {
    title: "Тузы и Восьмёрки",
    brewery: "Заповедник",
    url: "https://untappd.com/b/zapovednik-tuzy-i-vosmyorki/6064424",
    style: "Cider - Other Fruit",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6064424_0e896_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_04_25/b9c934a3a4bb191a3ec2d98aa5e3efcc_c_1473819723_raw.jpg",
  },
  {
    title: "Le Shouga Poiré",
    brewery: "Заповедник",
    url: "https://untappd.com/b/zapovednik-le-shouga-poire/6316394",
    style: "Cider - Perry / Poiré",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6316394_f992f_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_28/e4905c73019521cc24ad7a4cff99e886_c_1491459807_raw.jpg",
  },
  // todo 1000 checkin!
  {
    title: "Ice Cider (2023)",
    brewery: "Sólville",
    url: "https://untappd.com/b/solville-ice-cider-2023/5890370",
    style: "Cider - Ice",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-5890370_f4971_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_03_01/635f8d61ae55c8c943fa5b3959826cdc_c_1460031043_raw.jpg",
  },
  {
    title: "Ice Perry",
    brewery: "Andreev Ciderworks",
    url: "https://untappd.com/b/andreev-ciderworks-ice-perry/5061877",
    style: "Cider - Ice",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-5061877_95871_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_06_10/890ca934f3a6b948e4244f6eabc57f11_c_1486488444_raw.jpg",
  },
];
const meads: Beer[] = [
  {
    title: "Денница",
    brewery: "Щеглец",
    url: "https://untappd.com/b/sheglec-dennica/5910224",
    style: "Mead - Traditional",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-5910224_c7d97_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_07_05/da4799a5758225d419f9f2827d7dcbfe_c_1493500214_raw.jpg",
  },
  {
    title: "Большая страна: Донская вишня",
    brewery: "Одна тонна",
    url: "https://untappd.com/b/pivovarnya-odna-tonna-odna-tonna-brewery-bolshaya-strana-donskaya-vishnya/5970758",
    style: "Mead - Session / Short",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-5970758_0baf0_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_03_12/10e7c14857a8fdd8ee0920728253a0f8_c_1462637203_raw.jpg",
  },
  {
    title: "Practical Joke",
    brewery: "Big Village",
    url: "https://untappd.com/b/big-village-brewery-practical-joke/6134701",
    style: "Mead - Melomel",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6134701_4a7b0_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_03_17/aed9c2509df4d324f6cbb202c8d2ec52_c_1464074271_raw.jpg",
  },
  {
    title: "Cola Mead",
    brewery: "Степь и Ветер",
    url: "https://untappd.com/b/steppe-and-wind-meadery-step-i-veter-cola-mead/6340235",
    style: "Mead - Melomel",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6340235_4f57f_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_09_10/fd59bc87a1ff592c7e78fa2be0e40ade_c_1512428694_raw.jpg",
  },
  {
    title: "Сайсер Яблоки и мёд",
    brewery: "Gurin Craft × Ля Фуар Дэ Нижний Новгород",
    url: "https://untappd.com/b/gurin-craft-sajser-yabloki-i-myod/6026564",
    style: "Mead - Cyser",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6026564_6109e_sm.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_05_16/0efbb968a3d2712a8d5d5b96eea7c38b_c_1479283893_raw.jpg",
  },
  {
    title: "Сон Масала Christmas Edition",
    brewery: "Чаща",
    url: "https://untappd.com/b/pivovarnya-chasha-thicket-brewery-son-masala-christmas-edition/4637336",
    style: "Mead - Cyser",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-4637336_670a9_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_04_27/aa229c78f9c1384181c045243512ae7f_c_1474684443_raw.jpg",
  },
  {
    title: "Pyment White Batch #2",
    brewery: "Ashram",
    url: "https://untappd.com/b/ashram-cider-pyment-white-batch-2/5911384",
    style: "Mead - Cyser",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-5911384_74783_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_03_01/9545784cdbee47eb83c5d0486cdfec02_c_1460008429_raw.jpg",
  },
  {
    title: "Metheglin из одуванчиков Batch #4",
    brewery: "Ashram",
    url: "https://untappd.com/b/ashram-cider-metheglin-iz-oduvanchikov-batch-4/6182074",
    style: "Mead - Metheglin",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6182074_c0b24_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_03_29/a167aa74f9821e329d63898fb15ff286_c_1466805776_raw.jpg",
  },
  {
    title: "Juniper & Basil Tonic Mead",
    brewery: "Степь и Ветер",
    url: "https://untappd.com/b/steppe-and-wind-meadery-step-i-veter-juniper-and-basil-tonic-mead/5776656",
    style: "Mead - Other",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-5776656_b31d4_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_04_26/ea3da05bd113b76c0ec4e7d30a293b54_c_1474351188_raw.jpg",
  },
];
const nonAlcoBeers: Beer[] = [
  {
    url: "https://untappd.com/b/tradicni-pivovar-v-rakovniku-bakalar-nealko-za-studena-chmeleny-non-alcoholic-dry-hopped-lager/1171072",
    title: "Nealko Za studena chmelený",
    brewery: "Bakalář",
    style: "Non-Alcoholic - Lager",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-1171072_4e61a_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_10_26/f45d332a3cbde400feb07689d609ddce_c_1524241121_raw.jpg",
  },
  {
    url: "https://untappd.com/b/gorkovskaya-brewery-gorkovskaya-pivovarnya-ipa-0-0/3860563",
    title: "IPA 0,0",
    brewery: "Горьковская",
    style: "Non-Alcoholic - IPA",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-3860563_01898_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_09_26/b828fce1eac221cd57ab52ac5c6d1e60_c_1516254289_raw.jpg",
  },
  {
    url: "https://untappd.com/b/plague-zero-sportacus-talus/6326136",
    title: "Sportacus Talus",
    brewery: "Plague Zero",
    style: "Non-Alcoholic - Pale Ale",
    icon: "https://assets.untappd.com/site/brewery_logos/brewery-447721_81eb8.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_07_27/d77f6a0d36084ebfcc63b24e158c7846_c_1500082976_raw.jpg",
  },
  {
    url: "https://untappd.com/b/sidr-oktyabr-oktyabr-0/5568428",
    title: "Октябрь №0",
    brewery: "Сидр Октябрь",
    style: "Non-Alcoholic - Cider / Perry",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-5568428_b51a5_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_03_01/76a664ab0d92a30de742e15075713fbc_c_1460015489_raw.jpg",
  },
  {
    url: "https://untappd.com/b/black-cat-brewery-for-all-the-dogs-non-alcoholic/6282897",
    title: "For All the Dogs Non Alcoholic",
    brewery: "Black Cat Zero",
    style: "Non-Alcoholic - Sour",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6282897_6a48a_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_08_31/c20b2080415818059216a305827b062b_c_1510014216_raw.jpg",
  },
  {
    url: "https://untappd.com/b/4brewers-zavisimost-bazilik-no-alco/6470526",
    title: "Зависимость Базилик [No Alco]",
    brewery: "4BREWERS",
    style: "Non-Alcoholic - Gose",
    icon: "https://assets.untappd.com/site/beer_logos_hd/beer-6470526_b9eea_hd.jpeg",
    photo:
      "https://assets.untappd.com/photos/2025_11_10/659a1544f008ce5748e1e3ed44ab194d_c_1527658093_raw.jpg",
  },
];

const styleGroups = [
  { group: "IPA / APA", beers: ipaBeers },
  { group: "Lager / Pilsner / Bock", beers: lagerBeers },
  { group: "Wheat", beers: wheatBeers },
  { group: "Belgian", beers: belgianBeers },
  { group: "English", beers: englishBeers },
  { group: "Stout / Barleywine / Freeze", beers: stoutBeers },
  { group: "Sour / Gose", beers: sourGoseBeers },
  { group: "Flanders / Lambic / Wild / Farmhouse", beers: wildBeers },
  { group: "Cider", beers: ciders },
  { group: "Mead", beers: meads },
  { group: "Non-alco", beers: nonAlcoBeers },
];

const getSlug = (text: string): string => {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .trim();
};

const tocItems = computed(() =>
  styleGroups.map((group) => ({
    title: group.group,
    id: getSlug(group.group),
  })),
);

const showScrollTop = ref(false);

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};

onMounted(() => {
  const handleScroll = () => {
    showScrollTop.value = window.scrollY > 300;
  };
  window.addEventListener("scroll", handleScroll);
  onUnmounted(() => {
    window.removeEventListener("scroll", handleScroll);
  });
});
</script>

<template>
  <v-container>
    <v-row>
      <v-col> <h1 class="text-center text-h2">Пивные итоги 2025</h1> </v-col>
    </v-row>

    <v-row>
      <v-col>
        <div class="text-center">
          <div class="d-flex flex-wrap justify-center ga-2">
            <v-chip
              v-for="item in tocItems"
              :key="item.id"
              :href="`#${item.id}`"
              variant="outlined"
              class="ma-1"
            >
              {{ item.title }}
            </v-chip>
          </div>
        </div>
      </v-col>
    </v-row>

    <template v-for="styleGroup in styleGroups" :key="styleGroup.group">
      <v-row>
        <v-col>
          <h2 :id="getSlug(styleGroup.group)" class="text-center text-h3">
            {{ styleGroup.group }}
          </h2>
        </v-col>
      </v-row>

      <v-row class="flex-sm-column flex-md-row flex-sm-nowrap flex-md-wrap">
        <template v-for="beer in styleGroup.beers" :key="beer.url">
          <v-col md="4" sm="12" xl="2">
            <v-card
              min-width="min(372px, 100%)"
              class="beer-card"
              :href="beer.url"
              rounded="lg"
            >
              <div class="beer-card__media">
                <v-img
                  height="541"
                  cover
                  :src="beer.photo"
                  rounded="lg"
                ></v-img>
                <v-avatar
                  class="beer-card__icon"
                  size="100"
                  rounded="lg"
                  :image="beer.icon"
                />
              </div>
              <v-card-title class="text-center font-weight-bold mt-5 pb-0">{{
                beer.title || "-"
              }}</v-card-title>
              <v-card-subtitle class="text-center pb-3">
                <template v-if="beer.newBrewery">
                  <v-badge
                    inline
                    location="top right"
                    color="success"
                    content="new!"
                  >
                    <span class="mr-1">{{ beer.brewery || "-" }}</span>
                  </v-badge>
                </template>
                <template v-else>
                  <div>{{ beer.brewery || "-" }}</div>
                </template>
              </v-card-subtitle>
              <v-divider></v-divider>
              <v-card-text class="text-center">
                {{ beer.style }}
              </v-card-text>
            </v-card>
          </v-col>
        </template>
      </v-row>
    </template>

    <v-fab
      v-model="showScrollTop"
      location="bottom end"
      app
      icon="mdi-arrow-up"
      color="primary"
      @click="scrollToTop"
    />
  </v-container>
</template>

<style scoped lang="sass">
.beer-card
  position: relative
  overflow: visible

.beer-card__media
  position: relative

.beer-card__icon
  position: absolute
  left: 50%
  bottom: -20px
  transform: translateX(-50%)
  width: 80px
  height: 80px
  box-shadow: 0 1px 20px rgba(0, 0, 0, 0.35)
  border-radius: 0
  z-index: 2
</style>
