import re
from collections.abc import Callable
from textnode import *
from htmlnode import LeafNode, ParentNode


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        splitted_text = node.text.split(delimiter)
        if len(splitted_text) % 2 != 1:
            raise Exception(f"Error: Invalid Markdown syntax, closing delimiter '{delimiter}' not found")
        for i in range(len(splitted_text)):
            if i % 2 == 0 and splitted_text[i] != "":
                new_nodes.append(TextNode(splitted_text[i], TextType.TEXT))
            elif i % 2 != 0 and splitted_text[i] != "":
                new_nodes.append(TextNode(splitted_text[i], text_type))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r'\!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        md_images: tuple[str, str] = extract_markdown_images(node.text)
        if not md_images:
            new_nodes.append(node)
            continue
        first_image = True
        for md_image in md_images:
            if first_image:
                splitted_text = node.text.split(f"![{md_image[0]}]({md_image[1]})", 1)
                first_image = False
            else:
                splitted_text = splitted_text[-1].split(f"![{md_image[0]}]({md_image[1]})", 1)
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            new_nodes.append(TextNode(md_image[0], TextType.IMAGE, md_image[1]))
        if splitted_text[-1] != "":
            new_nodes.append(TextNode(splitted_text[-1], TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        md_links = extract_markdown_links(node.text)
        if len(md_links) == 0:
            new_nodes.append(node)
            continue
        first_link = True
        for md_link in md_links:
            if first_link:
                splitted_text = node.text.split(f"[{md_link[0]}]({md_link[1]})", 1)
                first_link = False
            else:
                splitted_text = splitted_text[-1].split(f"[{md_link[0]}]({md_link[1]})", 1)
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            new_nodes.append(TextNode(md_link[0], TextType.LINK, md_link[1]))
        if splitted_text[-1] != "":
            new_nodes.append(TextNode(splitted_text[-1], TextType.TEXT))
    return new_nodes

def md_to_textnodes(text: str) -> list[TextNode]:
    splitters = [
        split_nodes_image,
        split_nodes_link,
        ("`", TextType.CODE),
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC)
    ]

    text_nodes = [TextNode(text, TextType.TEXT)]
    for splitter in splitters:
        if isinstance(splitter, Callable):
            text_nodes = splitter(text_nodes)
        else:
            text_nodes = split_nodes_delimiter(text_nodes, *splitter)
    return text_nodes

def extract_title(markdown: str) -> str | None:
    try:
        title = re.search(r'(?<!#)# (.*)', markdown).group(1)
        return title
    except:
        raise Exception("no title found")