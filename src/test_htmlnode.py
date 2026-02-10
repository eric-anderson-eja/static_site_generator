import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "p", 
            "Hello", 
            None, 
            {"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_values(self):
        # Test that the constructor correctly assigns values
        node = HTMLNode("h1", "Title content")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Title content")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        # Test that __repr__ outputs what we expect
        node = HTMLNode("p", "text", None, {"class": "primary"})
        self.assertEqual(
            repr(node), 
            "HTMLNode(p, text, children: None, {'class': 'primary'})"
        )

if __name__ == "__main__":
    unittest.main()