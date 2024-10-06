import unittest

from inline_makrdown import *
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

    def test_markdown_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        result = extract_markdown_images(text)
        self.assertListEqual(expected_result, result)

    def test_image_markdown_invalid(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![haha]()"
        with self.assertRaises(ValueError) as context: extract_markdown_images(text)
        self.assertEqual(str(context.exception), "Inavlid markdown - missing url")

    def test_markdown_extract_Links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"        
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        result = extract_markdown_links(text)
        self.assertListEqual(expected_result, result)

    def test_link_markdown_invalid(self):
        text = "This is text with a link [to boot dev]() and [to youtube](https://www.youtube.com/@bootdotdev)"
        with self.assertRaises(ValueError) as context: extract_markdown_links(text)
        self.assertEqual(str(context.exception), "Invalid markdown - missing link")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )

    def test_split_multipule_markdowns(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        result = text_to_textnodes(text)

        expected_result = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]

        self.assertListEqual(expected_result, result)

    def test_split_multipule_markdowns_bold_only(self):
        text = "This is **text** with bold only"

        result = text_to_textnodes(text)

        expected_result = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with bold only", text_type_text),
        ]

        self.assertListEqual(expected_result, result)