# -*- coding: utf-8 -*-

import re
from datetime import timedelta
from typing import Dict, List

from resources.lib.formats.subtitleformat import (Subtitle, SubtitleLine,
                                                  time_from_text, time_to_text)
from resources.lib.formats.textsubtitleformat import TextSubtitleFormat

# 0:00:16.85 or 00:00:16.850
TIME_RE = re.compile(
    r"""(?P<hours>\d\d?):(?P<minutes>\d\d):(?P<seconds>\d\d\.\d\d\d?)""",
    re.IGNORECASE | re.DOTALL
)

TIME_FORMAT = "%(h)01d:%(m)02d:%(s)05.2f"


KEY_TO_PROPERTY: Dict[str, str] = {
    "layer": "layer",
    "marked": "marked",
    "start": "start_time",
    "end": "end_time",
    "style": "style",
    "name": "name",
    "marginl": "margin_l",
    "marginr": "margin_r",
    "marginv": "margin_v",
    "effect": "effect",
    "text": "text",
}


class SubStationAlphaSubtitleLine(SubtitleLine):

    def __init__(self):
        super().__init__()
        self.layer: str
        self.marked: str
        self.start_time: timedelta
        self.end_time: timedelta
        self.style: str
        self.name: str
        self.margin_left: str
        self.margin_right: str
        self.margin_vertical: str
        self.effect: str

    @staticmethod
    def from_text(line_text: str, format_keys: List[str]) -> "SubStationAlphaSubtitleLine":
        line = SubStationAlphaSubtitleLine()
        line_values: List[str] = line_text.split(",", len(format_keys))
        for format_key_index, format_key in enumerate(format_keys):
            key = format_key.lower()
            property = KEY_TO_PROPERTY[key]
            value = line_values[format_key_index].strip()
            if key == "start" or key == "end":
                setattr(line, property, time_from_text(value, TIME_RE))
            elif key == "text":
                setattr(line, property, value.replace("\\n", "\n").replace("\\N", "\n"))
            else:
                setattr(line, property, value)
        return line

    def to_text(self, format_keys: List[str]) -> str:
        line_values: List[str] = []
        for format_key in format_keys:
            key = format_key.lower()
            value = getattr(self, KEY_TO_PROPERTY[key])
            if key == "start" or key == "end":
                line_values.append(time_to_text(value, TIME_FORMAT))
            elif key == "text":
                line_values.append(value.replace("\n", "\\N"))
            else:
                line_values.append(value)
        return ",".join(line_values)


class SubStationAlphaSubtitle(Subtitle[SubStationAlphaSubtitleLine]):
    def __init__(self):
        super().__init__()
        self.heading: str = None
        self.format_keys: List[str] = []


class SubStationAlphaSubtitleFormat(TextSubtitleFormat[SubStationAlphaSubtitle, SubStationAlphaSubtitleLine]):

    def supports_subtitle(self, file_name: str) -> bool:
        return re.search(r"\.(ssa|ass)$", file_name, flags=re.IGNORECASE)

    def _parse_text(self, text: str) -> SubStationAlphaSubtitle:
        subtitle = SubStationAlphaSubtitle()
        text_keys = text.split("[Events]", 2)
        subtitle.heading = text_keys[0]
        format_and_dialogs = text_keys[1].strip().split("\n")
        subtitle.format_keys = [key.strip() for key in format_and_dialogs[0][len("Format:"):].split(",")]
        lines_text = [line_text[len("Dialogue:"):] for line_text in format_and_dialogs[1:]]
        subtitle.lines = [SubStationAlphaSubtitleLine.from_text(
            line_text, subtitle.format_keys) for line_text in lines_text]
        return subtitle

    def _render_text(self, subtitle: SubStationAlphaSubtitle) -> str:
        lines_dialogue = ["Dialogue: " + line.to_text(subtitle.format_keys) for line in subtitle.lines]
        text = "%s[Events]\nFormat: %s\n%s" % (
            subtitle.heading,
            ", ".join(subtitle.format_keys),
            "\n".join(lines_dialogue))
        return text
