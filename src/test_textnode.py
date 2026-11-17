import unittest
from textnode import TextNode, TextType, textnodes_to_htmlnodes
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("text node", TextType.BOLD)
        node2 = TextNode("text node", TextType.BOLD)
        self.assertEqual(node1, node2)

        node3 = TextNode("text node", TextType.TEXT)
        self.assertNotEqual(node1, node3)

        node4 = TextNode("link name", TextType.LINK, "http://localhost:8888")
        node5 = TextNode("link name", TextType.LINK)
        self.assertNotEqual(node4, node5)

class TestTextNodeToLeafNode(unittest.TestCase):
    def test_TEXT(self):
        text_node = TextNode("text", TextType.TEXT)
        converted_text_node = textnodes_to_htmlnodes(text_node)
        leaf_node = LeafNode(tag=None, value="text")
        self.assertEqual(str(leaf_node), str(converted_text_node))

    def test_bold(self):
        text_node = TextNode("text", TextType.BOLD)
        converted_text_node = textnodes_to_htmlnodes(text_node)
        leaf_node = LeafNode(tag="b", value="text")
        self.assertEqual(str(leaf_node), str(converted_text_node))

    def test_italic(self):
        text_node = TextNode("text", TextType.ITALIC)
        converted_text_node = textnodes_to_htmlnodes(text_node)
        leaf_node = LeafNode(tag="i", value="text")
        self.assertEqual(str(leaf_node), str(converted_text_node))

    def test_code(self):
        text_node = TextNode("function", TextType.CODE)
        converted_text_node = textnodes_to_htmlnodes(text_node)
        leaf_node = LeafNode(tag="code", value="function")
        self.assertEqual(str(leaf_node), str(converted_text_node))

    def test_link(self):
        text_node = TextNode("link", TextType.LINK, "url")
        converted_text_node = textnodes_to_htmlnodes(text_node)
        leaf_node = LeafNode(tag="a", value="link", props={"href": "url"})
        self.assertEqual(str(leaf_node), str(converted_text_node))

    def test_image(self):
        text_node = TextNode("picture_desc", TextType.IMAGE, "url")
        converted_text_node = textnodes_to_htmlnodes(text_node)
        leaf_node = LeafNode(tag="picture", value="", props={"src": "url", "alt": "picture_desc"})
        self.assertEqual(str(leaf_node), str(converted_text_node))
    
    def test_type_error(self):
        with self.assertRaises(TypeError):
            text_node = TextNode("a", "link", "url")
            textnodes_to_htmlnodes(text_node)

if __name__ == "__main__":
    unittest.main()