# src/test_generate.py
import unittest
from generate import extract_title

class TestGenerate(unittest.TestCase):
    def test_extract_title_basic(self):
        md = "# Hello\n\nThis is text."
        self.assertEqual(extract_title(md), "Hello")

    def test_extract_title_trims(self):
        md = "#   Trim me   "
        self.assertEqual(extract_title(md), "Trim me")

    def test_extract_title_missing(self):
        md = "## Subheading\nNo h1 here"
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
