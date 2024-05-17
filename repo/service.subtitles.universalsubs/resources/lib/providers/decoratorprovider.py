# -*- coding: utf-8 -*-

from typing import List

from resources.lib.providers.getrequest import GetRequest
from resources.lib.providers.getresult import GetResult
from resources.lib.providers.provider import Provider
from resources.lib.providers.searchrequest import SearchRequest
from resources.lib.providers.searchresult import SearchResult


class DecoratorProvider(Provider):

    def __init__(self, source: Provider):
        self.source = source
        super().__init__()

    def build_source_search_request(self, request: SearchRequest) -> SearchRequest:
        return request

    def _transform_search_results(self, request: SearchRequest, source_request: SearchRequest, source_results: List[SearchResult]) -> List[SearchResult]:
        return source_results

    def search(self, request: SearchRequest) -> List[SearchResult]:
        source_request = self.build_source_search_request(request)
        source_results = self.source.search(source_request)
        transformed_results = self._transform_search_results(request, source_request, source_results)
        return transformed_results

    def build_source_get_request(self, request: GetRequest) -> GetRequest:
        return request

    def _transform_get_results(self, request: GetRequest, source_request: GetRequest, source_results: List[GetResult]) -> List[GetResult]:
        return source_results

    def get(self, request: GetRequest) -> List[GetResult]:
        source_request = self.build_source_get_request(request)
        source_results: List[GetResult] = self.source.get(source_request)
        transformed_results = self._transform_get_results(request, source_request, source_results)
        return transformed_results
