"""Tests"""

import unittest

from html_classes_obfuscator import html_classes_obfuscator


class ParseHtmlClassNames(unittest.TestCase):
    """Tests

    Args:
        unittest (unittest.TestCase): Unittest library
    """

    def test_parse(self) -> None:
        """Test"""
        ParseHtmlClassNames.counter = 0

        def generate_class(current_classes_list):
            # pylint: disable=W0613
            ParseHtmlClassNames.counter += 1
            return "test_" + str(ParseHtmlClassNames.counter)

        parse = html_classes_obfuscator.parse_html_class_names('<div class="hello">hello</div>', {}, generate_class)
        expected_parse = (['hello'], ['test_1'], {'hello': 'test_1'})
        self.assertEqual(parse, expected_parse)

    def test_parse_multiple_class_names(self) -> None:
        """Test"""
        ParseHtmlClassNames.counter = 0

        def generate_class(current_classes_list):
            # pylint: disable=W0613
            ParseHtmlClassNames.counter += 1
            return "test_" + str(ParseHtmlClassNames.counter)

        parse = html_classes_obfuscator.parse_html_class_names('<div class="hello world">hello</div>', {}, generate_class)
        expected_parse = (['hello world'], ['test_1 test_2'], {'hello': 'test_1', "world": "test_2"})
        self.assertEqual(parse, expected_parse)
