# -*- coding: utf-8 -*-

import re
from html import unescape
from typing import Callable, List

import chardet
from unidecode import unidecode


def unescape_html(text: str, simplify_spaces=True) -> str:
    clean_text = unescape(text)
    if simplify_spaces:
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
    return clean_text


# def find_text_between(text: str, start_marker: str, end_marker: str, strip_markers: bool = False) -> str:
#     start_marker_index = text.find(start_marker)
#     if start_marker_index < 0:
#         return None
#     end_marker_index = text.find(end_marker, start_marker_index)
#     if end_marker_index < 0:
#         return None
#     if strip_markers:
#         result = text[start_marker_index + len(start_marker):end_marker_index]
#     else:
#         result = text[start_marker_index:end_marker_index + len(end_marker)]
#     return result


def normalize_text(text: str, lower: bool = True) -> str:
    normalized_text = re.sub(r"[^A-z0-9]+", " ", unidecode(text)).strip()
    return normalized_text.lower() if lower else normalized_text


def normalize_white_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def strip_text_from(what: str, where: str, beginning_only=False) -> str:
    what = re.compile((r"^[\s\.]*" if beginning_only else r"[\s\.]*") + r"[\s\.]+".join([re.escape(s)
                      for s in re.split(r"[\s\.\(\)\[\]]+", what.strip())]) + r"[\s\.]*", re.IGNORECASE)
    stripped = re.sub(what, " ", where).strip()
    return stripped


def strip_common_text(texts: List[str], strip_from_start: bool = True, strip_from_end: bool = True) -> List[str]:
    if not texts or len(texts) < 2 or (not strip_from_start and not strip_from_end):
        return texts
    if strip_from_start:
        for char in texts[0]:
            all_equals = True
            for text in texts[1:]:
                if not len(text) or text[0] != char:
                    all_equals = False
                    break
            if not all_equals:
                break
            texts = [text[1:] for text in texts]
    if strip_from_end:
        for char in texts[0][::-1]:
            all_equals = True
            for text in texts[1:]:
                if not len(text) or text[len(text) - 1] != char:
                    all_equals = False
                    break
            if not all_equals:
                break
            texts = [text[:-1] for text in texts]
    return texts


def bytes_to_string(content: bytes) -> str:
    detected_encoding = chardet.detect(content)["encoding"] or "utf-8"
    return content.decode(detected_encoding, "ignore")


def apply_until_unmodified(text: str, function: Callable[[str], str]) -> str:
    while True:
        updated_text = function(text)
        if updated_text == text:
            return updated_text
        text = updated_text
