# -*- coding: utf-8 -*-

import html
import re
from typing import Dict, List, Set, Union
from urllib.parse import quote

from resources.lib.common.language import Language
from resources.lib.common.mappedlanguages import MappedLanguages
from resources.lib.common.settings import Settings
from resources.lib.translation.translator import Translator
from resources.lib.utils.httpclient import HttpRequest

GOAN_KONKANI = Language("Goan Konkani", two_letter_code="gom", standard=False)

SUPPORTED_LANGUAGES: List[Language] = [
    Language("Afrikaans", two_letter_code="af"),
    Language("Albanian", two_letter_code="sq"),
    Language("Amharic", two_letter_code="am"),
    Language("Arabic", two_letter_code="ar"),
    Language("Armenian", two_letter_code="hy"),
    Language("Assamese", two_letter_code="as"),
    Language("Aymara", two_letter_code="ay"),
    Language("Azerbaijani", two_letter_code="az"),
    Language("Bambara", two_letter_code="bm"),
    Language("Basque", two_letter_code="eu"),
    Language("Belarusian", two_letter_code="be"),
    Language("Bengali", two_letter_code="bn"),
    Language("Bhojpuri", two_letter_code="bho"),
    Language("Bosnian", two_letter_code="bs"),
    Language("Bulgarian", two_letter_code="bg"),
    Language("Catalan", two_letter_code="ca"),
    Language("Cebuano", two_letter_code="ceb"),
    Language("Chinese", two_letter_code="zh"),
    Language("Corsican", two_letter_code="co"),
    Language("Croatian", two_letter_code="hr"),
    Language("Czech", two_letter_code="cs"),
    Language("Danish", two_letter_code="da"),
    Language("Divehi", two_letter_code="dv"),
    Language("Dogri", two_letter_code="doi"),
    Language("Dutch", two_letter_code="nl"),
    Language("English", two_letter_code="en"),
    Language("Esperanto", two_letter_code="eo"),
    Language("Estonian", two_letter_code="et"),
    Language("Ewe", two_letter_code="ee"),
    Language("Filipino", two_letter_code="fil"),
    Language("Finnish", two_letter_code="fi"),
    Language("French", two_letter_code="fr"),
    Language("Western Frisian", two_letter_code="fy"),
    Language("Galician", two_letter_code="gl"),
    Language("Georgian", two_letter_code="ka"),
    Language("German", two_letter_code="de"),
    Language("Greek", two_letter_code="el"),
    Language("Guaraní", two_letter_code="gn"),
    Language("Gujarati", two_letter_code="gu"),
    Language("Haitian", two_letter_code="ht"),
    Language("Hausa", two_letter_code="ha"),
    Language("Hawaiian", two_letter_code="haw"),
    Language("Hebrew", two_letter_code="he"),
    Language("Hindi", two_letter_code="hi"),
    Language("Hmong", two_letter_code="hmn"),
    Language("Hungarian", two_letter_code="hu"),
    Language("Icelandic", two_letter_code="is"),
    Language("Igbo", two_letter_code="ig"),
    Language("Iloko", two_letter_code="ilo"),
    Language("Indonesian", two_letter_code="id"),
    Language("Irish", two_letter_code="ga"),
    Language("Italian", two_letter_code="it"),
    Language("Japanese", two_letter_code="ja"),
    Language("Javanese", two_letter_code="jv"),
    Language("Kannada", two_letter_code="kn"),
    Language("Kazakh", two_letter_code="kk"),
    Language("Central Khmer", two_letter_code="km"),
    Language("Kinyarwanda", two_letter_code="rw"),
    GOAN_KONKANI,
    Language("Korean", two_letter_code="ko"),
    Language("Krio", two_letter_code="kri"),
    Language("Sorani", two_letter_code="ckb"),
    Language("Kurdish", two_letter_code="ku"),
    Language("Kirghiz", two_letter_code="ky"),
    Language("Lao", two_letter_code="lo"),
    Language("Latin", two_letter_code="la"),
    Language("Latvian", two_letter_code="lv"),
    Language("Lingala", two_letter_code="ln"),
    Language("Lithuanian", two_letter_code="lt"),
    Language("Luganda", two_letter_code="lg"),
    Language("Luxembourgish", two_letter_code="lb"),
    Language("Macedonian", two_letter_code="mk"),
    Language("Maithili", two_letter_code="mai"),
    Language("Malagasy", two_letter_code="mg"),
    Language("Malay", two_letter_code="ms"),
    Language("Malayalam", two_letter_code="ml"),
    Language("Maltese", two_letter_code="mt"),
    Language("Māori", two_letter_code="mi"),
    Language("Marathi", two_letter_code="mr"),
    Language("Manipuri", two_letter_code="mni"),
    Language("Lushai", two_letter_code="lus"),
    Language("Mongolian", two_letter_code="mn"),
    Language("Burmese", two_letter_code="my"),
    Language("Nepali", two_letter_code="ne"),
    Language("Norwegian", two_letter_code="no"),
    Language("Chichewa", two_letter_code="ny"),
    Language("Oriya", two_letter_code="or"),
    Language("Oromo", two_letter_code="om"),
    Language("Pashto", two_letter_code="ps"),
    Language("Persian", two_letter_code="fa"),
    Language("Polish", two_letter_code="pl"),
    Language("Portuguese", two_letter_code="pt"),
    Language("Punjabi", two_letter_code="pa"),
    Language("Quechua", two_letter_code="qu"),
    Language("Romanian", two_letter_code="ro"),
    Language("Russian", two_letter_code="ru"),
    Language("Samoan", two_letter_code="sm"),
    Language("Sanskrit", two_letter_code="sa"),
    Language("Gaelic", two_letter_code="gd"),
    Language("Northern Sotho", two_letter_code="nso"),
    Language("Serbian", two_letter_code="sr"),
    Language("Southern Sotho", two_letter_code="st"),
    Language("Shona", two_letter_code="sn"),
    Language("Sindhi", two_letter_code="sd"),
    Language("Sinhala", two_letter_code="si"),
    Language("Slovak", two_letter_code="sk"),
    Language("Slovenian", two_letter_code="sl"),
    Language("Somali", two_letter_code="so"),
    Language("Spanish", two_letter_code="es"),
    Language("Sundanese", two_letter_code="su"),
    Language("Swahili", two_letter_code="sw"),
    Language("Swedish", two_letter_code="sv"),
    Language("Tagalog", two_letter_code="tl"),
    Language("Tajik", two_letter_code="tg"),
    Language("Tamil", two_letter_code="ta"),
    Language("Tatar", two_letter_code="tt"),
    Language("Telugu", two_letter_code="te"),
    Language("Thai", two_letter_code="th"),
    Language("Tigrinya", two_letter_code="ti"),
    Language("Tsonga", two_letter_code="ts"),
    Language("Turkish", two_letter_code="tr"),
    Language("Turkmen", two_letter_code="tk"),
    Language("Akan", two_letter_code="ak"),
    Language("Ukrainian", two_letter_code="uk"),
    Language("Urdu", two_letter_code="ur"),
    Language("Uyghur", two_letter_code="ug"),
    Language("Uzbek", two_letter_code="uz"),
    Language("Vietnamese", two_letter_code="vi"),
    Language("Welsh", two_letter_code="cy"),
    Language("Xhosa", two_letter_code="xh"),
    Language("Yiddish", two_letter_code="yi"),
    Language("Yoruba", two_letter_code="yo"),
    Language("Zulu", two_letter_code="zu"),
]

LANGUAGE_MAPPINGS: Dict[Language, Union[Language, List[Language]]] = {
    GOAN_KONKANI: Language.konkani
}

RESULT_RE = re.compile(
    r'<div class="result-container">(?P<result>[^<]+)</div>',
    re.IGNORECASE | re.DOTALL
)


class GoogleTranslator(Translator):

    def __init__(self, settings: Settings) -> None:
        super().__init__(settings, MappedLanguages(SUPPORTED_LANGUAGES, LANGUAGE_MAPPINGS))

    @property
    def name(self) -> str:
        return "Google"

    @property
    def short_name(self) -> str:
        return "GG"

    def __fetch_translation(self, from_language: Language, to_language: Language, text: str) -> str:
        request = HttpRequest("https://translate.google.com:443/m?sl=%s&tl=%s&q=%s" %
                              (from_language.two_letter_code, to_language.two_letter_code, quote(text)))
        response = self._http_client.exchange(request)
        result_match = RESULT_RE.search(response.get_data_as_text())
        assert result_match
        return html.unescape(result_match["result"])

    def _translate(self, internal_from_language: Language, internal_to_language: Language, texts: List[str]) -> List[str]:
        return self._translate_in_blocks(texts, 2000, "\n\n", lambda text: self.__fetch_translation(internal_from_language, internal_to_language, text))
