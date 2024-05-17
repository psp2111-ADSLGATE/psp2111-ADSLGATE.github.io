# -*- coding: utf-8 -*-

import logging
import re
import time
from abc import abstractmethod
from datetime import timedelta
from typing import Any, Callable, List

from resources.lib.common.language import Language
from resources.lib.common.mappedlanguages import MappedLanguages
from resources.lib.common.settings import Settings
from resources.lib.utils.cache import Cache
from resources.lib.utils.httpclient import HttpClient


class UnsupportedTranslationException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

    def __str__(self):
        return self.message


class TranslateException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

    def __str__(self):
        return self.message


class Translator:

    def __init__(self, settings: Settings, languages: MappedLanguages):
        self._logger: logging.Logger = logging.getLogger(self.id)
        self.__languages = languages
        cache = Cache(
            'UniversalSubs.Cache.Translator.' + self.name,
            settings.addon_user_path.joinpath("cache-translator-" + self.name.lower()),
            settings.translation_cache_ttl)
        if False and settings.cache_whole_requests:  # NOTE: it barely ever makes sense to cache at request level from translations
            self._cache = Cache('UniversalSubs.Cache.Translator.' + self.name)  # dummy cache
            self._http_client = HttpClient(cache=cache)
        else:
            self._cache = cache
            self._http_client = HttpClient()

    @property
    def id(self) -> str:
        return 'UniversalSubs.Translator.' + self.name

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def short_name(self) -> str:
        return self.name

    @property
    def requires_normalized_spaces(self) -> bool:
        return True

    @abstractmethod
    def supports_translation(self, from_language: Language, to_language: Language) -> bool:
        return self.__languages.has_any_external(from_language) and self.__languages.has_any_external(to_language)

    @abstractmethod
    def _translate(self, internal_from_language: Language, internal_to_language: Language, texts: List[str]) -> List[str]:
        pass

    def _translate_in_blocks(
            self,
            texts: List[str],
            block_size: int,
            separator: str,
            # translate: Callable[[str | List[str]], str | List[str]],
            translate: Callable[[Any], Any],
            translate_params: List[str] = None,
            delay: timedelta = timedelta(seconds=0.5)
    ) -> List[str]:
        translations: List[str] = []
        text_blocks = self._build_text_blocks(texts, block_size, separator)
        delay_seconds = delay.total_seconds() if delay and delay.total_seconds() > 0 else None
        for text_block_index, text_block in enumerate(text_blocks):
            self._logger.debug("Processing text block %d of %d" % (text_block_index+1, len(text_blocks)))
            if translate_params is None:
                translate_result = translate(text_block)
            else:
                translate_result = translate(text_block, *translate_params)
            if isinstance(translate_result, str):
                translate_params = None
                translation = translate_result
            else:
                translate_params = translate_result[1:]
                translation = translate_result[0]
            if translation is None:
                raise TranslateException("Error obtaining translation from %s provider." % self.name)
            translations.extend(translation.split(separator))
            if delay_seconds:
                time.sleep(delay_seconds)
        assert len(texts) == len(translations)
        return translations

    def _build_text_blocks(self, texts: List[str], block_size: int, separator: str) -> List[str]:
        text_blocks: List[str] = []
        current_text_block = ""
        for text in texts:
            modified_current_text_block = current_text_block
            if modified_current_text_block:
                modified_current_text_block += separator
            modified_current_text_block += text
            if len(modified_current_text_block) > block_size:
                if current_text_block:
                    text_blocks.append(current_text_block)
                    current_text_block = text
                else:
                    # the current text is larger than the maximum requested block size, yet there's
                    # nothing we can do, since we don't allow breaking a text into differnt chunks
                    text_blocks.append(text)
            else:
                current_text_block = modified_current_text_block
        if current_text_block:
            text_blocks.append(current_text_block)
        return text_blocks

    def __ensure_supports_translation(self, from_language: Language, to_language: Language) -> None:
        if not self.supports_translation(from_language, to_language):
            raise UnsupportedTranslationException(
                "Translation from %s to %s not supported by %s provider." % (from_language.name, to_language.name, self.name))

    def translate(self, from_language: Language, to_language: Language, texts: List[str]) -> List[str]:
        self.__ensure_supports_translation(from_language, to_language)
        translations: List[str] = []
        pending_translations: List[str] = []
        pending_translations_keys: List[str] = []
        for text in texts:
            text = re.sub(r"\s+", " ",  text).strip() if self.requires_normalized_spaces else text.strip()
            cache_key = "%s:%s:%s" % (from_language.two_letter_code, to_language.two_letter_code, text)
            translation: str = self._cache.get(cache_key)
            translations.append(translation)
            if translation is None:
                pending_translations.append(text)
                pending_translations_keys.append(cache_key)
        if pending_translations:
            internal_from_language = self.__languages.to_internal_first(from_language)
            internal_to_language = self.__languages.to_internal_first(to_language)
            self._logger.info("Translations for %s lines out of %s not found in cache, translating from %s to %s",
                              len(pending_translations), len(texts), internal_from_language, internal_to_language)
            pending_translations = self._translate(internal_from_language, internal_to_language, pending_translations)
            for translation_index, translation in enumerate(translations):
                if translation is None:
                    translation = pending_translations.pop(0)
                    cache_key = pending_translations_keys.pop(0)
                    translations[translation_index] = translation
                    self._cache.set(cache_key, translation)
                    try:
                        assert translation == self._cache.get(cache_key, None)
                    except Exception as e:
                        self._logger.error(
                            "Translation for line %s added to cache already but not present in it", cache_key)
                        # raise e
        return translations
