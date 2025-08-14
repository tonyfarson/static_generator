import unittest

from textnode import TextNode, TextType
from inline import split_nodes_image, split_nodes_link


class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        out = split_nodes_image([node])
        self.assertEqual(
            out,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "A ![one](u1) and ![two](u2) end",
            TextType.TEXT,
        )
        out = split_nodes_image([node])
        self.assertEqual(
            out,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "u1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "u2"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_links_single(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        out = split_nodes_link([node])
        self.assertEqual(
            out,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "Start [one](u1) mid [two](u2) end",
            TextType.TEXT,
        )
        out = split_nodes_link([node])
        self.assertEqual(
            out,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("one", TextType.LINK, "u1"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("two", TextType.LINK, "u2"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_non_text_nodes_pass_through(self):
        nodes = [
            TextNode("![img](u)", TextType.CODE),
            TextNode("[label](u)", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_image(nodes), nodes)
        self.assertEqual(split_nodes_link(nodes), nodes)

    def test_no_matches_returns_original_text_node(self):
        node = TextNode("nothing here", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])
        self.assertEqual(split_nodes_link([node]), [node])


if __name__ == "__main__":
    unittest.main()
