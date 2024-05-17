# -*- coding: utf-8 -*-

import logging
from typing import Dict

from resources.lib.utils.text import normalize_text

RAISE_EXCEPTION_IF_INVALID_STANDARD = True


logger: logging.Logger = logging.getLogger('UniversalSubs.Language')


def __normalize_map(map: Dict[str, str]) -> Dict[str, str]:
    normalized_map: Dict[str, str] = {}
    for key, value in map.items():
        normalized_map[normalize_text(key)] = value
    return normalized_map


def __populate_map_fallbacks(map: Dict[str, str], fallbacks_map: Dict[str, str], log_missing: bool = False) -> None:
    for key, fallback_value in fallbacks_map.items():
        if not key in map:
            if log_missing:
                logger.fatal("Missing value for key " + key)
            map[key] = fallback_value


def __reverse_map(language_map: Dict[str, str]) -> Dict[str, str]:
    reversed_map: Dict[str, str] = {}
    for key, value in language_map.items():
        if value:
            reversed_map[value.lower()] = key
    return reversed_map


# ISO-639-1 codes
NAME_TO_TWO_LETTER_CODE: Dict[str, str] = {
    'Abkhaz': 'ab',
    'Afar': 'aa',
    'Afrikaans': 'af',
    'Akan': 'ak',
    'Albanian': 'sq',
    'Amharic': 'am',
    'Arabic': 'ar',
    'Aragonese': 'an',
    'Armenian': 'hy',
    'Assamese': 'as',
    'Avaric': 'av',
    'Avestan': 'ae',
    'Aymara': 'ay',
    'Azerbaijani': 'az',
    'Bambara': 'bm',
    'Bashkir': 'ba',
    'Basque': 'eu',
    'Belarusian': 'be',
    'Bengali': 'bn',
    'Bihari': 'bh',
    'Bislama': 'bi',
    'Bosnian': 'bs',
    'Breton': 'br',
    'Bulgarian': 'bg',
    'Burmese': 'my',
    'Catalan': 'ca',
    'Central Khmer': 'km',
    'Chamorro': 'ch',
    'Chechen': 'ce',
    'Chichewa': 'ny',
    'Chinese': 'zh',
    'Church Slavic': 'cu',
    'Chuvash': 'cv',
    'Cornish': 'kw',
    'Corsican': 'co',
    'Cree': 'cr',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Divehi': 'dv',
    'Dutch': 'nl',
    'Dzongkha': 'dz',
    'English': 'en',
    'Esperanto': 'eo',
    'Estonian': 'et',
    'Ewe': 'ee',
    'Faroese': 'fo',
    'Fijian': 'fj',
    'Finnish': 'fi',
    'French': 'fr',
    'Fulah': 'ff',
    'Gaelic': 'gd',
    'Galician': 'gl',
    'Georgian': 'ka',
    'German': 'de',
    'Greek': 'el',
    'Guaraní': 'gn',
    'Gujarati': 'gu',
    'Haitian': 'ht',
    'Hausa': 'ha',
    'Hebrew': 'he',
    'Herero': 'hz',
    'Hindi': 'hi',
    'Hiri Motu': 'ho',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Ido': 'io',
    'Igbo': 'ig',
    'Indonesian': 'id',
    'Interlingua': 'ia',
    'Interlingue': 'ie',
    'Inuktitut': 'iu',
    'Inupiaq': 'ik',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Javanese': 'jv',
    'Kalaallisut': 'kl',
    'Kannada': 'kn',
    'Kanuri': 'kr',
    'Kashmiri': 'ks',
    'Kazakh': 'kk',
    'Kikuyu': 'ki',
    'Kinyarwanda': 'rw',
    'Kirghiz': 'ky',
    'Komi': 'kv',
    'Kongo': 'kg',
    'Korean': 'ko',
    'Kuanyama': 'kj',
    'Kurdish': 'ku',
    'Lao': 'lo',
    'Latin': 'la',
    'Latvian': 'lv',
    'Limburgish': 'li',
    'Lingala': 'ln',
    'Lithuanian': 'lt',
    'Luba-Katanga': 'lu',
    'Luganda': 'lg',
    'Luxembourgish': 'lb',
    'Macedonian': 'mk',
    'Malagasy': 'mg',
    'Malay': 'ms',
    'Malayalam': 'ml',
    'Maltese': 'mt',
    'Manx': 'gv',
    'Māori': 'mi',
    'Marathi': 'mr',
    'Marshallese': 'mh',
    'Mongolian': 'mn',
    'Nauru': 'na',
    'Navajo': 'nv',
    'Ndonga': 'ng',
    'Nepali': 'ne',
    'North Ndebele': 'nd',
    'Northern Sami': 'se',
    'Norwegian Bokmål': 'nb',
    'Norwegian Nynorsk': 'nn',
    'Norwegian': 'no',
    'Occitan': 'oc',
    'Ojibwa': 'oj',
    'Oriya': 'or',
    'Oromo': 'om',
    'Ossetian': 'os',
    'Pāli': 'pi',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Punjabi': 'pa',
    'Pashto': 'ps',
    'Quechua': 'qu',
    'Romanian': 'ro',
    'Romansh': 'rm',
    'Rundi': 'rn',
    'Russian': 'ru',
    'Samoan': 'sm',
    'Sango': 'sg',
    'Sanskrit': 'sa',
    'Sardinian': 'sc',
    'Serbian': 'sr',
    'Shona': 'sn',
    'Sichuan Yi': 'ii',
    'Sindhi': 'sd',
    'Sinhala': 'si',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Somali': 'so',
    'South Ndebele': 'nr',
    'Southern Sotho': 'st',
    'Spanish': 'es',
    'Sundanese': 'su',
    'Swahili': 'sw',
    'Swati': 'ss',
    'Swedish': 'sv',
    'Tagalog': 'tl',
    'Tahitian': 'ty',
    'Tajik': 'tg',
    'Tamil': 'ta',
    'Tatar': 'tt',
    'Telugu': 'te',
    'Thai': 'th',
    'Tibetan': 'bo',
    'Tigrinya': 'ti',
    'Tonga': 'to',
    'Tsonga': 'ts',
    'Tswana': 'tn',
    'Turkish': 'tr',
    'Turkmen': 'tk',
    'Twi': 'tw',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Uyghur': 'ug',
    'Uzbek': 'uz',
    'Venda': 've',
    'Vietnamese': 'vi',
    'Volapük': 'vo',
    'Walloon': 'wa',
    'Welsh': 'cy',
    'Western Frisian': 'fy',
    'Wolof': 'wo',
    'Xhosa': 'xh',
    'Yiddish': 'yi',
    'Yoruba': 'yo',
    'Zhuang': 'za',
    'Zulu': 'zu',
}

# ISO-639-2/3 codes
NAME_TO_TREE_LETTER_CODE: Dict[str, str] = {
    'Abkhaz': 'abk',
    'Abkhazian': 'abk',
    'Achinese': 'ace',
    'Acoli': 'ach',
    'Adangme': 'ada',
    'Adyghe': 'ady',
    'Afar': 'aar',
    'Afrihili': 'afh',
    'Afrikaans': 'afr',
    'Afro-Asiatic': 'afa',
    'Ainu': 'ain',
    'Akan': 'aka',
    'Akkadian': 'akk',
    'Albanian': 'alb',
    'Aleut': 'ale',
    'Algonquian': 'alg',
    'Altaic': 'tut',
    'Amharic': 'amh',
    'Angika': 'anp',
    'Apache': 'apa',
    'Arabic': 'ara',
    'Aragonese': 'arg',
    'Aramaic': 'arc',
    'Arapaho': 'arp',
    'Arawak': 'arw',
    'Armenian': 'arm',
    'Aromanian': 'rup',
    'Artificial': 'art',
    'Assamese': 'asm',
    'Asturian': 'ast',
    'Athapascan': 'ath',
    'Australian': 'aus',
    'Austronesian': 'map',
    'Avaric': 'ava',
    'Avestan': 'ave',
    'Awadhi': 'awa',
    'Aymara': 'aym',
    'Azerbaijani': 'aze',
    'Balinese': 'ban',
    'Baltic': 'bat',
    'Baluchi': 'bal',
    'Bambara': 'bam',
    'Bamileke': 'bai',
    'Banda': 'bad',
    'Bantu': 'bnt',
    'Basa': 'bas',
    'Bashkir': 'bak',
    'Basque': 'baq',
    'Batak': 'btk',
    'Beja': 'bej',
    'Belarusian': 'bel',
    'Bemba': 'bem',
    'Bengali': 'ben',
    'Berber': 'ber',
    'Bhojpuri': 'bho',
    'Bihari': 'bih',
    'Bikol': 'bik',
    'Bini; Edo': 'bin',
    'Bislama': 'bis',
    'Blin': 'byn',
    'Blissymbols': 'zbl',
    'Bodo': 'brx',
    'Bosnian': 'bos',
    'Braj': 'bra',
    'Breton': 'bre',
    'Buginese': 'bug',
    'Bulgarian': 'bul',
    'Buriat': 'bua',
    'Burmese': 'bur',
    'Caddo': 'cad',
    'Catalan': 'cat',
    'Caucasian': 'cau',
    'Cebuano': 'ceb',
    'Celtic': 'cel',
    'Central American Indian': 'cai',
    'Central Khmer': 'khm',
    'Chagatai': 'chg',
    'Chamic': 'cmc',
    'Chamorro': 'cha',
    'Chechen': 'che',
    'Cherokee': 'chr',
    'Cheyenne': 'chy',
    'Chhattisgarhi': 'hne',
    'Chibcha': 'chb',
    'Chichewa': 'nya',
    'Chinese': 'chi',
    'Chinook jargon': 'chn',
    'Chipewyan': 'chp',
    'Choctaw': 'cho',
    'Church Slavic': 'chu',
    'Chuukese': 'chk',
    'Chuvash': 'chv',
    'Classical Syriac': 'syc',
    'Coptic': 'cop',
    'Cornish': 'cor',
    'Corsican': 'cos',
    'Cree': 'cre',
    'Creek': 'mus',
    'Creoles and pidgins, English based': 'cpe',
    'Creoles and pidgins, French-based': 'cpf',
    'Creoles and pidgins, Portuguese-based': 'cpp',
    'Creoles and pidgins': 'crp',
    'Crimean Tatar': 'crh',
    'Croatian': 'hrv',
    'Cushitic': 'cus',
    'Czech': 'cze',
    'Dakota': 'dak',
    'Danish': 'dan',
    'Dargwa': 'dar',
    'Dari': 'prs',
    'Delaware': 'del',
    'Dinka': 'din',
    'Divehi': 'div',
    'Dogri': 'doi',
    'Dogrib': 'dgr',
    'Dravidian': 'dra',
    'Duala': 'dua',
    'Dutch': 'dut',
    'Dyula': 'dyu',
    'Dzongkha': 'dzo',
    'Eastern Frisian': 'frs',
    'Efik': 'efi',
    'Ekajuk': 'eka',
    'Elamite': 'elx',
    'English': 'eng',
    'Erzya': 'myv',
    'Esperanto': 'epo',
    'Estonian': 'est',
    'Ewe': 'ewe',
    'Ewondo': 'ewo',
    'Extremaduran': 'ext',
    'Fang': 'fan',
    'Fanti': 'fat',
    'Faroese': 'fao',
    'Fijian': 'fij',
    'Filipino': 'fil',
    'Finnish': 'fin',
    'Finno-Ugrian': 'fiu',
    'Fon': 'fon',
    'French': 'fre',
    'Friulian': 'fur',
    'Fulah': 'ful',
    'Ga': 'gaa',
    'Gaelic': 'gla',
    'Galibi Carib': 'car',
    'Galician': 'glg',
    'Gayo': 'gay',
    'Gbaya': 'gba',
    'Geez': 'gez',
    'Georgian': 'geo',
    'German': 'ger',
    'Germanic': 'gem',
    'Gilbertese': 'gil',
    'Gondi': 'gon',
    'Gorontalo': 'gor',
    'Gothic': 'got',
    'Grebo': 'grb',
    'Greek': 'ell',
    'Guaraní': 'grn',
    'Gujarati': 'guj',
    'Haida': 'hai',
    'Haitian': 'hat',
    'Hausa': 'hau',
    'Hawaiian': 'haw',
    'Hebrew': 'heb',
    'Herero': 'her',
    'Hiligaynon': 'hil',
    'Himachali': 'him',
    'Hindi': 'hin',
    'Hiri Motu': 'hmo',
    'Hittite': 'hit',
    'Hmong': 'hmn',
    'Hungarian': 'hun',
    'Hupa': 'hup',
    'Iban': 'iba',
    'Icelandic': 'ice',
    'Ido': 'ido',
    'Igbo': 'ibo',
    'Ijo': 'ijo',
    'Iloko': 'ilo',
    'Inari Sami': 'smn',
    'Indic': 'inc',
    'Indo-European': 'ine',
    'Indonesian': 'ind',
    'Ingush': 'inh',
    'Interlingua': 'ina',
    'Interlingue': 'ile',
    'Inuktitut': 'iku',
    'Inupiaq': 'ipk',
    'Iranian': 'ira',
    'Irish': 'gle',
    'Iroquoian': 'iro',
    'Italian': 'ita',
    'Japanese': 'jpn',
    'Javanese': 'jav',
    'Judeo-Arabic': 'jrb',
    'Judeo-Persian': 'jpr',
    'Kabardian': 'kbd',
    'Kabyle': 'kab',
    'Kachin': 'kac',
    'Kalaallisut': 'kal',
    'Kalmyk': 'xal',
    'Kamba': 'kam',
    'Kannada': 'kan',
    'Kanuri': 'kau',
    'Kara-Kalpak': 'kaa',
    'Karachay-Balkar': 'krc',
    'Karelian': 'krl',
    'Karen': 'kar',
    'Kashmiri': 'kas',
    'Kashubian': 'csb',
    'Kawi': 'kaw',
    'Kazakh': 'kaz',
    'Khasi': 'kha',
    'Khoisan': 'khi',
    'Khotanese': 'kho',
    'Kikuyu': 'kik',
    'Kimbundu': 'kmb',
    'Kinyarwanda': 'kin',
    'Kirghiz': 'kir',
    'Klingon': 'tlh',
    'Komi': 'kom',
    'Kongo': 'kon',
    'Konkani': 'kok',
    'Korean': 'kor',
    'Kosraean': 'kos',
    'Kpelle': 'kpe',
    'Krio': 'kri',
    'Kru': 'kro',
    'Kuanyama': 'kua',
    'Kumyk': 'kum',
    'Kurdish': 'kur',
    'Kurukh': 'kru',
    'Kutenai': 'kut',
    'Ladino': 'lad',
    'Lahnda': 'lah',
    'Lamba': 'lam',
    'Land Dayak': 'day',
    'Lao': 'lao',
    'Latin': 'lat',
    'Latvian': 'lav',
    'Lezghian': 'lez',
    'Limburgish': 'lim',
    'Lingala': 'lin',
    'Lithuanian': 'lit',
    'Lojban': 'jbo',
    'Lower Sorbian': 'dsb',
    'Lozi': 'loz',
    'Luba-Katanga': 'lub',
    'Luba-Lulua': 'lua',
    'Luganda': 'lug',
    'Luiseno': 'lui',
    'Lule Sami': 'smj',
    'Lunda': 'lun',
    'Luo': 'luo',
    'Lushai': 'lus',
    'Luxembourgish': 'ltz',
    'Macedonian': 'mac',
    'Madurese': 'mad',
    'Magahi': 'mag',
    'Maithili': 'mai',
    'Makasar': 'mak',
    'Malagasy': 'mlg',
    'Malay': 'may',
    'Malayalam': 'mal',
    'Maltese': 'mlt',
    'Manchu': 'mnc',
    'Mandar': 'mdr',
    'Mandingo': 'man',
    'Manipuri': 'mni',
    'Manobo': 'mno',
    'Manx': 'glv',
    'Māori': 'mao',
    'Mapudungun': 'arn',
    'Marathi': 'mar',
    'Mari': 'chm',
    'Marshallese': 'mah',
    'Marwari': 'mwr',
    'Masai': 'mas',
    'Mayan': 'myn',
    'Mende': 'men',
    'Minangkabau': 'min',
    'Mirandese': 'mwl',
    'Mohawk': 'moh',
    'Moksha': 'mdf',
    'Mon-Khmer': 'mkh',
    'Mongo': 'lol',
    'Mongolian': 'mon',
    'Montenegrin': 'cnr',
    'Mossi': 'mos',
    'Multiple': 'mul',
    'Munda': 'mun',
    "Mi'kmaq": 'mic',
    'Nahuatl': 'nah',
    'Nauru': 'nau',
    'Navajo': 'nav',
    'Ndonga': 'ndo',
    'Neapolitan': 'nap',
    'Nepal Bhasa': 'new',
    'Nepali': 'nep',
    'Nias': 'nia',
    'Niger-Kordofanian': 'nic',
    'Nilo-Saharan': 'ssa',
    'Niuean': 'niu',
    'Nogai': 'nog',
    'North American Indian': 'nai',
    'North Ndebele': 'nde',
    'Northern Frisian': 'frr',
    'Northern Sami': 'sme',
    'Norwegian Bokmål': 'nob',
    'Norwegian Nynorsk': 'nno',
    'Norwegian': 'nor',
    'Nubian': 'nub',
    'Nyamwezi': 'nym',
    'Nyankole': 'nyn',
    'Nyoro': 'nyo',
    'Nzima': 'nzi',
    "N'Ko": 'nqo',
    'Occitan': 'oci',
    'Ojibwa': 'oji',
    'Oriya': 'ori',
    'Oromo': 'orm',
    'Osage': 'osa',
    'Ossetian': 'oss',
    'Otomian': 'oto',
    'Pahlavi': 'pal',
    'Palauan': 'pau',
    'Pali': 'pli',
    'Pampanga': 'pam',
    'Pangasinan': 'pag',
    'Papiamento': 'pap',
    'Papuan': 'paa',
    'Northern Sotho': 'nso',
    'Persian': 'per',
    'Philippine': 'phi',
    'Phoenician': 'phn',
    'Pohnpeian': 'pon',
    'Polish': 'pol',
    'Portuguese': 'por',
    'Prakrit': 'pra',
    'Punjabi': 'pan',
    'Pashto': 'pus',
    'Quechua': 'que',
    'Querétaro Otomi': 'otq',
    'Rajasthani': 'raj',
    'Rapanui': 'rap',
    'Rarotongan': 'rar',
    'Romance': 'roa',
    'Romanian': 'rum',
    'Romansh': 'roh',
    'Romany': 'rom',
    'Rundi': 'run',
    'Russian': 'rus',
    'Salishan': 'sal',
    'Samaritan Aramaic': 'sam',
    'Sami': 'smi',
    'Samoan': 'smo',
    'Sandawe': 'sad',
    'Sango': 'sag',
    'Sanskrit': 'san',
    'Santali': 'sat',
    'Sardinian': 'srd',
    'Sasak': 'sas',
    'Scots': 'sco',
    'Selkup': 'sel',
    'Semitic': 'sem',
    'Serbian': 'srp',
    'Serer': 'srr',
    'Shan': 'shn',
    'Shona': 'sna',
    'Sichuan Yi': 'iii',
    'Sicilian': 'scn',
    'Sidamo': 'sid',
    'Sign': 'sgn',
    'Siksika': 'bla',
    'Sindhi': 'snd',
    'Sinhala': 'sin',
    'Sino-Tibetan': 'sit',
    'Siouan': 'sio',
    'Skolt Sami': 'sms',
    'Slave': 'den',
    'Slavic': 'sla',
    'Slovak': 'slo',
    'Slovenian': 'slv',
    'Sogdian': 'sog',
    'Somali': 'som',
    'Songhai': 'son',
    'Soninke': 'snk',
    'Soranî': 'ckb',
    'Sorbian': 'wen',
    'South American Indian': 'sai',
    'South Ndebele': 'nbl',
    'Southern Altai': 'alt',
    'Southern Sami': 'sma',
    'Southern Sotho': 'sot',
    'Spanish': 'spa',
    'Sranan Tongo': 'srn',
    'Sukuma': 'suk',
    'Sumerian': 'sux',
    'Sundanese': 'sun',
    'Susu': 'sus',
    'Swahili': 'swa',
    'Swati': 'ssw',
    'Swedish': 'swe',
    'Swiss German': 'gsw',
    'Syriac': 'syr',
    'Tagalog': 'tgl',
    'Tahitian': 'tah',
    'Tai': 'tai',
    'Tajik': 'tgk',
    'Tamashek': 'tmh',
    'Tamil': 'tam',
    'Tatar': 'tat',
    'Telugu': 'tel',
    'Tereno': 'ter',
    'Tetum': 'tet',
    'Thai': 'tha',
    'Tibetan': 'tib',
    'Tigre': 'tig',
    'Tigrinya': 'tir',
    'Timne': 'tem',
    'Tiv': 'tiv',
    'Tlingit': 'tli',
    'Tok Pisin': 'tpi',
    'Tokelau': 'tkl',
    'Tonga (Nyasa)': 'tog',
    'Tonga': 'ton',
    'Tsimshian': 'tsi',
    'Tsonga': 'tso',
    'Tswana': 'tsn',
    'Tumbuka': 'tum',
    'Tupi': 'tup',
    'Turkish': 'tur',
    'Turkmen': 'tuk',
    'Tuvalu': 'tvl',
    'Tuvinian': 'tyv',
    'Twi': 'twi',
    'Udmurt': 'udm',
    'Ugaritic': 'uga',
    'Ukrainian': 'ukr',
    'Umbundu': 'umb',
    'Uncoded': 'mis',
    'Upper Sorbian': 'hsb',
    'Urdu': 'urd',
    'Uyghur': 'uig',
    'Uzbek': 'uzb',
    'Vai': 'vai',
    'Venda': 'ven',
    'Vietnamese': 'vie',
    'Volapük': 'vol',
    'Votic': 'vot',
    'Wakashan': 'wak',
    'Walloon': 'wln',
    'Waray': 'war',
    'Washo': 'was',
    'Welsh': 'wel',
    'Western Frisian': 'fry',
    'Wolaitta': 'wal',
    'Wolof': 'wol',
    'Xhosa': 'xho',
    'Yakut': 'sah',
    'Yao': 'yao',
    'Yapese': 'yap',
    'Yiddish': 'yid',
    'Yoruba': 'yor',
    'Yucatec Maya': 'yua',
    'Yupik': 'ypk',
    'Zande': 'znd',
    'Zapotec': 'zap',
    'Zaza': 'zza',
    'Zenaga': 'zen',
    'Zhuang': 'zha',
    'Zulu': 'zul',
    'Zuni': 'zun',
    "Gwich'in": 'gwi',
}

NAME_TO_TWO_LETTER_CODE = __normalize_map(NAME_TO_TWO_LETTER_CODE)
NAME_TO_TREE_LETTER_CODE = __normalize_map(NAME_TO_TREE_LETTER_CODE)

__populate_map_fallbacks(NAME_TO_TWO_LETTER_CODE, NAME_TO_TREE_LETTER_CODE)
__populate_map_fallbacks(NAME_TO_TREE_LETTER_CODE, NAME_TO_TWO_LETTER_CODE, True)

TWO_LETTER_CODE_TO_NAME: Dict[str, str] = __reverse_map(NAME_TO_TWO_LETTER_CODE)
TREE_LETTER_CODE_TO_NAME: Dict[str, str] = __reverse_map(NAME_TO_TREE_LETTER_CODE)


class Language:

    basque: "Language"
    belarusian: "Language"
    bulgarian: "Language"
    catalan: "Language"
    central_khmer: "Language"
    chichewa: "Language"
    chinese: "Language"
    dutch: "Language"
    english: "Language"
    french: "Language"
    galician: "Language"
    german: "Language"
    hawaiian: "Language"
    hindi: "Language"
    hmong: "Language"
    hungarian: "Language"
    inuktitut: "Language"
    italian: "Language"
    japanese: "Language"
    kalaallisut: "Language"
    kirghiz: "Language"
    konkani: "Language"
    kurdish: "Language"
    luganda: "Language"
    mongolian: "Language"
    montenegrin: "Language"
    ndonga: "Language"
    norwegian: "Language"
    oriya: "Language"
    persian: "Language"
    portuguese: "Language"
    punjabi: "Language"
    rundi: "Language"
    serbian: "Language"
    sinhala: "Language"
    spanish: "Language"

    unknown: "Language"

    def __init__(self, name: str, two_letter_code: str = None, three_letter_code: str = None, standard: bool = True) -> None:
        assert name
        name = normalize_text(name)
        if standard:
            if two_letter_code and two_letter_code != NAME_TO_TWO_LETTER_CODE.get(name):
                if RAISE_EXCEPTION_IF_INVALID_STANDARD:
                    raise Exception('Wrong two letter code specified for name "%s": %s' % (name, two_letter_code))
                else:
                    logger.fatal('Wrong two letter code specified for name "%s": %s' % (name, two_letter_code))
            if three_letter_code and three_letter_code != NAME_TO_TREE_LETTER_CODE.get(name):
                if RAISE_EXCEPTION_IF_INVALID_STANDARD:
                    raise Exception('Wrong three letter code specified for name "%s": %s' % (name, three_letter_code))
                else:
                    logger.fatal('Wrong three letter code specified for name "%s": %s' %
                                 (name, three_letter_code))
            if not two_letter_code:
                two_letter_code = NAME_TO_TWO_LETTER_CODE.get(name)
            if not three_letter_code:
                three_letter_code = NAME_TO_TREE_LETTER_CODE.get(name)
            if not two_letter_code or not three_letter_code:
                if RAISE_EXCEPTION_IF_INVALID_STANDARD:
                    raise Exception('Could not resolve language codes for name "%s"' % name)
                else:
                    logger.fatal('Could not resolve language codes for name "%s"' % name)
        self.name: str = name
        self.two_letter_code: str = two_letter_code or three_letter_code
        self.three_letter_code: str = three_letter_code or two_letter_code

    def __eq__(self, other) -> bool:
        if not isinstance(other, Language):
            return False
        return self.name == other.name \
            and self.two_letter_code == other.two_letter_code \
            and self.three_letter_code == other.three_letter_code

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return "%s [%s:%s]" % (self.name, self.two_letter_code, self.three_letter_code)

    def __repr__(self) -> str:
        return "%s(name=%s, 2lc=%s, 3lc=%s)" % (type(self).__name__, self.name, self.two_letter_code, self.three_letter_code)

    def has_name(self, name: str) -> bool:
        return self.name == normalize_text(name)

    def has_code(self, code: str) -> bool:
        return self.two_letter_code == code or self.three_letter_code == code

    @staticmethod
    def from_standard_name(name: str) -> "Language":
        try:
            return Language(name)
        except Exception as e:
            return None

    @staticmethod
    def from_two_letter_code(two_letter_code: str) -> "Language":
        assert two_letter_code
        name = TWO_LETTER_CODE_TO_NAME.get(
            two_letter_code) or TREE_LETTER_CODE_TO_NAME.get(two_letter_code)
        return Language(name) if name else Language.unknown

    @staticmethod
    def from_three_letter_code(three_letter_code: str) -> "Language":
        assert three_letter_code
        name = TREE_LETTER_CODE_TO_NAME.get(
            three_letter_code) or TWO_LETTER_CODE_TO_NAME.get(three_letter_code)
        return Language(name) if name else Language.unknown


Language.basque = Language("Basque")
Language.belarusian = Language("Belarusian")
Language.bulgarian = Language("Bulgarian")
Language.catalan = Language("Catalan")
Language.central_khmer = Language("Central Khmer")
Language.chichewa = Language("Chichewa")
Language.chinese = Language("Chinese")
Language.dutch = Language("Dutch")
Language.english = Language("English")
Language.french = Language("French")
Language.galician = Language("Galician")
Language.german = Language("German")
Language.hawaiian = Language("Hawaiian")
Language.hindi = Language("Hindi")
Language.hmong = Language("Hmong")
Language.hungarian = Language("Hungarian")
Language.inuktitut = Language("Inuktitut")
Language.italian = Language("Italian")
Language.japanese = Language("Japanese")
Language.kalaallisut = Language("Kalaallisut")
Language.kirghiz = Language("Kirghiz")
Language.konkani = Language("Konkani")
Language.kurdish = Language("Kurdish")
Language.luganda = Language("Luganda")
Language.mongolian = Language("Mongolian")
Language.montenegrin = Language("Montenegrin")
Language.ndonga = Language("Ndonga")
Language.norwegian = Language("Norwegian")
Language.oriya = Language("Oriya")
Language.persian = Language("Persian")
Language.portuguese = Language("Portuguese")
Language.punjabi = Language("Punjabi")
Language.rundi = Language("Rundi")
Language.serbian = Language("Serbian")
Language.sinhala = Language("Sinhala")
Language.spanish = Language("Spanish")

Language.unknown = Language("Unknown", "xx", "xxx", False)
