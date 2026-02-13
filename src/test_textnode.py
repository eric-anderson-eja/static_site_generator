import unittest
from textnode import TextNode, TextType, text_node_to_html_node


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

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT_PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is alt text", TextType.IMAGE_TEXT, "https://www.boot.dev/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev/img.png", "alt": "This is alt text"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


if __name__ == "__main__":
    unittest.main()