# -*- coding: utf-8 -*-

import re
from abc import ABC, abstractmethod
from datetime import timedelta
from re import Pattern
from typing import Callable, Generic, List, TypeVar


class SubtitleParseException(Exception):
    def __init__(self, format: "SubtitleFormat", message: str = None) -> None:
        self.format: format
        self.message = message or "Error parsing subtitle with %s." % format.__class__.__name__
        super().__init__()

    def __str__(self):
        return self.message


class SubtitleRenderException(Exception):
    def __init__(self, format: "SubtitleFormat", message: str = None) -> None:
        self.format: format
        self.message = message or "Error rendering subtitle with %s." % format.__class__.__name__
        super().__init__()

    def __str__(self):
        return self.message


def time_from_text(time_text: str, regex: Pattern, strip_chars: str = ":") -> timedelta:
    assert time_text
    assert regex
    time_text_match = regex.match(time_text)
    if not time_text_match:
        return None
    seconds, second_fraction = divmod(float(time_text_match["seconds"].strip(strip_chars).replace(",", ".")), 1)
    return timedelta(
        hours=int((time_text_match["hours"] or "0").strip(strip_chars)),
        minutes=int(time_text_match["minutes"].strip(strip_chars)),
        seconds=seconds,
        milliseconds=round(second_fraction*1000))


def time_to_text(time: timedelta, format: str, comma_decimals: bool = False) -> str:
    assert time
    assert format
    remainder_seconds = time.total_seconds()
    hours, remainder_minutes = divmod(remainder_seconds, 3600)
    minutes, seconds = divmod(remainder_minutes, 60)
    time_text = format % {'h': int(hours), 'm': int(minutes), 's': seconds}
    return time_text.replace(".", ",") if comma_decimals else time_text


class SubtitleLine(ABC):

    def __init__(self):
        self.text: str = None

    @property
    def plain_text(self) -> str:
        return re.sub(r"[ ]+", " ", re.sub(r"</?[A-z]>", "", self.text)).strip()


TSubtitleLine = TypeVar('TSubtitleLine', bound=SubtitleLine)


class Subtitle(ABC, Generic[TSubtitleLine]):

    def __init__(self):
        self.lines: List[TSubtitleLine] = []


TSubtitle = TypeVar('TSubtitle', bound=Subtitle)


class SubtitleFormat(ABC, Generic[TSubtitle, TSubtitleLine]):

    @abstractmethod
    def supports_subtitle(self, file_name: str) -> bool:
        pass

    def parse(self, content: bytes) -> TSubtitle:
        try:
            return self._parse(content)
        except Exception as e:
            raise SubtitleParseException(self) from e

    @abstractmethod
    def _parse(self, content: bytes) -> TSubtitle:
        pass

    def render(self, subtitle: TSubtitle) -> bytes:
        try:
            return self._render(subtitle)
        except Exception as e:
            raise SubtitleRenderException(self) from e

    @abstractmethod
    def _render(self, subtitle: TSubtitle) -> bytes:
        pass

    def process(self, content: bytes, tranformer: Callable[[TSubtitleLine], TSubtitleLine]) -> bytes:
        subtitle = self._parse(content)
        subtitle.lines = [tranformer(source_line) for source_line in subtitle.lines]
        return self.render(subtitle)
