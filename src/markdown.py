# src/markdown.py
import re
from typing import List
from htmlnode import ParentNode, LeafNode, HTMLNode
from blocks import markdown_to_blocks, block_to_block_type, BlockType
from inline import text_to_textnodes
from textnode import text_node_to_html_node


def _text_to_children(text: str) -> List[HTMLNode]:
    # Convert inline-markdown text into a list of HTMLNodes
    tnodes = text_to_textnodes(text)
    return [text_node_to_html_node(t) for t in tnodes]


def _paragraph_node(block: str) -> ParentNode:
    # Join wrapped lines inside a paragraph with spaces
    text = " ".join(block.split("\n"))
    return ParentNode("p", _text_to_children(text))


def _heading_node(block: str) -> ParentNode:
    m = re.match(r"^(#{1,6})\s+(.*)$", block)
    if not m:
        # Fallback to paragraph if somehow malformed
        return _paragraph_node(block)
    level = len(m.group(1))
    text = m.group(2).strip()
    return ParentNode(f"h{level}", _text_to_children(text))


def _quote_node(block: str) -> ParentNode:
    # Strip leading '>' (and optional space) from each line, then join with spaces
    lines = [re.sub(r"^>\s?", "", ln) for ln in block.split("\n")]
    text = " ".join(lines)
    return ParentNode("blockquote", _text_to_children(text))


def _ul_node(block: str) -> ParentNode:
    # Unordered list: each line begins with "- "
    items: List[ParentNode] = []
    for ln in block.split("\n"):
        item_text = re.sub(r"^- ", "", ln, count=1)
        items.append(ParentNode("li", _text_to_children(item_text)))
    return ParentNode("ul", items)


def _ol_node(block: str) -> ParentNode:
    # Ordered list: each line begins with "<num>. "
    items: List[ParentNode] = []
    for ln in block.split("\n"):
        item_text = re.sub(r"^\d+\.\s+", "", ln, count=1)
        items.append(ParentNode("li", _text_to_children(item_text)))
    return ParentNode("ol", items)


def _code_node(block: str) -> ParentNode:
    # Do NOT parse inline markdown inside code blocks
    lines = block.split("\n")
    # Remove opening and closing ``` fences; preserve internal newlines plus a trailing newline
    content = "\n".join(lines[1:-1]) + "\n"
    code_leaf = LeafNode("code", content)
    return ParentNode("pre", [code_leaf])


def markdown_to_html_node(markdown: str) -> ParentNode:
    # Convert a full Markdown document into a single root <div> with child nodes
    blocks = markdown_to_blocks(markdown)
    children: List[HTMLNode] = []
    for block in blocks:
        btype = block_to_block_type(block)
        if btype == BlockType.PARAGRAPH:
            children.append(_paragraph_node(block))
        elif btype == BlockType.HEADING:
            children.append(_heading_node(block))
        elif btype == BlockType.CODE:
            children.append(_code_node(block))
        elif btype == BlockType.QUOTE:
            children.append(_quote_node(block))
        elif btype == BlockType.UNORDERED_LIST:
            children.append(_ul_node(block))
        elif btype == BlockType.ORDERED_LIST:
            children.append(_ol_node(block))
        else:
            children.append(_paragraph_node(block))
    return ParentNode("div", children)
