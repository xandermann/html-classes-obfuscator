"""Tests"""

import unittest

from html_classes_obfuscator import html_classes_obfuscator


class TestsGenerateJS(unittest.TestCase):
    """Tests

    Args:
        unittest (unittest.TestCase): Unittest library
    """

    def test_generate_js_query_selector_double_quotes(self) -> None:
        """Test"""
        new_js = html_classes_obfuscator.generate_js('document.querySelector(".hello")', {"hello": "test_1"})
        expected_new_js = 'document.querySelector(".test_1")'
        self.assertEqual(new_js, expected_new_js)

    # TODO
    # def test_generate_js_query_selector_simple_quotes(self) -> None:
    #     """Test"""
    #     new_js = html_classes_obfuscator.generate_js("document.querySelector('.hello')", {"hello": "test_1"})
    #     expected_new_js = 'document.querySelector(".test_1")'
    #     self.assertEqual(new_js, expected_new_js)

    def test_generate_js_query_selector_all(self) -> None:
        """Test"""
        new_js = html_classes_obfuscator.generate_js('document.querySelectorAll(".hello")', {"hello": "test_1"})
        expected_new_js = 'document.querySelectorAll(".test_1")'
        self.assertEqual(new_js, expected_new_js)

    # TODO
    # def test_generate_js_query_selector_all_simple_quotes(self) -> None:
    #     """Test"""
    #     new_js = html_classes_obfuscator.generate_js("document.querySelectorAll('.hello')", {"hello": "test_1"})
    #     expected_new_js = "document.querySelectorAll('.test_1')"
    #     self.assertEqual(new_js, expected_new_js)

    def test_generate_js_toggle_class_list(self) -> None:
        """Test"""
        new_js = html_classes_obfuscator.generate_js('myDiv.classList.toggle("hello")', {"hello": "test_1"})
        expected_new_js = 'myDiv.classList.toggle("test_1")'
        self.assertEqual(new_js, expected_new_js)

    # TODO
    # def test_generate_js_toggle_class_list_simple_quotes(self) -> None:
    #     """Test"""
    #     new_js = html_classes_obfuscator.generate_js("myDiv.classList.toggle('hello')", {"hello": "test_1"})
    #     expected_new_js = "myDiv.classList.toggle('test_1')"
    #     self.assertEqual(new_js, expected_new_js)
