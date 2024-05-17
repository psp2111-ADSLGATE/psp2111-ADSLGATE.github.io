# -*- coding: utf-8 -*-

from datetime import timedelta
from pathlib import Path
from typing import List

from resources.lib.common.language import Language


class Settings:

    addon_id: str
    addon_path: Path
    addon_user_path: Path

    providers: List[str] = []
    file_system_provider_path: Path
    translators: List[str] = []
    translation_extra_languages: List[Language] = [
        Language.english,
        Language.chinese,
        Language.hindi,
        Language.spanish,
        Language.french,
        Language.portuguese,
        Language.italian
    ]
    include_author_on_results: bool = True
    include_downloads_on_results: bool = True
    search_cache_ttl: timedelta = timedelta(minutes=30)
    translation_cache_ttl: timedelta = timedelta(days=30)
    cache_whole_requests: bool = False
    exclude_splitted_subtitles = True

    clean_up_subtitles = True
    clean_up_ads = True
    clean_up_hi_markers = False
    clean_up_rules_update_url: str = "https://raw.githubusercontent.com/bkiziuk/service.subsmangler/master/resources/regexdef.def"
    clean_up_rules_update_interval: timedelta = None
