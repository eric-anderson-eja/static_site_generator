import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_extra_spaces(self):
        self.assertEqual(extract_title("#   Space Case   "), "Space Case")

    def test_no_h1_raises_exception(self):
        with self.assertRaises(Exception):
            extract_title("## Only an h2")