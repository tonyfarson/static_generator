from typing import List
from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(
    old_nodes: List[TextNode],
    delimiter: str,
    text_type: TextType,
) -> List[TextNode]:
    """
    Split TextType.TEXT nodes by a given delimiter and convert delimited segments
    into the provided text_type. Non-TEXT nodes are passed through unchanged.

    Example:
      "This is a **bold** word"
      -> [TEXT("This is a "), BOLD("bold"), TEXT(" word")]

    Rules:
      - If the number of delimiters is odd (i.e., parts is even), raise ValueError.
      - Empty segments are skipped (no zero-length nodes).
    """
    new_nodes: List[TextNode] = []

    for node in old_nodes:
        # Only split plain TEXT nodes.
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # Even number of parts => unmatched delimiter (invalid markdown)
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid markdown: unmatched delimiter {delimiter!r} in {node.text!r}"
            )

        # Even indices = plain text, odd indices = delimited (target) text
        for idx, segment in enumerate(parts):
            if segment == "":
                continue  # skip empty pieces
            if idx % 2 == 0:
                new_nodes.append(TextNode(segment, TextType.TEXT))
            else:
                new_nodes.append(TextNode(segment, text_type))

    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    For each TEXT node, split out markdown images:
      ![alt](url)  ->  TEXT(before), IMAGE(alt,url), TEXT(after)
    Non-TEXT nodes are passed through unchanged.
    Empty TEXT segments are not appended.
    """
    new_nodes: List[TextNode] = []

    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)
        if not matches:
            new_nodes.append(node)
            continue

        # Process each image match in order, splitting the remaining text each time
        for alt, url in matches:
            token = f"![{alt}]({url})"
            before, *rest = text.split(token, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = rest[0] if rest else ""

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    For each TEXT node, split out markdown links:
      [label](url)  ->  TEXT(before), LINK(label,url), TEXT(after)
    Non-TEXT nodes are passed through unchanged.
    Empty TEXT segments are not appended.
    """
    new_nodes: List[TextNode] = []

    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)
        if not matches:
            new_nodes.append(node)
            continue

        for label, url in matches:
            token = f"[{label}]({url})"
            before, *rest = text.split(token, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(label, TextType.LINK, url))
            text = rest[0] if rest else ""

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    """
    Convert a raw markdown string into a list of TextNodes by applying, in order:
      1) images
      2) links
      3) code spans (`...`)
      4) bold (**...**)
      5) italics (_..._)
    """
    nodes: List[TextNode] = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes
