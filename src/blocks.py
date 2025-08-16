# src/blocks.py
import re
from enum import Enum
from typing import List

# ---------- Lesson 1: block splitter ----------

def markdown_to_blocks(markdown: str) -> List[str]:
    # Split a Markdown document into logical blocks.
    # - Blocks are separated by one or more blank lines.
    # - Trim whitespace on each block and each line inside the block.
    # - Remove empty results.
    if not markdown:
        return []

    text = markdown.replace("\r\n", "\n").strip()
    if not text:
        return []

    parts = re.split(r"\n\s*\n+", text)

    blocks: List[str] = []
    for part in parts:
        lines = [ln.strip() for ln in part.split("\n")]
        cleaned = "\n".join(ln for ln in lines if ln != "")
        if cleaned:
            blocks.append(cleaned)

    return blocks


# ---------- Lesson 2: block types ----------

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    # Classify a stripped markdown block as one of the supported types.
    # Rules:
    #   - Heading: single line; 1–6 '#' then a space and text.
    #   - Code: first line is exactly ``` and last line is exactly ```.
    #   - Quote: every line starts with '>'.
    #   - Unordered list: every line starts with '- ' (dash + space).
    #   - Ordered list: each line 'N. ' where N starts at 1 and increments by 1.
    #   - Otherwise: paragraph.
    if not block:
        return BlockType.PARAGRAPH

    lines = block.split("\n")

    # Code block: opening and closing fences must be exactly ```
    if len(lines) >= 2 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE

    # Heading: exactly one line, 1-6 '#' then a space and text
    if len(lines) == 1 and re.match(r"^(#{1,6})\s+.+$", lines[0]) is not None:
        return BlockType.HEADING

    # Quote: every line begins with '>' (space optional)
    if all(re.match(r"^>.*$", ln) is not None for ln in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- " (dash + space) at column 0
    if all(re.match(r"^- .+$", ln) is not None for ln in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: each line 'N. ' with N starting at 1 and incrementing by 1
    nums: List[int] = []
    for ln in lines:
        m = re.match(r"^(\d+)\.\s+.+$", ln)
        if not m:
            nums = []
            break
        nums.append(int(m.group(1)))

    if nums and nums[0] == 1 and all(nums[i] == nums[i - 1] + 1 for i in range(1, len(nums))):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
