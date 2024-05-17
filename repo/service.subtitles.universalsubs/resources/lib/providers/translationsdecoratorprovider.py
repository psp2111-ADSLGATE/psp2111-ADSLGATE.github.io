# -*- coding: utf-8 -*-

import copy
from typing import List

from resources.lib.common.language import Language
from resources.lib.providers.decoratorprovider import DecoratorProvider
from resources.lib.providers.getrequest import GetRequest
from resources.lib.providers.getresult import GetResult
from resources.lib.providers.provider import Provider
from resources.lib.providers.searchrequest import SearchRequest
from resources.lib.providers.searchresult import SearchResult
from resources.lib.translation.subtitletranslator import SubtitleTranslator
from resources.lib.utils.yaml import to_yaml


class TranslationsDecoratorProvider(DecoratorProvider):

    def __init__(self, source: Provider, translators: List[SubtitleTranslator], request_extra_languages: List[Language] = []):
        super().__init__(source)
        self.translators: List[SubtitleTranslator] = [SubtitleTranslator(translator) for translator in translators]
        self.request_extra_languages = request_extra_languages

    @property
    def name(self) -> str:
        return "Translations"

    def build_source_search_request(self, request: SearchRequest) -> SearchRequest:
        request = copy.deepcopy(request)
        extra_languages = [
            extra_language
            for extra_language in (self.request_extra_languages or []) + (request.file_languages or [])
            if extra_language != Language.unknown and not extra_language in request.languages
        ]
        if len(extra_languages):
            original_request_languages: List[Language] = request.languages.copy()
            request.count_result_predicate = lambda r: r.language == Language.unknown or r.language in original_request_languages
            request.languages.extend(extra_languages)
        return request

    def __build_search_result(self, source_result: SearchResult, target_language: Language, translator: SubtitleTranslator = None) -> SearchResult:
        result = copy.deepcopy(source_result)
        result.id = "%s|%s|%s|%s" % (
            translator.name if translator else '',
            source_result.language.three_letter_code,
            target_language.three_letter_code,
            source_result.id)
        result.language = target_language
        if translator:
            result.provider_name = translator.name + "|" + result.provider_name
            result.title = "%s %s:%s | %s" % (
                translator.short_name if translator else '',
                source_result.language.three_letter_code,
                target_language.three_letter_code,
                result.title)
        return result

    def _transform_search_results(self, request: SearchRequest, source_request: SearchRequest, source_results: List[SearchResult]) -> List[SearchResult]:
        original_results: List[SearchResult] = []
        translation_results: List[SearchResult] = []
        for source_result in source_results:
            if source_result.language == Language.unknown:
                original_result = self.__build_search_result(source_result, Language.unknown)
                original_results.append(original_result)
                continue
            # NOTE:
            # 'request' is the original request passed along to the decorator provider
            # 'source_request' is the modified request built by the decorator that is provided to the source/decorated provider
            for request_language in request.languages:
                if request_language == source_result.language:
                    original_result = self.__build_search_result(source_result, source_result.language)
                    original_results.append(original_result)
                    continue
                for translator in self.translators:
                    if translator.supports_translation(source_result.language, request_language):
                        translation_result = self.__build_search_result(source_result, request_language, translator)
                        translation_results.append(translation_result)
        self._logger.info("Added %s translation search result(s):\n%s",
                          len(translation_results), to_yaml(translation_results))
        return original_results + translation_results

    def build_source_get_request(self, request: GetRequest) -> GetRequest:
        request = copy.deepcopy(request)
        request.search_result_id = request.search_result_id.split("|", 3)[3]
        return request

    def _transform_get_results(self, request: GetRequest, source_request: GetRequest, source_results: List[GetResult]) -> List[GetResult]:
        search_result_id_parts = request.search_result_id.split("|", 3)
        from_language = Language.from_three_letter_code(search_result_id_parts[1])
        to_language = Language.from_three_letter_code(search_result_id_parts[2])
        if from_language == to_language:
            return source_results
        translator = next(t for t in self.translators if t.name == search_result_id_parts[0])
        if not translator or not translator.supports_translation(from_language, to_language):
            return []
        translation_results: List[GetResult] = []
        for source_result in source_results:
            self._logger.info("Translating \"%s\" from %s to %s", source_result.file_name, from_language, to_language)
            try:
                translation_result = translator.translate(source_result, from_language, to_language)
                translation_result.provider_name = self.name + "|" + translation_result.provider_name
                translation_results.append(translation_result)
                self._logger.info("Finished translating \"%s\" from %s to %s", source_result.file_name,
                                  from_language, to_language)
            except:
                self._logger.error("Error translating result \"%s\" from %s to %s" % source_result.file_name,
                                   from_language, to_language, exc_info=True)
                pass
        return translation_results
