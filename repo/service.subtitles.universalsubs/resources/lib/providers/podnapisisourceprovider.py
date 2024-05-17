# -*- coding: utf-8 -*-

from typing import Dict, List, Set, Tuple, Union
from urllib.parse import parse_qs, urlparse

from bs4 import ResultSet, Tag

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

ARGENTINO = Language("Argentino", two_letter_code="es-ar", standard=False)
BELARUS = Language("Belarus", two_letter_code="be", standard=False)
BRAZILIAN = Language("Brazilian", two_letter_code="pt-br", standard=False)
CANTONESE = Language("Cantonese", two_letter_code="yyef", standard=False)
FARSI = Language("Farsi", two_letter_code="fa", standard=False)
GREENLANDIC = Language("Greenlandic", two_letter_code="kl", standard=False)
HAWAIIAN = Language("Hawaiian", two_letter_code="haw", standard=False)
KHMER = Language("Khmer", two_letter_code="km", standard=False)
KYRGYZ = Language("Kyrgyz", two_letter_code="ky", standard=False)
MANDARIN = Language("Mandarin", two_letter_code="cmn", standard=False)
NDONGA = Language("Ndonga", two_letter_code="nb", standard=False)
PANJABI = Language("Panjabi", two_letter_code="pa", standard=False)
SERBIAN_LATIN = Language("Serbian (Latin)", two_letter_code="sr-latn", standard=False)


SUPPORTED_LANGUAGES: List[Language] = [
    Language("Afrikaans", two_letter_code="af"),
    Language("Albanian", two_letter_code="sq"),
    Language("Amharic", two_letter_code="am"),
    Language("Arabic", two_letter_code="ar"),
    Language("Aragonese", two_letter_code="an"),
    ARGENTINO,
    Language("Assamese", two_letter_code="as"),
    Language("Azerbaijani", two_letter_code="az"),
    Language("Basque", two_letter_code="eu"),
    BELARUS,
    Language("Bengali", two_letter_code="bn"),
    Language("Bosnian", two_letter_code="bs"),
    BRAZILIAN,
    Language("Bulgarian", two_letter_code="bg"),
    CANTONESE,
    Language("Catalan", two_letter_code="ca"),
    Language("Chinese", two_letter_code="zh"),
    Language("Croatian", two_letter_code="hr"),
    Language("Czech", two_letter_code="cs"),
    Language("Danish", two_letter_code="da"),
    Language("Dutch", two_letter_code="nl"),
    Language("Dzongkha", two_letter_code="dz"),
    Language("English", two_letter_code="en"),
    Language("Esperanto", two_letter_code="eo"),
    Language("Estonian", two_letter_code="et"),
    Language("Faroese", two_letter_code="fo"),
    FARSI,
    Language("Finnish", two_letter_code="fi"),
    Language("French", two_letter_code="fr"),
    Language("Georgian", two_letter_code="ka"),
    Language("German", two_letter_code="de"),
    Language("Greek", two_letter_code="el"),
    GREENLANDIC,
    Language("Gujarati", two_letter_code="gu"),
    Language("Haitian", two_letter_code="ht"),
    HAWAIIAN,
    Language("Hebrew", two_letter_code="he"),
    Language("Hindi", two_letter_code="hi"),
    Language("Hungarian", two_letter_code="hu"),
    Language("Icelandic", two_letter_code="is"),
    Language("Indonesian", two_letter_code="id"),
    Language("Irish", two_letter_code="ga"),
    Language("Italian", two_letter_code="it"),
    Language("Japanese", two_letter_code="ja"),
    Language("Javanese", two_letter_code="jv"),
    Language("Kannada", two_letter_code="kn"),
    Language("Kazakh", two_letter_code="kk"),
    KHMER,
    Language("Kinyarwanda", two_letter_code="rw"),
    Language("Korean", two_letter_code="ko"),
    Language("Kurdish", two_letter_code="ku"),
    KYRGYZ,
    Language("Lao", two_letter_code="lo"),
    Language("Latin", two_letter_code="la"),
    Language("Latvian", two_letter_code="lv"),
    Language("Lithuanian", two_letter_code="lt"),
    Language("Luxembourgish", two_letter_code="lb"),
    Language("Macedonian", two_letter_code="mk"),
    Language("Malay", two_letter_code="ms"),
    Language("Malayalam", two_letter_code="ml"),
    Language("Maltese", two_letter_code="mt"),
    MANDARIN,
    Language("Marathi", two_letter_code="mr"),
    Language("Mongolian", two_letter_code="mn"),
    NDONGA,
    Language("Nepali", two_letter_code="ne"),
    Language("Northern Sami", two_letter_code="se"),
    Language("Norwegian Nynorsk", two_letter_code="nn"),
    Language("Norwegian", two_letter_code="no"),
    Language("Occitan", two_letter_code="oc"),
    Language("Oriya", two_letter_code="or"),
    PANJABI,
    Language("Pashto", two_letter_code="ps"),
    Language("Polish", two_letter_code="pl"),
    Language("Portuguese", two_letter_code="pt"),
    Language("Quechua", two_letter_code="qu"),
    Language("Romanian", two_letter_code="ro"),
    Language("Russian", two_letter_code="ru"),
    SERBIAN_LATIN,
    Language("Serbian", two_letter_code="sr"),
    Language("Sinhala", two_letter_code="si"),
    Language("Slovak", two_letter_code="sk"),
    Language("Slovenian", two_letter_code="sl"),
    Language("Spanish", two_letter_code="es"),
    Language("Swahili", two_letter_code="sw"),
    Language("Swedish", two_letter_code="sv"),
    Language("Tagalog", two_letter_code="tl"),
    Language("Tamil", two_letter_code="ta"),
    Language("Telugu", two_letter_code="te"),
    Language("Thai", two_letter_code="th"),
    Language("Turkish", two_letter_code="tr"),
    Language("Turkmen", two_letter_code="tk"),
    Language("Ukrainian", two_letter_code="uk"),
    Language("Urdu", two_letter_code="ur"),
    Language("Uyghur", two_letter_code="ug"),
    Language("Vietnamese", two_letter_code="vi"),
    Language("Volapük", two_letter_code="vo"),
    Language("Walloon", two_letter_code="wa"),
    Language("Welsh", two_letter_code="cy"),
    Language("Xhosa", two_letter_code="xh"),
    Language("Zulu", two_letter_code="zu"),
]

LANGUAGE_MAPPINGS: Dict[Language, Union[Language, List[Language]]] = {
    ARGENTINO: Language.spanish,
    BELARUS: Language.belarusian,
    BRAZILIAN: Language.portuguese,
    CANTONESE: Language.chinese,
    FARSI: Language.persian,
    GREENLANDIC: Language.kalaallisut,
    HAWAIIAN: Language.hawaiian,
    KHMER: Language.central_khmer,
    KYRGYZ: Language.kirghiz,
    MANDARIN: Language.chinese,
    NDONGA: Language.ndonga,
    PANJABI: Language.punjabi,
    SERBIAN_LATIN: Language.serbian,
}


class PodnapisiSourceProvider(SourceProvider):

    def __init__(self, settings: Settings):
        super().__init__(settings, MappedLanguages(SUPPORTED_LANGUAGES, LANGUAGE_MAPPINGS))
        self._http_client.base_url = "https://www.podnapisi.net"
        self._http_client.default_headers["Host"] = "www.podnapisi.net"
        self._http_client.default_headers["Referer"] = "https://www.podnapisi.net"
        self._http_client.default_headers["Accept"] = "text/html,application/xhtml+xml,application/xml"
        self._http_client.default_headers["Accept-Language"] = "en-US,en"

    @property
    def name(self) -> str:
        return "PodnapisiNET"

    @property
    def short_name(self) -> str:
        return "PN"

    def __fetch_search_results_page(self, request: SearchRequest, request_internal_languages: List[Language], page: int) -> Tuple[ResultSet, int]:
        http_request = HttpRequest("/en/subtitles/search/")
        http_request.add_url_query_params({
            "language": sorted([l.two_letter_code for l in request_internal_languages]),
            "movie_type": ["tv-series", "mini-series"] if request.is_show_search else "movie",
            "type": "episode" if request.is_show_search else None,
            "seasons": request.show_season_number if request.is_show_search else None,
            "episodes": request.show_episode_number if request.is_show_search else None,
            "keywords": request.show_title if request.is_show_search else self._build_search_term(request),
            "page": page
        })
        http_request.headers["Accept-Language"] = ";".join([l.two_letter_code for l in request_internal_languages])
        http_response = self._http_client.exchange(http_request)
        results_html = http_response.get_data_as_html()
        results_tbody = results_html.find('tbody')
        if not results_tbody:
            return [], None
        pagination_ul = results_html.select_one("ul.pagination")
        next_page = None
        if pagination_ul:
            next_page_url = urlparse(pagination_ul.select_one("a.page-link").attrs["href"])
            next_page = next((next_page for next_page in parse_qs(next_page_url.query).get("page", [])), None)
        return results_tbody.find_all("tr", recursive=False), next_page

    def _fetch_search_results(self, request: SearchRequest, request_internal_languages: List[Language]) -> List[SearchResult]:
        results: List[SearchResult] = []
        results_counter: SearchResultsCounter = request.build_counter()
        page = 1
        while page:
            row_tags, page = self.__fetch_search_results_page(request, request_internal_languages, page)
            for row_tag in row_tags:
                # fps = float(row.select_one("td:nth-child(2)").get_text(strip=True))
                cds = int(row_tag.select_one("td:nth-child(3)").get_text(strip=True))
                if self._settings.exclude_splitted_subtitles and cds > 1:
                    continue
                result = SearchResult()
                result.id = row_tag.select_one('a[title="Download subtitles."]').attrs["href"]
                result.title = row_tag.select_one('a[alt="Subtitles\' page"]').get_text(strip=True)
                description_tag = row_tag.select_one("td:nth-child(1) > span:nth-child(2)")
                result.release_info = description_tag.get_text(strip=True) if description_tag else None
                result.is_hearing_impaired = row_tag.select_one('i.text-cc') is not None
                result.language = self._supported_languages.get_internal_by_code(
                    row_tag.select_one("abbr.language").get_text(strip=True))
                author_tag = row_tag.select_one(
                    'a[title^="Add "][title$=" to active filters."][href*="&contributors="]')
                result.author = author_tag.get_text(strip=True) if author_tag else None
                rating_tag = row_tag.select_one("div.rating")
                rating_td_tag: Tag = next(p for p in rating_tag.parents if p.name == "td")
                result.rating = float(rating_tag.attrs["data-title"].split("%")[0])/20
                downloads_tag = rating_td_tag.find_previous("td").find_previous("td")
                result.downloads = int(downloads_tag.get_text(strip=True))
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
