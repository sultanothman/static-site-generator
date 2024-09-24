import unittest

from inline_makrdown import split_nodes_delimiter
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

class TestHTMLNode(unittest.TestCase):
    def test_spliter_one_node_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)

        expected_result = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]

        result = split_nodes_delimiter([node], '`', text_type_code)

        for i in range(len(result)):
            self.assertEqual(expected_result[i], result[i])

    def test_spliter_one_node_italic(self):
        node = TextNode("This is text with a *italic block* word", text_type_text)

        expected_result = [
            TextNode("This is text with a ", text_type_text),
            TextNode("italic block", text_type_italic),
            TextNode(" word", text_type_text),
        ]

        result = split_nodes_delimiter([node], '*', text_type_italic)

        for i in range(len(result)):
            self.assertEqual(expected_result[i], result[i])

    def test_spliter_one_node_bold(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)

        expected_result = [
            TextNode("This is text with a ", text_type_text),
            TextNode("bold block", text_type_bold),
            TextNode(" word", text_type_text),
        ]

        result = split_nodes_delimiter([node], '**', text_type_bold)

        for i in range(len(result)):
            self.assertEqual(expected_result[i], result[i])

    def test_spliter_tow_nodes(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)
        node2 = TextNode("Second text with a **bold block** words", text_type_text)

        expected_result = [
            TextNode("This is text with a ", text_type_text),
            TextNode("bold block", text_type_bold),
            TextNode(" word", text_type_text),
            TextNode("Second text with a ", text_type_text),
            TextNode("bold block", text_type_bold),
            TextNode(" words", text_type_text),
        ]

        result = split_nodes_delimiter([node, node2], '**', text_type_bold)

        for i in range(len(result)):
            self.assertEqual(expected_result[i], result[i])

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes,
        )