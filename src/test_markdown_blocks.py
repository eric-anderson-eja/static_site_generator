import unittest
from markdown_blocks import block_to_block_type, markdown_to_blocks, BlockType, markdown_to_html_node

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

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_headings(self):
        md = """
# The Main Title

### A smaller sub-heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>The Main Title</h1><h3>A smaller sub-heading</h3></div>",
        )

    def test_mixed_lists(self):
        md = """
- First item
- Second item with **bold**

1. First ordered
2. Second ordered
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<ul><li>First item</li><li>Second item with <b>bold</b></li></ul>"
            "<ol><li>First ordered</li><li>Second ordered</li></ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_blockquote(self):
        md = """
> This is a quote
> that spans two lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote that spans two lines</blockquote></div>",
        )
    def test_empty(self):
        md = ""
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()