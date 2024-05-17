# -*- coding: utf-8 -*-

import re
import time
from typing import Dict, List, Set, Tuple, Union

from resources.lib.common.language import Language
from resources.lib.common.mappedlanguages import MappedLanguages
from resources.lib.common.settings import Settings
from resources.lib.translation.translator import Translator
from resources.lib.utils.httpclient import HttpRequest

CANTONESE = Language("Cantonese (Traditional)", two_letter_code="yue", standard=False)
CHINESE_LITERARY = Language("Chinese (Literary)", two_letter_code="lzh", standard=False)
CHINESE_SIMPLIFIED = Language("Chinese Simplified", two_letter_code="zh-Hans", standard=False)
CHINESE_TRADITIONAL = Language("Chinese Traditional", two_letter_code="zh-Hant", standard=False)
FRENCH_CANADA = Language("French (Canada)", two_letter_code="fr-CA", standard=False)
LUGANDA = Language("Luganda", two_letter_code="lug", standard=False)
HMONG_DAW = Language("Hmong Daw", two_letter_code="mww", standard=False)
INUINNAQTUN = Language("Inuinnaqtun", two_letter_code="ikt", standard=False)
GOAN_KONKANI = Language("Goan Konkani", two_letter_code="gom", standard=False)
KURDISH_NORTHERN = Language("Kurdish (Northern)", two_letter_code="kmr", standard=False)
MONGOLIAN_CYRILLIC = Language("Mongolian (Cyrillic)", two_letter_code="mn-Cyrl", standard=False)
MONGOLIAN_TRADITIONAL = Language("Mongolian (Traditional)", two_letter_code="mn-Mong", standard=False)
NORWEGIAN_BOKMAL = Language("Norwegian Bokmål", two_letter_code="nb", standard=False)
CHICHEWA = Language("Chichewa", two_letter_code="nya", standard=False)
RUNDI = Language("Rundi", two_letter_code="run", standard=False)
SERBIAN_CYRILLIC = Language("Serbian (Cyrillic)", two_letter_code="sr-Cyrl", standard=False)
SERBIAN_LATIN = Language("Serbian (Latin)", two_letter_code="sr-Latn", standard=False)

SUPPORTED_LANGUAGES: List[Language] = [
    Language("Afrikaans", two_letter_code="af"),
    Language("Albanian", two_letter_code="sq"),
    Language("Amharic", two_letter_code="am"),
    Language("Arabic", two_letter_code="ar"),
    Language("Armenian", two_letter_code="hy"),
    Language("Assamese", two_letter_code="as"),
    Language("Azerbaijani", two_letter_code="az"),
    Language("Bengali", two_letter_code="bn"),
    Language("Bashkir", two_letter_code="ba"),
    Language("Basque", two_letter_code="eu"),
    Language("Bhojpuri", two_letter_code="bho"),
    Language("Bodo", two_letter_code="brx"),
    Language("Bosnian", two_letter_code="bs"),
    Language("Bulgarian", two_letter_code="bg"),
    CANTONESE,
    Language("Catalan", two_letter_code="ca"),
    Language("Chhattisgarhi", two_letter_code="hne"),
    CHINESE_LITERARY,
    CHINESE_SIMPLIFIED,
    CHINESE_TRADITIONAL,
    Language("Croatian", two_letter_code="hr"),
    Language("Czech", two_letter_code="cs"),
    Language("Danish", two_letter_code="da"),
    Language("Dari", two_letter_code="prs"),
    Language("Divehi", two_letter_code="dv"),
    Language("Dogri", two_letter_code="doi"),
    Language("Dutch", two_letter_code="nl"),
    Language("English", two_letter_code="en"),
    Language("Estonian", two_letter_code="et"),
    Language("Faroese", two_letter_code="fo"),
    Language("Fijian", two_letter_code="fj"),
    Language("Filipino", two_letter_code="fil"),
    Language("Finnish", two_letter_code="fi"),
    FRENCH_CANADA,
    Language("French", two_letter_code="fr"),
    Language("Galician", two_letter_code="gl"),
    LUGANDA,
    Language("Georgian", two_letter_code="ka"),
    Language("German", two_letter_code="de"),
    Language("Greek", two_letter_code="el"),
    Language("Gujarati", two_letter_code="gu"),
    Language("Haitian", two_letter_code="ht"),
    Language("Hausa", two_letter_code="ha"),
    Language("Hebrew", two_letter_code="he"),
    Language("Hindi", two_letter_code="hi"),
    HMONG_DAW,
    Language("Hungarian", two_letter_code="hu"),
    Language("Icelandic", two_letter_code="is"),
    Language("Igbo", two_letter_code="ig"),
    Language("Indonesian", two_letter_code="id"),
    INUINNAQTUN,
    Language("Inuktitut", two_letter_code="iu"),
    Language("Irish", two_letter_code="ga"),
    Language("Italian", two_letter_code="it"),
    Language("Japanese", two_letter_code="ja"),
    Language("Kannada", two_letter_code="kn"),
    Language("Kashmiri", two_letter_code="ks"),
    Language("Kazakh", two_letter_code="kk"),
    Language("Central Khmer", two_letter_code="km"),
    Language("Kinyarwanda", two_letter_code="rw"),
    GOAN_KONKANI,
    Language("Korean", two_letter_code="ko"),
    Language("Kurdish", two_letter_code="ku"),
    KURDISH_NORTHERN,
    Language("Kirghiz", two_letter_code="ky"),
    Language("Lao", two_letter_code="lo"),
    Language("Latvian", two_letter_code="lv"),
    Language("Lingala", two_letter_code="ln"),
    Language("Lithuanian", two_letter_code="lt"),
    Language("Lower Sorbian", two_letter_code="dsb"),
    Language("Macedonian", two_letter_code="mk"),
    Language("Maithili", two_letter_code="mai"),
    Language("Malagasy", two_letter_code="mg"),
    Language("Malay", two_letter_code="ms"),
    Language("Malayalam", two_letter_code="ml"),
    Language("Maltese", two_letter_code="mt"),
    Language("Māori", two_letter_code="mi"),
    Language("Marathi", two_letter_code="mr"),
    MONGOLIAN_CYRILLIC,
    MONGOLIAN_TRADITIONAL,
    Language("Burmese", two_letter_code="my"),
    Language("Nepali", two_letter_code="ne"),
    NORWEGIAN_BOKMAL,
    CHICHEWA,
    Language("Oriya", two_letter_code="or"),
    Language("Pashto", two_letter_code="ps"),
    Language("Persian", two_letter_code="fa"),
    Language("Polish", two_letter_code="pl"),
    Language("Portuguese", two_letter_code="pt"),
    Language("Punjabi", two_letter_code="pa"),
    Language("Querétaro Otomi", two_letter_code="otq"),
    Language("Romanian", two_letter_code="ro"),
    RUNDI,
    Language("Russian", two_letter_code="ru"),
    Language("Samoan", two_letter_code="sm"),
    SERBIAN_CYRILLIC,
    SERBIAN_LATIN,
    Language("Northern Sotho", two_letter_code="nso"),
    Language("Southern Sotho", two_letter_code="st"),
    Language("Tswana", two_letter_code="tn"),
    Language("Shona", two_letter_code="sn"),
    Language("Sindhi", two_letter_code="sd"),
    Language("Sinhala", two_letter_code="si"),
    Language("Slovak", two_letter_code="sk"),
    Language("Slovenian", two_letter_code="sl"),
    Language("Somali", two_letter_code="so"),
    Language("Spanish", two_letter_code="es"),
    Language("Swahili", two_letter_code="sw"),
    Language("Swedish", two_letter_code="sv"),
    Language("Tahitian", two_letter_code="ty"),
    Language("Tamil", two_letter_code="ta"),
    Language("Tatar", two_letter_code="tt"),
    Language("Telugu", two_letter_code="te"),
    Language("Thai", two_letter_code="th"),
    Language("Tibetan", two_letter_code="bo"),
    Language("Tigrinya", two_letter_code="ti"),
    Language("Tonga", two_letter_code="to"),
    Language("Turkish", two_letter_code="tr"),
    Language("Turkmen", two_letter_code="tk"),
    Language("Ukrainian", two_letter_code="uk"),
    Language("Upper Sorbian", two_letter_code="hsb"),
    Language("Urdu", two_letter_code="ur"),
    Language("Uyghur", two_letter_code="ug"),
    Language("Uzbek", two_letter_code="uz"),
    Language("Vietnamese", two_letter_code="vi"),
    Language("Welsh", two_letter_code="cy"),
    Language("Xhosa", two_letter_code="xh"),
    Language("Yoruba", two_letter_code="yo"),
    Language("Yucatec Maya", two_letter_code="yua"),
    Language("Zulu", two_letter_code="zu"),
]

LANGUAGE_MAPPINGS: Dict[Language, Union[Language, List[Language]]] = {
    CHINESE_SIMPLIFIED: Language.chinese,
    CHINESE_TRADITIONAL: Language.chinese,
    CHINESE_LITERARY: Language.chinese,
    CANTONESE: Language.chinese,
    FRENCH_CANADA: Language.french,
    LUGANDA: Language.luganda,
    HMONG_DAW: Language.hmong,
    INUINNAQTUN: Language.inuktitut,
    GOAN_KONKANI: Language.konkani,
    KURDISH_NORTHERN: Language.kurdish,
    MONGOLIAN_CYRILLIC: Language.mongolian,
    MONGOLIAN_TRADITIONAL: Language.mongolian,
    NORWEGIAN_BOKMAL: Language.norwegian,
    CHICHEWA: Language.chichewa,
    RUNDI: Language.rundi,
    SERBIAN_CYRILLIC: Language.serbian,
    SERBIAN_LATIN: Language.serbian,
}


# AbusePreventionHelper.init.apply(this, params_AbusePreventionHelper);
# //rrer":""}}); var params_AbusePreventionHelper = [1707070300340,"MI8IZijShjyAdautxddTdsW1cMBEDWUa",3600000]; var pa
KEY_AND_TOKEN_RE = re.compile(
    r'var params_AbusePreventionHelper\s*=\s*\[(?P<key>\d+)\s*,\s*"(?P<token>[^"]+)"',
    re.IGNORECASE | re.DOTALL
)


class BingTranslator(Translator):

    def __init__(self, settings: Settings) -> None:
        super().__init__(settings, MappedLanguages(SUPPORTED_LANGUAGES, LANGUAGE_MAPPINGS))

    @property
    def name(self) -> str:
        return "Bing"

    @property
    def short_name(self) -> str:
        return "BG"

    def __fetch_key_and_token(self) -> Tuple[str, str]:
        request = HttpRequest("https://www.bing.com/Translator")
        text = self._http_client.exchange(request).get_data_as_text()
        match = KEY_AND_TOKEN_RE.search(text)
        assert match
        return match["key"], match["token"]

    def __fetch_translation(self, from_language: Language, to_language: Language, text: str, key: str, token: str) -> str:
        request = HttpRequest("https://www.bing.com/ttranslatev3?IG=1&IID=1", "POST")
        request.headers = {'Origin': 'https://www.bing.com'}
        request.set_urlencoded_form_data({
            "fromLang": from_language.two_letter_code,
            "to": to_language.two_letter_code,
            "text":  text,
            "key": key,
            "token": token,
        })
        response = self._http_client.exchange(request)
        try:
            response_json = response.get_data_as_json()
            return response_json[0]["translations"][0]["text"]
        except:
            self._logger.warn("Error parsing translation result: " + response.get_data_as_text())
            time.sleep(10)  # cooldown after error
            return None

    def __fetch_translation_key_and_token(self, from_language: Language, to_language: Language, text: str, key: str, token: str) -> List[str]:
        translation = self.__fetch_translation(from_language, to_language, text, key, token)
        if translation is None:
            key, token = self.__fetch_key_and_token()
            translation = self.__fetch_translation(from_language, to_language, text, key, token)
        return [translation, key, token]

    def _translate(self, internal_from_language: Language, internal_to_language: Language, texts: List[str]) -> List[str]:
        return self._translate_in_blocks(
            texts,
            500,
            "\n\n",
            lambda text, key, token: self.__fetch_translation_key_and_token(
                internal_from_language, internal_to_language, text, key, token),
            self.__fetch_key_and_token())
