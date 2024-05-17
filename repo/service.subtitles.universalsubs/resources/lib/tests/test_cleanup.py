#!/usr/bin/python

import sys
import textwrap
import unittest
from pathlib import Path

if __name__ == '__main__' and not __package__:
    __package__ = 'resources.lib.tests'
    sys.path.append(str(Path(__file__).resolve().parents[len(__package__.split("."))]))
    try:
        sys.path.remove(str(Path(__file__).resolve().parent))
    except ValueError:
        pass

from ..providers.cleanupdecoratorprovider import CleanupDecoratorProvider


class TestTextCleanup(unittest.TestCase):

    def __test_custom_cleanup(self, source_text: str, expected_text: str) -> None:
        source_text = textwrap.dedent(source_text)
        expected_text = textwrap.dedent(expected_text).strip()
        resulting_text = CleanupDecoratorProvider.apply_custom_rules(source_text)
        self.assertEqual(expected_text, resulting_text)

    def test_custom_cleanup_with_start_font_tag(self) -> None:
        source_text = """
        <FONT color="red">text</font>
        FONT COLOR='black'>text</font>
        <FONT COLOR='white'>text</font>
        </FONT color="green">text</font>
        """
        expected_text = """
        <font color="red">text</font>
        <font color="black">text</font>
        <font color="white">text</font>
        <font color="green">text</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_custom_cleanup_with_end_font_tag(self) -> None:
        source_text = """
        <font color="red">text</FONT>
        <font color="black">text<FONT>
        <font color="white">textFONT>
        """
        expected_text = """
        <font color="red">text</font>
        <font color="black">text</font>
        <font color="white">text</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_custom_cleanup_with_redundant_multiple_font_tag(self) -> None:
        source_text = """
        <font color="red">text</font>
        <font color="red">text</font>
        <font color="red">text</font>
        """
        expected_text = """
        <font color="red">text
        text
        text</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_custom_cleanup_with_redundant_empty_font_tag(self) -> None:
        source_text = """
        <font color="white">text.
        some </font><font color="white">more text.</font>
        """
        expected_text = """
        <font color="white">text.
        some more text.</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_custom_cleanup_with_redundant_spaces_font_tag(self) -> None:
        source_text = """
        <font color="white">text.
        some </font>  <font color="white">more text.</font>
        """
        expected_text = """
        <font color="white">text.
        some more text.</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_custom_cleanup_with_redundant_chars_font_tag(self) -> None:
        source_text = """
        <font color="white">text.
        some </font> XX <font color="white">more text.</font>
        """
        expected_text = """
        <font color="white">text.
        some XX more text.</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_custom_cleanup_with_redundant_chars_font_tag_2(self) -> None:
        source_text = f"""
        T<font color="#ffff00">ext 1</font>
        """
        expected_text = """
        <font color="#ffff00">Text 1</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_custom_cleanup_with_begining_spaces(self) -> None:
        source_text = """
          <font color="red">text
        <font color="green">  text
        """
        expected_text = """
        <font color="red">text
        <font color="green">text
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_custom_cleanup_with_end_spaces(self) -> None:
        source_text = f"""
        - text.  </font>
        - text.</font>{'  '}
        """
        expected_text = """
        - text.</font>
        - text.</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_remove_single_dialog_marker(self) -> None:
        source_text = f"""
        <font color="white">- Text...</font>
        """
        expected_text = """
        <font color="white">Text...</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_fix_dialog_marker_within_font_tag_1(self) -> None:
        source_text = f"""
        Text 1. <font color="red">-Text 2</font>
        """
        expected_text = """
        Text 1. <font color="red">- Text 2</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_fix_dialog_marker_within_font_tag_2(self) -> None:
        source_text = f"""
        <font color="green">Text 1.</font> <font color="red">-Text 2</font>
        """
        expected_text = """
        <font color="green">Text 1.</font> <font color="red">- Text 2</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_fix_dialog_marker_within_font_tags_3(self) -> None:
        source_text = f"""
        <font color="white">Text 1.</font> <font color="green">-Text 2.</font> <font color="red">-Text 3</font>
        """
        expected_text = """
        <font color="white">Text 1.</font> <font color="green">- Text 2.</font> <font color="red">- Text 3</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_fix_dialog_marker_within_font_tags_4(self) -> None:
        source_text = f"""
        <font color="red">Text 1.</font>-Text 2.
        """
        expected_text = """
        <font color="red">Text 1.</font> - Text 2.
        """
        self.__test_custom_cleanup(source_text, expected_text)

    def test_fix_dialog_marker_within_font_tags_5(self) -> None:
        source_text = f"""
        <font color="red">- Text 1.</font><font color="green">- Text 2</font> <font color="green">Text 3.</font> <font color="red">- Text 4.</font> <font color="green">- Text 5.</font>
        """
        expected_text = """
        <font color="red">- Text 1.</font> <font color="green">- Text 2 Text 3.</font> <font color="red">- Text 4.</font> <font color="green">- Text 5.</font>
        """
        self.__test_custom_cleanup(source_text, expected_text)


if __name__ == '__main__':
    unittest.main()
