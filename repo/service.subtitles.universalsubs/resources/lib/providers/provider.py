# -*- coding: utf-8 -*-

import logging
from abc import abstractmethod
from typing import List

from resources.lib.providers.getrequest import GetRequest
from resources.lib.providers.getresult import GetResult
from resources.lib.providers.searchrequest import SearchRequest
from resources.lib.providers.searchresult import SearchResult


class Provider:

    def __init__(self):
        self._logger: logging.Logger = logging.getLogger(self.id)

    @property
    def id(self) -> str:
        return 'UniversalSubs.Provider.' + self.name

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def short_name(self) -> str:
        return self.name

    @abstractmethod
    def search(self, request: SearchRequest) -> List[SearchResult]:
        pass

    @abstractmethod
    def get(self, request: GetRequest) -> List[GetResult]:
        pass
