# -*- coding: utf-8 -*-

import re
from datetime import timedelta
from typing import Dict

from resources.lib.formats.subtitleformat import Subtitle, SubtitleLine
from resources.lib.formats.textsubtitleformat import TextSubtitleFormat
from resources.lib.utils.json import from_json, to_json


class GooglePlaySubtitleLine(SubtitleLine):

    def __init__(self):
        super().__init__()
        self.start_time: timedelta
        self.duration: timedelta

    @staticmethod
    def from_event(event: Dict[str, any]) -> "GooglePlaySubtitleLine":
        line = GooglePlaySubtitleLine()
        line.start_time = timedelta(milliseconds=event["tStartMs"])
        line.duration = timedelta(milliseconds=event["dDurationMs"])
        line.text = event["segs"][0]["utf8"]
        return line

    def to_event(self) -> Dict[str, any]:
        return {
            "tStartMs": int(self.start_time.total_seconds() * 1000),
            "dDurationMs": int(self.duration.total_seconds() * 1000),
            "segs": [{"utf8": self.text}]
        }


class GooglePlaySubtitle(Subtitle[GooglePlaySubtitleLine]):
    pass


class GooglePlaySubtitleFormat(TextSubtitleFormat[GooglePlaySubtitle, GooglePlaySubtitleLine]):

    def supports_subtitle(self, file_name: str) -> bool:
        return re.search(r"\.(json|jsonc)$", file_name, flags=re.IGNORECASE)

    def _parse_text(self, text: str) -> GooglePlaySubtitle:
        parsed_json = from_json(text)
        subtitle = GooglePlaySubtitle()
        subtitle.lines = [GooglePlaySubtitleLine.from_event(event) for event in parsed_json['events']]
        return subtitle

    def _render_text(self, subtitle: GooglePlaySubtitle) -> str:
        text = to_json({"events": [line.to_event() for line in subtitle.lines]})
        return text
