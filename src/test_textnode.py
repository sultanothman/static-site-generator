import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq_url_none(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_eq_all_properties(self):
        node = TextNode("This is a text node", "bold", "localhost:8008")
        node2 = TextNode("This is a text node", "bold", "localhost:8008")

        self.assertEqual(node == node2, True)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", "italic", "localhost:8008")
        node2 = TextNode("This is a text node", "bold", "localhost:8008")

        self.assertEqual(node == node2, False)

    def test_not_eq_text(self):
        node = TextNode("This is a text node of course", "bold", "localhost:8008")
        node2 = TextNode("This is a text node", "bold", "localhost:8008")

        self.assertEqual(node == node2, False)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", "bold", "localhost:8888")
        node2 = TextNode("This is a text node", "bold", "localhost:8008")

        self.assertEqual(node == node2, False)

if __name__ == "__main__":
    unittest.main()