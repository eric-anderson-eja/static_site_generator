import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, url=None)
        self.assertEqual(node, node2)

    def test_not_eq_texttype(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, url=None)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("WRONG Text", TextType.BOLD_TEXT, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, url=None)
        self.assertNotEqual(node, node2)

    def test_not_url(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, url="TEST")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, url=None)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()