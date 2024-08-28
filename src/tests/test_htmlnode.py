from unittest import TestCase
from src.nodes.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(TestCase):
    def test_props_to_html_1(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        result = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), result)

    def test_props_to_html_2(self):
        props = {
            "prop": "value",
        }
        result = ' prop="value"'
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), result)

    def test_props_to_html_3(self):
        props = {
            "prop1": "value1",
            "prop2": "value2",
        }
        result = ' prop1="value1" prop2="value2"'
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), result)
    

class TestLeafNode(TestCase):
    def test_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
    
    def test_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_no_value(self):
        node = LeafNode("p")
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag(self):
        value = "This is a paragraph of text."
        node = LeafNode(value=value)
        self.assertEqual(node.to_html(), value)
    
    def test_with_kwargs(self):
        tag = "a"
        value = "Click me!"
        props = {"href": "https://www.google.com"}
        node = LeafNode(children=None, props=props, value=value, tag=tag)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


class TestParentNode(TestCase):
    def test_no_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
    
    def test_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {'style': 'text-align:right'}
        )
        self.assertEqual(
            node.to_html(),
            '<p style="text-align:right"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
            )

    def test_nested_nodes(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "ol",
                    [
                        LeafNode("li", "Coffee"),
                        LeafNode("li", "Tea"),
                        LeafNode("li", "Milk"),
                    ],
                ),
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "Coffee"),
                        LeafNode("li", "Tea"),
                        LeafNode("li", "Milk"),
                    ],
                )
            ]
        )
        self.assertEqual(
            node.to_html(), 
            '<p><ol><li>Coffee</li><li>Tea</li><li>Milk</li></ol><ul><li>Coffee</li><li>Tea</li><li>Milk</li></ul></p>'
            )

    def test_no_children(self):
        node = ParentNode("p")
        self.assertRaisesRegex(
            ValueError, 
            'Parent node must have children', 
            node.to_html
            )

    def test_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertRaises(ValueError, node.to_html)

    def test_nested_nodes_with_props(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "ol",
                    [
                        LeafNode("li", "Coffee"),
                        LeafNode("li", "Tea"),
                        LeafNode("li", "Milk"),
                    ],
                ),
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "Coffee"),
                        LeafNode("li", "Tea"),
                        LeafNode("li", "Milk"),
                    ],
                    {
                        "style": "list-style-type:upper-roman"
                    }
                )
            ],
            {
                'style': 'text-align:right'
            }
        )
        self.assertEqual(
            node.to_html(), 
            '<p style="text-align:right"><ol><li>Coffee</li><li>Tea</li><li>Milk</li></ol><ul style="list-style-type:upper-roman"><li>Coffee</li><li>Tea</li><li>Milk</li></ul></p>'
            )

