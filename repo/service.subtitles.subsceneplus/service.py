# -*- coding: utf-8 -*-

import os
import re
import requests
import ssl
from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter
import shutil
import sys
import six
import xbmcvfs
import time
from six.moves import urllib_parse
from kodi_six import xbmc, xbmcplugin, xbmcgui, xbmcaddon
from zipfile import ZipFile


class TLS12HttpAdapter(HTTPAdapter):
    """"Transport adapter that forces the use of TLS v1.2."""
    def init_poolmanager(self, connections, maxsize, block=False):
        tls = ssl.PROTOCOL_TLSv1_2 if six.PY3 else ssl.PROTOCOL_TLSv1
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=tls)


__addon__ = xbmcaddon.Addon()
__scriptid__ = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')

__cwd__ = xbmcvfs.translatePath(__addon__.getAddonInfo('path')) if six.PY3 else xbmc.translatePath(__addon__.getAddonInfo('path'))
__profile__ = xbmcvfs.translatePath(__addon__.getAddonInfo('profile')) if six.PY3 else xbmc.translatePath(__addon__.getAddonInfo('profile'))
__resource__ = xbmcvfs.translatePath(os.path.join(__cwd__, 'resources', 'lib')) if six.PY3 else xbmc.translatePath(os.path.join(__cwd__, 'resources', 'lib'))
__temp__ = xbmcvfs.translatePath(os.path.join(__profile__, 'temp', '')) if six.PY3 else xbmc.translatePath(os.path.join(__profile__, 'temp', ''))


BASE_URL = "https://subscene.best"

s = requests.Session()
s.mount("https://", TLS12HttpAdapter())
ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'
s.headers.update({'User-Agent': ua, 'Referer': BASE_URL + '/', 'Origin': BASE_URL})

if xbmcvfs.exists(__temp__):
    shutil.rmtree(__temp__)
xbmcvfs.mkdirs(__temp__)

sys.path.append(__resource__)

subscene_languages = {
    'Albanian': {'id': 1, '3let': 'alb', '2let': 'sq', 'name': 'Albanian'},
    'Arabic': {'id': 2, '3let': 'ara', '2let': 'ar', 'name': 'Arabic'},
    'Big 5 code': {'id': 3, '3let': 'chi', '2let': 'zh', 'name': 'Chinese'},
    'Brazillian Portuguese': {'id': 4, '3let': 'por', '2let': 'pb', 'name': 'Brazilian Portuguese'},
    'Bulgarian': {'id': 5, '3let': 'bul', '2let': 'bg', 'name': 'Bulgarian'},
    'Chinese BG code': {'id': 7, '3let': 'chi', '2let': 'zh', 'name': 'Chinese'},
    'Croatian': {'id': 8, '3let': 'hrv', '2let': 'hr', 'name': 'Croatian'},
    'Czech': {'id': 9, '3let': 'cze', '2let': 'cs', 'name': 'Czech'},
    'Danish': {'id': 10, '3let': 'dan', '2let': 'da', 'name': 'Danish'},
    'Dutch': {'id': 11, '3let': 'dut', '2let': 'nl', 'name': 'Dutch'},
    'English': {'id': 13, '3let': 'eng', '2let': 'en', 'name': 'English'},
    'Estonian': {'id': 16, '3let': 'est', '2let': 'et', 'name': 'Estonian'},
    'Farsi/Persian': {'id': 46, '3let': 'per', '2let': 'fa', 'name': 'Persian'},
    'Finnish': {'id': 17, '3let': 'fin', '2let': 'fi', 'name': 'Finnish'},
    'French': {'id': 18, '3let': 'fre', '2let': 'fr', 'name': 'French'},
    'German': {'id': 19, '3let': 'ger', '2let': 'de', 'name': 'German'},
    'Greek': {'id': 21, '3let': 'gre', '2let': 'el', 'name': 'Greek'},
    'Hebrew': {'id': 22, '3let': 'heb', '2let': 'he', 'name': 'Hebrew'},
    'Hungarian': {'id': 23, '3let': 'hun', '2let': 'hu', 'name': 'Hungarian'},
    'Icelandic': {'id': 25, '3let': 'ice', '2let': 'is', 'name': 'Icelandic'},
    'Indonesian': {'id': 44, '3let': 'ind', '2let': 'id', 'name': 'Indonesian'},
    'Italian': {'id': 26, '3let': 'ita', '2let': 'it', 'name': 'Italian'},
    'Japanese': {'id': 27, '3let': 'jpn', '2let': 'ja', 'name': 'Japanese'},
    'Korean': {'id': 28, '3let': 'kor', '2let': 'ko', 'name': 'Korean'},
    'Lithuanian': {'id': 43, '3let': 'lit', '2let': 'lt', 'name': 'Lithuanian'},
    'Malay': {'id': 50, '3let': 'may', '2let': 'ms', 'name': 'Malay'},
    'Norwegian': {'id': 30, '3let': 'nor', '2let': 'no', 'name': 'Norwegian'},
    'Polish': {'id': 31, '3let': 'pol', '2let': 'pl', 'name': 'Polish'},
    'Portuguese': {'id': 32, '3let': 'por', '2let': 'pt', 'name': 'Portuguese'},
    'Romanian': {'id': 33, '3let': 'rum', '2let': 'ro', 'name': 'Romanian'},
    'Russian': {'id': 34, '3let': 'rus', '2let': 'ru', 'name': 'Russian'},
    'Serbian': {'id': 35, '3let': 'scc', '2let': 'sr', 'name': 'Serbian'},
    'Slovak': {'id': 36, '3let': 'slo', '2let': 'sk', 'name': 'Slovak'},
    'Slovenian': {'id': 37, '3let': 'slv', '2let': 'sl', 'name': 'Slovenian'},
    'Spanish': {'id': 38, '3let': 'spa', '2let': 'es', 'name': 'Spanish'},
    'Swedish': {'id': 39, '3let': 'swe', '2let': 'sv', 'name': 'Swedish'},
    'Thai': {'id': 40, '3let': 'tha', '2let': 'th', 'name': 'Thai'},
    'Turkish': {'id': 41, '3let': 'tur', '2let': 'tr', 'name': 'Turkish'},
    'Vietnamese': {'id': 45, '3let': 'vie', '2let': 'vi', 'name': 'Vietnamese'}
}


def get_episode_pattern(episode):
    parts = episode.split(':')
    if len(parts) < 2:
        return "%%%%%"
    season = int(parts[0])
    epnr = int(parts[1])
    patterns = [
        "s%#02de%#02d" % (season, epnr),
        "%#02dx%#02d" % (season, epnr),
        "%#01de%#02d" % (season, epnr),
    ]
    if season < 10:
        patterns.append(r"(?:\A|\D)%dx%#02d" % (season, epnr))
    return '(?:%s)' % '|'.join(patterns)


def get_season_patt(episode):
    parts = episode.split(':')
    if len(parts) < 2:
        return "%%%%%"
    season = int(parts[0])
    patterns = [
        r"s%#02de\d+" % (season),
        r"%#02dx\d+" % (season),
    ]
    if season < 10:
        patterns.append(r"(?:\A|\D)%dx\d+" % (season))
    return '(?:%s)' % '|'.join(patterns)


def log(msg):
    try:
        xbmc.log("### %s" % (msg), level=xbmc.LOGDEBUG)
    except:
        xbmc.log("### : %s" % ('ERROR LOG'), level=xbmc.LOGDEBUG)


def seasons(i):
    from ordinal import ordinal
    """Seasons as strings for searching"""
    i = int(i)
    if i == 0:
        return 'Specials'
    else:
        return ordinal(i)


def Search(item):
    search_data = []
    search_data = searchsubtitles(item)
    if search_data is not None:
        for item_data in search_data:
            if ((item['season'] == item_data['SeriesSeason'] and item['episode'] == item_data['SeriesEpisode'])
                    or (item['season'] == "" and item['episode'] == "")):  # for file search, season and episode == ""
                listitem = xbmcgui.ListItem(label=item_data["LanguageName"],
                                            label2="%s [COLOR gray][I](%s)[/I][/COLOR]" % (item_data["SubFileName"], item_data['comment']) if item_data["comment"] != '' else item_data["SubFileName"]
                                            )
                listitem.setArt({'icon': str(item_data["SubRating"]), 'thumb': item_data["ISO639"]})
                listitem.setProperty("sync", ("false", "true")[str(item_data["sync"]) is True])
                listitem.setProperty("hearing_imp", ("false", "true")[int(item_data["SubHearingImpaired"]) != 0])
                url = "plugin://{0}/?action=download&link={1}&filename={2}&format={3}&season={4}&episode={5}".format(
                    __scriptid__,
                    item_data["ZipDownloadLink"],
                    item_data["SubFileName"],
                    item_data["SubFormat"],
                    item["season"],
                    item["episode"]
                )

                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=False)


def searchsubtitles(item):
    lists = ''
    import PTN
    if not item['file_original_path'].startswith('http'):
        cleanfolders = os.path.basename(item['file_original_path'])
    elif item.get('mansearch'):
        cleanfolders = urllib_parse.unquote(item.get('mansearchstr'))
    else:
        cleanfolders = item.get('title')
    parsed = PTN.parse(cleanfolders)
    item['title'] = parsed.get('title') or item.get('title')
    item['year'] = parsed.get('year') or item.get('year')
    if parsed.get('season') == 'None':
        parsed['season'] = ''
    if parsed.get('episode') == 'None':
        parsed['episode'] = ''
    if not (item.get('season') and item.get('episode') and item.get('tvshow')):
        item['tvshow'] = parsed.get('title') if (parsed.get('season') and parsed.get('episode')) else item.get('tvshow')
        item['season'] = str(parsed.get('season')) or ''
        item['episode'] = str(parsed.get('episode')) or ''
    search_string = item.get('tvshow') or item.get('title')
    lists = search_links(search_string, item)
    return lists


def get_language_codes(languages):
    codes = {}
    for lang in subscene_languages:
        if subscene_languages[lang]['3let'] in languages:
            codes[str(subscene_languages[lang]['id'])] = 1
    keys = codes.keys()
    return keys


def search_links(nume='', item=None):
    subs_list = []
    if item.get('season') and item.get('season') != 'None':
        season_ordinal = seasons(int(item.get('season')))
        nume = '%s - %s Season' % (item.get('tvshow'), season_ordinal)
    urlcautare = '%s/search' % (BASE_URL)
    search_data = {"query": nume}
    url = BASE_URL
    t = s.get(url)
    cj = s.cookies
    time.sleep(1)
    codes = get_language_codes(item['3let_language'])
    requests.utils.add_dict_to_cookiejar(cj, {'LanguageFilter': ','.join(codes), 'HearingImpaired': '2', 'ForeignOnly': 'False'})
    u = s.get(urlcautare, params=search_data, cookies=cj)
    continuturl = u.text
    first_search = []
    for nothing, datas, content_datas in re.findall('<h2( class=".+?")?>(.+?)</h2(.+?)</ul>', continuturl, re.IGNORECASE | re.DOTALL):
        details = re.findall('href="(.+?)">(.+?)<', content_datas, re.IGNORECASE | re.DOTALL)
        if details:
            for legatura, numelegatura in details:
                first_search.append((legatura, numelegatura))
            if datas == "Exact":
                break

    subtitle_pattern = r'''<td class="a1">\s+<a\s+href="(?P<link>/subtitle/[^"]+)">\s+<div>\s+<span class="[^"]+\s+''' \
                       r'''(?P<quality>\w+-icon)">\s+(?P<language>[^\r\n\t]+)\s+</span>\s+<span\s+class="new">\s+''' \
                       r'''(?P<filename>[^\r\n\t]+)\s+</span>\s+</div>\s+</a>\s+</td>\s+<td class="[^"]+">\s+''' \
                       r'''(?P<numfiles>[^\r\n\t]*)\s+</td>\s+<td class="(?P<hiclass>[^"]+)">(?:.*?)''' \
                       r'''<td class="a6">\s+<div[^>]+>\s+(?P<comment>[^\r\n\t]+)\s+</div>'''
    filename = os.path.splitext(os.path.basename(item['file_original_path']))[0]
    selected = []
    if first_search:
        if six.PY2:
            import HTMLParser
            _html_parser = HTMLParser.HTMLParser()
        else:
            import html
            _html_parser = html
        if len(first_search) > 0:
            if len(first_search) > 1:
                dialog = xbmcgui.Dialog()
                sel = dialog.select("subscene", [x[1] for x in first_search])
            else:
                sel = 0
            if sel >= 0:
                g = s.get('%s%s' % (BASE_URL, first_search[sel][0]))
                continuturl = g.text
                matching = re.finditer(subtitle_pattern, continuturl, re.IGNORECASE | re.DOTALL)
                if item['episode'] != "" and item.get('episode') != 'None':
                    season = item['season']
                    episode = item['episode']
                    epstr = '{season}:{episode}'.format(**locals())
                    episode_regex = re.compile(get_episode_pattern(epstr), re.IGNORECASE)
                    season_reg = re.compile(get_season_patt(epstr), re.IGNORECASE)
                else:
                    episode_regex = None
                for matches in matching:
                    numfiles = 1
                    if matches.group('numfiles') != "":
                        numfiles = int(matches.group('numfiles'))
                    languagefound = matches.group('language')
                    language_info = subscene_languages.get(languagefound)
                    if language_info and language_info['3let'] in item['3let_language']:
                        link = BASE_URL + matches.group('link')
                        subtitle_name = matches.group('filename').strip()
                        hearing_imp = (matches.group('hiclass') == "a41")
                        if matches.group('quality') == "positive-icon":
                            rating = '5'
                        else:
                            rating = '0'
                        comment = re.sub("[\r\n\t]+", " ", _html_parser.unescape(matches.group('comment').strip()))
                        sync = True if (filename != "" and filename.lower() == subtitle_name.lower()) else False
                        if episode_regex:
                            if episode_regex.search(subtitle_name) or not season_reg.search(subtitle_name):
                                selected.append({'SeriesSeason': (item['season']),
                                                 'SeriesEpisode': item['episode'],
                                                 'LanguageName': languagefound,
                                                 'promo': '',
                                                 'SubFileName': (subtitle_name.strip()),
                                                 'SubRating': rating,
                                                 'ZipDownloadLink': link,
                                                 'ISO639': language_info['2let'],
                                                 'SubFormat': 'srt',
                                                 'MatchedBy': 'fulltext',
                                                 'SubHearingImpaired': hearing_imp,
                                                 'sync': sync,
                                                 'comment': comment})
                        else:
                            selected.append({'SeriesSeason': (item['season']),
                                             'SeriesEpisode': item['episode'],
                                             'LanguageName': languagefound,
                                             'promo': '',
                                             'SubFileName': (subtitle_name.strip()),
                                             'SubRating': rating,
                                             'ZipDownloadLink': link,
                                             'ISO639': language_info['2let'],
                                             'SubFormat': 'srt',
                                             'MatchedBy': 'fulltext',
                                             'SubHearingImpaired': hearing_imp,
                                             'sync': sync,
                                             'comment': comment})
    return selected


def Download(url, season, episode):
    subtitle_list = []
    pub_list = []
    exts = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"]
    f = s.get(url).text
    downlinkreg = r'''class="download".+?href="([^"]+)'''
    downlink = re.findall(downlinkreg, f, re.IGNORECASE | re.DOTALL)[0]
    time.sleep(1)
    response = s.head(downlink)
    cT = response.headers['content-type']
    if re.search('application/x-zip-compressed', cT) \
        or re.search('application/x-rar-compressed', cT) \
            or re.search('application/zip', cT):
        g = s.get(downlink)
        if re.search('application/x-rar-compressed', cT):
            import patoolib
            extractPath = os.path.join(__temp__, "Extracted")
            fname = "%s.rar" % (os.path.join(__temp__, "subtitle"))
            g = s.get(downlink)
            open(fname, 'wb').write(g.content)
            if not os.path.exists(extractPath):
                os.makedirs(extractPath)
                patoolib.extract_archive(fname, outdir=extractPath)
            for root, dirs, files in os.walk(extractPath):
                for filex in files:
                    dirfile = os.path.join(root, filex)
                    if (os.path.splitext(filex)[1] in exts):
                        subtitle_list.append(dirfile)

        else:
            archive = ZipFile(six.BytesIO(g.content), 'r')
            files = archive.namelist()
            files.sort()
            for file in files:
                contents = archive.read(file)
                if (os.path.splitext(file)[1] in exts):
                    if len(files) == 1:
                        dest = os.path.join(__temp__, "%s" % (file))
                    else:
                        dest = os.path.join(__temp__, "%s" % (file))
                    f = open(dest, 'wb')
                    f.write(contents)
                    f.close()
                    subtitle_list.append(dest)
    elif re.search('text/html', cT):
        g = s.get(downlink).content
        dest = os.path.join(__temp__, "subscene.srt")
        f = open(dest, 'wb')
        f.write(g)
        f.close()
        subtitle_list.append(dest)
    if xbmcvfs.exists(subtitle_list[0]):
        subs_list = []
        if episode != "" and season != "" and episode != "None" and season != "None":
            epstr = '{season}:{episode}'.format(**locals())
            episode_regex = re.compile(get_episode_pattern(epstr), re.IGNORECASE)
        else:
            episode_regex = None
        if episode_regex:
            for subs in subtitle_list:
                if episode_regex.search(os.path.basename(subs)):
                    subs_list.append(subs)
            if len(subs_list) >= 1:
                subtitle_list = subs_list
        if len(subtitle_list) > 1:
            selected = []
            subtitle_list_s = subtitle_list
            dialog = xbmcgui.Dialog()
            sel = dialog.select("%s" % ('Selecteaza o subtitrare'),
                                [((os.path.join(os.path.basename(os.path.dirname(x)), os.path.basename(x)))
                                  if (os.path.basename(x) == os.path.basename(subtitle_list_s[0])
                                      and os.path.basename(x) == os.path.basename(subtitle_list_s[1]))
                                  else os.path.basename(x))
                                 for x in subtitle_list_s])
            if sel >= 0:
                selected.append(subtitle_list_s[sel])
                return selected
            else:
                return None
        else:
            return subtitle_list
    else:
        return None


def get_params(string=""):
    param = []
    if string == "":
        paramstring = sys.argv[2]
    else:
        paramstring = string
    if len(paramstring) >= 2:
        params = paramstring
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


params = get_params()

if params['action'] == 'search' or params['action'] == 'manualsearch':
    item = {}
    item['temp'] = False
    item['rar'] = False
    item['mansearch'] = False
    item['year'] = xbmc.getInfoLabel("VideoPlayer.Year")                         # Year
    item['season'] = str(xbmc.getInfoLabel("VideoPlayer.Season"))                  # Season
    item['episode'] = str(xbmc.getInfoLabel("VideoPlayer.Episode"))                 # Episode
    item['tvshow'] = xbmc.getInfoLabel("VideoPlayer.TVshowtitle")  # Show
    item['title'] = xbmc.getInfoLabel("VideoPlayer.OriginalTitle")  # try to get original title
    item['file_original_path'] = xbmc.Player().getPlayingFile()                 # Full path of a playing file
    item['3let_language'] = []  # ['scc','eng']

    if 'searchstring' in params:
        item['mansearch'] = True
        item['mansearchstr'] = params['searchstring'].replace(' ', '+')

    for lang in urllib_parse.unquote(params['languages']).split(","):
        if lang == "Portuguese (Brazil)":
            lan = "pob"
        elif lang == "Greek":
            lan = "ell"
        else:
            lan = xbmc.convertLanguage(lang, xbmc.ISO_639_2)

        item['3let_language'].append(lan)

    if item['title'] == "":
        item['title'] = xbmc.getInfoLabel("VideoPlayer.Title")      # no original title, get just Title

    if item['episode'].lower().find("s") > -1:                                      # Check if season is "Special"
        item['season'] = "0"                                                          #
        item['episode'] = item['episode'][-1:]

    if (item['file_original_path'].find("http") > -1):
        item['temp'] = True

    elif (item['file_original_path'].find("rar://") > -1):
        item['rar'] = True
        item['file_original_path'] = os.path.dirname(item['file_original_path'][6:])

    elif (item['file_original_path'].find("stack://") > -1):
        stackPath = item['file_original_path'].split(" , ")
        item['file_original_path'] = stackPath[0][8:]

    Search(item)

elif params['action'] == 'download':
    subs = Download(params["link"], params["season"], params["episode"])
    if subs:
        try:
            if len(subs) > 1:
                dialog = xbmcgui.Dialog()
                sel = dialog.select("Select item",
                                    [sub for sub in subs])
                if sel >= 0:
                    xbmc.Player().setSubtitles(subs[sel])
            else:
                xbmc.Player().setSubtitles(subs[0])
        except:
            pass
        for sub in subs:
            listitem = xbmcgui.ListItem(label=sub)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sub, listitem=listitem, isFolder=False)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
