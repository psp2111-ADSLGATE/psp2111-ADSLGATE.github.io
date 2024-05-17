#!/usr/bin/python

import logging
import os
import sys
from datetime import timedelta
from pathlib import Path

if __name__ == '__main__' and not __package__:
    __package__ = 'resources.lib.tests'
    sys.path.append(str(Path(__file__).resolve().parents[len(__package__.split("."))]))
    try:
        sys.path.remove(str(Path(__file__).resolve().parent))
    except ValueError:
        pass

from ..common.language import Language
from ..common.settings import Settings
from ..providers.getresult import GetResult
from ..translation.bingtranslator import BingTranslator
from ..translation.googletranslator import GoogleTranslator
from ..translation.libretranslator import LibreTranslator
from ..translation.subtitletranslator import SubtitleTranslator
from ..utils.compression import Compression
from ..utils.logging import init_logging_from_yaml
from ..utils.yaml import to_yaml

Compression.seven_zip_exec_path = Path("C:/Program Files/7-Zip/7z.exe")

settings = Settings()
settings.addon_id = "service.subtitles.universalsubs"
settings.addon_path = Path(__file__).joinpath("..", "..", "..", "..").resolve()
settings.addon_user_path = Path(os.environ["UNIVERSAL_SUBS_USER_PATH"]).resolve()
settings.include_author_on_results = True
settings.include_downloads_on_results = True
settings.exclude_splitted_subtitles = True
settings.search_cache_ttl = timedelta(minutes=30)
settings.translation_cache_ttl = timedelta(days=30)

init_logging_from_yaml(settings.addon_path.joinpath('logging.test.yaml'))
logger = logging.getLogger('UniversalSubs')
logger.info("Settings: %s", to_yaml(settings))

# translator = SubtitleTranslator(GoogleTranslator(settings))
# translator = SubtitleTranslator(LibreTranslator(settings))
translator = SubtitleTranslator(BingTranslator(settings))

examples_path = settings.addon_path.joinpath("resources", "examples")

subtitle = GetResult()
for file_name in [
    "advancedsubstationalpha.ass",
    "googleplay.json",
    "microdvd.sub",
    "mplayer2.txt",
    "subrip.srt",
    "substationalpha.ssa",
    "webvtt.vtt",
    "webvtt2.vtt",
    "youtubesbv.sbv"
]:
    subtitle.file_name = file_name
    subtitle.content = None
    with open(examples_path.joinpath(subtitle.file_name).absolute(), 'rb') as file:
        subtitle.content = file.read()
    subtitle.is_forced = False
    subtitle.is_hearing_impaired = False
    translated_subtitle = translator.translate(subtitle, Language.english, Language.spanish)
    (file_name, file_ext) = os.path.splitext(file_name)
    translated_subtitle.file_name = file_name + "." + Language.spanish.two_letter_code + file_ext
    logger.info("%s\n%s" % (translated_subtitle.file_name, translated_subtitle.content.decode("utf-8")))
    translated_subtitle.write_into(examples_path)
