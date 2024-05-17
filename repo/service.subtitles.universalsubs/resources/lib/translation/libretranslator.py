# -*- coding: utf-8 -*-

import re
from typing import Dict, List, Set, Union

from resources.lib.common.language import Language
from resources.lib.common.mappedlanguages import MappedLanguages
from resources.lib.common.settings import Settings
from resources.lib.translation.translator import Translator
from resources.lib.utils.httpclient import HttpRequest

CHINESE_TRADITIONAL = Language("Chinese (Traditional)", two_letter_code="zt", standard=False)
NORWEGIAN_BOKMAL = Language("Norwegian Bokmål", two_letter_code="nb", standard=False)

SUPPORTED_LANGUAGES: List[Language] = [
    Language("Albanian", two_letter_code="sq"),
    Language("Arabic", two_letter_code="ar"),
    Language("Azerbaijani", two_letter_code="az"),
    Language("Bengali", two_letter_code="bn"),
    Language("Bulgarian", two_letter_code="bg"),
    Language("Catalan", two_letter_code="ca"),
    CHINESE_TRADITIONAL,
    Language("Chinese", two_letter_code="zh"),
    Language("Czech", two_letter_code="cs"),
    Language("Danish", two_letter_code="da"),
    Language("Dutch", two_letter_code="nl"),
    Language("English", two_letter_code="en"),
    Language("Esperanto", two_letter_code="eo"),
    Language("Estonian", two_letter_code="et"),
    Language("Finnish", two_letter_code="fi"),
    Language("French", two_letter_code="fr"),
    Language("German", two_letter_code="de"),
    Language("Greek", two_letter_code="el"),
    Language("Hebrew", two_letter_code="he"),
    Language("Hindi", two_letter_code="hi"),
    Language("Hungarian", two_letter_code="hu"),
    Language("Indonesian", two_letter_code="id"),
    Language("Irish", two_letter_code="ga"),
    Language("Italian", two_letter_code="it"),
    Language("Japanese", two_letter_code="ja"),
    Language("Korean", two_letter_code="ko"),
    Language("Latvian", two_letter_code="lv"),
    Language("Lithuanian", two_letter_code="lt"),
    Language("Malay", two_letter_code="ms"),
    NORWEGIAN_BOKMAL,
    Language("Persian", two_letter_code="fa"),
    Language("Polish", two_letter_code="pl"),
    Language("Portuguese", two_letter_code="pt"),
    Language("Romanian", two_letter_code="ro"),
    Language("Russian", two_letter_code="ru"),
    Language("Serbian", two_letter_code="sr"),
    Language("Slovak", two_letter_code="sk"),
    Language("Slovenian", two_letter_code="sl"),
    Language("Spanish", two_letter_code="es"),
    Language("Swedish", two_letter_code="sv"),
    Language("Tagalog", two_letter_code="tl"),
    Language("Thai", two_letter_code="th"),
    Language("Turkish", two_letter_code="tr"),
    Language("Ukrainian", two_letter_code="uk"),
    Language("Urdu", two_letter_code="ur"),
    Language("Vietnamese", two_letter_code="vi"),
]

LANGUAGE_MAPPINGS: Dict[Language, Union[Language, List[Language]]] = {
    CHINESE_TRADITIONAL: Language.chinese,
    NORWEGIAN_BOKMAL: Language.norwegian,
}

SECRET_RE = re.compile(r'\sapiSecret: "(?P<secret>[^"]+)"', re.IGNORECASE | re.DOTALL)


class LibreTranslator(Translator):

    def __init__(self, settings: Settings) -> None:
        super().__init__(settings, MappedLanguages(SUPPORTED_LANGUAGES, LANGUAGE_MAPPINGS))

    @property
    def name(self) -> str:
        return "Libre"

    @property
    def short_name(self) -> str:
        return "LB"

    def __fetch_secret(self) -> str:
        request = HttpRequest("https://libretranslate.com/js/app.js?v=1.5.5")
        text = self._http_client.exchange(request).get_data_as_text()
        match = SECRET_RE.search(text)
        assert match
        return match["secret"]

    def __fetch_translation(self, from_language: Language, to_language: Language, text: str, secret: str) -> str:
        # request = HttpRequest("https://libretranslate.com/translate", "POST")
        # request.set_json_data({
        #     "q": text_chunk,
        #     "source": from_language.two_letter_code,
        #     "target": to_language.two_letter_code,
        #     "format": "text",
        #     "api_key": ""
        # })
        request = HttpRequest("https://libretranslate.com/translate", "POST")
        request.throw_on_error_codes = False
        request.headers = {'Origin': 'https://libretranslate.com'}
        request.set_urlencoded_form_data({
            "q": text,
            "source": from_language.two_letter_code,
            "target": to_language.two_letter_code,
            "format": "text",
            "secret": secret,
        })
        response = self._http_client.exchange(request)
        if response.status_code == 400:
            return None
        response_json = response.get_data_as_json()
        return response_json["translatedText"]

    def fetch_translation_and_secret(self, from_language: Language, to_language: Language, text: str, secret: str) -> List[str]:
        translation = self.__fetch_translation(from_language, to_language, text, secret)
        if translation is None:
            secret = self.__fetch_secret()
            translation = self.__fetch_translation(from_language, to_language, text, secret)
        return [translation, secret]

    def _translate(self, internal_from_language: Language, internal_to_language: Language, texts: List[str]) -> List[str]:
        return self._translate_in_blocks(
            texts,
            2000,
            "\n\n",
            lambda text, secret: self.fetch_translation_and_secret(
                internal_from_language, internal_to_language, text, secret),
            [self.__fetch_secret()])
