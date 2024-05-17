# -*- coding: utf-8 -*-

import re

from resources.lib.formats.subtitleformat import Subtitle, SubtitleLine
from resources.lib.formats.textsubtitleformat import TextSubtitleFormat

LINE_RE = re.compile(
    r"""\[(?P<start_frame>\d+)\]\[(?P<end_frame>\d+)\](?P<text>.*)""",
    re.IGNORECASE | re.DOTALL
)


class MPlayer2SubtitleLine(SubtitleLine):

    def __init__(self):
        super().__init__()
        self.start_frame: int
        self.end_frame: int

    @staticmethod
    def from_text(line_text: str) -> "MPlayer2SubtitleLine":
        line_text_match = LINE_RE.match(line_text)
        assert line_text_match
        line = MPlayer2SubtitleLine()
        line.start_frame = int(line_text_match["start_frame"])
        line.end_frame = int(line_text_match["end_frame"])
        line.text = line_text_match["text"].replace("|", "\n")
        return line

    def to_text(self) -> str:
        return "[%s][%s]%s" % (self.start_frame, self.end_frame, self.text.strip().replace("\n", "|"))


class MPlayer2Subtitle(Subtitle[MPlayer2SubtitleLine]):
    pass


class MPlayer2SubtitleFormat(TextSubtitleFormat[MPlayer2Subtitle, MPlayer2SubtitleLine]):

    def supports_subtitle(self, file_name: str) -> bool:
        return re.search(r"\.(txt)$", file_name, flags=re.IGNORECASE)

    def _parse_text(self, text: str) -> MPlayer2Subtitle:
        lines_text = [line_text.strip() for line_text in re.split(r'\n\s*', text) if line_text]
        subtitle = MPlayer2Subtitle()
        subtitle.lines = [MPlayer2SubtitleLine.from_text(line_text) for line_text in lines_text]
        return subtitle

    def _render_text(self, subtitle: MPlayer2Subtitle) -> str:
        lines_text = [line.to_text() for line in subtitle.lines]
        text = "\n".join(lines_text)
        return text
