import unittest
from markdown import *

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [], "Empty input should return an empty list.")
    
    def test_single_line(self):
        self.assertEqual(markdown_to_blocks("Hello, world!"), ["Hello, world!"], "Single line should return one block.")
    
    def test_multiple_lines_no_empty(self):
        self.assertEqual(
            markdown_to_blocks("Line 1\nLine 2\nLine 3"),
            ["Line 1\nLine 2\nLine 3"],
            "Lines without gaps should return one block."
        )
    
    def test_multiple_blocks(self):
        input_text = "Block 1 line 1\nBlock 1 line 2\n\nBlock 2 line 1\n\nBlock 3 line 1\nBlock 3 line 2"
        expected_output = [
            "Block 1 line 1\nBlock 1 line 2",
            "Block 2 line 1",
            "Block 3 line 1\nBlock 3 line 2"
        ]
        self.assertEqual(markdown_to_blocks(input_text), expected_output, "Multiple blocks should be correctly identified.")
    
    def test_leading_trailing_empty_lines(self):
        input_text = "\n\nBlock 1\n\nBlock 2\n\n"
        expected_output = ["Block 1", "Block 2"]
        self.assertEqual(
            markdown_to_blocks(input_text),
            expected_output,
            "Leading and trailing empty lines should be ignored."
        )
    
    def test_empty_lines_with_spaces(self):
        input_text = "Block 1 line 1\n\n  \nBlock 2 line 1\n\n"
        expected_output = ["Block 1 line 1", "Block 2 line 1"]
        self.assertEqual(
            markdown_to_blocks(input_text),
            expected_output,
            "Empty lines with spaces should be treated as empty."
        )
    
    def test_only_empty_lines(self):
        self.assertEqual(markdown_to_blocks("\n\n\n"), [], "Only empty lines should return an empty list.")


    def test_complex_markdown(self):
        text = (
            "# This is a heading\n\n"
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"
            "* This is the first list item in a list block\n"
            "* This is a list item\n"
            "* This is another list item"
        )
        
        expected_output = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        
        self.assertEqual(
            markdown_to_blocks(text),
            expected_output,
            "Complex markdown input with headings, paragraphs, and lists should be split into separate blocks."
        )

if __name__ == "__main__":
    unittest.main()
