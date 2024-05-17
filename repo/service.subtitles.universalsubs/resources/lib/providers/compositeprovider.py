# -*- coding: utf-8 -*-

import copy
from typing import List

from resources.lib.providers.getrequest import GetRequest
from resources.lib.providers.getresult import GetResult
from resources.lib.providers.provider import Provider
from resources.lib.providers.searchrequest import (SearchRequest,
                                                   SearchResultsCounter)
from resources.lib.providers.searchresult import SearchResult


class CompositeProvider(Provider):

    def __init__(self, sources: List[Provider]):
        super().__init__()
        self.sources = sources

    @property
    def name(self) -> str:
        return "Composite"

    def build_source_search_request(self, request: SearchRequest) -> SearchRequest:
        return request

    def search(self, request: SearchRequest) -> List[SearchResult]:
        results: List[SearchResult] = []
        results_counter: SearchResultsCounter = request.build_counter()
        for source in self.sources:
            try:
                source_request = request
                if request.max_results:
                    source_request = copy.deepcopy(request)
                    source_request.max_results = request.max_results - results_counter.accepted_results
                source_results = source.search(source_request)
                for source_result in source_results:
                    source_result.title = "%s | %s" % (source.short_name, source_result.title)
                    source_result.id = "%s|%s" % (source.name, source_result.id)
                    results.append(source_result)
                    results_counter.try_accept_result(source_result)
                    if results_counter.reached_max_results:
                        return results
            except Exception as e:
                self._logger.error("Caught error fetching results from %s provider." % source.name, exc_info=True)
        return results

    def get(self, request: GetRequest) -> List[GetResult]:
        search_result_id_parts = request.search_result_id.split("|", 1)
        source = next((s for s in self.sources if s.name == search_result_id_parts[0]), None)
        if not source:
            return []
        source_request = copy.deepcopy(request)
        source_request.search_result_id = search_result_id_parts[1]
        source_results: List[GetResult] = source.get(source_request)
        return source_results
