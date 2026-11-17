import re
from block_type import BlockType


def md_to_blocks(markdown: str) -> list[str]:
    raw_md_blocks = markdown.strip().split("\n\n")
    striped_md_blocks = []
    for md_blocks in raw_md_blocks:
        striped_md_blocks.append(md_blocks.strip())
    return striped_md_blocks

def block_to_block_type(block: str) -> BlockType:
    res = re.search(r'^#{1,6} [\S]+', block)
    if res is not None:
        return BlockType.HEADING
    
    res = re.search(r'^> ?[\S]', block)
    if res is not None:
        return BlockType.QUOTE

    res = re.search(r'^`{3}\n[\w\W]+\n`{3}', block)
    if res is not None:
        return BlockType.CODE

    res = re.findall(r'(?<![^\n])- ', block)
    if res is not None and len(res) == len(block.split("\n")):
        return BlockType.UL
    
    res = re.findall(r'(?<![^\n])\d\. ', block)
    if res is not None and len(res) == len(block.split("\n")):
        return BlockType.OL

    return BlockType.PARAGRAPH
    
    
    