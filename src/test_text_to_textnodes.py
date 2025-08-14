import unittest

from textnode import TextNode, TextType
from inline import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_example_from_prompt(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        out = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(out, expected)

    def test_simple_mixture(self):
        text = "Start **B** _I_ `C` [L](u) ![A](img)"
        out = text_to_textnodes(text)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("B", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("I", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("C", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("L", TextType.LINK, "u"),
            TextNode(" ", TextType.TEXT),
            TextNode("A", TextType.IMAGE, "img"),
        ]
        self.assertEqual(out, expected)


if __name__ == "__main__":
    unittest.main()
