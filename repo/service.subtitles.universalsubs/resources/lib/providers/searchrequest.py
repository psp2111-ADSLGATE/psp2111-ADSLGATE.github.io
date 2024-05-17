# -*- coding: utf-8 -*-

import os
from pathlib import Path
from re import IGNORECASE, UNICODE, compile
from typing import Callable, List
from urllib.parse import ParseResult, unquote, urlparse
from urllib.request import url2pathname

from resources.lib.common.language import Language
from resources.lib.providers.searchresult import SearchResult

URL_REGEX = compile(r'[A-z]+://.*', IGNORECASE | UNICODE)


def is_file_path(file_path_or_url: str) -> bool:
    return not URL_REGEX.search(file_path_or_url)


class SearchResultsCounter:

    def __init__(self, max_results: int, accept_result_predicate: Callable[[SearchResult], bool]) -> None:
        self._max_results: int = max_results
        self._accept_result_predicate: Callable[[SearchResult], bool] = accept_result_predicate
        self._accepted_results: int = 0

    def try_accept_result(self, search_result: SearchResult) -> bool:
        if not self._accept_result_predicate or self._accept_result_predicate(search_result):
            self._accepted_results += 1

    @property
    def max_results(self) -> int:
        return self._max_results

    @property
    def accepted_results(self) -> int:
        return self._accepted_results

    @property
    def pending_results(self) -> int:
        return self._max_results - self._accepted_results if self._max_results else 0

    @property
    def reached_max_results(self) -> bool:
        return self._accepted_results >= self._max_results if self._max_results else False


class SearchRequest:

    year: int = None
    show_season_number: int = None
    show_episode_number: int = None
    show_title: str = None
    title: str = None
    languages: List[Language] = []
    manual_search_text: str = None
    file_url: str
    file_languages: List[Language] = []
    max_results: int = 50
    count_result_predicate: Callable[[SearchResult], bool] = None

    @property
    def is_show_search(self) -> bool:
        return True if self.show_title else False

    @property
    def is_manual_search(self) -> bool:
        return self.manual_search_text

    @property
    def is_file(self) -> bool:
        return self.file_url.startswith("file://")

    @property
    def file_parsed_url(self) -> ParseResult:
        return urlparse(self.file_url) if self.file_url else None

    @property
    def file_path(self) -> Path:
        if not self.is_file:
            return None
        file_parsed_url = self.file_parsed_url
        host = "{0}{0}{mnt}{0}".format(os.path.sep, mnt=file_parsed_url.netloc)
        return Path(os.path.normpath(os.path.join(host, url2pathname(unquote(file_parsed_url.path)))))

    def get_file_name(self, include_extension: bool = True) -> str:
        (file_directory, file_name) = os.path.split(unquote(self.file_parsed_url.path))
        if include_extension:
            return file_name
        (file_base_name, file_ext) = os.path.splitext(file_name)
        return file_base_name

    def set_file_url_or_path(self, file_path_or_url: str) -> None:
        url = Path(file_path_or_url).as_uri() if is_file_path(file_path_or_url) else file_path_or_url
        self.file_url = url

    def build_counter(self) -> SearchResultsCounter:
        return SearchResultsCounter(self.max_results, self.count_result_predicate)
