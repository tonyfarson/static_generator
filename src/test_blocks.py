# src/test_block_types.py
import unittest
from blocks import block_to_block_type, BlockType

class TestBlockTypes(unittest.TestCase):
    # Headings
    def test_heading_valid_levels(self):
        self.assertEqual(block_to_block_type("# Title"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### H6"), BlockType.HEADING)

    def test_heading_requires_space_and_max_6_hashes(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    # Code
    def test_code_block_exact_fences(self):
        code = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_code_block_language_tag_not_allowed_by_rule(self):
        code_lang = "```python\nprint('hi')\n```"
        self.assertNotEqual(block_to_block_type(code_lang), BlockType.CODE)

    def test_code_block_missing_end_is_not_code(self):
        not_code = "```\nprint('hi')"
        self.assertEqual(block_to_block_type(not_code), BlockType.PARAGRAPH)

    # Quotes
    def test_quote_every_line_starts_with_gt(self):
        self.assertEqual(block_to_block_type("> one\n> two"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">one\n>two"), BlockType.QUOTE)  # space optional

    def test_quote_breaks_if_any_line_missing_gt(self):
        self.assertEqual(block_to_block_type("> ok\nnope"), BlockType.PARAGRAPH)

    # Unordered lists
    def test_unordered_list_dash_space_each_line(self):
        self.assertEqual(block_to_block_type("- a\n- b\n- c"), BlockType.UNORDERED_LIST)

    def test_unordered_list_rejects_indent_or_wrong_bullet(self):
        self.assertEqual(block_to_block_type(" - a\n- b"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("* a\n* b"), BlockType.PARAGRAPH)

    # Ordered lists
    def test_ordered_list_increments_starting_at_one(self):
        good = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(good), BlockType.ORDERED_LIST)

    def test_ordered_list_rejects_wrong_start_or_gap(self):
        self.assertEqual(block_to_block_type("2. two\n3. three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. one\n3. three"), BlockType.PARAGRAPH)

    def test_ordered_list_requires_space_after_dot(self):
        self.assertEqual(block_to_block_type("1.one\n2.two"), BlockType.PARAGRAPH)

    # Paragraph
    def test_paragraph_fallback(self):
        self.assertEqual(block_to_block_type("Just some text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("line 1\nline 2"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
