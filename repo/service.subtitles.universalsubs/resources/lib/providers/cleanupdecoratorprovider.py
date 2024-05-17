# -*- coding: utf-8 -*-

import copy
import functools
import math
import os
import re
import shutil
import time
from pathlib import Path
from typing import Dict, List

from resources.lib.common.settings import Settings
from resources.lib.formats.subtitleformat import Subtitle, SubtitleLine
from resources.lib.formats.subtitleformatsregistry import \
    SubtitleFormatsRegistry
from resources.lib.providers.decoratorprovider import DecoratorProvider
from resources.lib.providers.getrequest import GetRequest
from resources.lib.providers.getresult import GetResult
from resources.lib.providers.provider import Provider
from resources.lib.utils.httpclient import HttpClient, HttpRequest
from resources.lib.utils.text import apply_until_unmodified

TAG_MARKERS: List[str] = ["<font ", "<font>", "</font"]
PAUSE_MARKERS: List[str] = [',', ';', ':', '.', '?', '!']


class TextLineBreak:
    def __init__(self, priority: int, index: int, effective_index: int) -> None:
        self.priority: int = priority
        self.index: int = index  # relative to line
        self.effective_index: int = effective_index  # relative to line

    def distance_to(self, target_effective_index: int) -> int:
        return abs(target_effective_index - self.effective_index)

    def score(self, target_effective_index: int) -> int:
        if self.priority == 0:
            return 15 - self.distance_to(target_effective_index)
        elif self.priority == 1:
            return 4 - self.distance_to(target_effective_index)
        else:
            return 0 - self.distance_to(target_effective_index)


class TextLineInfo:

    def __init__(self, offset_index: int, starts_inside_tag: bool, text: str) -> None:
        self.offset_index: int = offset_index
        self.length: int = len(text)
        self.effective_length: int = 0
        self.candidate_breaks: List[TextLineBreak] = []
        self.starts_inside_tag: bool = starts_inside_tag
        self.ends_inside_tag: bool = starts_inside_tag
        current_index: int = 0
        previous_char: str = None
        for current_char in text:
            if not self.ends_inside_tag and current_char == '<':
                current_text_start = text[current_index:]
                if any(current_text_start.startswith(tag_marker) for tag_marker in TAG_MARKERS):
                    self.ends_inside_tag = True
            elif self.ends_inside_tag:
                if current_char == '>':
                    self.ends_inside_tag = False
            else:
                if current_index > 0 and current_index < len(text) - 1:
                    if previous_char == ' ' and (current_char == '[' or current_char == '-'):
                        self.candidate_breaks.append(TextLineBreak(0, current_index, self.effective_length))
                    elif current_char == ' ':
                        priority = 0 if previous_char == ']' else 1 if previous_char in PAUSE_MARKERS else 2
                        self.candidate_breaks.append(TextLineBreak(priority, current_index, self.effective_length))
                self.effective_length += 1
                previous_char = current_char
            current_index += 1


class TextInfo:

    def __init__(self, text: str) -> None:
        self.lines_info: List[TextLineInfo] = []
        current_offset = 0
        inside_tag = False
        for line_text in text.splitlines():
            line_info = TextLineInfo(current_offset, inside_tag, line_text)
            current_offset += line_info.length + 1
            inside_tag = line_info.ends_inside_tag
            self.lines_info.append(line_info)

    @property
    def total_length(self) -> int:
        return functools.reduce(lambda tl, li: tl + li.length, self.lines_info, 0)

    @property
    def total_effective_length(self) -> int:
        return functools.reduce(lambda tl, li: tl + li.effective_length, self.lines_info, 0)


class CleanupDecoratorProvider(DecoratorProvider):

    def __init__(self, source: Provider, settings: Settings):
        super().__init__(source)
        self._settings = settings
        self._formats_registry = SubtitleFormatsRegistry()
        self._clean_up_rules: Dict[str, List[str]] = None

    @property
    def name(self) -> str:
        return "Cleanup"

    def __ensure_clean_up_rules_file_exists(self) -> Path:
        sections_rules_path = self._settings.addon_user_path.joinpath("clean_up_rules.ini")
        if not sections_rules_path.exists() or \
            (self._settings.clean_up_rules_update_interval and self._settings.clean_up_rules_update_url
             and self._settings.clean_up_rules_update_interval.total_seconds() < (time.time() - os.path.getmtime(sections_rules_path))):
            try:
                http_response = HttpClient().exchange(HttpRequest(self._settings.clean_up_rules_update_url))
                http_response.write_into(sections_rules_path)
            except:
                self._logger.error("Error updating cleanup rules from \"%s\"" % self.update_url, exc_info=True)
        if not sections_rules_path.exists():
            try:
                reference_sections_rules_path = self._settings.addon_path.joinpath("resources", "clean_up_rules.ini")
                shutil.copyfile(reference_sections_rules_path, sections_rules_path)
            except:
                self._logger.error("Error copying cleanup rules from \"%s\"" % self.update_url, exc_info=True)
                return None
        return sections_rules_path

    def __ensure_clean_up_rules_loaded(self) -> None:
        if self._clean_up_rules:
            return  # cleanup rules already loaded
        self._clean_up_rules: Dict[str, List[str]] = {}
        clean_up_rules_path = self.__ensure_clean_up_rules_file_exists()
        if not clean_up_rules_path:
            return  # was unable to download nor copy the cleanup rules
        section_rules: List[str] = None
        with open(clean_up_rules_path, "rt", encoding='utf-8') as file:
            for file_line in file:
                file_line = re.sub("#.*", "", file_line).strip()  # strip comments
                if not file_line:
                    continue
                section_name_match = re.match(r"\[([^\]]+)\]", file_line)
                if section_name_match:
                    section_name = section_name_match[1].lower()
                    section_rules = self._clean_up_rules.get(section_name, None)
                    if section_rules is None:
                        self._clean_up_rules[section_name] = section_rules = []
                elif section_rules is not None:
                    section_rules.append(file_line)

    def apply_clean_up_rules(self, text: str, clean_up_rules: List[str]) -> str:
        for clean_up_rule in clean_up_rules:
            try:
                text = re.sub(clean_up_rule, '', text, flags=re.IGNORECASE | re.DOTALL)
            except Exception as e:
                self._logger.debug("Error processing cleanup rule %s: '", clean_up_rule, str(e))
        return text

    @staticmethod
    def apply_custom_rules(text: str) -> str:
        # fix opening <font> tags
        text = re.sub(
            r"""(<\s*|[ \t]*)(/\s*|[ \t]*)font(\s*)color(\s*)=(\s*)["'](?P<color>[^"']+)["'](\s*)>""",
            r'<font color="\g<color>">',
            text,
            flags=re.IGNORECASE)
        # fix closing <font> tags
        text = re.sub(r'(<\s*|[ \t]*)(/\s*|[ \t]*)font(\s*)>', '</font>', text, flags=re.IGNORECASE)
        # simplify <font> tags enclosing at most 2 characters out or only white space
        text = apply_until_unmodified(text, lambda t: re.sub(
            r'<font color="(?P<color>[^"]+)">(?P<text1>[^<]*)</font>(?P<text2>\s*[^<]{0,2}\s*)<font color="(?P=color)">',
            r'<font color="\g<color>">\g<text1>\g<text2>', t))
        text = apply_until_unmodified(text, lambda t: re.sub(
            r'(?P<before>^|</font>)(?P<text>\s*[^<]{0,2}\s*)(?P<font><font[^>]*>)',
            r'\g<before>\g<font>\g<text>', t))
        # add missing space after dialog marker
        text = re.sub(
            r'(?P<before>^\s*|^\s*<font[^>]*>\s*|[\.!\?\)\]\}]\s*</?font[^>]*>\s*|[\.!\?\)\]\}]\s*</font>\s*<font[^>]*>\s*|[\.!\?\)\]\}]\s*)[-—]',
            r'\g<before> - ', text)
        # fix space after opening <font> tags
        text = re.sub(r"""<font([^>]*)>(\s+)""", r"\2<font\1>", text)
        # fix space before closing <font> tags
        text = re.sub(r"""(\s+)</font>""", r"</font>\1", text)
        # remove white space before special characters
        text = re.sub(r'\s+([,\.;:!\?\)\]\}])', r"\1", text)
        # remove white space after special characters
        text = re.sub(r'(¡¿\(\[\{])\s+', r"\1", text)
        # simplify consecutive white spaces
        text = re.sub(r' {2,}', ' ', text)
        # strip white space at begining of lines
        text = re.sub(r'^\s*(<font[^>]*>)">\s*', r"\1", text, flags=re.MULTILINE)
        text = re.sub(r'^\s+', r"", text, flags=re.MULTILINE)
        text = text.lstrip()
        # strip white space at end of lines
        text = re.sub(r'\s*</font>\s*$', r'</font>', text, flags=re.MULTILINE)
        text = re.sub(r'\s+$', r'', text, flags=re.MULTILINE)
        text = text.rstrip()
        # strip single dialog marker
        if len(re.findall(r"- ", text)) == 1 and re.match(r"(^- |^<font[^>]*>- )", text):
            text = re.sub(r"(^|^<font[^>]*>)- ", r"\1", text)
        return text

    @staticmethod
    def apply_line_breaks(text: str, max_line_length: int = 45) -> str:
        text_info = TextInfo(text)
        if len(text_info.lines_info) != 1:
            return text
        line_info: TextLineInfo = text_info.lines_info[0]
        target_effective_index = math.ceil(line_info.effective_length / 2) + 1
        if line_info.effective_length < max_line_length and not any(b for b in line_info.candidate_breaks if b.priority == 0):
            return text
        sorted_prority_breaks = sorted(line_info.candidate_breaks,
                                       key=lambda b: b.score(target_effective_index), reverse=True)
        selected_break: TextLineBreak = next((b for b in sorted_prority_breaks), None)
        if selected_break:
            return text[:selected_break.index].strip() + "\n" + text[selected_break.index:].strip()
        return text

    def clean_up_subtitle(self, subtitle: Subtitle, ads_rules: List[str], hi_marks_rules: List[str]) -> GetResult:
        for _line in reversed(subtitle.lines):
            line: SubtitleLine = _line
            line_text: str = line.text or ""
            line_text = re.sub(' {2,}', ' ', line_text).strip()
            if ads_rules:
                line_text = self.apply_clean_up_rules(line_text, ads_rules)
            if hi_marks_rules:
                line_text = self.apply_clean_up_rules(line_text, hi_marks_rules)
            line_text = CleanupDecoratorProvider.apply_custom_rules(line_text)
            line_text = CleanupDecoratorProvider.apply_line_breaks(line_text)
            if not line_text:
                subtitle.lines.remove(line)
            else:
                line.text = line_text

    def _transform_get_results(self, request: GetRequest, source_request: GetRequest, source_results: List[GetResult]) -> List[GetResult]:
        self.__ensure_clean_up_rules_loaded()
        ads_rules: List[str] = self._clean_up_rules.get("ads", []) + self._clean_up_rules.get("ads_" + request.language.three_letter_code, []) \
            if self._settings.clean_up_ads else None
        hi_marks_rules: List[str] = self._clean_up_rules.get(
            "ccmarks", []) if self._settings.clean_up_hi_markers else None
        cleanedup_results: List[GetResult] = []
        for source_result in source_results:
            try:
                format, subtitle = self._formats_registry.parse(source_result.file_name, source_result.content)
                self.clean_up_subtitle(subtitle, ads_rules, hi_marks_rules)
                cleanedup_result = copy.deepcopy(source_result)
                cleanedup_result.provider_name = self.name + "|" + source_result.provider_name
                cleanedup_result.content = format.render(subtitle)
                cleanedup_results.append(cleanedup_result)
            except:
                self._logger.error("Error cleaning up result \"%s\"" % source_result.file_name, exc_info=True)
                cleanedup_results.append(source_result)
        return cleanedup_results
