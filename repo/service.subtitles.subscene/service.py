# -*- coding: utf-8 -*-

import os
import traceback
import sys
import xbmc
import time
if sys.version_info.major == 3:
    import urllib.request
    import urllib.parse
    import urllib.error
else:
    import urllib
    import urllib2
    import HTMLParser
import xbmcvfs
import xbmcaddon
import xbmcgui
import xbmcplugin
import uuid
import unicodedata
import re
import difflib
from operator import itemgetter

__addon__ = xbmcaddon.Addon()
__author__ = __addon__.getAddonInfo('author')
__scriptid__ = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__language__ = __addon__.getLocalizedString

if sys.version_info.major == 3:
    __cwd__ = xbmcvfs.translatePath(__addon__.getAddonInfo('path'))
    __profile__ = xbmcvfs.translatePath(__addon__.getAddonInfo('profile'))
    __resource__ = xbmcvfs.translatePath(os.path.join(__cwd__, 'resources', 'lib'))
    __temp__ = xbmcvfs.translatePath(os.path.join(__profile__, 'temp', ''))
else:
    __cwd__ = unicode(xbmc.translatePath(__addon__.getAddonInfo('path')), 'utf-8')
    __profile__ = unicode(xbmc.translatePath(__addon__.getAddonInfo('profile')), 'utf-8')
    __resource__ = unicode(xbmc.translatePath(os.path.join(__cwd__, 'resources', 'lib')), 'utf-8')
    __temp__ = unicode(xbmc.translatePath(os.path.join(__profile__, 'temp', '')), 'utf-8')

sys.path.append(__resource__)

from SubsceneUtilities import log, geturl, get_language_codes, subscene_languages, get_episode_pattern

main_url = "https://subscene.com"

aliases = {
    "marvels agents of shield": "Agents of Shield",
    "marvels agents of s.h.i.e.l.d": "Agents of Shield",
    "marvels jessica jones": "Jessica Jones",
    "dcs legends of tomorrow": "Legends of Tomorrow"
}

# Seasons as strings for searching
seasons = ["Specials", "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth"]
seasons = seasons + ["Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth", "Sixteenth", "Seventeenth",
                     "Eighteenth", "Nineteenth", "Twentieth"]
seasons = seasons + ["Twenty-first", "Twenty-second", "Twenty-third", "Twenty-fourth", "Twenty-fifth", "Twenty-sixth",
                     "Twenty-seventh", "Twenty-eighth", "Twenty-ninth"]

search_section_pattern = "<h2 class=\"(?P<section>\w+)\">(?:[^<]+)</h2>\s+<ul>(?P<content>.*?)</ul>"
movie_season_pattern = ("<a href=\"(?P<link>/subtitles/[^\"]*)\">(?P<title>[^<]+)\((?P<year>\d{4})\)</a>\s+"
                        "</div>\s+<div class=\"subtle count\">\s+(?P<numsubtitles>\d+)")


def rmtree(path):
    if sys.version_info.major < 3:
        if isinstance(path, unicode):
            path = path.encode('utf-8')
    dirs, files = xbmcvfs.listdir(path)
    for dir in dirs:
        rmtree(os.path.join(path, dir))
    for file in files:
        xbmcvfs.delete(os.path.join(path, file))
    xbmcvfs.rmdir(path)


# cleaning up temp directory if it exists
if xbmcvfs.exists(__temp__):
    try:
        rmtree(__temp__)
    except:
        pass


def find_movie(content, title, year):
    found_urls = {}
    found_movies = []
    if sys.version_info.major == 3:
        import html
    else:
        html = HTMLParser.HTMLParser()

    for secmatches in re.finditer(search_section_pattern, content, re.IGNORECASE | re.DOTALL):
        log(__name__, secmatches.group('section'))
        for matches in re.finditer(movie_season_pattern, secmatches.group('content'), re.IGNORECASE | re.DOTALL):
            if matches.group('link') in found_urls:
                if secmatches.group('section') == 'close':
                    found_movies[found_urls[matches.group('link')]]['is_close'] = True
                if secmatches.group('section') == 'exact':
                    found_movies[found_urls[matches.group('link')]]['is_exact'] = True
                continue
            found_urls[matches.group('link')] = len(found_movies)

            found_title = matches.group('title')
            found_title = html.unescape(found_title)
            log(__name__, "Found movie on search page: %s (%s)" % (found_title, matches.group('year')))
            found_movies.append(
                {'t': found_title.lower(),
                 'y': int(matches.group('year')),
                 'is_exact': secmatches.group('section') == 'exact',
                 'is_close': secmatches.group('section') == 'close',
                 'l': matches.group('link'),
                 'c': int(matches.group('numsubtitles'))})

    year = int(year)
    title = title.lower()
    # Priority 1: matching title and year
    for movie in found_movies:
        if movie['t'].find(title) > -1:
            if movie['y'] == year:
                log(__name__, "Matching movie found on search page: %s (%s)" % (movie['t'], movie['y']))
                return movie['l']

    # Priority 2: matching title and one off year
    for movie in found_movies:
        if movie['t'].find(title) > -1:
            if movie['y'] == year + 1 or movie['y'] == year - 1:
                log(__name__, "Matching movie found on search page (one off year): %s (%s)" % (movie['t'], movie['y']))
                return movie['l']

    # Priority 3: "Exact" match according to search result page
    close_movies = []
    for movie in found_movies:
        if movie['is_exact']:
            log(__name__, "Using 'Exact' match: %s (%s)" % (movie['t'], movie['y']))
            return movie['l']
        if movie['is_close']:
            close_movies.append(movie)

    # Priority 4: "Close" match according to search result page
    if len(close_movies) > 0:
        close_movies = sorted(close_movies, key=itemgetter('c'), reverse=True)
        log(__name__, "Using 'Close' match: %s (%s)" % (close_movies[0]['t'], close_movies[0]['y']))
        return close_movies[0]['l']

    return None


def find_tv_show_season(content, tvshow, season):
    url_found = None
    found_urls = []
    possible_matches = []
    all_tvshows = []

    if sys.version_info.major == 3:
        import html
    else:
        html = HTMLParser.HTMLParser()

    for matches in re.finditer(movie_season_pattern, content, re.IGNORECASE | re.DOTALL):
        found_title = matches.group('title')
        found_title = html.unescape(found_title)

        if matches.group('link') in found_urls:
            continue
        log(__name__, "Found tv show season on search page: %s" % found_title)
        found_urls.append(matches.group('link'))
        s = difflib.SequenceMatcher(None, (found_title + ' ' + matches.group('year')).lower(), tvshow.lower())
        all_tvshows.append(matches.groups() + (s.ratio() * int(matches.group('numsubtitles')),))
        if found_title.lower().find(tvshow.lower() + " ") > -1:
            if found_title.lower().find(season.lower()) > -1:
                log(__name__, "Matching tv show season found on search page: %s" % found_title)
                possible_matches.append(matches.groups())

    if len(possible_matches) > 0:
        possible_matches = sorted(possible_matches, key=lambda x: -int(x[3]))
        url_found = possible_matches[0][0]
        log(__name__, "Selecting matching tv show with most subtitles: %s (%s)" % (
            possible_matches[0][1], possible_matches[0][3]))
    else:
        if len(all_tvshows) > 0:
            all_tvshows = sorted(all_tvshows, key=lambda x: -int(x[4]))
            url_found = all_tvshows[0][0]
            log(__name__, "Selecting tv show with highest fuzzy string score: %s (score: %s subtitles: %s)" % (
                all_tvshows[0][1], all_tvshows[0][4], all_tvshows[0][3]))

    return url_found


def append_subtitle(item):
    title = item['filename']
    if 'comment' in item and item['comment'] != '':
        title = "%s[CR][COLOR silver][I](%s)[/I][/COLOR]" % (title, item['comment'])
    if sys.version_info.major == 3:
        listitem = xbmcgui.ListItem(label=item['lang']['name'],
                                    label2=title)
        listitem.setArt({'icon': item['rating'], 'thumb': item['lang']['2let']})
    else:
        listitem = xbmcgui.ListItem(label=item['lang']['name'],
                                    label2=title,
                                    iconImage=item['rating'],
                                    thumbnailImage=item['lang']['2let'])

    listitem.setProperty("sync", 'true' if item["sync"] else 'false')
    listitem.setProperty("hearing_imp", 'true' if item["hearing_imp"] else 'false')
    # ForeignOnly change
    # listitem.setProperty("forced", 'true')

    # below arguments are optional, it can be used to pass any info needed in download function
    # anything after "action=download&" will be sent to addon once user clicks listed subtitle to downlaod
    url = "plugin://%s/?action=download&link=%s&filename=%s" % (__scriptid__,
                                                                item['link'],
                                                                item['filename'])
    if 'episode' in item:
        url += "&episode=%s" % item['episode']
    # add it to list, this can be done as many times as needed for all subtitles found
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=False)


def getallsubs(url, allowed_languages, filename="", episode=""):
    subtitle_pattern = ("<td class=\"a1\">\s+<a href=\"(?P<link>/subtitles/[^\"]+)\">\s+"
                        "<span class=\"[^\"]+ (?P<quality>\w+-icon)\">\s+(?P<language>[^\r\n\t]+)\s+</span>\s+"
                        "<span>\s+(?P<filename>[^\r\n\t]+)\s+</span>\s+"
                        "</a>\s+</td>\s+"
                        "<td class=\"[^\"]+\">\s+(?P<numfiles>[^\r\n\t]*)\s+</td>\s+"
                        "<td class=\"(?P<hiclass>[^\"]+)\">"
                        "(?:.*?)<td class=\"a6\">\s+<div>\s+(?P<comment>[^\"]+)&nbsp;\s*</div>")

    codes = get_language_codes(allowed_languages)
    if len(codes) < 1:
        if sys.version_info.major == 3:
            xbmc.executebuiltin('Notification(%s,%s)' % (__scriptname__, __language__(32004)))
        else:
            xbmc.executebuiltin((u'Notification(%s,%s)' % (__scriptname__, __language__(32004))).encode('utf-8'))
        return
    # All subs of language
    log(__name__, 'LanguageFilter='+','.join(codes))
    content, response_url = geturl(url, 'LanguageFilter='+','.join(codes))
    # ForeignOnly change
    # log(__name__, 'ForeignOnly=True;LanguageFilter='+','.join(codes))
    # content, response_url = geturl(url, 'ForeignOnly=True;LanguageFilter='+','.join(codes))

    if content is None:
        return

    subtitles = []
    if sys.version_info.major == 3:
        import html
    else:
        html = HTMLParser.HTMLParser()

    episode_regex = None
    if episode != "":
        episode_regex = re.compile(get_episode_pattern(episode), re.IGNORECASE)
        log(__name__, "regex: %s" % get_episode_pattern(episode))

    for matches in re.finditer(subtitle_pattern, content, re.IGNORECASE | re.DOTALL):
        numfiles = 1
        if matches.group('numfiles') != "":
            numfiles = int(matches.group('numfiles'))
        languagefound = matches.group('language')
        language_info = subscene_languages[languagefound]

        if language_info and language_info['3let'] in allowed_languages:
            link = main_url + matches.group('link')
            subtitle_name = matches.group('filename').strip()
            log(__name__, 'Subtitle %s %s' % (link, subtitle_name))
            hearing_imp = (matches.group('hiclass') == "a41")
            rating = '0'
            if matches.group('quality') == "bad-icon":
                log(__name__, 'Subtitle classed as bad, ignoring')
                continue
            if matches.group('quality') == "positive-icon":
                log(__name__, 'Subtitle classed as good')
                rating = '5'

            comment = re.sub("[\r\n\t]+", " ", html.unescape(matches.group('comment').strip()))

            sync = False
            if filename != "" and filename.lower() == subtitle_name.lower():
                sync = True

            if episode != "":
                log(__name__, "match: "+subtitle_name)
                if episode_regex.search(subtitle_name):
                    subtitles.append({'rating': rating, 'filename': subtitle_name, 'sync': sync, 'link': link,
                                      'lang': language_info, 'hearing_imp': hearing_imp, 'comment': comment})
                elif numfiles > 2:
                    subtitle_name = subtitle_name + ' ' + (__language__(32001) % int(matches.group('numfiles')))
                    subtitles.append({'rating': rating, 'filename': subtitle_name, 'sync': sync, 'link': link,
                                      'lang': language_info, 'hearing_imp': hearing_imp, 'comment': comment,
                                      'episode': episode})
            else:
                subtitles.append({'rating': rating, 'filename': subtitle_name, 'sync': sync, 'link': link,
                                  'lang': language_info, 'hearing_imp': hearing_imp, 'comment': comment})

    subtitles.sort(key=lambda x: [not x['sync'], not x['lang']['name'] == PreferredSub])
    for s in subtitles:
        append_subtitle(s)
    log(__name__, 'All subtitles: %s' % subtitles)


def prepare_search_string(s):
    s = str(s)
    s = s.strip()
    s = re.sub(r'\s+\(\d\d\d\d\)$', '', s)  # remove year from title
    return str(s)


def search_movie(title, year, languages, filename):
    title = prepare_search_string(title)

    log(__name__, "Search movie = %s" % title)
    if sys.version_info.major == 3:
        url = main_url + "/subtitles/searchbytitle?query=" + urllib.parse.quote_plus(title)
    else:
        url = main_url + "/subtitles/searchbytitle?query=" + urllib.quote_plus(title)
    content, response_url = geturl(url)

    if content is not None:
        log(__name__, "Multiple movies found, searching for the right one ...")
        subspage_url = find_movie(content, title, year)
        if subspage_url is not None:
            log(__name__, "Movie found in list, getting subs ...")
            url = main_url + subspage_url
            getallsubs(url, languages, filename)
        else:
            log(__name__, "Movie not found in list: %s" % title)
            if title.lower().find("&") > -1:
                title = title.replace("&", "and")
                log(__name__, "Trying searching with replacing '&' to 'and': %s" % title)
                subspage_url = find_movie(content, title, year)
                if subspage_url is not None:
                    log(__name__, "Movie found in list, getting subs ...")
                    url = main_url + subspage_url
                    getallsubs(url, languages, filename)
                else:
                    log(__name__, "Movie not found in list: %s" % title)


def search_tvshow(tvshow, season, episode, languages, filename):
    tvshow = prepare_search_string(tvshow)

    tvshow_lookup = tvshow.lower().replace("'", "").strip(".")
    if tvshow_lookup in aliases:
        log(__name__, 'found alias for "%s"' % tvshow_lookup)
        tvshow = aliases[tvshow_lookup]

    search_string = tvshow + " - " + seasons[int(season)] + " Season"

    log(__name__, "Search tvshow = %s" % search_string)
    if sys.version_info.major == 3:
        url = main_url + "/subtitles/searchbytitle?query=" + urllib.parse.quote_plus(search_string)
    else:
        url = main_url + "/subtitles/searchbytitle?query=" + urllib.quote_plus(search_string)
    content, response_url = geturl(url)

    if content is not None:
        log(__name__, "Multiple tv show seasons found, searching for the right one ...")
        tv_show_seasonurl = find_tv_show_season(content, tvshow, seasons[int(season)])
        if tv_show_seasonurl is not None:
            log(__name__, "Tv show season found in list, getting subs ...")
            url = main_url + tv_show_seasonurl
            epstr = "%d:%d" % (int(season), int(episode))
            getallsubs(url, languages, filename, epstr)


def search_manual(searchstr, languages, filename):
    search_string = prepare_search_string(searchstr)
    url = main_url + "/subtitles/searchbytitle?query=" + search_string
    getallsubs(url, languages, filename)


def search_filename(filename, languages):
    title, year = xbmc.getCleanMovieTitle(filename)
    log(__name__, "clean title: \"%s\" (%s)" % (title, year))
    try:
        yearval = int(year)
    except ValueError:
        yearval = 0
    match = re.search(r'\WS(?P<season>\d\d)E(?P<episode>\d\d)', filename, flags=re.IGNORECASE)
    if match is not None:
        tvshow = title[:match.start('season') - 1].strip()
        season = match.group('season').lstrip('0')
        episode = match.group('episode').lstrip('0')
        search_tvshow(tvshow, season, episode, languages, filename)
    elif title and yearval > 1900:
        search_movie(title, year, languages, filename)
    else:
        search_manual(filename, languages, filename)


def search(item):
    filename = os.path.splitext(os.path.basename(item['file_original_path']))[0]
    log(__name__, "Search_subscene='%s', filename='%s', addon_version=%s" % (item, filename, __version__))

    if item['mansearch']:
        search_manual(item['mansearchstr'], item['3let_language'], filename)
    elif item['tvshow']:
        search_tvshow(item['tvshow'], item['season'], item['episode'], item['3let_language'], filename)
    elif item['title'] and item['year']:
        search_movie(item['title'], item['year'], item['3let_language'], filename)
    elif item['title']:
        search_filename(item['title'], item['3let_language'])
    else:
        search_filename(filename, item['3let_language'])


def download(link, episode=""):
    subtitle_list = []
    exts = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"]
    downloadlink_pattern = "...<a href=\"(.+?)\" rel=\"nofollow\" onclick=\"DownloadSubtitle"

    uid = uuid.uuid4()
    if sys.version_info.major == 3:
        tempdir = os.path.join(__temp__, str(uid))
    else:
        tempdir = os.path.join(__temp__, unicode(uid))

    try:
        os.makedirs(tempdir)
    except OSError:
        log(__name__, "Failed to create temp directory " + tempdir)
    else:
        log(__name__, "Successfully created temp directory " + tempdir)

    content, response_url = geturl(link)
    content = str(content)
    match = re.compile(downloadlink_pattern).findall(content)
    if match:
        downloadlink = main_url + match[0]
        viewstate = 0
        previouspage = 0
        subtitleid = 0
        typeid = "zip"
        filmid = 0

        if sys.version_info.major == 3:
            postparams = urllib.parse.urlencode(
                {'__EVENTTARGET': 's$lc$bcr$downloadLink', '__EVENTARGUMENT': '', '__VIEWSTATE': viewstate,
                 '__PREVIOUSPAGE': previouspage, 'subtitleId': subtitleid, 'typeId': typeid, 'filmId': filmid}).encode()
        else:
            postparams = urllib.urlencode(
                {'__EVENTTARGET': 's$lc$bcr$downloadLink', '__EVENTARGUMENT': '', '__VIEWSTATE': viewstate,
                 '__PREVIOUSPAGE': previouspage, 'subtitleId': subtitleid, 'typeId': typeid, 'filmId': filmid})
#        useragent = ("User-Agent=Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) "
#                     "Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)")
#        useragent = ("User-Agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Safari/537.36")
        useragent = ("Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0")
        headers = {'User-Agent': useragent, 'Referer': link}
        log(__name__, "Fetching subtitles using url '%s' with referer header '%s' and post parameters '%s'" % (
            downloadlink, link, postparams))

        local_tmp_file = os.path.join(tempdir, "subscene.xxx")

        time_interval = 3
        num_of_retries = 5
        if sys.version_info.major == 3:
            request = urllib.request.Request(downloadlink, postparams, headers)
            for _ in range(num_of_retries):
                try:
                    response = urllib.request.urlopen(request)
                except:
                    typ, val, tb = sys.exc_info()
                    log(__name__, traceback.format_exception(typ, val, tb))
                    num_of_retries -= 1
                    # If there aren't any retries - exit loop and raise error
                    if not num_of_retries:
                        log(__name__, "Download failure, giving up")
                        pass
                    log(__name__, "Download failure, %s attempts left" % num_of_retries)
                    time.sleep(time_interval)
                else:
                    local_tmp_file = os.path.join(tempdir, "subscene.xxx")
                    log(__name__, "Saving downloaded file to '%s'" % local_tmp_file)
                    local_file_handle = xbmcvfs.File(local_tmp_file, "w")
                    local_file_handle.write(bytearray(response.read()))
                    local_file_handle.close()
                    break
            else:
                log(__name__, "Download failure, returning empty subtitle list")
                return subtitle_list
        else:
            request = urllib2.Request(downloadlink, postparams, headers)
            for _ in range(num_of_retries):
                try:
                    response = urllib2.urlopen(request)
                except urllib2.URLError:
                    typ, val, tb = sys.exc_info()
                    log(__name__, traceback.format_exception(typ, val, tb))
                    num_of_retries -= 1
                    # If there aren't any retries - exit loop and raise error
                    if not num_of_retries:
                        log(__name__, "Download failure, giving up")
                        raise
                    log(__name__, "Download failure, %s attempts left" % num_of_retries)
                    time.sleep(time_interval)
                else:
                    log(__name__, "Saving downloaded file to '%s'" % local_tmp_file)
                    local_file_handle = xbmcvfs.File(local_tmp_file, "wb")
                    local_file_handle.write(response.read())
                    local_file_handle.close()
                    break
            else:
                raise

        if response is not None and response.getcode() != 200:
            log(__name__, "Failed to download subtitle file, HTTP error %s" % response.getcode())
            return subtitle_list

        packed = False

        try:
            log(__name__, "Checking archive type")
            # Check archive type (rar/zip/else) through the file header (rar=Rar!, zip=PK)
            myfile = xbmcvfs.File(local_tmp_file, "rb")
            myfile.seek(0, 0)
            if myfile.read(1) == 'R':
                typeid = "rar"
                packed = True
                log(__name__, "Discovered RAR Archive")
            else:
                myfile.seek(0, 0)
                if myfile.read(1) == 'P':
                    typeid = "zip"
                    packed = True
                    log(__name__, "Discovered ZIP Archive")
                else:
                    typeid = "srt"
                    packed = False
                    log(__name__, "Discovered a non-archive file")
            myfile.close()
            local_tmp_file = os.path.join(tempdir, "subscene." + typeid)
            xbmcvfs.rename(os.path.join(tempdir, "subscene.xxx"), local_tmp_file)
            log(__name__, "Saving to %s" % local_tmp_file)
        except:
            log(__name__, "Failed to save subtitle to %s" % local_tmp_file)

        if packed:
            xbmc.sleep(500)
            if (sys.platform == "linux" or sys.platform == "linux2") and not 'ANDROID_ROOT' in list(os.environ.keys()):
                platform = "linux"
                log(__name__, "Platform identified as Linux")
            else:
                platform = "non-linux"
                log(__name__, "Platform identified as Non-Linux")
            if sys.version_info.major == 3:
                log(__name__, "Checking '%s' for subtitle files to copy" % local_tmp_file)
                if platform == "linux":
                    (dirs, files) = xbmcvfs.listdir('%s' % xbmcvfs.translatePath(local_tmp_file))
                    if len(files) == 0:
                        log(__name__, "Trying trailing slash")
                        (dirs, files) = xbmcvfs.listdir('%s/' % xbmcvfs.translatePath(local_tmp_file))
                    if len(files) == 0:
                        log(__name__, "Trying zip://")
                        (dirs, files) = xbmcvfs.listdir('zip://%s/' % urllib.parse.quote_plus(local_tmp_file))
                else:
                    # Kodi on windows and possibly Android requires archive:// protocol, so testing both
                    log(__name__, "Trying archive:\\\\")
                    (dirs, files) = xbmcvfs.listdir('archive:\\\\%s' % xbmcvfs.translatePath(urllib.parse.quote_plus(local_tmp_file)))
                    if len(files) == 0:
                        log(__name__, "Trying directly")
                        (dirs, files) = xbmcvfs.listdir('%s' % xbmcvfs.translatePath(local_tmp_file))
                    if len(files) == 0:
                        log(__name__, "Trying zip://")
                        (dirs, files) = xbmcvfs.listdir('zip://%s/' % urllib.parse.quote_plus(local_tmp_file))
                for file in files:
                    dest = os.path.join(tempdir, file)
                    log(__name__, "=== Found subtitle file %s" % dest)
                    if platform == "linux":
                        # Kodi on linux does not understand 'archive://' protocol
                        src = os.path.join(local_tmp_file, file)
                        log(__name__, "trying to copy '%s' to '%s'" % (src, dest))
                        if not xbmcvfs.copy(src, dest):
                            log(__name__, "copying failed")
                        else:
                            log(__name__, "copying succeeded")
                    else:
                        # Kodi on windows and possibly Android requires archive:// protocol, so testing both
                        src = xbmcvfs.translatePath(os.path.join("archive:\\\\%s" % urllib.parse.quote_plus(local_tmp_file), file))
                        log(__name__, "trying to copy '%s' to '%s'" % (src, dest))
                        if not xbmcvfs.copy(src, dest):
                            log(__name__, "copying failed")
                            # trying again
                            src = os.path.join(local_tmp_file, file)
                            log(__name__, "trying to copy '%s' to '%s'" % (src, dest))
                            if not xbmcvfs.copy(src, dest):
                                # trying yet again
                                src = 'zip://%s/' % urllib.parse.quote_plus(os.path.join(local_tmp_file, file))
                                if not xbmcvfs.copy(src, dest):
                                    log(__name__, "copying failed")
                                else:
                                    log(__name__, "copying succeeded using zip://")
                            else:
                                log(__name__, "copying succeeded using directly")
                        else:
                            log(__name__, "copying succeeded using archive:\\\\")

                    subtitle_list.append(dest)
            else:
                log(__name__, "Extracting '%s' to '%s'" % (local_tmp_file, tempdir))
                xbmc.executebuiltin(('XBMC.Extract("%s","%s")' % (local_tmp_file, tempdir,)).encode('utf-8'), True)
                for file in xbmcvfs.listdir(local_tmp_file)[1]:
                    file = os.path.join(tempdir, file)
                    if os.path.splitext(file)[1] in exts:
                        log(__name__, "=== Found subtitle file %s" % file)
                        subtitle_list.append(file)

        episode_pattern = None
        if episode != '':
            episode_pattern = re.compile(get_episode_pattern(episode), re.IGNORECASE)

        log(__name__, "Checking temp dir subfolders for subtitle files...")
        for dir in xbmcvfs.listdir(tempdir)[0]:
            log(__name__, "Check dir subfolder %s" % dir)
            for file in xbmcvfs.listdir(os.path.join(tempdir, dir))[1]:
                log(__name__, "Check dir subfolder file %s" % file)
                if os.path.splitext(file)[1] in exts:
                    log(__name__, 'match '+episode+' '+file)
                    if episode_pattern and not episode_pattern.search(file):
                        continue
                    log(__name__, "=== returning subtitle file %s" % file)
                    subtitle_list.append(os.path.join(tempdir, dir, file))

        log(__name__, "Checking temp dir for subtitle files...")
        for file in xbmcvfs.listdir(tempdir)[1]:
            log(__name__, "Check dir file %s" % file)
            if os.path.splitext(file)[1] in exts:
                log(__name__, 'match '+episode+' '+file)
                if episode_pattern and not episode_pattern.search(file):
                    continue
                log(__name__, "=== returning subtitle file %s" % file)
                subtitle_list.append(os.path.join(tempdir, file))

        if len(subtitle_list) == 0:
            if sys.version_info.major == 3:
                if episode:
                    log(__name__, "=== Could not find matching episode in subtitle pack")
                    xbmc.executebuiltin('Notification(%s,%s)' % (__scriptname__, __language__(32002)))
                else:
                    log(__name__, "=== Download didn't contain a subtitle file")
                    xbmc.executebuiltin('Notification(%s,%s)' % (__scriptname__, __language__(32003)))
            else:
                if episode:
                    log(__name__, "=== Could not find matching episode in subtitle pack")
                    xbmc.executebuiltin((u'Notification(%s,%s)' % (__scriptname__, __language__(32002))).encode('utf-8'))
                else:
                    log(__name__, "=== Download didn't contain a subtitle file")
                    xbmc.executebuiltin((u'Notification(%s,%s)' % (__scriptname__, __language__(32003))).encode('utf-8'))

    return subtitle_list


def normalizeString(string):
    if sys.version_info.major == 3:
        return unicodedata.normalize(
            'NFKD', string
        )
    else:
        return unicodedata.normalize(
            'NFKD', unicode(unicode(string, 'utf-8'))
        ).encode('ascii', 'ignore')


def get_params():
    param = {}
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = paramstring
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
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
    item['year'] = xbmc.getInfoLabel("VideoPlayer.Year")  # Year
    item['season'] = str(xbmc.getInfoLabel("VideoPlayer.Season"))  # Season
    item['episode'] = str(xbmc.getInfoLabel("VideoPlayer.Episode"))  # Episode
    if item['episode'].lower().find("s") > -1:  # Check if season is "Special"
        item['season'] = "0"  #
        item['episode'] = item['episode'][-1:]

    item['tvshow'] = normalizeString(xbmc.getInfoLabel("VideoPlayer.TVshowtitle"))  # Show
    item['title'] = normalizeString(xbmc.getInfoLabel("VideoPlayer.OriginalTitle"))  # try to get original title
    if item['title'] == "":
        item['title'] = normalizeString(xbmc.getInfoLabel("VideoPlayer.Title"))  # no original title, get just Title

    if 'searchstring' in params:
        item['mansearch'] = True
        item['mansearchstr'] = params['searchstring']

    item['3let_language'] = []
    PreferredSub = params.get('preferredlanguage')

    if 'languages' in params:
        if sys.version_info.major == 3:
            for lang in urllib.parse.unquote(params['languages']).split(","):
                item['3let_language'].append(xbmc.convertLanguage(lang, xbmc.ISO_639_2))
        else:
            for lang in urllib.unquote(params['languages']).decode('utf-8').split(","):
                item['3let_language'].append(xbmc.convertLanguage(lang.decode('utf-8'), xbmc.ISO_639_2))

    if sys.version_info.major == 3:
        item['file_original_path'] = urllib.parse.unquote(xbmc.Player().getPlayingFile())  # Full path
    else:
        item['file_original_path'] = urllib.unquote(xbmc.Player().getPlayingFile().decode('utf-8'))  # Full path

    if item['file_original_path'].find("http") > -1:
        item['temp'] = True

    elif item['file_original_path'].find("rar://") > -1:
        item['rar'] = True
        item['file_original_path'] = os.path.dirname(item['file_original_path'][6:])

    elif item['file_original_path'].find("stack://") > -1:
        stackPath = item['file_original_path'].split(" , ")
        item['file_original_path'] = stackPath[0][8:]

    search(item)

elif params['action'] == 'download':
    # we pickup all our arguments sent from def Search()
    if 'episode' in params:
        subs = download(params["link"], params["episode"])
    else:
        subs = download(params["link"])
    # we can return more than one subtitle for multi CD versions, for now we are still working out how to handle that
    # in XBMC core
    for sub in subs:
        listitem = xbmcgui.ListItem(label=sub)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sub, listitem=listitem, isFolder=False)


xbmcplugin.endOfDirectory(int(sys.argv[1]))  # send end of directory to XBMC


