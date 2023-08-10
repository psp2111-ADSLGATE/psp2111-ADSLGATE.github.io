# -*- coding: utf-8 -*-
from modules.kodi_utils import local_string as ls

years_movies = [
2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995,
1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966,
1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937,
1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1921, 1920, 1919, 1918, 1917, 1916, 1915, 1914, 1913, 1912, 1911, 1910, 1909, 1908,
1907, 1906, 1905, 1904, 1903, 1902, 1901, 1900
	]

years_tvshows = [
2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995,
1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966,
1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942
	]

decades_movies = [
2020, 2010, 2000, 1990, 1980, 1970, 1960, 1950, 1940, 1930, 1920, 1910, 1900
	]

decades_tvshows = [
2020, 2010, 2000, 1990, 1980, 1970, 1960, 1950, 1940
	]

oscar_winners = (
(545611, 776503, 581734, 496243, 490132, 399055, 376867, 314365, 194662, 76203, 68734, 74643, 45269, 12162, 12405, 6977, 1422, 1640, 70, 122),
(1574, 453, 98, 14, 1934, 597, 409, 197, 13, 424, 33, 274, 581, 403, 380, 746, 792, 606, 279, 11050),
(783, 9443, 16619, 12102, 11778, 703, 1366, 510, 240, 9277, 238, 1051, 11202, 3116, 17917, 10633, 874, 15121, 11113, 5769),
(947, 1725, 284, 665, 17281, 826, 2897, 15919, 654, 11426, 27191, 2769, 705, 25430, 23383, 33667, 887, 28580, 17661, 27367),
(289, 43266, 223, 770, 34106, 43278, 43277, 12311, 3078, 56164, 33680, 42861, 143, 65203, 28966, 631)
	)

movie_certifications = [
'G',
'PG',
'PG-13',
'R',
'NC-17',
'NR'
	]

tvshow_certifications = [
'tv-y',
'tv-y7',
'tv-g',
'tv-pg',
'tv-14',
'tv-ma'
	]

languages = [
(ls(32861), 'ar'), (ls(32862), 'bs'),   (ls(32863), 'bg'),   (ls(32864), 'zh'),   (ls(32865), 'hr'),   (ls(32866), 'nl'),   (ls(32867), 'en'),
(ls(32868), 'fi'), (ls(32869), 'fr'),   (ls(32870), 'de'),   (ls(32871), 'el'),   (ls(32872), 'he'),   (ls(32873), 'hi'),   (ls(32874), 'hu'),
(ls(32875), 'is'), (ls(32876), 'it'),   (ls(32877), 'ja'),   (ls(32878), 'ko'),   (ls(32879), 'mk'),   (ls(32880), 'no'),   (ls(32881), 'fa'),
(ls(32882), 'pl'), (ls(32883), 'pt'),   (ls(32884), 'pa'),   (ls(32885), 'ro'),   (ls(32886), 'ru'),   (ls(32887), 'sr'),   (ls(32888), 'sl'),
(ls(32889), 'es'), (ls(32890), 'sv'),   (ls(32891), 'tr'),   (ls(32892), 'uk')
	]

meta_languages = [
{'iso': 'zh', 'name': 'Chinese'},          {'iso': 'hr', 'name': 'Croatian'},
{'iso': 'cs', 'name': 'Czech'},            {'iso': 'da', 'name': 'Danish'},
{'iso': 'nl', 'name': 'Dutch'},            {'iso': 'en', 'name': 'English'},
{'iso': 'fi', 'name': 'Finnish'},          {'iso': 'fr', 'name': 'French'},
{'iso': 'de', 'name': 'German'},           {'iso': 'el', 'name': 'Greek'},
{'iso': 'he', 'name': 'Hebrew'},           {'iso': 'hu', 'name': 'Hungarian'},
{'iso': 'it', 'name': 'Italian'},          {'iso': 'ja', 'name': 'Japanese'},
{'iso': 'ko', 'name': 'Korean'},           {'iso': 'no', 'name': 'Norwegian'},
{'iso': 'pl', 'name': 'Polish'},           {'iso': 'pt', 'name': 'Portuguese'},
{'iso': 'ru', 'name': 'Russian'},          {'iso': 'sl', 'name': 'Slovenian'},
{'iso': 'es', 'name': 'Spanish'},          {'iso': 'sv', 'name': 'Swedish'},
{'iso': 'tr', 'name': 'Turkish'},          {'iso': 'ar-SA', 'name': 'Arabic Saudi Arabia'}
	]

language_choices =  {
'None': 'None',              'Afrikaans': 'afr',            'Albanian': 'alb',             'Arabic': 'ara',
'Armenian': 'arm',           'Basque': 'baq',               'Bengali': 'ben',              'Bosnian': 'bos',
'Breton': 'bre',             'Bulgarian': 'bul',            'Burmese': 'bur',              'Catalan': 'cat',
'Chinese': 'chi',            'Croatian': 'hrv',             'Czech': 'cze',                'Danish': 'dan',
'Dutch': 'dut',              'English': 'eng',              'Esperanto': 'epo',            'Estonian': 'est',
'Finnish': 'fin',            'French': 'fre',               'Galician': 'glg',             'Georgian': 'geo',
'German': 'ger',             'Greek': 'ell',                'Hebrew': 'heb',               'Hindi': 'hin',
'Hungarian': 'hun',          'Icelandic': 'ice',            'Indonesian': 'ind',           'Italian': 'ita',
'Japanese': 'jpn',           'Kazakh': 'kaz',               'Khmer': 'khm',                'Korean': 'kor',
'Latvian': 'lav',            'Lithuanian': 'lit',           'Luxembourgish': 'ltz',        'Macedonian': 'mac',
'Malay': 'may',              'Malayalam': 'mal',            'Manipuri': 'mni',             'Mongolian': 'mon',
'Montenegrin': 'mne',        'Norwegian': 'nor',            'Occitan': 'oci',              'Persian': 'per',
'Polish': 'pol',             'Portuguese': 'por',           'Portuguese(Brazil)': 'pob',   'Romanian': 'rum',
'Russian': 'rus',            'Serbian': 'scc',              'Sinhalese': 'sin',            'Slovak': 'slo',
'Slovenian': 'slv',          'Spanish': 'spa',              'Swahili': 'swa',              'Swedish': 'swe',
'Syriac': 'syr',             'Tagalog': 'tgl',              'Tamil': 'tam',                'Telugu': 'tel',
'Thai': 'tha',               'Turkish': 'tur',              'Ukrainian': 'ukr',            'Urdu': 'urd',
'Vietnamese': 'vie'
	}

regions = [
{'code': 'AF', 'name': ls(32893)},   {'code': 'AL', 'name': ls(32894)},   {'code': 'DZ', 'name': ls(32895)},   {'code': 'AQ', 'name': ls(32896)},
{'code': 'AR', 'name': ls(32897)},   {'code': 'AM', 'name': ls(32898)},   {'code': 'AU', 'name': ls(32899)},   {'code': 'AT', 'name': ls(32900)},
{'code': 'BD', 'name': ls(32901)},   {'code': 'BY', 'name': ls(32902)},   {'code': 'BE', 'name': ls(32903)},   {'code': 'BR', 'name': ls(32904)},
{'code': 'BG', 'name': ls(32905)},   {'code': 'KH', 'name': ls(32906)},   {'code': 'CA', 'name': ls(32907)},   {'code': 'CL', 'name': ls(32908)},
{'code': 'CN', 'name': ls(32909)},   {'code': 'HR', 'name': ls(32910)},   {'code': 'CZ', 'name': ls(32911)},   {'code': 'DK', 'name': ls(32912)},
{'code': 'EG', 'name': ls(32913)},   {'code': 'FI', 'name': ls(32914)},   {'code': 'FR', 'name': ls(32915)},   {'code': 'DE', 'name': ls(32916)},
{'code': 'GR', 'name': ls(32917)},   {'code': 'HK', 'name': ls(32918)},   {'code': 'HU', 'name': ls(32919)},   {'code': 'IS', 'name': ls(32920)},
{'code': 'IN', 'name': ls(32921)},   {'code': 'ID', 'name': ls(32922)},   {'code': 'IR', 'name': ls(32923)},   {'code': 'IQ', 'name': ls(32924)},
{'code': 'IE', 'name': ls(32925)},   {'code': 'IL', 'name': ls(32926)},   {'code': 'IT', 'name': ls(32927)},   {'code': 'JP', 'name': ls(32928)},
{'code': 'MY', 'name': ls(32929)},   {'code': 'NP', 'name': ls(32930)},   {'code': 'NL', 'name': ls(32931)},   {'code': 'NZ', 'name': ls(32932)},
{'code': 'NO', 'name': ls(32933)},   {'code': 'PK', 'name': ls(32934)},   {'code': 'PY', 'name': ls(32935)},   {'code': 'PE', 'name': ls(32936)},
{'code': 'PH', 'name': ls(32937)},   {'code': 'PL', 'name': ls(32938)},   {'code': 'PT', 'name': ls(32939)},   {'code': 'PR', 'name': ls(32940)},
{'code': 'RO', 'name': ls(32941)},   {'code': 'RU', 'name': ls(32942)},   {'code': 'SA', 'name': ls(32943)},   {'code': 'RS', 'name': ls(32944)},
{'code': 'SG', 'name': ls(32945)},   {'code': 'SK', 'name': ls(32946)},   {'code': 'SI', 'name': ls(32947)},   {'code': 'ZA', 'name': ls(32948)},
{'code': 'ES', 'name': ls(32949)},   {'code': 'LK', 'name': ls(32950)},   {'code': 'SE', 'name': ls(32951)},   {'code': 'CH', 'name': ls(32952)},
{'code': 'TH', 'name': ls(32953)},   {'code': 'TR', 'name': ls(32954)},   {'code': 'UA', 'name': ls(32955)},   {'code': 'AE', 'name': ls(32956)},
{'code': 'GB', 'name': ls(32957)},   {'code': 'US', 'name': ls(32958)},   {'code': 'UY', 'name': ls(32959)},   {'code': 'VE', 'name': ls(32960)},
{'code': 'VN', 'name': ls(32961)},   {'code': 'YE', 'name': ls(32962)},   {'code': 'ZW', 'name': ls(32963)}
	]

movie_genres = {
ls(32548): ['28', 'genre_action'],                ls(32549): ['12', 'genre_adventure'],
ls(32550): ['16', 'genre_animation'],             ls(32551): ['35', 'genre_comedy'],
ls(32552): ['80', 'genre_crime'],                 ls(32553): ['99', 'genre_documentary'],
ls(32554): ['18', 'genre_drama'],                 ls(32555): ['10751', 'genre_family'],
ls(32558): ['14', 'genre_fantasy'],               ls(32559): ['36', 'genre_history'],
ls(32560): ['27', 'genre_horror'],                ls(32561): ['10402', 'genre_music'],
ls(32557): ['9648', 'genre_mystery'],             ls(32562): ['10749', 'genre_romance'],
ls(32563): ['878', 'genre_scifi'],                ls(32564): ['10770', 'genre_soap'],
ls(32565): ['53', 'genre_thriller'],              ls(32566): ['10752', 'genre_war'], 
ls(32567): ['37', 'genre_western']
	}

tvshow_genres = {
'%s & %s' % (ls(32548), ls(32549)): ['10759', 'genre_action'],         ls(32550): ['16', 'genre_animation'],
ls(32551): ['35', 'genre_comedy'],                                     ls(32552): ['80', 'genre_crime'],
ls(32553): ['99', 'genre_documentary'],                                ls(32554): ['18', 'genre_drama'],
ls(32555): ['10751', 'genre_family'],                                  ls(32556): ['10762', 'genre_kids'],
ls(32557): ['9648', 'genre_mystery'],                                  ls(32568):['10763', 'genre_news'],
ls(32569): ['10764', 'genre_reality'],                                 ls(33057): ['10765', 'genre_scifi'],
ls(32570): ['10766', 'genre_soap'],                                    ls(32570): ['10767', 'genre_talk'],
ls(32572): ['10768', 'genre_war'],                                     ls(32567): ['37', 'genre_western']
	}

networks = [
{'id':54,'name':'Disney Channel','logo': 'network_disney'},                   {'id':44,'name':'Disney XD','logo': 'network_disneyxd'},
{'id':2,'name':'ABC','logo': 'network_abc'},                                  {'id':493,'name':'BBC America','logo': 'network_bbcamerica'},
{'id':6,'name':'NBC','logo': 'network_nbc'},                                  {'id':13,'name':'Nickelodeon','logo': 'network_nickelodeon'},
{'id':14,'name':'PBS','logo': 'network_pbs'},                                 {'id':16,'name':'CBS','logo': 'network_cbs'},
{'id':19,'name':'FOX','logo': 'network_fox'},                                 {'id':21,'name':'The WB','logo': 'network_thewb'},
{'id':24,'name':'BET','logo': 'network_bet'},                                 {'id':30,'name':'USA Network','logo': 'network_usanetwork'},
{'id':23,'name':'CBC','logo': 'network_cbc'},                                 {'id': 88, 'name': 'FX', 'logo': 'network_fx'},
{'id':33,'name':'MTV','logo': 'network_mtv'},                                 {'id':34,'name':'Lifetime','logo': 'network_lifetime'},
{'id':35,'name':'Nick Junior','logo': 'network_nickjr'},                      {'id':41,'name':'TNT','logo': 'network_tnt'},
{'id':43,'name':'National Geographic','logo': 'network_natgeo'},              {'id':47,'name':'Comedy Central','logo': 'network_comedycentral'},
{'id':49,'name':'HBO','logo': 'network_hbo'},                                 {'id':55,'name':'Spike','logo': 'network_spike'},
{'id':67,'name':'Showtime','logo': 'network_showtime'},                       {'id':56,'name':'Cartoon Network','logo': 'network_cartoonnetwork'},
{'id':65,'name':'History Channel','logo': 'network_history'},                 {'id':84,'name':'TLC','logo': 'network_tlc'},
{'id':68,'name':'TBS','logo': 'network_tbs'},                                 {'id':71,'name':'The CW','logo': 'network_thecw'},
{'id':74,'name':'Bravo','logo': 'network_bravo'},                             {'id':76,'name':'E!','logo': 'network_e'},
{'id':77,'name':'Syfy','logo': 'network_syfy'},                               {'id':80,'name':'Adult Swim','logo': 'network_adultswim'},
{'id':91,'name':'Animal Planet','logo': 'network_animalplanet'},              {'id':110,'name':'CTV','logo': 'network_ctv'},
{'id':129,'name':'A&E','logo': 'network_ane'},                                {'id':158,'name':'VH1','logo': 'network_vh1'},
{'id':174,'name':'AMC','logo': 'network_amc'},                                {'id':928,'name':'Crackle','logo': 'network_crackle'},
{'id':202,'name':'WGN America','logo': 'network_wgnamerica'},                 {'id':209,'name':'Travel Channel','logo': 'network_travel'},
{'id':213, 'name':'Netflix','logo': 'network_netflix'},                       {'id':251,'name':'Audience','logo': 'network_audience'},
{'id':270,'name':'SundanceTV','logo': 'network_sundancetv'},                  {'id':318,'name':'Starz','logo': 'network_starz'},
{'id':359,'name':'Cinemax','logo': 'network_cinemax'},                        {'id':364,'name':'truTV','logo': 'network_trutv'},
{'id':384,'name':'Hallmark Channel','logo': 'network_hallmark'},              {'id':397,'name':'TV Land','logo': 'network_tvland'},
{'id':1024,'name':'Amazon','logo': 'network_amazon'},                         {'id':1267,'name':'Freeform','logo': 'network_freeform'},
{'id':4,'name':'BBC 1','logo': 'network_bbc1'},                               {'id':332,'name':'BBC 2','logo': 'network_bbc2'},
{'id':3,'name':'BBC 3','logo': 'network_bbc3'},                               {'id':100,'name':'BBC 4','logo': 'network_bbc4'},
{'id':214,'name':'Sky 1','logo': 'network_sky1'},                             {'id':9,'name':'ITV','logo': 'network_itv'},
{'id':26,'name':'Channel 4','logo': 'network_channel4'},                      {'id':99,'name':'Channel 5','logo': 'network_channel5'},
{'id':136,'name':'E4','logo': 'network_e4'},                                  {'id':210,'name':'HGTV','logo': 'network_hgtv'},
{'id':453,'name':'Hulu','logo': 'network_hulu'},                              {'id':1436,'name':'YouTube Red','logo': 'network_youtubered'},
{'id':64,'name':'Discovery Channel','logo': 'network_discovery'},             {'id':2739,'name':'Disney+','logo': 'network_disneyplus'},
{'id':2552,'name':'Apple TV +','logo': 'network_appletvplus'},                {'id':2697,'name':'Acorn TV','logo': 'network_acorntv'},
{'id':1709,'name':'CBS All Access','logo': 'network_cbsallaccess'},           {'id':3186,'name':'HBO Max','logo': 'network_hbomax'},
{'id':2243,'name':'DC Universe','logo': 'network_dcuniverse'},                {'id':2076,'name':'Paramount Network','logo': 'network_paramount'},
{'id':4330,'name':'Paramount+','logo': 'network_paramountplus'},              {'id': 3353, 'name': 'Peacock', 'logo': 'network_peacock'},
{'id':4353,'name':'Discovery+','logo': 'network_discoveryplus'},              {'id': 132, 'name': 'Oxygen', 'logo': 'network_oxygen'},
{'id': 244, 'name': 'Discovery ID', 'logo': 'network_discoveryid'}
	]

watch_providers = [
{'name': 'Netflix', 'id': 8, 'logo': 't2yyOv40HZeVlLjYsCsPHnWLk4W.jpg'},                     {'name': 'Amazon Prime Video', 'id': 9, 'logo': 'emthp39XA2YScoYL1p0sdbAH2WA.jpg'},
{'name': 'Disney Plus', 'id': 337, 'logo': '7rwgEs15tFwyR9NPQ5vpzxTj19Q.jpg'},               {'name': 'Google Play Movies', 'id': 3, 'logo': 'tbEdFQDwx5LEVr8WpSeXQSIirVq.jpg'},
{'name': 'Sun Nxt', 'id': 309, 'logo': 'uW4dPCcbXaaFTyfL5HwhuDt5akK.jpg'},                   {'name': 'Apple TV', 'id': 2, 'logo': 'peURlLlr8jggOwK53fJ5wdQl05y.jpg'},
{'name': 'MUBI', 'id': 11, 'logo': 'bVR4Z1LCHY7gidXAJF5pMa4QrDS.jpg'},                       {'name': 'Apple TV Plus', 'id': 350, 'logo': '6uhKBfmtzFqOcLousHwZuzcrScK.jpg'},
{'name': 'fuboTV', 'id': 257, 'logo': 'jPXksae158ukMLFhhlNvzsvaEyt.jpg'},                    {'name': 'Classix', 'id': 445, 'logo': 'iaMw6nOyxUzXSacrLQ0Au6CfZkc.jpg'},
{'name': 'Hulu', 'id': 15, 'logo': 'zxrVdFjIjLqkfnwyghnfywTn3Lh.jpg'},                       {'name': 'Curiosity Stream', 'id': 190, 'logo': '67Ee4E6qOkQGHeUTArdJ1qRxzR2.jpg'},
{'name': 'Paramount Plus', 'id': 531, 'logo': 'xbhHHa1YgtpwhC8lb1NQ3ACVcLd.jpg'},            {'name': 'GuideDoc', 'id': 100, 'logo': 'iX0pvJ2GFATbVIH5IHMwG0ffIdV.jpg'},
{'name': 'Public Domain Movies', 'id': 638, 'logo': 'liEIj6CkvojVDiMWeexGvflSPZT.jpg'},      {'name': 'HBO Max', 'id': 384, 'logo': 'Ajqyt5aNxNGjmF9uOfxArGrdf3X.jpg'},
{'name': 'Netflix Kids', 'id': 175, 'logo': 'j2OLGxyy0gKbPVI0DYFI2hJxP6y.jpg'},              {'name': 'Eventive', 'id': 677, 'logo': 'fadQYOyKL0tqfyj012nYJxm3N2I.jpg'},
{'name': 'Spamflix', 'id': 521, 'logo': 'xN97FFkFAdY1JvHhS4zyPD4URgD.jpg'},                  {'name': 'AMC+', 'id': 526, 'logo': 'xlonQMSmhtA2HHwK3JKF9ghx7M8.jpg'},
{'name': 'Cultpix', 'id': 692, 'logo': '59azlQKUgFdYq6QI5QEAxIeecyL.jpg'},                   {'name': 'DOCSVILLE', 'id': 475, 'logo': 'bvcdVO7SDHKEa6D40g1jntXKNj.jpg'},
{'name': 'Peacock', 'id': 386, 'logo': '8VCV78prwd9QzZnEm0ReO6bERDa.jpg'},                   {'name': 'VIX ', 'id': 457, 'logo': '58aUMVWJRolhWpi4aJCkGHwfKdg.jpg'},
{'name': 'FilmBox+', 'id': 701, 'logo': '4FqTBYsUSZgS9z9UGKgxSDBbtc8.jpg'},                  {'name': 'Peacock Premium', 'id': 387, 'logo': 'xTHltMrZPAJFLQ6qyCBjAnXSmZt.jpg'},
{'name': 'aha', 'id': 532, 'logo': 'm3NWxxR23l1w1e156fyTuw931gx.jpg'},                       {'name': 'Amazon Video', 'id': 10, 'logo': '5NyLm42TmCqCMOZFvH4fcoSNKEW.jpg'},
{'name': 'Kocowa', 'id': 464, 'logo': 'xfAAOAERZCnPB5jW5lhboAcXk8L.jpg'},                    {'name': 'WOW Presents Plus', 'id': 546, 'logo': 'mgD0T960hnYU4gBxbPPBrcDfgWg.jpg'},
{'name': 'Takflix', 'id': 1771, 'logo': 'cnIHBy3uLWhHRR7VeWQhK3ZsYP0.jpg'},                  {'name': 'Crunchyroll', 'id': 283, 'logo': '8Gt1iClBlzTeQs8WQm8UrCoIxnQ.jpg'},
{'name': 'YouTube', 'id': 192, 'logo': 'oIkQkEkwfmcG7IGpRR1NB8frZZM.jpg'},                   {'name': 'Magellan TV', 'id': 551, 'logo': 'gekkP93StjYdiMAInViVmrnldNY.jpg'},
{'name': 'BroadwayHD', 'id': 554, 'logo': 'xLu1rkZNOKuNnRNr70wySosfTBf.jpg'},                {'name': 'KoreaOnDemand', 'id': 575, 'logo': 'uHv6Y4YSsr4cj7q4cBbAg7WXKEI.jpg'},
{'name': 'Dekkoo', 'id': 444, 'logo': 'u2H29LCxRzjZVUoZUQAHKm5P8Zc.jpg'},                    {'name': 'Starz Apple TV', 'id': 1855, 'logo': 'hB24bAA8Y2ei6pbEGuCNdKUOjxI.jpg'},
{'name': 'Filmzie', 'id': 559, 'logo': 'olmH7t5tEng8Yuq33KmvpvaaVIg.jpg'},                   {'name': 'Showtime Apple TV', 'id': 675, 'logo': 'xVN3LKkOtCrlFT9mavhkx8SzMwV.jpg'},
{'name': 'True Story', 'id': 567, 'logo': 'osREemsc9uUB2J8VTkQeAVk2fu9.jpg'},                {'name': 'AMC Plus Apple TV ', 'id': 1854, 'logo': 'yFgm7vxwKZ4jfXIlPizlgoba2yi.jpg'},
{'name': 'DocAlliance Films', 'id': 569, 'logo': 'aQ1ritN00jXc7RAFfUoQKGAAfp7.jpg'},         {'name': 'Britbox Apple TV ', 'id': 1852, 'logo': 'cN85Wjk0FIFr3z6rbiimz10uWVo.jpg'},
{'name': 'Hoichoi', 'id': 315, 'logo': 'd4vHcXY9rwnr763wQns2XJThclt.jpg'},                   {'name': 'BritBox', 'id': 151, 'logo': 'aGIS8maihUm60A3moKYD9gfYHYT.jpg'},
{'name': 'Pluto TV', 'id': 300, 'logo': 't6N57S17sdXRXmZDAkaGP0NHNG0.jpg'},                  {'name': 'Starz', 'id': 43, 'logo': 'eWp5LdR4p4uKL0wACBBXapDV2lB.jpg'},
{'name': 'Rakuten Viki', 'id': 344, 'logo': 'qjtOUIUnk4kRpcZmaddjqDHM0dR.jpg'},              {'name': 'Discovery Plus Amazon', 'id': 584, 'logo': 'a2OcajC4bM5ItniQdjyOV7tgthW.jpg'},
{'name': 'iQIYI', 'id': 581, 'logo': '8MXYXzZGoPAEQU13GWk1GVvKNUS.jpg'},                     {'name': 'Showtime Amazon', 'id': 203, 'logo': 'zoL69abPHiVC1Qzd4kM6hwLSo0j.jpg'},
{'name': 'AMC+ Amazon', 'id': 528, 'logo': '9edKQczyuMmQM1yS520hgmJbcaC.jpg'},               {'name': 'Funimation Now', 'id': 269, 'logo': 'fWq61Fy4onav0wZJTA3c2fs0G66.jpg'},
{'name': 'The Roku Channel', 'id': 207, 'logo': 'z0h7mBHwm5KfMB2MKeoQDD2ngEZ.jpg'},          {'name': 'Showtime Roku Premium', 'id': 632, 'logo': 'qMf2zirM2w0sO0mdAIIoP5XnQn8.jpg'},
{'name': 'Runtime', 'id': 1875, 'logo': 'nvCfpn94VKJN4ZpkDgoupJWlXqq.jpg'},                  {'name': 'AMC+ Roku Premium', 'id': 635, 'logo': 'ni2NgPmIqqJRXeiA8Zdj4UhBZnU.jpg'},
{'name': 'YouTube Premium', 'id': 188, 'logo': '6IPjvnYl6WWkIwN158qBFXCr2Ne.jpg'},           {'name': 'YouTube Free', 'id': 235, 'logo': '4SCmZgf7AeJLKKRPcbf5VFkGpBj.jpg'},
{'name': 'Hoopla', 'id': 212, 'logo': 'aJ0b9BLU1Cvv5hIz9fEhKKc1x1D.jpg'},                    {'name': 'The CW', 'id': 83, 'logo': '6Y6w3F5mYoRHCcNAG0ZD2AndLJ2.jpg'},
{'name': 'Vudu', 'id': 7, 'logo': '21dEscfO8n1tL35k4DANixhffsR.jpg'},                        {'name': 'Starz Roku Premium', 'id': 634, 'logo': '5OAb2w7D9C2VHa0k5PaoAYeFYFE.jpg'},
{'name': 'VUDU Free', 'id': 332, 'logo': 'xzfVRl1CgJPYa9dOoyVI3TDSQo2.jpg'},                 {'name': 'Criterion Channel', 'id': 258, 'logo': '4TJTNWd2TT1kYj6ocUEsQc8WRgr.jpg'},
{'name': 'Showtime', 'id': 37, 'logo': '4kL33LoKd99YFIaSOoOPMQOSw1A.jpg'},                   {'name': 'PBS', 'id': 209, 'logo': 'bbxgdl6B5T75wJE713BiTCIBXyS.jpg'},
{'name': 'FXNow', 'id': 123, 'logo': 'twV9iQPYeaoBzwsfRFGMGoMIUg8.jpg'},                     {'name': 'Pantaflix', 'id': 177, 'logo': '2tAjxjo1n3H7fsXqMsxWFMeFUWp.jpg'},
{'name': 'Tubi TV', 'id': 73, 'logo': 'w2TDH9TRI7pltf5LjN3vXzs7QbN.jpg'},                    {'name': 'Kanopy', 'id': 191, 'logo': 'wbCleYwRFpUtWcNi7BLP3E1f6VI.jpg'},
{'name': 'Comedy Central', 'id': 243, 'logo': 'gmU9aPV3XUFusVs4kK1rcICUKqL.jpg'},            {'name': 'Microsoft Store', 'id': 68, 'logo': 'shq88b09gTBYC4hA7K7MUL8Q4zP.jpg'},
{'name': 'Redbox', 'id': 279, 'logo': 'gbyLHzl4eYP0oP9oJZ2oKbpkhND.jpg'},                    {'name': 'ABC', 'id': 148, 'logo': 'l9BRdAgQ3MkooOalsuu3yFQv2XP.jpg'},
{'name': 'Crackle', 'id': 12, 'logo': '7P2JHkfv4AmU2MgSPGaJ0z6nNLG.jpg'},                    {'name': 'DIRECTV', 'id': 358, 'logo': 'xL9SUR63qrEjFZAhtsipskeAMR7.jpg'},
{'name': 'Fandor', 'id': 25, 'logo': 'eAhAUvV2ouai3cGti5y70YOtrBN.jpg'},                     {'name': 'MGM Plus', 'id': 34, 'logo': '6A1gRIJqLfFHOoTvbTxDAbuU2nQ.jpg'},
{'name': 'Freeform', 'id': 211, 'logo': 'rgpmwMkXqFYch9cway9qWMw0uXu.jpg'},                  {'name': 'Syfy', 'id': 215, 'logo': 'f7iqKjWYdVoYVIvKP3nboULcrM2.jpg'},
{'name': 'Lifetime', 'id': 157, 'logo': '3wJNOOCbvqi7fJAdgf1QpL7Wwe2.jpg'},                  {'name': 'realeyz', 'id': 14, 'logo': '10BQc1kYmgjXFrFKb3xsRcDDn14.jpg'},
{'name': 'Shudder', 'id': 99, 'logo': 'pheENW1BxlexXX1CKJ4GyWudyMA.jpg'},                    {'name': 'Screambox', 'id': 185, 'logo': 'c2Ey5Q3uUjZgfWWQQIdVIjVfxE4.jpg'},
{'name': 'Acorn TV', 'id': 87, 'logo': '5P99DkK1jVs95KcE8bYG9MBtGQ.jpg'},                    {'name': 'Sundance Now', 'id': 143, 'logo': 'pZ9TSk3wlRYwiwwRxTsQJ7t2but.jpg'},
{'name': 'Popcornflix', 'id': 241, 'logo': 'olvOut34aWUFf1YoOqiqtjidiTK.jpg'},               {'name': 'Pantaya', 'id': 247, 'logo': '94IdHexespnJs96kmGiJlflfiwU.jpg'},
{'name': 'Boomerang', 'id': 248, 'logo': 'oRXiHzPl2HJMXXFR4eebsb8F5Oc.jpg'},                 {'name': 'Urban Movie Channel', 'id': 251, 'logo': '5uTsmZnDQmIOjZPEv8TNTy7GRJB.jpg'},
{'name': 'Dove Channel', 'id': 254, 'logo': 'cBCzPOX6ir5L8hCoJlfIWycxauh.jpg'},              {'name': 'History Vault', 'id': 268, 'logo': '3bm7P1O8WRqK6CYqfffJv4fba2p.jpg'},
{'name': 'Nickhits', 'id': 261, 'logo': 'oMwjMgYiT2jcR7ELqCH3TPzpgTX.jpg'},                  {'name': 'Eros Now', 'id': 218, 'logo': '4XYI2rzRm34skcvamytegQx7Dmu.jpg'},
{'name': 'Yupp TV', 'id': 255, 'logo': '8qNJcPBHZ4qewHrDJ7C7s2DBQ3V.jpg'},                   {'name': 'Magnolia Selects', 'id': 259, 'logo': 'foT1TtL67MgEOWR6Cib8dKyCvJI.jpg'},
{'name': 'WWE Network', 'id': 260, 'logo': 'rDYZ9v3Y09fuFyan51tHKE1mFId.jpg'},               {'name': 'Noggin', 'id': 262, 'logo': 'yxBUPUBFzHE72uFXvFr1l0fnMJA.jpg'},
{'name': 'Smithsonian Channel', 'id': 276, 'logo': 'UAZ2lJBWszijybQD4frqw2jxRO.jpg'},        {'name': 'Laugh Out Loud', 'id': 275, 'logo': 'w4GTJ1EDrgJku49XKSnRag9kKCT.jpg'},
{'name': 'Hallmark Movies', 'id': 281, 'logo': 'llEJ6av9kAniTQUR9hF9mhVbzlB.jpg'},           {'name': 'Pure Flix', 'id': 278, 'logo': 'orsVBNvPWxJNOVSEHMOk2h8R1wA.jpg'},
{'name': 'Lifetime Movie Club', 'id': 284, 'logo': 'p1v0UKH13xQsMjumRgCGmCdlgKm.jpg'},       {'name': 'Cinemax', 'id': 289, 'logo': 'kEnyHRflZPNWEOIXroZPhfdGi46.jpg'},
{'name': 'OVID', 'id': 433, 'logo': 'nXi2nRDPMNivJyFOifEa2t15Xuu.jpg'},                      {'name': 'Cohen Media Amazon', 'id': 1811, 'logo': 'jV7sSPzUYYHHmoATkD9PhFoEZXb.jpg'},
{'name': 'Viewster Amazon', 'id': 295, 'logo': 'mlH42JbZMrapSF6zc8iTYURcZlH.jpg'},           {'name': 'USA Network', 'id': 322, 'logo': 'ldU2RCgdvkcSEBWWbttCpVO450z.jpg'},
{'name': 'Sling TV Orange and Blue', 'id': 299, 'logo': 'tZ4xzOtCRHjAw7tYJphivEfDr1L.jpg'},  {'name': 'HiDive', 'id': 430, 'logo': '9baY98ZKyDaNArp1H9fAWqiR3Zi.jpg'},
{'name': 'Topic', 'id': 454, 'logo': 'ubWucXFn34TrVlJBaJFgPaC4tOP.jpg'},                     {'name': 'Night Flight Plus', 'id': 455, 'logo': 'ba8l0e5CkpVnrdFgzBySP7ckZnZ.jpg'},
{'name': 'Retrocrush', 'id': 446, 'logo': '9ONs8SMAXtkiyaEIKATTpbwckx8.jpg'},                {'name': 'Shout! Factory TV', 'id': 439, 'logo': 'ju3T8MFGNIoPiYpwHFpNlrYNyG7.jpg'},
{'name': 'Chai Flicks', 'id': 438, 'logo': '3tCqvc5hPm5nl8Hm8o2koDRZlPo.jpg'},               {'name': 'PBS Masterpiece Amazon', 'id': 294, 'logo': 'mMALQK52OFGoYUKOSCZILZkfGWs.jpg'},
{'name': 'The Film Detective', 'id': 470, 'logo': 'rOwEnT8oDSTZ5rDKmyaa3O4gUnc.jpg'},        {'name': 'MUBI Amazon', 'id': 201, 'logo': 'aJUiN18NZFbpSkHZQV1C1cTpz8H.jpg'},       
{'name': 'AcornTV Amazon', 'id': 196, 'logo': '8WWD7t5Irwq9kAH4rufQ4Pe1Dog.jpg'},            {'name': 'Screambox Amazon', 'id': 202, 'logo': 'naqM14qSfg2q0S2zDylM5zQQ3jn.jpg'},
{'name': 'Bet+ Amazon', 'id': 343, 'logo': 'obBJU4ak4XvAOUM5iVmSUxDvqC3.jpg'},               {'name': 'FlixFling', 'id': 331, 'logo': '4U02VrbgLfUKJAUCHKzxWFtnPx4.jpg'},
{'name': 'Darkmatter TV', 'id': 355, 'logo': 'x4AFz5koB2R8BRn8WNh6EqXUGHc.jpg'},             {'name': 'AMC on Demand', 'id': 352, 'logo': 'kJlVJLgbNPvKDYC0YMp3yA2OKq2.jpg'},
{'name': 'TCM', 'id': 361, 'logo': '8TbsXATKVD4Humjzi6a8SVaSY7o.jpg'},                       {'name': 'TNT', 'id': 363, 'logo': 'gJnQ40Z6T7HyY6fbmmI6qKE0zmK.jpg'},
{'name': 'BBC America', 'id': 397, 'logo': 'ukSXbR5qFjO2qCHpc6ZhcGPSjTJ.jpg'},               {'name': 'IndieFlix', 'id': 368, 'logo': '2NRn6OApVKfDTKLuHDRN8UadLRw.jpg'},
{'name': 'Here TV', 'id': 417, 'logo': 'sa10pK4Jwr5aA7rvafFP2zyLFjh.jpg'},                   {'name': 'Flix Premiere', 'id': 432, 'logo': '6fX0J6x7zXsUCvPFczgOW4oD34D.jpg'},
{'name': 'TBS', 'id': 506, 'logo': 'rcebVnRvZvPXauK4353Jgiu4DWI.jpg'},                       {'name': 'AsianCrush', 'id': 514, 'logo': '3VxDqUk25KU5860XxHKwV9cy3L8.jpg'},
{'name': 'FILMRISE', 'id': 471, 'logo': 'mEiBVz62M9j3TCebmOspMfqkIn.jpg'},                   {'name': 'Revry', 'id': 473, 'logo': 'r1UgUKmt83FSDOIHBdRWKooZPNx.jpg'},
{'name': 'Spectrum On Demand', 'id': 486, 'logo': '79mRAYq40lcYiXkQm6N7YErSSHd.jpg'},        {'name': 'VRV', 'id': 504, 'logo': 'rtTqPKRrVVXxvPV0T9OmSXhwXnY.jpg'},
{'name': 'Hi-YAH', 'id': 503, 'logo': 'mB2eDIncwSAlyl8WAtfV24qEIkk.jpg'},                    {'name': 'tru TV', 'id': 507, 'logo': 'pg4bIFyUsSIhFChqOz5Up1BxuIU.jpg'},
{'name': 'Discovery Plus', 'id': 520, 'logo': 'wYRiUqIgWcfUvO6OPcXuUNd4tc2.jpg'},            {'name': 'ARROW', 'id': 529, 'logo': '4UfmxLzph9Aso9pr9bXohp0V3sr.jpg'},
{'name': 'Plex', 'id': 538, 'logo': 'wDWvnupneMbY6RhBTHQC9zU0SCX.jpg'},                      {'name': 'Alamo on Demand', 'id': 547, 'logo': '1UP7ysjKolfD0rmp2fLmvyRHkdn.jpg'},
{'name': 'Dogwoof On Demand', 'id': 536, 'logo': '9sk88OAxDZSdMOzg8VuqtGpgWQ3.jpg'},         {'name': 'MovieSaints', 'id': 562, 'logo': 'fdWE8jpmQqkZrwg2ZMuCLz6ms5P.jpg'},
{'name': 'Film Movement Plus', 'id': 579, 'logo': 'tKJdVrC0fjEtQtYYjlVwX9rmqrj.jpg'},        {'name': 'Metrograph', 'id': 585, 'logo': '8PmpsrVDLJ3m8I37W6UNFEymhm7.jpg'},
{'name': 'Freevee', 'id': 613, 'logo': 'uBE4RMH15mrkuz6vXzuJc7ZLXp1.jpg'},                   {'name': 'Kino Now', 'id': 640, 'logo': 'ttxbDVmHMuNTKcSLOyIHFs7TdRh.jpg'},
{'name': 'ShortsTV Amazon', 'id': 688, 'logo': 'm0mvKlSjn38S9w7WVNV7a7XyPIe.jpg'},           {'name': 'Bet+', 'id': 1759, 'logo': 'eZVDDqlBHpuk8GELhQchRIkA6th.jpg'},
{'name': 'ESPN Plus', 'id': 1768, 'logo': 'iJBj5b4HYbjEPiwKJWQfcRr3nP2.jpg'},                {'name': 'Paramount+ Showtime', 'id': 1770, 'logo': 'vfUoancVnPRAxj8iBqhllanF0Eq.jpg'},
{'name': 'Klassiki', 'id': 1793, 'logo': 'fXGdolQR7QlHgdx2hPCxoVQG8eP.jpg'},                 {'name': 'Starz Amazon', 'id': 1794, 'logo': 'x36C6aseF5l4uX99Kpse9dbPwBo.jpg'},
{'name': 'Viaplay', 'id': 76, 'logo': 'cvl65OJnz14LUlC3yGK1KHj8UYs.jpg'},                    {'name': 'Popflick', 'id': 1832, 'logo': 'wbKHI2d5417yAAY7QestC3qnXyo.jpg'}
	]

media_lists = [
"'tmdb_movies%'",
"'tmdb_tv%'",
"'tmdb_popular_people%'",
"'tmdb_images_person%'",
"'tmdb_media%'",
"'tmdb_company%'",
"'trakt_movies%'",
"'trakt_tv%'",
"'trakt_trending_user_lists%'",
"'trakt_popular_user_lists%'",
"'imdb_%'",
"'tmdb_people%'",
"'imdb_keyword%'",
"'imdb_blunders%'",
"'fen_discover%'",
"'fen_FURK_T_FILE%'",
"'fen_pm_instant_transfer%'",
"'fen_rd_check_hash%'",
"'FEN_AD_%'",
"'FEN_RD_%'",
"'FEN_FOLDER_%'",
"'https%'"
	]