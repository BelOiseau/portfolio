import re
from htmlnode import *
from block_type import BlockType
from block_conversion import *
from text_conversion import md_to_textnodes
from textnode import *


def markdown_to_htmlnode(markdown: str) -> ParentNode:
    block_type_to_tag = {
        BlockType.PARAGRAPH: "p",
        BlockType.CODE: "pre",
        BlockType.HEADING: ["h1", "h2", "h3", "h4", "h5", "h6"],
        BlockType.QUOTE: "blockquote",
        BlockType.UL: "ul",
        BlockType.OL: "ol"
    }
    
    md_blocks = md_to_blocks(markdown)
    childrens = []
    for md_block in md_blocks:
        block_type = block_to_block_type(md_block)

        if block_type == BlockType.HEADING:
            header_size = md_block.count('#', 0, 6) - 1
            tag = block_type_to_tag[block_type][header_size]
        else:
            tag = block_type_to_tag[block_type]

        childrens.append(ParentNode(tag, text_to_children(md_block, block_type)))
    return ParentNode("div", childrens)

def text_to_children(markdown_block: str, block_type: BlockType) ->list[HTMLNode]:
    if block_type in [BlockType.UL, BlockType.OL]:
        if block_type == BlockType.UL:
            lines = markdown_block[2:].split("\n- ")
        else:
            lines = re.findall(r'(?<=\d\. ).*', markdown_block)

        grand_childrens = []
        for line in lines:
            text_nodes = md_to_textnodes(line)
            childrens = []
            for text_node in text_nodes:
                childrens.append(textnodes_to_htmlnodes(text_node))
            grand_childrens.append(ParentNode("li", childrens))
        return grand_childrens

    if block_type == BlockType.CODE:
        inner_text = re.search(r'(?<=^`{3}\n)[\w\W]+(?=\n`{3})', markdown_block)
        return [LeafNode("code", inner_text[0])]

    if block_type == BlockType.HEADING:
        offset = markdown_block.count('#', 0, 6) + 1
        clean_md = markdown_block[offset:]
    elif block_type == BlockType.QUOTE:
        lines = re.findall(r'(?<=>) ?(.*)', markdown_block)
        clean_md = " ".join(lines)
    else:
        clean_md = markdown_block.replace("\n", " ")
    text_nodes = md_to_textnodes(clean_md)

    childrens = []
    for text_node in text_nodes:
        childrens.append(textnodes_to_htmlnodes(text_node))
    return childrens







