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


class TestTextLineBreak(unittest.TestCase):

    def __test_line_break(self, source_text: str, expected_text: str, max_line_length: int = 50) -> None:
        source_text = textwrap.dedent(source_text).strip()
        expected_text = textwrap.dedent(expected_text).strip()
        cleanup_text = CleanupDecoratorProvider.apply_line_breaks(source_text, max_line_length)
        self.assertEqual(cleanup_text, expected_text)

    def test_always_breaks_brackets_at_beginning(self) -> None:
        source_text = """
        [some text 1] some text 2
        """
        expected_text = """
        [some text 1]
        some text 2
        """
        self.__test_line_break(source_text, expected_text, 200)

    def test_always_breaks_brackets_at_end(self) -> None:
        source_text = """
        some text 1 [some text 2]
        """
        expected_text = """
        some text 1
        [some text 2]
        """
        self.__test_line_break(source_text, expected_text, 200)

    def test_always_breaks_dialogs(self) -> None:
        source_text = """
        - some text 1. - some text 2.
        """
        expected_text = """
        - some text 1.
        - some text 2.
        """
        self.__test_line_break(source_text, expected_text, 200)

    def test_breaks_dialogs(self) -> None:
        source_text = """
        - some text 1. - some text 2. - some text 3.
        """
        expected_text = """
        - some text 1. - some text 2.
        - some text 3.
        """
        self.__test_line_break(source_text, expected_text, 200)

    def test_breaks_dialogs_with_fonts(self) -> None:
        source_text = """
        - <font color="ffffff">some text 1.</font> - some text 2. - some text 3.
        """
        expected_text = """
        - <font color="ffffff">some text 1.</font> - some text 2.
        - some text 3.
        """
        self.__test_line_break(source_text, expected_text, 200)

    def test_breaks_long_lines(self) -> None:
        source_text = """
        some text1 some text2 some text3 some text4 some text5 some text6.
        """
        expected_text = """
        some text1 some text2 some text3
        some text4 some text5 some text6.
        """
        self.__test_line_break(source_text, expected_text, 35)

    def test_does_not_break_short_lines(self) -> None:
        source_text = """
        some text1 some text2.
        """
        expected_text = """
        some text1 some text2.
        """
        self.__test_line_break(source_text, expected_text, 50)

    def test_does_not_break_short_lines2(self) -> None:
        source_text = """
        <font color="#ffff00">- You arrived just in time.</font>
        """
        expected_text = """
        <font color="#ffff00">- You arrived just in time.</font>
        """
        self.__test_line_break(source_text, expected_text, 50)

    def test_breaks_with_font2(self) -> None:
        source_text = """
        - Oh... Claudio.<font color="#ffff00"> - Mink!</font>
        """
        expected_text = """
        - Oh... Claudio.<font color="#ffff00">
        - Mink!</font>
        """
        self.__test_line_break(source_text, expected_text, 50)

    def test_breaks_with_font3(self) -> None:
        source_text = """
        - Oh... Claudio. <font color="#ffff00">- Mink!</font>
        """
        expected_text = """
        - Oh... Claudio. <font color="#ffff00">
        - Mink!</font>
        """
        self.__test_line_break(source_text, expected_text, 50)


if __name__ == '__main__':
    unittest.main()
