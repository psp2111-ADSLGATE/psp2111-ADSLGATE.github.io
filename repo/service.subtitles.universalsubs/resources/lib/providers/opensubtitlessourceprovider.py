# -*- coding: utf-8 -*-

import re
from datetime import timedelta
from typing import Dict, List, Tuple, Union
from urllib.parse import quote

from bs4 import BeautifulSoup, Tag

from resources.lib.common.language import Language
from resources.lib.common.mappedlanguages import MappedLanguages
from resources.lib.common.settings import Settings
from resources.lib.providers.getrequest import GetRequest
from resources.lib.providers.getresult import GetResult
from resources.lib.providers.searchrequest import (SearchRequest,
                                                   SearchResultsCounter)
from resources.lib.providers.searchresult import SearchResult
from resources.lib.providers.sourceprovider import SourceProvider
from resources.lib.utils.httpclient import HttpRequest
from resources.lib.utils.text import normalize_white_space

MAX_TITLE_RESULTS = 5

CHINESE_CANTONESE = Language("Chinese (Cantonese)", three_letter_code="zhc", standard=False)
CHINESE_SIMPLIFIED = Language("Chinese (simplified)", three_letter_code="chi", standard=False)
CHINESE_TRADITIONAL = Language("Chinese (traditional)", three_letter_code="zht", standard=False)
CHINESE_BILINGUAL = Language("Chinese bilingual", three_letter_code="zhe", standard=False)
KHMER = Language("Khmer", three_letter_code="khm", standard=False)
MONTENEGRIN = Language("Montenegrin", three_letter_code="mne", standard=False)
ODIA = Language("Odia", three_letter_code="ori", standard=False)
PORTUGUESE_BR = Language("Portuguese (BR)", three_letter_code="pob", standard=False)
PORTUGUESE_MZ = Language("Portuguese (MZ)", three_letter_code="pom", standard=False)
SERBIAN = Language("Serbian", three_letter_code="scc", standard=False)
SINHALESE = Language("Sinhalese", three_letter_code="sin", standard=False)
SPANISH_EU = Language("Spanish (EU)", three_letter_code="spn", standard=False)
SPANISH_LA = Language("Spanish (LA)", three_letter_code="spl", standard=False)
TOKI_PONA = Language("Toki Pona", three_letter_code="tok", standard=False)


SUPPORTED_LANGUAGES: List[Language] = [
    Language("Abkhazian", three_letter_code="abk"),
    Language("Afrikaans", three_letter_code="afr"),
    Language("Albanian", three_letter_code="alb"),
    Language("Amharic", three_letter_code="amh"),
    Language("Arabic", three_letter_code="ara"),
    Language("Aragonese", three_letter_code="arg"),
    Language("Armenian", three_letter_code="arm"),
    Language("Assamese", three_letter_code="asm"),
    Language("Asturian", three_letter_code="ast"),
    Language("Azerbaijani", three_letter_code="aze"),
    Language("Basque", three_letter_code="baq"),
    Language("Belarusian", three_letter_code="bel"),
    Language("Bengali", three_letter_code="ben"),
    Language("Bosnian", three_letter_code="bos"),
    Language("Breton", three_letter_code="bre"),
    Language("Bulgarian", three_letter_code="bul"),
    Language("Burmese", three_letter_code="bur"),
    Language("Catalan", three_letter_code="cat"),
    CHINESE_CANTONESE,
    CHINESE_SIMPLIFIED,
    CHINESE_TRADITIONAL,
    CHINESE_BILINGUAL,
    Language("Croatian", three_letter_code="hrv"),
    Language("Czech", three_letter_code="cze"),
    Language("Danish", three_letter_code="dan"),
    Language("Dari", three_letter_code="prs"),
    Language("Dutch", three_letter_code="dut"),
    Language("English", three_letter_code="eng"),
    Language("Esperanto", three_letter_code="epo"),
    Language("Estonian", three_letter_code="est"),
    Language("Extremaduran", three_letter_code="ext"),
    Language("Finnish", three_letter_code="fin"),
    Language("French", three_letter_code="fre"),
    Language("Gaelic", three_letter_code="gla"),
    Language("Galician", three_letter_code="glg"),
    Language("Georgian", three_letter_code="geo"),
    Language("German", three_letter_code="ger"),
    Language("Greek", three_letter_code="ell"),
    Language("Hebrew", three_letter_code="heb"),
    Language("Hindi", three_letter_code="hin"),
    Language("Hungarian", three_letter_code="hun"),
    Language("Icelandic", three_letter_code="ice"),
    Language("Igbo", three_letter_code="ibo"),
    Language("Indonesian", three_letter_code="ind"),
    Language("Interlingua", three_letter_code="ina"),
    Language("Irish", three_letter_code="gle"),
    Language("Italian", three_letter_code="ita"),
    Language("Japanese", three_letter_code="jpn"),
    Language("Kannada", three_letter_code="kan"),
    Language("Kazakh", three_letter_code="kaz"),
    KHMER,
    Language("Korean", three_letter_code="kor"),
    Language("Kurdish", three_letter_code="kur"),
    Language("Latvian", three_letter_code="lav"),
    Language("Lithuanian", three_letter_code="lit"),
    Language("Luxembourgish", three_letter_code="ltz"),
    Language("Macedonian", three_letter_code="mac"),
    Language("Malay", three_letter_code="may"),
    Language("Malayalam", three_letter_code="mal"),
    Language("Manipuri", three_letter_code="mni"),
    Language("Marathi", three_letter_code="mar"),
    Language("Mongolian", three_letter_code="mon"),
    MONTENEGRIN,
    Language("Navajo", three_letter_code="nav"),
    Language("Nepali", three_letter_code="nep"),
    Language("Northern Sami", three_letter_code="sme"),
    Language("Norwegian", three_letter_code="nor"),
    Language("Occitan", three_letter_code="oci"),
    ODIA,
    Language("Persian", three_letter_code="per"),
    Language("Polish", three_letter_code="pol"),
    PORTUGUESE_BR,
    PORTUGUESE_MZ,
    Language("Portuguese", three_letter_code="por"),
    Language("Pashto", three_letter_code="pus"),
    Language("Romanian", three_letter_code="rum"),
    Language("Russian", three_letter_code="rus"),
    Language("Santali", three_letter_code="sat"),
    SERBIAN,
    Language("Sindhi", three_letter_code="snd"),
    SINHALESE,
    Language("Slovak", three_letter_code="slo"),
    Language("Slovenian", three_letter_code="slv"),
    Language("Somali", three_letter_code="som"),
    SPANISH_EU,
    SPANISH_LA,
    Language("Spanish", three_letter_code="spa"),
    Language("Swahili", three_letter_code="swa"),
    Language("Swedish", three_letter_code="swe"),
    Language("Syriac", three_letter_code="syr"),
    Language("Tagalog", three_letter_code="tgl"),
    Language("Tamil", three_letter_code="tam"),
    Language("Tatar", three_letter_code="tat"),
    Language("Telugu", three_letter_code="tel"),
    Language("Thai", three_letter_code="tha"),
    TOKI_PONA,
    Language("Turkish", three_letter_code="tur"),
    Language("Turkmen", three_letter_code="tuk"),
    Language("Ukrainian", three_letter_code="ukr"),
    Language("Urdu", three_letter_code="urd"),
    Language("Uzbek", three_letter_code="uzb"),
    Language("Vietnamese", three_letter_code="vie"),
    Language("Welsh", three_letter_code="wel"),
]

LANGUAGE_MAPPINGS: Dict[Language, Union[Language, List[Language]]] = {
    CHINESE_CANTONESE: Language.chinese,
    CHINESE_SIMPLIFIED: Language.chinese,
    CHINESE_TRADITIONAL: Language.chinese,
    CHINESE_BILINGUAL: Language.chinese,
    KHMER: Language.central_khmer,
    MONTENEGRIN: Language.montenegrin,
    ODIA: Language.oriya,
    PORTUGUESE_BR: Language.portuguese,
    PORTUGUESE_MZ: Language.portuguese,
    SERBIAN: Language.serbian,
    SINHALESE: Language.sinhala,
    SPANISH_EU: Language.spanish,
    SPANISH_LA: Language.spanish,
    TOKI_PONA: [],
}


class OpenSubtitlesSourceProvider(SourceProvider):

    def __init__(self, settings: Settings):
        super().__init__(settings, MappedLanguages(SUPPORTED_LANGUAGES, LANGUAGE_MAPPINGS))
        self._http_client.base_url = "https://www.opensubtitles.org"
        self._http_client.default_headers["Host"] = "www.opensubtitles.org"
        self._http_client.default_headers["Referer"] = "https://www.opensubtitles.org"
        self._http_client.default_headers["Accept"] = "text/html,application/xhtml+xml,application/xml"
        self._http_client.default_headers["Accept-Language"] = "en-US,en"
        self._http_client.force_https = True

    @property
    def name(self) -> str:
        return "OpenSubtitles"

    @property
    def short_name(self) -> str:
        return "OS"

    def __fetch_search_title_urls(self, request: SearchRequest, request_internal_languages: List[Language]) -> List[Tuple[str, str]]:
        search_term = self._build_search_term(request)
        language_codes = ",".join([l.three_letter_code for l in request_internal_languages]) \
            if request_internal_languages else 'all'
        http_request = HttpRequest("/en/search2/sublanguageid-%s/moviename-%s" % (language_codes, quote(search_term)))
        http_request.follow_redirects = False
        http_response = self._http_client.exchange(http_request)
        if 300 <= http_response.status_code < 400:
            redirect_url = http_response.get_header_value("Location").replace(" ", "+")
            if re.search(r"/en/search/sublanguageid-[^/]+/idmovie-\d+", redirect_url) or \
                    re.search(r"/en/search/imdbid-\d+/sublanguageid-[^/]+/moviename", redirect_url):
                self._logger.info("Detected redirect to single title URL: " + redirect_url)
                return [(search_term, redirect_url)]
            else:
                self._logger.info("Detected redirect to titles search URL: " + redirect_url)
                http_request = HttpRequest(redirect_url)
                http_response = self._http_client.exchange(http_request)
        titles: List[Tuple[str, str]] = []
        result_tr_tags = http_response.get_data_as_html().select("table#search_results > tbody > tr")[1:]
        for result_tr_tag in result_tr_tags:
            if len(result_tr_tag.find_all("td", recursive=False)) < 5:
                continue  # skip add rows
            if result_tr_tag.select_one('img[src$="/icons/tv-series.gif"]'):
                continue  # skip tv show rows (we are interested only in movies or episode results)
            # <a class="bnone" title="subtitles - &quot;Pluto&quot; Episode #1.3" href="/en/search/sublanguageid-eng,spa/idmovie-1406543">"Pluto" Episode #1.3 (2023)</a>
            result_anchor_tag = result_tr_tag.select_one("a.bnone")
            title_name = normalize_white_space(result_anchor_tag.get_text(strip=True))
            title_url = result_anchor_tag.attrs["href"]
            titles.append((title_name, title_url))
        return titles

    def __parse_single_search_result(self, result_html: BeautifulSoup) -> SearchResult:
        result = SearchResult()
        title_language_cds = normalize_white_space(result_html.select_one("h2").get_text(strip=True))
        match = re.search(
            r'(?P<title>[^<]+)\s+(?P<language>[A-z]+)\s+subtitles \((?P<year>\d\d\d\d)\) (?P<cds>\d+)CD\s+[^<]+', title_language_cds)
        if self._settings.exclude_splitted_subtitles and int(match["cds"]) > 1:
            return None
        result.title = "%s (%s)" % (match['title'], match["year"])
        result.language = self._supported_languages.get_internal_by_name(match["language"])
        result.is_hearing_impaired = result_html.select_one('h1').parent.select_one(
            'img[src$="/icons/hearing_impaired.gif"]') is not None
        details_tag = next(fs for fs in result_html.select("fieldset")
                           if fs.find("legend").get_text(strip=True) == "Subtitle details")
        result.downloads = details_tag.select_one('a[title="downloaded"]').get_text(strip=True)
        result.downloads = int(re.sub(r"[^\d]", "", result.downloads))
        result.id = details_tag.select_one('a[download="download"]').attrs["href"]
        release_image_tag = details_tag.select_one('img[title="Release name"]')
        result.release_info = normalize_white_space(release_image_tag.parent.get_text(strip=True))
        author_image_tag = details_tag.select_one('img[title="Uploader"]')
        result.author = author_image_tag.parent.get_text(strip=True)
        if not result.author or result.author == "Anonymous":
            result.author = None
        result.rating = float(len(details_tag.select('div#subvote img[src$="/icons/star-on.gif"]')))
        return result

    def __parse_many_search_results(self, results_html: BeautifulSoup) -> List[SearchResult]:
        result_tr_tags = results_html.select("table#search_results > tbody > tr:not([style='display:none'])")[1:]
        results: List[SearchResult] = []
        for result_tr_tag in result_tr_tags:
            if len(result_tr_tag.find_all("td", recursive=False)) < 9:
                continue  # skip ad rows
            cds = int(re.sub("CDS?", "", result_tr_tag.select_one("td:nth-child(3)").get_text(strip=1)))
            if self._settings.exclude_splitted_subtitles and cds > 1:
                continue  # skip multi cd results
            result = SearchResult()
            result.title = normalize_white_space(result_tr_tag.select_one("a.bnone").get_text(strip=True))
            next_is_release_info = False
            for content in result_tr_tag.select_one('td:nth-child(1)').contents:
                if next_is_release_info:
                    if isinstance(content, Tag):
                        result.release_info = content.attrs["title"] if content.name == "span" else None
                    else:
                        result.release_info = str(content)
                    break
                if isinstance(content, Tag) and content.name == "br":
                    next_is_release_info = True
            result.is_hearing_impaired = result_tr_tag.select_one('img[src$="/icons/hearing_impaired.gif"]') is not None
            download_anchor = result_tr_tag.select_one('a[href^="/en/subtitleserve/"]')
            result.id = download_anchor.attrs["href"]
            result.downloads = int(re.sub(r"[^\d]", "", download_anchor.get_text(strip=True)))
            result.author = result_tr_tag.select_one('a[href^="/en/profile/iduser-"]').get_text(strip=True)
            result.language = self._supported_languages.get_internal_by_code(
                result_tr_tag.select_one("div.flag").parent.attrs["href"].split("-")[-1:][0])
            if result.language == Language.unknown:
                continue
            result.rating = float(result_tr_tag.select_one('span[title$=" votes"]').get_text(strip=True))
            results.append(result)
        return results

    def _fetch_search_results(self, request: SearchRequest, request_internal_languages: List[Language]) -> List[SearchResult]:
        results: List[SearchResult] = []
        results_counter: SearchResultsCounter = request.build_counter()
        titles = self.__fetch_search_title_urls(request, request_internal_languages)
        for title_index, (title_name, title_url) in enumerate(titles[:MAX_TITLE_RESULTS]):
            self._logger.info("Processing search results for title %s" % title_name)
            http_request = HttpRequest(title_url, follow_redirects=False)
            http_request.sleep_before = timedelta(seconds=1) if title_index > 0 else None
            http_response = self._http_client.exchange(http_request)
            if 300 <= http_response.status_code < 400:
                http_request = HttpRequest(http_response.get_header_value("Location"))
                http_response = self._http_client.exchange(http_request)
                result = self.__parse_single_search_result(http_response.get_data_as_html())
                if result:
                    results.append(result)
                    results_counter.try_accept_result(result)
                    if results_counter.reached_max_results:
                        return results
            else:
                for result in self.__parse_many_search_results(http_response.get_data_as_html()):
                    results.append(result)
                    results_counter.try_accept_result(result)
                    if results_counter.reached_max_results:
                        return results
        return results

    def _get(self, request: GetRequest) -> List[GetResult]:
        http_request = HttpRequest(request.search_result_id)
        http_response = self._http_client.exchange(http_request)
        results = self._process_get_subtitles_data(http_response.file_name, http_response.data)
        return results
