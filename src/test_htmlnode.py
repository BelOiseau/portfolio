import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        htmlnode1 = HTMLNode("p", "content")
        self.assertEqual(htmlnode1.tag, "p")
        self.assertEqual(htmlnode1.value, "content")

        props = {"class": "article-content"}
        htmlnode2 = HTMLNode("div", children=[htmlnode1], props=props)
        self.assertEqual(htmlnode2.tag, "div")
        self.assertEqual(htmlnode2.children, [htmlnode1])
        self.assertEqual(htmlnode2.props, props)

        htmlnode3 = HTMLNode()
        self.assertEqual(htmlnode3.tag, None)
        self.assertEqual(htmlnode3.value, None)
        self.assertEqual(htmlnode3.children, None)
        self.assertEqual(htmlnode3.props, None)
    
    def test_repr(self):
        htmlnode1 = HTMLNode("a", "link to sub", props={"href": "http:localhost:8888/sub", "class": "red-link"})
        htmlnode2 = HTMLNode("li", children=[htmlnode1])
        htmlnode3 = HTMLNode("ul", children=[htmlnode2], props={"class": "link-list"})
        htmlnode3_repr = "tag: 'ul', value: 'None', children: [tag: 'li', value: 'None', children: [tag: 'a', value: 'link to sub', children: None, props: {'href': 'http:localhost:8888/sub', 'class': 'red-link'}], props: None], props: {'class': 'link-list'}"
        self.assertEqual(str(htmlnode3), htmlnode3_repr)

    def test_props_to_html(self):
        htmlnode = HTMLNode("button", props={"class": "change-style-button", "type": "button"})
        expected_output = f' class="change-style-button" type="button"'
        self.assertEqual(htmlnode.props_to_html(), expected_output)
    
    def test_to_hmtl(self):
        htmlnode = HTMLNode("p", "paragraph")
        with self.assertRaises(NotImplementedError):
            htmlnode.to_html()


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            wrong_leaf = LeafNode()


        with self.assertRaises(ValueError):
            wrong_leaf = LeafNode(tag=None, value=None)
            wrong_leaf.to_html()
        
        props = {"class": "leaf"}
        good_leaf = LeafNode("b", "bold", props)
        self.assertEqual(good_leaf.tag, "b")
        self.assertEqual(good_leaf.value, "bold")
        self.assertEqual(good_leaf.props, props)
        no_props_leaf = LeafNode("i", "italic")
        self.assertEqual(no_props_leaf.props, None)


    def test_to_html_and_repr(self):
        props = {"href": "http://localhost:8888"}
        leaf = LeafNode("a", "click me", props)
        expected_output = f"tag: 'a', value: 'click me', props: {props}"
        self.assertEqual(str(leaf), expected_output)
        self.assertEqual(leaf.to_html(), '<a href="http://localhost:8888">click me</a>')

        leaf2 = LeafNode(tag=None, value="content")
        self.assertEqual(leaf2.to_html(), "content")

        leaf3 = LeafNode("p", "content")
        self.assertEqual(leaf3.to_html(), "<p>content</p>")

class TestParentNode(unittest.TestCase):
    def test_init(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        props = {"class": "parent"}
        with self.assertRaises(ValueError):
            wrong_node = ParentNode(tag=None, children=None, props=props)
            wrong_node.to_html()

        with self.assertRaises(ValueError):
            wrong_node = ParentNode(tag="div", children=None, props=props)
            wrong_node.to_html()
        
        good_node = ParentNode("div", children, props)
        self.assertEqual(good_node.tag, "div")
        self.assertEqual(good_node.children, children)
        self.assertEqual(good_node.props, props)
        good_node2 = ParentNode("div", children)
        self.assertEqual(good_node2.props, None)

    def test_to_html_with_parent(self):
        children = [
            ParentNode(
                "table",
                [
                    LeafNode("caption", "user table"),
                    ParentNode("tr", [LeafNode("td", "id"), LeafNode("td", "name")]),
                    ParentNode("tr", [LeafNode("td", "1"), LeafNode("td", "Nathan")]),
                ],
                {"class": "simple-table"}
            )
        ]

        props = {"class": "parent"}
        parent_node = ParentNode("div", children, props)
        self.assertEqual(
            parent_node.to_html(),
            '<div class="parent"><table class="simple-table"><caption>user table</caption><tr><td>id</td><td>name</td></tr><tr><td>1</td><td>Nathan</td></tr></table></div>'
        )

    def test_to_html_without_parent(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        parent_node = ParentNode("p", children)
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

        
