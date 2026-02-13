import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = LeafNode("a", "Click me!", props)
        self.assertEqual(
            node.to_html(), 
            '<a href="https://www.google.com" target="_blank">Click me!</a>'
        )

    # Test a bold tag
    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    # Test an italic tag
    def test_leaf_to_html_italic(self):
        node = LeafNode("i", "Italic text")
        self.assertEqual(node.to_html(), "<i>Italic text</i>")

    # Test raw text (No tag)
    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "This is just raw text.")
        self.assertEqual(node.to_html(), "This is just raw text.")
        
    # Test that it raises a ValueError if value is missing
    def test_leaf_no_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    # Test the __repr__ output
    def test_repr(self):
        node = LeafNode("p", "Testing repr", {"class": "primary"})
        self.assertEqual(
            repr(node), 
            "LeafNode(p, Testing repr, {'class': 'primary'})"
        )