# -*- coding: utf-8 -*-
import sys
import gzip
import time
if sys.version_info.major == 3:
    import urllib.request, urllib.error, urllib.parse
else:
    from StringIO import StringIO
    import urllib2
import xbmc
import json
import re

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


def get_setting(name):
    """
    Get Kodi setting
    :param name: id of the setting.
        Example:
    :type name: str
    :return: string value of the setting
    :rtype: str
    """

    command = '{"jsonrpc":"2.0", "id":1, ' \
              '"method":"Settings.GetSettingValue",' \
              '"params":{"setting":"' + name + '"}}'
    try:
        response = xbmc.executeJSONRPC(command)
    except Exception as e:
        xbmc.log("### [%s] - %s" % (module, "Couldn't execute JSON-RPC",), level=xbmc.LOGWARNING)
        xbmc.log("### [%s] - %s" % (module, str(e),), level=xbmc.LOGWARNING)
        return
    try:
        data = json.loads(response)
    except Exception as e:
        xbmc.log("### [%s] - %s" % (module, "Couldn't parse JSON response",), level=xbmc.LOGWARNING)
        xbmc.log("### [%s] - %s" % (module, str(e),), level=xbmc.LOGWARNING)
        return None

    result = data.get("result")
    if result:
        return result.get("value")
    else:
        return None


def get_language_codes(languages):
    codes = {}
    for lang in subscene_languages:
        if subscene_languages[lang]['3let'] in languages:
            codes[str(subscene_languages[lang]['id'])] = 1
    if sys.version_info.major == 3:
        keys = list(codes.keys())
    else:
        keys = codes.keys()
    return keys


def get_episode_pattern(episode):
    parts = episode.split(':')
    if len(parts) < 2:
        return "%%%%%"
    season = int(parts[0])
    epnr = int(parts[1])
    patterns = [
        "s%#02de%#02d" % (season, epnr),
        "%#02dx%#02d" % (season, epnr),
    ]
    if season < 10:
        patterns.append("(?:\A|\D)%dx%#02d" % (season, epnr))
    return '(?:%s)' % '|'.join(patterns)

subscene_start = time.time()


def log(module, msg):
    global subscene_start
    if get_setting("log_level")=="debug":
        # set all logging to LOGWARNING to be included in Kodi log
        loglevel=xbmc.LOGWARNING
    else:
        # set logging to debug to only log output when Kodi is set to DEBUG
        loglevel=xbmc.LOGDEBUG

    if sys.version_info.major == 3:
        xbmc.log("### [%s] %f - %s" % (module, time.time() - subscene_start, msg,), level=loglevel)
    else:
        xbmc.log((u"### [%s] %f - %s" % (module, time.time() - subscene_start, msg,)).encode('utf-8'), level=loglevel)


def geturl(url, cookies=None):
    log(__name__, "Getting url: %s" % url)
    try:
        if sys.version_info.major == 3:
            request = urllib.request.Request(url)
        else:
            request = urllib2.Request(url)
        request.add_header('Accept-encoding', 'gzip')
        if cookies:
            request.add_header('Cookie', cookies)
        # request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0')
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0')
        if sys.version_info.major == 3:
            response = urllib.request.urlopen(request)
        else:
            response = urllib2.urlopen(request)
        log(__name__, "request done")
        if response.info().get('Content-Encoding') == 'gzip':
            if sys.version_info.major == 3:
                f = gzip.GzipFile(fileobj=response)
            else:
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
            content = f.read()
            # content is binary, decoding into string
            content = content.decode("utf-8")
        else:
            content = response.read()
        log(__name__, "read done")
        log(__name__, "content:\n%s" % content)
        # Fix non-unicode characters in movie titles
        strip_unicode = re.compile("([^-_a-zA-Z0-9!@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\.\{\}\|\?<>\\]+|[^\s]+)")
        content = strip_unicode.sub('', content)
        return_url = response.geturl()
        log(__name__, "return_url:\n%s" % return_url)
        log(__name__, "fetching done")
    except:
        log(__name__, "Failed to get url: %s" % url)
        content = None
        return_url = None
    return content, return_url

