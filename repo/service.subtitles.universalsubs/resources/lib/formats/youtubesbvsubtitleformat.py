# -*- coding: utf-8 -*-

import re
from datetime import timedelta

from resources.lib.formats.subtitleformat import (Subtitle, SubtitleLine,
                                                  time_from_text, time_to_text)
from resources.lib.formats.textsubtitleformat import TextSubtitleFormat

LINE_RE = re.compile(
    r"""(?P<start_time>\d\d?:\d\d:\d\d\.\d\d\d),(?P<end_time>\d\d?:\d\d:\d\d\.\d\d\d)\n(?P<text>.+)""",
    re.IGNORECASE | re.DOTALL
)

# 00:00:20.729 or 0:00:20.729
TIME_RE = re.compile(
    r"""(?P<hours>\d\d?):(?P<minutes>\d\d):(?P<seconds>\d\d\.\d\d\d)""",
    re.IGNORECASE | re.DOTALL
)

TIME_FORMAT = "%(h)01d:%(m)02d:%(s)06.3f"  # %02d:%02d:%06.3f


class YouTubeSBVSubtitleLine(SubtitleLine):

    def __init__(self):
        super().__init__()
        self.start_time: timedelta
        self.end_time: timedelta

    @staticmethod
    def from_text(line_text: str) -> "YouTubeSBVSubtitleLine":
        line_text_match = LINE_RE.match(line_text)
        assert line_text_match
        line = YouTubeSBVSubtitleLine()
        line.start_time = time_from_text(line_text_match["start_time"], TIME_RE)
        line.end_time = time_from_text(line_text_match["end_time"], TIME_RE)
        line.text = line_text_match["text"]
        return line

    def to_text(self) -> str:
        return "%s,%s\n%s" % (
            time_to_text(self.start_time, TIME_FORMAT),
            time_to_text(self.end_time, TIME_FORMAT),
            self.text.strip())


class YouTubeSBVSubtitle(Subtitle[YouTubeSBVSubtitleLine]):
    def __init__(self):
        super().__init__()


class YouTubeSBVSubtitleFormat(TextSubtitleFormat[YouTubeSBVSubtitle, YouTubeSBVSubtitleLine]):

    def supports_subtitle(self, file_name: str) -> bool:
        return re.search(r"\.(sbv)$", file_name, flags=re.IGNORECASE)

    def _parse_text(self, text: str) -> YouTubeSBVSubtitle:
        lines_text = [line_text for line_text in re.split(r'\n\n\s*', text) if line_text]
        subtitle = YouTubeSBVSubtitle()
        subtitle.lines = [YouTubeSBVSubtitleLine.from_text(line_text) for line_text in lines_text]
        return subtitle

    def _render_text(self, subtitle: YouTubeSBVSubtitle) -> str:
        lines_text = [line.to_text() for line in subtitle.lines]
        text = "\n\n".join(lines_text)
        return text
