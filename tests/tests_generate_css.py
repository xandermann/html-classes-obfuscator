"""Tests"""

import unittest

from html_classes_obfuscator import html_classes_obfuscator


class TestsGenerateCSS(unittest.TestCase):
    """Tests

    Args:
        unittest (unittest.TestCase): Unittest library
    """

    def test_generate_css_simple_case(self) -> None:
        """Test"""
        new_css = html_classes_obfuscator.generate_css('.hello{color:blue}', {"hello": "test_1"})
        expected_new_css = '.test_1{color:blue}'
        self.assertEqual(new_css, expected_new_css)

    def test_generate_css_double_case(self) -> None:
        """Test"""
        new_css = html_classes_obfuscator.generate_css('.hello .world{color:blue}', {"hello": "test_1", "world": "test_2"})
        expected_new_css = '.test_1 .test_2{color:blue}'
        self.assertEqual(new_css, expected_new_css)

    def test_generate_css_tailwind_case(self) -> None:
        """Test"""
        new_css = html_classes_obfuscator.generate_css(r'.lg\:1\/4{color:blue}', {"lg:1/4": "test_1"})
        expected_new_css = '.test_1{color:blue}'
        self.assertEqual(new_css, expected_new_css)

    def test_generate_css_pseudo_elements_case(self) -> None:
        """Test"""
        new_css = html_classes_obfuscator.generate_css('.hello .world:not(.not_me, div){color:blue}', {"hello": "test_1", "world": "test_2", "not_me": "test_3"})
        expected_new_css = '.test_1 .test_2:not(.test_3, div){color:blue}'
        self.assertEqual(new_css, expected_new_css)

    def test_generate_css_with_brackets_in_class_name(self) -> None:
        """Test with `[` and `]` case"""
        new_css = html_classes_obfuscator.generate_css(r".after\:h-\[2px\]::after{height:2px}", {"after:h-[2px]": "test_1"})
        expected_new_css = '.test_1::after{height:2px}'
        self.assertEqual(new_css, expected_new_css)
