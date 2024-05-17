# -*- coding: utf-8 -*-

import math
import re
from datetime import timedelta
from typing import Dict, List, Set, Tuple, Union
from urllib.parse import quote

from bs4 import BeautifulSoup

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
from resources.lib.utils.text import (normalize_white_space, strip_common_text,
                                      strip_text_from)

MAX_TITLE_RESULTS = 5

BRAZILLIAN_PORTUGUESE = Language("Brazillian Portuguese", standard=False)
BULGARIAN_ENGLISH = Language("Bulgarian/ English", standard=False)
CAMBODIAN_KHMER = Language("Cambodian/Khmer", standard=False)
CHINESE_BG_CODE = Language("Chinese BG code", standard=False)
CHINESE_BIG_5_CODE = Language("Big 5 code", standard=False)
DUTCH_ENGLISH = Language("Dutch/ English", standard=False)
ENGLISH_GERMAN = Language("English/ German", standard=False)
FARSI_PERSIAN = Language("Farsi/Persian", standard=False)
GREENLANDIC = Language("Greenlandic", standard=False)
HUNGARIAN_ENGLISH = Language("Hungarian/ English", standard=False)

SUPPORTED_LANGUAGES: List[Language] = [
    Language("Albanian"),
    Language("Arabic"),
    Language("Armenian"),
    Language("Azerbaijani"),
    Language("Basque"),
    Language("Belarusian"),
    Language("Bengali"),
    Language("Bosnian"),
    BRAZILLIAN_PORTUGUESE,
    Language("Bulgarian"),
    BULGARIAN_ENGLISH,
    Language("Burmese"),
    CAMBODIAN_KHMER,
    Language("Catalan"),
    CHINESE_BG_CODE,
    CHINESE_BIG_5_CODE,
    Language("Croatian"),
    Language("Czech"),
    Language("Danish"),
    Language("Dutch"),
    DUTCH_ENGLISH,
    Language("English"),
    ENGLISH_GERMAN,
    Language("Esperanto"),
    Language("Estonian"),
    FARSI_PERSIAN,
    Language("Finnish"),
    Language("French"),
    Language("Georgian"),
    Language("German"),
    Language("Greek"),
    GREENLANDIC,
    Language("Hebrew"),
    Language("Hindi"),
    Language("Hungarian"),
    HUNGARIAN_ENGLISH,
    Language("Icelandic"),
    Language("Indonesian"),
    Language("Italian"),
    Language("Japanese"),
    Language("Kannada"),
    Language("Kinyarwanda"),
    Language("Korean"),
    Language("Kurdish"),
    Language("Latvian"),
    Language("Lithuanian"),
    Language("Macedonian"),
    Language("Malay"),
    Language("Malayalam"),
    Language("Manipuri"),
    Language("Mongolian"),
    Language("Nepali"),
    Language("Norwegian"),
    Language("Pashto"),
    Language("Polish"),
    Language("Portuguese"),
    Language("Punjabi"),
    Language("Romanian"),
    Language("Russian"),
    Language("Serbian"),
    Language("Sinhala"),
    Language("Slovak"),
    Language("Slovenian"),
    Language("Somali"),
    Language("Spanish"),
    Language("Sundanese"),
    Language("Swahili"),
    Language("Swedish"),
    Language("Tagalog"),
    Language("Tamil"),
    Language("Telugu"),
    Language("Thai"),
    Language("Turkish"),
    Language("Ukrainian"),
    Language("Urdu"),
    Language("Vietnamese"),
    Language("Yoruba"),
]

LANGUAGE_MAPPINGS: Dict[Language, Union[Language, List[Language]]] = {
    BRAZILLIAN_PORTUGUESE:  Language.portuguese,
    BULGARIAN_ENGLISH: Language.bulgarian,
    CAMBODIAN_KHMER: Language.central_khmer,
    CHINESE_BG_CODE: Language.chinese,
    CHINESE_BIG_5_CODE: Language.chinese,
    DUTCH_ENGLISH: Language.dutch,
    ENGLISH_GERMAN: Language.german,
    FARSI_PERSIAN: Language.persian,
    GREENLANDIC: Language.kalaallisut,
    HUNGARIAN_ENGLISH: Language.hungarian,
}

NUMBER_TO_POSITION = {
    1: "First",
    2: "Second",
    3: "Third",
    4: "Fourth",
    5: "Fifth",
    6: "Sixth",
    7: "Seventh",
    8: "Eighth",
    9: "Ninth",
    10: "Tenth",
    11: "Eleventh",
    12: "Twelfth",
    13: "Thirteenth",
    14: "Fourteenth",
    15: "Fifteenth",
    16: "Sixteenth",
    17: "Seventeenth",
    18: "Eighteenth",
    19: "Nineteenth",
    20: "Twentieth",
    21: "Twenty-first",
    22: "Twenty-second",
    23: "Twenty-third",
    24: "Twenty-fourth",
    25: "Twenty-fifth",
    26: "Twenty-sixth",
    27: "Twenty-seventh",
    28: "Twenty-eighth",
    29: "Twenty-ninth",
    30: "Thirtieth",
    31: "Thirty-first",
    32: "Thirty-second",
    33: "Thirty-third",
    34: "Thirty-fourth",
    35: "Thirty-fifth",
    36: "Thirty-sixth",
    37: "Thirty-seventh",
    38: "Thirty-eighth",
    39: "Thirty-ninth",
    40: "Fortieth",
    41: "Forty-first",
    42: "Forty-second",
    43: "Forty-third",
    44: "Forty-fourth",
    45: "Forty-fifth",
    46: "Forty-sixth",
    47: "Forty-seventh",
    48: "Forty-eighth",
    49: "Forty-ninth",
    50: "Fiftieth",
    51: "Fifty-first",
    52: "Fifty-second",
    53: "Fifty-third",
    54: "Fifty-fourth",
    55: "Fifty-fifth",
    56: "Fifty-sixth",
    57: "Fifty-seventh",
    58: "Fifty-eighth",
    59: "Fifty-ninth",
    60: "Sixtieth",
    61: "Sixty-first",
    62: "Sixty-second",
    63: "Sixty-third",
    64: "Sixty-fourth",
    65: "Sixty-fifth",
    66: "Sixty-sixth",
    67: "Sixty-seventh",
    68: "Sixty-eighth",
    69: "Sixty-ninth",
    70: "Seventieth",
    71: "Seventy-first",
    72: "Seventy-second",
    73: "Seventy-third",
    74: "Seventy-fourth",
    75: "Seventy-fifth",
    76: "Seventy-sixth",
    77: "Seventy-seventh",
    78: "Seventy-eighth",
    79: "Seventy-ninth",
    80: "Eightieth",
    81: "Eighty-first",
    82: "Eighty-second",
    83: "Eighty-third",
    84: "Eighty-fourth",
    85: "Eighty-fifth",
    86: "Eighty-sixth",
    87: "Eighty-seventh",
    88: "Eighty-eighth",
    89: "Eighty-ninth",
    90: "Ninetieth",
    91: "Ninety-first",
    92: "Ninety-second",
    93: "Ninety-third",
    94: "Ninety-fourth",
    95: "Ninety-fifth",
    96: "Ninety-sixth",
    97: "Ninety-seventh",
    98: "Ninety-eighth",
    99: "Ninety-ninth",
}


class SubsceneSourceProvider(SourceProvider):

    def __init__(self, settings: Settings):
        super().__init__(settings, MappedLanguages(SUPPORTED_LANGUAGES, LANGUAGE_MAPPINGS))
        self._http_client.base_url = "https://subscene.com"
        self._http_client.default_headers["Host"] = "subscene.com"
        self._http_client.default_headers["Referer"] = "https://subscene.com"
        self._http_client.default_headers["Accept"] = "text/html,application/xhtml+xml,application/xml"
        self._http_client.default_headers["Accept-Language"] = "en-US,en"
        self._http_client.force_https = True

    @property
    def name(self) -> str:
        return "Subscene"

    @property
    def short_name(self) -> str:
        return "SC"

    def _build_search_term(self, request: SearchRequest, include_year: bool = False) -> str:
        if request.is_manual_search:
            return request.manual_search_text
        elif request.is_show_search:
            search_term_parts = [request.show_title]
            if request.show_season_number is not None:
                search_term_parts.append(" - %s season" % NUMBER_TO_POSITION[request.show_season_number])
            # if request.show_episode_number is not None:
            #     search_term_parts.append(" - %s episode" % NUMBER_TO_POSITION[request.show_episode_number])
            return "".join(search_term_parts)
        else:
            return "%s%s" % (request.title, " (%s)" % request.year if include_year and request.year else "")

    def __fetch_search_title_urls(self, request: SearchRequest) -> List[Tuple[str, str]]:
        http_request = HttpRequest("/subtitles/searchbytitle")
        http_request.set_urlencoded_form_data({"query": self._build_search_term(request), "l": ""})
        http_response = self._http_client.exchange(http_request)
        titles: List[Tuple[str, str]] = []
        result_anchor_tags = http_response.get_data_as_html().select("div.search-result > ul > li > div.title > a")
        for result_anchor_tag in result_anchor_tags:
            title_name = normalize_white_space(result_anchor_tag.get_text(strip=True))
            title_url = result_anchor_tag.attrs["href"]
            if request.is_show_search and request.show_season_number:
                if not re.search(r" - %s Season(\s+\(\d\d\d\d\)$|)" % NUMBER_TO_POSITION[request.show_season_number], title_name):
                    continue
            if any(t for t in titles if t[1] == title_url):
                continue
            titles.append((title_name, title_url))
        return titles

    def __matches_episode(self, text: str, year: int, season_number: int, episode_number, default_result: bool = True) -> bool:
        if year is not None and year > 1900:
            text = text.replace(str(year), "")
        if season_number is not None:
            text = re.sub("S0+" + str(season_number), "", text)
        text = re.sub(r"(480p|720p|1080p|1440p|2160p|2k|4k|x\.265|x\.264|h\.265|h\.264|2.0|5.1|7.1)",
                      "", text, flags=re.IGNORECASE)
        separators = r"[\s\[\]\(\)\._~-]"
        episode_range_re = r"(^|" + separators + r")E?(?P<rstart>\d+)\s*[-~_]\s*E?(?P<rend>\d+)(" + separators + r"|$)"
        episode_range_match = re.search(episode_range_re, text, flags=re.IGNORECASE)
        if episode_range_match:
            return int(episode_range_match["rstart"]) < episode_number < int(episode_range_match["rend"])
        episode_number_re = r"(^|" + separators + r")E?(?P<number>\d+)(" + separators + r"|$)"
        episode_number_match = re.search(episode_number_re, text, flags=re.IGNORECASE)
        if episode_number_match:
            return episode_number == int(episode_number_match["number"])
        return default_result

    def __parse_many_search_results(self,
                                    request: SearchRequest,
                                    request_internal_languages: List[Language],
                                    title: str,
                                    results_html: BeautifulSoup) -> List[SearchResult]:
        result_tr_tags = results_html.select("div.content tbody tr")[1:]
        results: List[SearchResult] = []
        for result_tr_tag in result_tr_tags:
            if len(result_tr_tag.find_all("td", recursive=False)) < 5:
                continue  # skip ad rows
            result = SearchResult()
            download_anchor = result_tr_tag.select_one('td:nth-child(1) > a')
            if not download_anchor:
                continue
            result.id = download_anchor.attrs["href"]
            result.title = title
            result.language = self._supported_languages.get_internal_by_name(
                download_anchor.select_one("span:nth-child(1)").get_text(strip=True))
            result.release_info = download_anchor.select_one("span:nth-child(2)").get_text(strip=True)
            if not request.is_show_search:
                result.id = "||%s" % result.id
            else:
                if not self.__matches_episode(result.release_info, request.year, request.show_season_number, request.show_episode_number):
                    continue
                result.id = "%s|%s|%s" % (request.show_season_number, request.show_episode_number, result.id)
            if not result.language in request_internal_languages:
                continue
            result.is_hearing_impaired = result_tr_tag.select_one("td.a41") is not None
            result.author = result_tr_tag.select_one('a[href^="/u/"]').get_text(strip=True)
            result.rating = 10 \
                if download_anchor.select_one(".positive-icon") \
                else 5 if download_anchor.select_one(".neutral-icon") else 0
            results.append(result)
        return results

    def _fetch_search_results(self, request: SearchRequest, request_internal_languages: List[Language]) -> List[SearchResult]:
        results: List[SearchResult] = []
        results_counter: SearchResultsCounter = request.build_counter()
        titles = self.__fetch_search_title_urls(request)
        for title_index, (title_name, title_url) in enumerate(titles[:MAX_TITLE_RESULTS]):
            self._logger.info("Processing search results for title %s" % title_name)
            http_request = HttpRequest(title_url)
            http_request.headers["Referer"] = "https://subscene.com/subtitles/searchbytitle"
            http_request.sleep_before = timedelta(seconds=1) if title_index > 0 else None
            http_response = self._http_client.exchange(http_request)
            for result in self.__parse_many_search_results(request, request_internal_languages, title_name, http_response.get_data_as_html()):
                results.append(result)
                results_counter.try_accept_result(result)
                if results_counter.reached_max_results:
                    return results
        return results

    def _get(self, request: GetRequest) -> List[GetResult]:
        search_result_id_parts = request.search_result_id.split("|", 2)
        http_request = HttpRequest(search_result_id_parts[2])
        http_response = self._http_client.exchange(http_request)
        download_url = http_response.get_data_as_html().select_one("a#downloadButton").attrs["href"]
        http_request = HttpRequest(download_url)
        http_response = self._http_client.exchange(http_request)
        results = self._process_get_subtitles_data(http_response.file_name, http_response.data)
        if search_result_id_parts[0] or search_result_id_parts[1] and len(results) > 1:
            # NOTE: most Subscene results for TV Shows are multi-episode packs, so we attempt to
            # find the results matching the requested season/episode number, discard the rest.
            season_number = int(search_result_id_parts[0])
            episode_number = int(search_result_id_parts[1])
            # In a multi-episode pack, all files are usually prefixed or suffixed with the same text; because this prefix
            # or suffix may include numbers, it's best to strip it before attempting to parse season/episode information.
            file_names = strip_common_text([r.file_name for r in results])
            results = [
                result for index, result in enumerate(results)
                if self.__matches_episode(file_names[index], None, season_number, episode_number, False)
            ]
        return results
