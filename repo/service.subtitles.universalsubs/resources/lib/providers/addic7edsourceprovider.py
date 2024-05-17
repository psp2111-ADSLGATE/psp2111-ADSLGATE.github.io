# -*- coding: utf-8 -*-

import re
from datetime import timedelta
from typing import Dict, List, Tuple, Union

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

MAX_TITLE_RESULTS = 5


CANTONESE = Language("Cantonese", standard=False)
CATALA = Language("Català", standard=False)
CHINESE_SIMPLIFIED = Language("Chinese (Simplified)", standard=False)
CHINESE_TRADITIONAL = Language("Chinese (Traditional)", standard=False)
EUSKERA = Language("Euskera", standard=False)
FRENCH_CANADIAN = Language("French (Canadian)", standard=False)
GALEGO = Language("Galego", standard=False)
PORTUGUESE_BRAZILIAN = Language("Portuguese (Brazilian)", standard=False)
SERBIAN_CYRILLIC = Language("Serbian (Cyrillic)", standard=False)
SERBIAN_LATIN = Language("Serbian (Latin)", standard=False)
SPANISH_ARGENTINA = Language("Spanish (Argentina)", standard=False)
SPANISH_LATIN_AMERICA = Language("Spanish (Latin America)", standard=False)
SPANISH_SPAIN = Language("Spanish (Spain)", standard=False)

SUPPORTED_LANGUAGES: List[Language] = [
    Language("Albanian"),
    Language("Arabic"),
    Language("Armenian"),
    Language("Azerbaijani"),
    Language("Bengali"),
    Language("Bosnian"),
    Language("Bulgarian"),
    CANTONESE,
    CATALA,
    CHINESE_SIMPLIFIED,
    CHINESE_TRADITIONAL,
    Language("Croatian"),
    Language("Czech"),
    Language("Danish"),
    Language("Dutch"),
    Language("English"),
    Language("Estonian"),
    EUSKERA,
    Language("Finnish"),
    Language("French"),
    FRENCH_CANADIAN,
    GALEGO,
    Language("German"),
    Language("Greek"),
    Language("Hebrew"),
    Language("Hindi"),
    Language("Hungarian"),
    Language("Icelandic"),
    Language("Indonesian"),
    Language("Italian"),
    Language("Japanese"),
    Language("Kannada"),
    Language("Klingon"),
    Language("Korean"),
    Language("Latvian"),
    Language("Lithuanian"),
    Language("Macedonian"),
    Language("Malay"),
    Language("Malayalam"),
    Language("Marathi"),
    Language("Norwegian"),
    Language("Persian"),
    Language("Polish"),
    Language("Portuguese"),
    PORTUGUESE_BRAZILIAN,
    Language("Romanian"),
    Language("Russian"),
    SERBIAN_CYRILLIC,
    SERBIAN_LATIN,
    Language("Sinhala"),
    Language("Slovak"),
    Language("Slovenian"),
    Language("Spanish"),
    SPANISH_ARGENTINA,
    SPANISH_LATIN_AMERICA,
    SPANISH_SPAIN,
    Language("Swedish"),
    Language("Tagalog"),
    Language("Tamil"),
    Language("Telugu"),
    Language("Thai"),
    Language("Turkish"),
    Language("Ukrainian"),
    Language("Vietnamese"),
    Language("Welsh"),
]

LANGUAGE_MAPPINGS: Dict[Language, Union[Language, List[Language]]] = {
    CANTONESE: Language.chinese,
    CATALA: Language.catalan,
    CHINESE_SIMPLIFIED: Language.chinese,
    CHINESE_TRADITIONAL: Language.chinese,
    EUSKERA: Language.basque,
    FRENCH_CANADIAN: Language.french,
    GALEGO: Language.galician,
    PORTUGUESE_BRAZILIAN: Language.portuguese,
    SERBIAN_CYRILLIC: Language.serbian,
    SERBIAN_LATIN: Language.serbian,
    SPANISH_ARGENTINA: Language.spanish,
    SPANISH_LATIN_AMERICA: Language.spanish,
    SPANISH_SPAIN: Language.spanish,
}


class Addic7edSourceProvider(SourceProvider):

    def __init__(self, settings: Settings):
        super().__init__(settings, MappedLanguages(SUPPORTED_LANGUAGES, LANGUAGE_MAPPINGS))
        self._http_client.base_url = "https://www.addic7ed.com"
        self._http_client.default_headers["Host"] = "www.addic7ed.com"
        self._http_client.default_headers["Referer"] = "https://www.addic7ed.com"
        self._http_client.default_headers["Accept"] = "text/html,application/xhtml+xml,application/xml"
        self._http_client.default_headers["Accept-Language"] = "en-US,en"

    @property
    def name(self) -> str:
        return "Addic7ed"

    @property
    def short_name(self) -> str:
        return "AD7"

    @property
    def _overrides_ratings_from_downloads(self) -> bool:
        return True

    def __fetch_search_title_urls(self, request: SearchRequest) -> List[Tuple[str, str]]:
        http_request = HttpRequest("/search.php", follow_redirects=False)
        http_request.add_url_query_params({"search": self._build_search_term(request), "Submit": "Search"})
        http_response = self._http_client.exchange(http_request)
        titles: List[Tuple[str, str]] = []
        if 300 <= http_response.status_code < 400:
            title_name = self._build_search_term(request)
            title_url = http_response.get_header_value("Location")
            titles.append((title_name, title_url))
        else:
            titles_html = http_response.get_data_as_html()
            title_anchors = titles_html.select('table.tabel[align="center"][width="80%"][border="0"] tr a')
            for title_anchor in title_anchors:
                # title_tr.select_one('img[src$="/film.png"]') # movie result
                # title_tr.select_one('img[src$="/television.png"]') # tv show result
                title_name = title_anchor.get_text(strip=True)
                title_url = title_anchor.attrs["href"]
                titles.append((title_name, title_url))
        return titles

    def _fetch_search_results(self, request: SearchRequest, request_internal_languages: List[Language]) -> List[SearchResult]:
        results: List[SearchResult] = []
        titles = self.__fetch_search_title_urls(request)
        results_counter: SearchResultsCounter = request.build_counter()
        for title_index, (title_name, title_url) in enumerate(titles[:MAX_TITLE_RESULTS]):
            self._logger.info("Processing search results for title %s" % title_name)
            http_request = HttpRequest(title_url)
            http_request.sleep_before = timedelta(seconds=1) if title_index > 0 else None
            http_response = self._http_client.exchange(http_request)
            results_html = http_response.get_data_as_html()
            results_img = results_html.select('img[src$="images/folder_page.png"]')
            for result_img in results_img:
                result_tbody = result_img.find_parent("tbody")
                result = SearchResult()
                result.language = self._supported_languages.get_internal_by_name(
                    result_tbody.select_one("td.language").get_text(strip=True))
                if not result.language in request_internal_languages:
                    continue
                result.id = result_tbody.select_one('a.buttonDownload[href^="/original/"]').attrs["href"]
                result.title = title_name
                result.release_info = result_img.parent.get_text(strip=True)
                result.release_info = re.sub(
                    r"^Version (.*), Duration: [\d.]+", r"\1",
                    result.release_info)
                result.author = result_tbody.select_with('a[href^="/user/"]', lambda t: t.get_text(strip=True))
                result.downloads = int(re.sub(
                    r"^\d+ times edited · (\d+) Downloads · \d+ sequences", r"\1",
                    result_tbody.select_one('td.newsDate[colspan="2"]').get_text(strip=True)))
                result.is_hearing_impaired = False  # no way to detect if match has information for  HI
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
