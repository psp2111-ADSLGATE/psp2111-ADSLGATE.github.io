# -*- coding: utf-8 -*-

import os
import os.path
import re
import shutil
import tempfile
from abc import abstractmethod
from pathlib import Path
from typing import List

from resources.lib.common.language import Language
from resources.lib.common.mappedlanguages import MappedLanguages
from resources.lib.common.settings import Settings
from resources.lib.providers.getrequest import GetRequest
from resources.lib.providers.getresult import GetResult
from resources.lib.providers.provider import Provider
from resources.lib.providers.searchrequest import SearchRequest
from resources.lib.providers.searchresult import SearchResult
from resources.lib.utils.cache import Cache
from resources.lib.utils.compression import Compression
from resources.lib.utils.httpclient import HttpClient
from resources.lib.utils.json import to_json
from resources.lib.utils.text import strip_text_from
from resources.lib.utils.yaml import to_yaml

HTTP_USER_AGENT = "User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.21 Safari/537.36"


RE_SUBTITLE_FILE_NAME = re.compile(r"\.(ass|srt|ssa|sub|vvt)$", re.IGNORECASE)
RE_COMPRESSED_FILE_NAME = re.compile(r"\.(zip|rar|7z)$", re.IGNORECASE)
RE_FORCED_SUBTITLE_FILE_NAME = re.compile(r"\b(forced)\b", re.IGNORECASE)
RE_HEARING_IMPAIRED_SUBTITLE_FILE_NAME = re.compile(r"\b(sdh|hi)\b", re.IGNORECASE)

FEATURE_CORRECTIONS = [
    ("5 1", "5.1"),
    ("5 1ch", "5.1"),
    ("7 1", "7.1"),
    ("7 1ch", "7.1"),
    ("dts hd", "DTS-HD"),
    ("23976", "23.976"),
    ("dvdrip", "DVDRip"),
    ("bdrip", "BDRip"),
    ("brrip", "BDRip"),
    ("blu ray", "BluRay"),
    ("bluray", "BluRay"),
    ("directors cut", "DC"),
    ("director's cut", "DC"),
    ("xvid", "XviD"),
    ("divx", "DivX"),
    ("ac3", "AC3"),
    ("sdh", "SDH"),
    ("hi", "HI"),
]


class SourceProvider(Provider):

    def __init__(self,
                 settings: Settings,
                 supported_languages: MappedLanguages):
        super().__init__()
        self.__settings = settings
        self.__supported_languages = supported_languages
        cache = Cache(
            'UniversalSubs.Cache.Provider.' + self.name,
            settings.addon_user_path.joinpath("cache-provider-" + self.name.lower()),
            settings.search_cache_ttl)
        if settings.cache_whole_requests:
            self.__cache = Cache('UniversalSubs.Cache.Provider.' + self.name)  # dummy cache
            self.__http_client = HttpClient(cache=cache)
        else:
            self.__cache = cache
            self.__http_client = HttpClient()

    @property
    def _settings(self) -> Settings:
        return self.__settings

    @property
    def _supported_languages(self) -> MappedLanguages:
        return self.__supported_languages

    @property
    def _http_client(self) -> HttpClient:
        return self.__http_client

    @property
    def _overrides_ratings_from_downloads(self) -> bool:
        return False

    def _overrides_is_sync_from_description_and_filename(self) -> bool:
        return True

    def _compute_result_score(self, search_result: SearchResult) -> float:
        return ((search_result.rating or 0.0) + 1) * (1 if search_result.is_sync else 0.5)

    def _build_search_term(self, request: SearchRequest, include_year: bool = False) -> str:
        if request.is_manual_search:
            return request.manual_search_text
        elif request.is_show_search:
            search_term_parts = [request.show_title]
            if request.show_season_number is not None:
                search_term_parts.append(" S%#02d" % request.show_season_number)
            if request.show_episode_number is not None:
                search_term_parts.append("E%#02d" % request.show_episode_number)
            return "".join(search_term_parts)
        else:
            return "%s%s" % (request.title, " (%s)" % request.year if include_year and request.year else "")

    @abstractmethod
    def _fetch_search_results(self, request: SearchRequest, request_internal_languages: List[Language]) -> List[SearchResult]:
        pass

    def __resolve_search_request_internal_languages(self, request: SearchRequest) -> List[Language]:
        supported_external_languages = self.__supported_languages.external_values.intersection(request.languages or [])
        if self.__supported_languages.external_values and request.languages and not supported_external_languages:
            return None  # source provider supports known set of languages but none match specified in request, will skip request
        # Source providers understand their internal languages representation so we convert the languages before delegating
        supported_internal_languages = self.__supported_languages.to_internal(supported_external_languages)
        # Sort in consistent order, as languages are commonly made part of cache related keys and this way we increase cache hit rate
        supported_internal_languages = sorted(supported_internal_languages, key=lambda l: l.name)
        return supported_internal_languages

    def search(self, request: SearchRequest) -> List[SearchResult]:
        self._logger.info("Searching with request:\n%s" % to_yaml(request))
        request_internal_languages = self.__resolve_search_request_internal_languages(request)
        if request_internal_languages is None:
            self._logger.info("No supported requested languages found, skipping search request")
            return []
        else:
            self._logger.info("Resolved request internal languages:\n%s" % to_yaml(request_internal_languages))
        results: List[SearchResult] = []
        cache_key = "search:%s" % to_json(request)
        results = self.__cache.get_or_initialize(
            cache_key,
            lambda: self._fetch_search_results(request, request_internal_languages))
        request_file_name = request.get_file_name(False)
        for result in results:
            result.provider_name = self.name
            # providers set the language property using the internal languages, we map that to external/standard languages
            result.language = self._supported_languages.to_external_first(result.language)
            self.__update_release_info(result)
            if self._overrides_is_sync_from_description_and_filename:
                result.is_sync = result.release_info and re.search(
                    re.escape(request_file_name), result.release_info, re.I) is not None
        if self._overrides_ratings_from_downloads:
            max_downloads = max(0, float(max([sr.downloads for sr in results], default=0)))
            for result in results:
                result.rating = (result.downloads / max_downloads) * 5 if max_downloads else 0.0
        results = sorted(results, key=lambda search_result: self._compute_result_score(search_result), reverse=True)
        self._logger.info("Found %s search result(s):\n%s", len(results), to_yaml(results))
        # self._logger.info("Found %s search result(s):\n - %s", len(results),
        #                  "\n - ".join(["%s | %s | %s" % (r.id, r.title, r.release_info) for r in results]))
        return results

    def __update_release_info(self, result: SearchResult) -> None:
        if result.release_info:
            result.release_info = re.sub(r"[\s\.\[\]_-]+", " ", result.release_info).strip()
            for feature, corrected_feature in FEATURE_CORRECTIONS:
                result.release_info = re.sub(r"(^|\s)" + re.escape(feature) + r"(\s|$)",
                                             r"\g<1>" + corrected_feature + r"\g<2>", result.release_info, flags=re.IGNORECASE)
            result.release_info = strip_text_from(result.title, result.release_info)
            result.release_info = strip_text_from(re.sub(r"\s*\(\d\d\d\d\)\s*$", "", result.title), result.release_info)
        if self._settings.include_author_on_results and result.author:
            result.release_info = "%s | by %s" % (result.release_info, result.author) \
                if result.release_info else "by %s" % (result.author)
        if self._settings.include_downloads_on_results and result.downloads >= 0:
            result.release_info = "%s | %s dls" % (result.release_info, result.downloads) \
                if result.release_info else "%s dls" % (result.downloads)

    def _is_compressed_file_name(self, file_name: str) -> bool:
        """Test if file name is valid for compressed file."""
        return bool(RE_COMPRESSED_FILE_NAME.search(file_name))

    def _is_subtitle_file_name(self, file_name: str) -> bool:
        """Test if file name is valid for subtitle."""
        return bool(RE_SUBTITLE_FILE_NAME.search(file_name))

    def _is_forced_subtitle_file_name(self, file_name: str) -> bool:
        """Test if file name includes forced markers."""
        return bool(RE_FORCED_SUBTITLE_FILE_NAME.search(file_name))

    def _is_hearing_impaired_subtitle_file_name(self, file_name: str) -> bool:
        """Test if file name includes hearing impaired markers."""
        return bool(RE_HEARING_IMPAIRED_SUBTITLE_FILE_NAME.search(file_name))

    def _build_get_result(self, file_name: str, file_content: bytes) -> GetResult:
        result = GetResult()
        result.file_name = file_name
        result.is_forced = self._is_forced_subtitle_file_name(file_name)
        result.is_hearing_impaired = self._is_hearing_impaired_subtitle_file_name(file_name)
        result.content = file_content
        return result

    def _process_get_subtitles_data(self, file_name: str, file_content: bytes) -> List[GetResult]:
        compression_type = Compression.test_compression_type(file_content=file_content)
        results: List[GetResult] = []
        if not compression_type:
            results.append(self._build_get_result(file_name, file_content))
        else:
            temp_uncompress_directory_path = Path(tempfile.mkdtemp())
            temp_compressed_file_path = temp_uncompress_directory_path.joinpath(file_name)
            try:
                with open(temp_compressed_file_path, "wb") as compressed_file:
                    compressed_file.write(file_content)
            except Exception:
                self._logger.fatal("Failed to save compressed file to '%s'" % temp_compressed_file_path)
            if not Compression.uncompress(temp_compressed_file_path, temp_uncompress_directory_path, compression_type):
                self._logger.fatal("Failed to uncompress file at '%s'" % temp_compressed_file_path)
            else:
                for root_path, _, file_names in os.walk(temp_uncompress_directory_path):
                    root_path = Path(root_path)
                    for file_name in [file_name for file_name in file_names if self._is_subtitle_file_name(file_name)]:
                        with open(root_path.joinpath(file_name), 'rb') as file:
                            file_content: bytes = file.read()
                        results.append(self._build_get_result(file_name, file_content))
            try:
                shutil.rmtree(temp_uncompress_directory_path, ignore_errors=True)
            except Exception:
                self._logger.warning("Error caught cleaning up unpack directory %s", temp_uncompress_directory_path)
                return False
        return results

    @abstractmethod
    def _get(self, request: GetRequest) -> List[GetResult]:
        pass

    def get(self, request: GetRequest) -> List[GetResult]:
        self._logger.info("Getting with request: %s" % to_yaml(request))
        results = self._get(request)
        for result in results:
            result.provider_name = self.name
        self._logger.info("Get results: %s", to_yaml(results))
        return results
