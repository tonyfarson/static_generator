import unittest

from textnode import TextNode, TextType
from inline import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_simple(self):
        node = TextNode("This has a `code` span.", TextType.TEXT)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            out,
            [
                TextNode("This has a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" span.", TextType.TEXT),
            ],
        )

    def test_bold_double_asterisk(self):
        node = TextNode("Here is **bold** text.", TextType.TEXT)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.TEXT),
            ],
        )

    def test_multiple_italic_underscores(self):
        node = TextNode("A _one_ and _two_ example.", TextType.TEXT)
        out = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            out,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("one", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.ITALIC),
                TextNode(" example.", TextType.TEXT),
            ],
        )

    def test_mixed_input_nodes(self):
        # The second node is already BOLD; it should pass through unchanged
        nodes = [
            TextNode("pre _it_", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode(" _post_", TextType.TEXT),
        ]
        out = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            out,
            [
                TextNode("pre ", TextType.TEXT),
                TextNode("it", TextType.ITALIC),
                TextNode("already bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("post", TextType.ITALIC),
            ],
        )

    def test_unmatched_raises(self):
        node = TextNode("Broken **bold here", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_leading_and_trailing(self):
        node = TextNode("**bold**", TextType.TEXT)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(out, [TextNode("bold", TextType.BOLD)])

    def test_empty_segments_are_skipped(self):
        # e.g., "word****word" should not create empty nodes for the middle
        node = TextNode("word****word", TextType.TEXT)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("word", TextType.TEXT),
                TextNode("word", TextType.TEXT),  # because "" (bold) "" => skipped
            ],
        )


if __name__ == "__main__":
    unittest.main()
