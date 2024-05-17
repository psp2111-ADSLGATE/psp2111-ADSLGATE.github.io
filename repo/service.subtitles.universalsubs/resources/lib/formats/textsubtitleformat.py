from abc import abstractmethod

import chardet

from resources.lib.formats.subtitleformat import (SubtitleFormat, TSubtitle,
                                                  TSubtitleLine)


class TextSubtitleFormat(SubtitleFormat[TSubtitle, TSubtitleLine]):

    def _parse(self, content: bytes) -> TSubtitle:
        detected_encoding = chardet.detect(content)["encoding"] or "utf-8"
        text = content.decode(detected_encoding, "ignore").replace("\r\n", "\n").replace("\r", "\n")
        return self._parse_text(text)

    @abstractmethod
    def _parse_text(self, text: str) -> TSubtitle:
        pass

    def _render(self, subtitle: TSubtitle, encoding: str = "utf-8") -> bytes:
        text = self._render_text(subtitle)
        return text.encode(encoding or "utf-8", "strict")

    @abstractmethod
    def _render_text(self, subtitle: TSubtitle) -> str:
        pass
