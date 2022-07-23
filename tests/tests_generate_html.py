"""Tests"""

import unittest

from html_classes_obfuscator import html_classes_obfuscator


class TestsGenerateHTML(unittest.TestCase):
    """Tests

    Args:
        unittest (unittest.TestCase): Unittest library
    """

    def test_generate_html_simple_quotes(self) -> None:
        """Test simple quotes case"""
        new_html = html_classes_obfuscator.generate_html('<div class="hello">hello</div>', ["hello"], ["test_1"])
        expected_new_html = "<div class=test_1>hello</div>"
        self.assertEqual(new_html, expected_new_html)

    def test_generate_html_double_quotes(self) -> None:
        """Test double quotes case"""
        new_html = html_classes_obfuscator.generate_html("<div class='hello'>hello</div>", ["hello"], ["test_1"])
        expected_new_html = "<div class=test_1>hello</div>"
        self.assertEqual(new_html, expected_new_html)

    def test_generate_html_multiples_attributes(self) -> None:
        """Test when there is multiples html classes"""
        new_html = html_classes_obfuscator.generate_html("<div class='hello world'>hello</div>", ["hello world"], ["test_1 test_2"])
        expected_new_html = '<div class="test_1 test_2">hello</div>'
        self.assertEqual(new_html, expected_new_html)

    def test_generate_html_no_quotes(self) -> None:
        """Test double quotes case"""
        new_html = html_classes_obfuscator.generate_html("<div class=hello>hello</div>", ["hello"], ["test_1"])
        expected_new_html = "<div class=test_1>hello</div>"
        self.assertEqual(new_html, expected_new_html)

    def test_generate_html_no_quotes_inside_div(self) -> None:
        """Test no quotes case"""
        new_html = html_classes_obfuscator.generate_html("<div class=hello>hello</div>", ["hello"], ["test_1"])
        expected_new_html = "<div class=test_1>hello</div>"
        self.assertEqual(new_html, expected_new_html)

    def test_generate_html_with_attributes(self) -> None:
        """Test when there is other attributes"""
        new_html = html_classes_obfuscator.generate_html("<div class=hello title=hello>hello</div>", ["hello"], ["test_1"])
        expected_new_html = "<div class=test_1 title=hello>hello</div>"
        self.assertEqual(new_html, expected_new_html)

    def test_generate_html_with_brackets_in_class_name(self) -> None:
        """Test with `[` and `]` case"""
        new_html = html_classes_obfuscator.generate_html("<div class='after:h-[2px]'>hello</div>", ["after:h-[2px]"], ["test_1"])
        expected_new_html = "<div class=test_1>hello</div>"
        self.assertEqual(new_html, expected_new_html)

    def test_generate_html_with_percentage(self) -> None:
        """Test with `%` case"""
        new_html = html_classes_obfuscator.generate_html("<div class='max-w-[80%]'></div>", ["max-w-[80%]"], ["test_1"])
        expected_new_html = "<div class=test_1></div>"
        self.assertEqual(new_html, expected_new_html)

    def test_generate_html_with_dash_no_quotes(self) -> None:
        """Test with `-` when no quotes"""
        new_html = html_classes_obfuscator.generate_html('<div class=flex><div class=flex-shrink></div></div>', ["flex", "flex-shrink"], ["test_1", "test_2"])
        expected_new_html = '<div class=test_1><div class=test_2></div></div>'
        self.assertEqual(new_html, expected_new_html)
