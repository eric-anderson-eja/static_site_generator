import unittest
import re

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image, 
    split_nodes_link
)
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT_PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT_PLAIN),
                TextNode("bolded", TextType.BOLD_TEXT),
                TextNode(" word", TextType.TEXT_PLAIN),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT_PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT_PLAIN),
                TextNode("bolded", TextType.BOLD_TEXT),
                TextNode(" word and ", TextType.TEXT_PLAIN),
                TextNode("another", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT_PLAIN)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT_PLAIN),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word", TextType.TEXT_PLAIN),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT_PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT_PLAIN),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" word", TextType.TEXT_PLAIN),
            ],
            new_nodes,
        )

    def test_exception_unclosed_delimiter(self):
        node = TextNode("This is text with an unclosed *italic word", TextType.TEXT_PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfbe92.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("another", "https://i.imgur.com/dfbe92.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    import unittest

class TestSplitNodes(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT_PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT_PLAIN),
                TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "![first](https://url.com/1.png) middle ![second](https://url.com/2.png) end",
            TextType.TEXT_PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4) # Change this from 5 to 4
        self.assertEqual(new_nodes[0].text, "first")
        self.assertEqual(new_nodes[1].text, " middle ")
        self.assertEqual(new_nodes[2].text, "second")
        self.assertEqual(new_nodes[3].text, " end")

    def test_split_links(self):
        node = TextNode(
            "Click [here](https://google.com) and [there](https://bing.com)",
            TextType.TEXT_PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[1].text_type, TextType.LINK_TEXT)
        self.assertEqual(new_nodes[3].url, "https://bing.com")

    def test_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT_PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Just plain text")



if __name__ == "__main__":
    unittest.main()