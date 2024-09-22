import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq_url_none(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)
    
    def test_eq_all_properties(self):
        node = TextNode("This is a text node", text_type_bold, "localhost:8008")
        node2 = TextNode("This is a text node", text_type_bold, "localhost:8008")
        self.assertEqual(node == node2, True)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", text_type_italic, "localhost:8008")
        node2 = TextNode("This is a text node", text_type_bold, "localhost:8008")
        self.assertEqual(node == node2, False)

    def test_not_eq_text(self):
        node = TextNode("This is a text node of course", text_type_bold, "localhost:8008")
        node2 = TextNode("This is a text node", text_type_bold, "localhost:8008")
        self.assertEqual(node == node2, False)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", text_type_bold, "localhost:8888")
        node2 = TextNode("This is a text node", text_type_bold, "localhost:8008")
        self.assertEqual(node == node2, False)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        node2 = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", text_type_image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", text_type_bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


if __name__ == "__main__":
    unittest.main()