# -*- coding: utf-8 -*-

import logging
from typing import List, Tuple

from resources.lib.formats.googleplaysubtitleformat import \
    GooglePlaySubtitleFormat
from resources.lib.formats.microdvdsubtitleformat import MicroDVDSubtitleFormat
from resources.lib.formats.mplayer2subtitleformat import MPlayer2SubtitleFormat
from resources.lib.formats.subripsubtitleformat import SubRipSubtitleFormat
from resources.lib.formats.substationalphasubtitleformat import \
    SubStationAlphaSubtitleFormat
from resources.lib.formats.subtitleformat import Subtitle, SubtitleFormat
from resources.lib.formats.webvttsubtitleformat import WebVTTSubtitleFormat
from resources.lib.formats.youtubesbvsubtitleformat import \
    YouTubeSBVSubtitleFormat


class UnsupportedSubtitleFormatException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

    def __str__(self):
        return self.message


class SubtitleFormatsRegistry:

    def __init__(self):
        self._logger: logging.Logger = logging.getLogger("UniversalSubs.SubtitleFormatsRegistry")
        self._available_formats: List[SubtitleFormat] = [
            GooglePlaySubtitleFormat(),
            MicroDVDSubtitleFormat(),
            MPlayer2SubtitleFormat(),
            SubRipSubtitleFormat(),
            SubStationAlphaSubtitleFormat(),
            WebVTTSubtitleFormat(),
            YouTubeSBVSubtitleFormat()
        ]

    def find_formats_for(self, file_name: str, throw_if_missing: bool = None) -> List[SubtitleFormat]:
        formats = [
            format for format in self._available_formats if format.supports_subtitle(file_name)]
        if throw_if_missing and not formats:
            raise UnsupportedSubtitleFormatException("No supported subtitle format found for file '%s'." % file_name)
        return formats

    def has_format_for(self, file_name: str) -> bool:
        return len(self.resolve_subtitle_format(file_name, False)) > 0

    def parse(self, file_name: str, content: bytes) -> Tuple[SubtitleFormat, Subtitle]:
        last_exception = Exception()
        for format in self.find_formats_for(file_name, True):
            try:
                return [format, format.parse(content)]
            except Exception as e:
                self._logger.warn("Error parsing file '%s' with format '%s'" %
                                  (file_name, format.__class__.__name__), exc_info=True)
                last_exception = e
                pass
        raise UnsupportedSubtitleFormatException(
            "No supported subtitle format was able to parse file '%s'." % file_name) from last_exception
