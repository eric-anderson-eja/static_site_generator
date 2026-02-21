import unittest
from markdown_blocks import block_to_block_type, markdown_to_blocks, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
# This is a heading


This is a paragraph with too many newlines below it.


- Item 1
- Item 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph with too many newlines below it.",
                "- Item 1\n- Item 2",
            ],
        )

import unittest
# Assuming your code is in a file named block_markdown.py
# from block_markdown import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):

    def test_headings(self):
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### triple heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### hex heading"), BlockType.HEADING)
        # Invalid heading (no space)
        self.assertEqual(block_to_block_type("####### too many"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#no_space"), BlockType.PARAGRAPH)

    def test_code_block(self):
        code = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        # Invalid code (missing newline after backticks)
        invalid_code = "```print('hello')\n```"
        self.assertEqual(block_to_block_type(invalid_code), BlockType.PARAGRAPH)

    def test_quote_block(self):
        quote = "> This is a quote\n> with multiple lines"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        # One line missing the >
        bad_quote = "> line 1\nline 2"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        ul = "- item 1\n- item 2"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)
        # Missing space after dash
        bad_ul = "-item 1\n- item 2"
        self.assertEqual(block_to_block_type(bad_ul), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        ol = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)
        # Starts at wrong number
        bad_ol = "2. first\n3. second"
        self.assertEqual(block_to_block_type(bad_ol), BlockType.PARAGRAPH)
        # Skips a number
        jumpy_ol = "1. first\n3. second"
        self.assertEqual(block_to_block_type(jumpy_ol), BlockType.PARAGRAPH)

    def test_paragraph(self):
        para = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(para), BlockType.PARAGRAPH)



if __name__ == "__main__":
    unittest.main()