import unittest
import copy
from textnode import *
from htmlnode import *
from text_conversion import *
from md_to_html import markdown_to_htmlnode


class TestTextConversion(unittest.TestCase):
    sep_to_type: list[tuple[str, TextType]] = [
        ("`", TextType.CODE),
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
    ]
    
    def test_split_nodes_del(self):
        text_node1 = TextNode("Here is **bold** text. Here `function`. With _italic_.", TextType.TEXT)
        bold_split_to_html = split_nodes_delimiter([text_node1], "**", TextType.BOLD)
        bold_res = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text. Here `function`. With _italic_.", TextType.TEXT)
        ]
        self.assertEqual(bold_split_to_html, bold_res)

        italic_split_to_html = split_nodes_delimiter([text_node1], "_", TextType.ITALIC)
        italic_res = [
            TextNode("Here is **bold** text. Here `function`. With ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(italic_split_to_html, italic_res)

        code_split_to_html = split_nodes_delimiter([text_node1], "`", TextType.CODE)
        code_res = [
            TextNode("Here is **bold** text. Here ", TextType.TEXT),
            TextNode("function", TextType.CODE),
            TextNode(". With _italic_.", TextType.TEXT)
        ]
        self.assertEqual(code_split_to_html, code_res)

        text_node2 = TextNode("Here is **bold** text. Here `code_function`. With _italic_.", TextType.TEXT)
        current_res = [text_node2]
        for sep_type in self.sep_to_type:
            current_res = split_nodes_delimiter(current_res, *sep_type)
        expected_res = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text. Here ", TextType.TEXT),
            TextNode("code_function", TextType.CODE),
            TextNode(". With ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(current_res, expected_res)

    def test_wrong_md_syntax_split_node_del(self):
        text_node = TextNode("Here is **bold** text. Here** `code_function`. With _italic_.", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([text_node], "**", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([text_node], "_", TextType.TEXT)

    def test_split_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        current = split_nodes_image([TextNode(text, TextType.TEXT)])
        expected = [TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")]
        self.assertEqual(current, expected)
    
        text2 = "text without image"
        current = split_nodes_image([TextNode(text2, TextType.TEXT)])
        expected = [TextNode(text2, TextType.TEXT)]
        self.assertEqual(current, expected)

        text3 = "![image](https://url.fr), and then ![image2](https://url2.fr) that's it"
        current = split_nodes_image([TextNode(text3, TextType.TEXT)])
        expected = [TextNode("image", TextType.IMAGE, "https://url.fr"),
                    TextNode(", and then ", TextType.TEXT),
                    TextNode("image2", TextType.IMAGE, "https://url2.fr"),
                    TextNode(" that's it", TextType.TEXT)]
        self.assertEqual(current, expected)

        text4 = "![image](https://url.fr), and then ![image](https://url.fr) that's it"
        current = split_nodes_image([TextNode(text4, TextType.TEXT)])
        expected = [TextNode("image", TextType.IMAGE, "https://url.fr"),
                    TextNode(", and then ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://url.fr"),
                    TextNode(" that's it", TextType.TEXT)]
        self.assertEqual(current, expected)

    def test_split_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        current = split_nodes_link([TextNode(text, TextType.TEXT)])
        expected = [TextNode("This is text with a link ", TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(current, expected)

        text2 = "[link](http://) and [link](http://)"
        current = split_nodes_link([TextNode(text2, TextType.TEXT)])
        expected = [TextNode("link", TextType.LINK, "http://"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "http://")]
        self.assertEqual(current, expected)

        text3 = "text without link"
        current = split_nodes_link([TextNode(text3, TextType.TEXT)])
        expected = [TextNode(text3, TextType.TEXT)]
        self.assertEqual(current, expected)

    def test_md_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        current = md_to_textnodes(text)
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
        self.assertEqual(current, expected)

        text2 = "`func_power(x: int, y: int) -> int: return x ** y` is a _simple_ **python function** learned [here](https://www.boot.dev)"
        current = md_to_textnodes(text2)
        expected = [
            TextNode("func_power(x: int, y: int) -> int: return x ** y", TextType.CODE),
            TextNode(" is a ", TextType.TEXT),
            TextNode("simple", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("python function", TextType.BOLD),
            TextNode(" learned ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertEqual(current,expected)

        text3 = "Simple text with nothing special."
        current = md_to_textnodes(text3)
        expected = [TextNode("Simple text with nothing special.", TextType.TEXT)]
        self.assertEqual(current, expected)

class TestLinkExtraction(unittest.TestCase):
    def test_link_extract(self):
        text = "see [documentation](https://docs.python.org/3/library/re.html#re.findall), and see also this [regex tester](https://regexr.com/) with this ![image](http://link.fr)"
        current_res = extract_markdown_links(text)
        expected_res = [
            ("documentation", "https://docs.python.org/3/library/re.html#re.findall"),
            ("regex tester", "https://regexr.com/")
        ]
        self.assertEqual(current_res, expected_res)

    def test_image_extract(self):
        text = "look this ![image](https://i.imgur.com/aKaOqIh.gif) or stop being my friend...\nalso check ![this one](https://i.imgur.com/fJRm4Vk.jpeg)! I found it [here](https://i.imgur.com)"
        current_res = extract_markdown_images(text)
        expected_res = [
            ("image", "https://i.imgur.com/aKaOqIh.gif"),
            ("this one", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(current_res, expected_res)

class TestMdToHTMLParentNode(unittest.TestCase):
    def test_code_block(self):
        md = """```
This text
Should remain _the same_
```"""
        html_node = markdown_to_htmlnode(md)
        html = html_node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This text\nShould remain _the same_</code></pre></div>",
    )

    def test_paragraphs(self):
        md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        html_node = markdown_to_htmlnode(md)
        html = html_node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_ul(self):
        md = """- This is
- a unsorted
- list"""
        html_node = markdown_to_htmlnode(md)
        html = html_node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is</li><li>a unsorted</li><li>list</li></ul></div>"
        )

    def test_ol(self):
        md = """1. This is
2. an ordered
3. list"""
        html_node = markdown_to_htmlnode(md)
        html = html_node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is</li><li>an ordered</li><li>list</li></ol></div>"
        )

    def test_headings(self):
        md = "# This is h1 with **bold** stuff inside"
        html_node = markdown_to_htmlnode(md)
        html = html_node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is h1 with <b>bold</b> stuff inside</h1></div>"
        )

        md = "###### This is h6 with **bold** stuff inside"
        html_node = markdown_to_htmlnode(md)
        html = html_node.to_html()
        self.assertEqual(
            html,
            "<div><h6>This is h6 with <b>bold</b> stuff inside</h6></div>"
        )

    def test_quote(self):
        md = "> quote with _space_"
        html_node = markdown_to_htmlnode(md)
        html = html_node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote with <i>space</i></blockquote></div>"
        )

        md = ">quote with _space_"
        html_node = markdown_to_htmlnode(md)
        html = html_node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote with <i>space</i></blockquote></div>"
        )

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """# titre h1

Et puis autre chose.

# autre titre h1"""
        self.assertEqual("titre h1", extract_title(md))

        md = "## md sans titre h1, c'est du h2..."
        with self.assertRaises(Exception):
            extract_title(md)

        
        
        