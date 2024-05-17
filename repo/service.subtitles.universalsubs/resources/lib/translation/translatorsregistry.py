# -*- coding: utf-8 -*-

import logging
from typing import Dict, List

from resources.lib.common.settings import Settings
from resources.lib.translation.bingtranslator import BingTranslator
from resources.lib.translation.googletranslator import GoogleTranslator
from resources.lib.translation.libretranslator import LibreTranslator
from resources.lib.translation.translator import Translator


class TranslatorsRegistry:

    def __init__(self, settings: Settings):
        self._logger: logging.Logger = logging.getLogger("UniversalSubs.TranslatorsRegistry")
        self._translators: Dict[str, Translator] = {
            translator.name: translator
            for translator in [
                BingTranslator(settings),
                GoogleTranslator(settings),
                LibreTranslator(settings)
            ]
        }

    def get_translators(self, names: List[str] = None) -> List[Translator]:
        return [self._translators[name] for name in names]
