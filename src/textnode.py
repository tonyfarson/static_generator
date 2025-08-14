from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: "TextNode") -> LeafNode:
    """
    Convert a TextNode to a LeafNode based on the TextType.

    - TEXT   -> LeafNode(None, text)
    - BOLD   -> LeafNode("b", text)
    - ITALIC -> LeafNode("i", text)
    - CODE   -> LeafNode("code", text)
    - LINK   -> LeafNode("a", text, {"href": url})            (url required)
    - IMAGE  -> LeafNode("img", "", {"src": url, "alt": text}) (url required)
    """
    ttype = text_node.text_type
    text = text_node.text
    url = text_node.url

    if ttype == TextType.TEXT:
        return LeafNode(None, text)
    if ttype == TextType.BOLD:
        return LeafNode("b", text)
    if ttype == TextType.ITALIC:
        return LeafNode("i", text)
    if ttype == TextType.CODE:
        return LeafNode("code", text)
    if ttype == TextType.LINK:
        if not url:
            raise ValueError("LINK TextNode requires a url for href")
        return LeafNode("a", text, {"href": url})
    if ttype == TextType.IMAGE:
        if not url:
            raise ValueError("IMAGE TextNode requires a url for src")
        return LeafNode("img", "", {"src": url, "alt": text})

    raise ValueError(f"Unsupported TextType: {ttype}")
