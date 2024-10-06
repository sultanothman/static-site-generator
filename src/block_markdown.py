import re
from textnode import *

block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"
block_type_paragraph = "paragraph"

def markdown_to_blocks(markdown):
    blocks = re.split(r"\n\s*\n", markdown)
    for i, block in enumerate(blocks):
        striped_block = block.strip()
        blocks[i] = striped_block
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* ") :
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block[0].isdigit() and block[1] == '.':
        for line in lines:
            if not block[0].isdigit() and not block[1] == '.':
                return block_type_paragraph
        return block_type_olist
    return block_type_paragraph


