# -*- coding: utf-8 -*-

from resources.lib.common.language import Language


class SearchResult:

    def __init__(self):
        self.id: str = None
        self.title: str = None
        self.release_info: str = None
        self.language: Language = None
        self.author: str = None
        self.downloads: int = -1
        self.rating: float = 0.0  # must be a value from 0.0 to 5.0
        self.is_sync: bool = False
        self.is_hearing_impaired: bool = False
        self.provider_name: str = None
