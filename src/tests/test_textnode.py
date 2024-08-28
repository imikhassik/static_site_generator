import unittest

from src.nodes.textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)
    
    def test_dif_urls(self):
        node = TextNode("This is a text node", "bold", "http://example.com")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", "bold", "http://example.com")
        node2 = TextNode("This is a text node", "bold", "http://example.com")
        self.assertEqual(node, node2)


class TestConvertTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("This is a text node", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        text_node = TextNode("This is a text node", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        text_node = TextNode("This is a text node", "italic")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        text_node = TextNode("This is a text node", "code")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        text_node = TextNode("This is a text node", "link", "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": text_node.url})

    def test_image(self):
        text_node = TextNode("This is an image", "image", "https://boot.dev/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, text_node.text)
        self.assertEqual(html_node.props, {"src": text_node.url, "alt": text_node.text})

    def test_none(self):
        text_node = TextNode("This is a text node", "")
        self.assertRaisesRegex(Exception, "No text_type", text_node_to_html_node, text_node)


if __name__ == "__main__":
    unittest.main()
