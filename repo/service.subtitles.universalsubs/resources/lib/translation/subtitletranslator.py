# -*- coding: utf-8 -*-

import copy
import os
from typing import List

from resources.lib.common.language import Language
from resources.lib.formats.subtitleformatsregistry import \
    SubtitleFormatsRegistry
from resources.lib.providers.getresult import GetResult
from resources.lib.translation.translator import Translator


class SubtitleTranslator:

    def __init__(self, translator: Translator) -> None:
        self.translator = translator
        self.formats_registry = SubtitleFormatsRegistry()

    @property
    def name(self) -> str:
        return self.translator.name

    @property
    def short_name(self) -> str:
        return self.translator.short_name

    def supports_subtitle(self, subtitle: GetResult) -> bool:
        return self.formats_registry.has_format_for(subtitle.file_name)

    def supports_translation(self, from_language: Language, to_language: Language) -> bool:
        return self.translator.supports_translation(from_language, to_language)

    def translate(self, result: GetResult, from_language: Language, to_language: Language) -> GetResult:
        format, subtitle = self.formats_registry.parse(result.file_name, result.content)
        source_texts: List[str] = [line.plain_text for line in subtitle.lines]
        translation_texts = [line_text for line_text in self.translator.translate(
            from_language, to_language, source_texts)]
        for index, subtitle_line in enumerate(subtitle.lines):
            subtitle_line.text = translation_texts[index]
        translated_result = copy.deepcopy(result)
        (translated_file_name, translated_file_ext) = os.path.splitext(translated_result.file_name)
        translated_result.file_name = translated_file_name + "." + to_language.two_letter_code + translated_file_ext
        translated_result.content = format.render(subtitle)
        return translated_result
