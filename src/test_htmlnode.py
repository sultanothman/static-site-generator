import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    #########  HTMLNode tests  #########
    def test_props_to_html_htmlnode(self):
        node = HTMLNode(props = {"href":"https://www.boot.dev", "name":"link"})
        expected_result = " href=\"https://www.boot.dev\" name=\"link\""

        result = node.props_to_html()

        self.assertEqual(expected_result, result)

    def test_repr_with_value_htmlnode(self):
        node = HTMLNode("<p>", "testing with value", None, {"href":"https://www.boot.dev", "name":"link"})
        expected_result = "HTMLNode(tag=<p>, value=testing with value, props= href=\"https://www.boot.dev\" name=\"link\")"

        result = repr(node)

        self.assertEqual(expected_result, result)

    def test_repr_with_children_htmlnode(self):
        child_node = [HTMLNode("<p>", "child-node", None, {"href":"https://www.boot.dev", "name":"link"})]
        parent_node = HTMLNode("<p>", "testing with child-node", child_node, {"name":"parent"})
        
        expected_result = "HTMLNode(tag=<p>, value=testing with child-node, child=HTMLNode(tag=<p>, value=child-node, props= href=\"https://www.boot.dev\" name=\"link\"), props= name=\"parent\")"
        
        result = repr(parent_node)

        self.assertEqual(expected_result, result)
    
    def test_repr_with_no_props_htmlnode(self):
        node = HTMLNode("<p>", "testing with value", None, None)
        expected_result = "HTMLNode(tag=<p>, value=testing with value)"

        result = repr(node)

        self.assertEqual(expected_result, result)

    def test_repr_with_no_tag_htmlnode(self):
        node = HTMLNode(None, "testing with value", None, {"name":"test"})
        expected_result = "HTMLNode(value=testing with value, props= name=\"test\")"

        result = repr(node)

        self.assertEqual(expected_result, result)

    #########  LeafNode tests  #########
    def test_all_arguments_leafnode(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        
        expected_result = "<a href=\"https://www.google.com\">Click me!</a>"

        result = node.to_html()

        self.assertEqual(expected_result, result)
        
    def test_no_tag_leafnode(self):
        node = LeafNode(None, "text of test", {"name":"test"})

        expected_result = "text of test"

        result = node.to_html()

        self.assertEqual(expected_result, result)

    def test_value_only_leafnode(self):
        node = LeafNode(None, "text of test")

        expected_result = "text of test"

        result = node.to_html()

        self.assertEqual(expected_result, result)

    def test_no_props_leafnode(self):
        node = LeafNode("p", "this is a paragraph")

        expected_result = "<p>this is a paragraph</p>"

        result = node.to_html()

        self.assertEqual(result, expected_result)

    def test_no_value_leafnode(self):
        node = LeafNode("b", None, {"name":"should fail"})

        with self.assertRaises(ValueError) as context : node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no value")

    #########  ParentNode tests  #########
    def test_all_arguments_parentnode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"name":"parent"}
        )
        
        expected_result = "<p name=\"parent\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        result = node.to_html()

        self.assertEqual(result, expected_result)
        
    def test_no_props_parentnode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        
        expected_result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        result = node.to_html()

        self.assertEqual(result, expected_result)

    def test_no_tag_parentnode(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        with self.assertRaises(ValueError) as context: node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: tag is mandatory")

    def test_no_children_parentnode(self):
        node = ParentNode(
            "p",
            None,
        )

        with self.assertRaises(ValueError) as context: node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: children are mandatory")

    def test_nested_parent_nodes_parentnode(self):
        node = ParentNode(
            "ul",
            [
                ParentNode(
                    "l",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                    ]
                ),
                LeafNode("l", "part of list")
            ]
        )

        expected_result = "<ul><l><b>Bold text</b>Normal text<i>italic text</i></l><l>part of list</l></ul>"

        result = node.to_html()

        self.assertEqual(expected_result, result)

if __name__ == "__main__":
    unittest.main()