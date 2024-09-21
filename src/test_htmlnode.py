import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props = {"href":"https://www.boot.dev", "name":"link"})
        expected_result = " href=https://www.boot.dev name=link"

        test_result = node.props_to_html()

        self.assertEqual(test_result, expected_result)

    def test_repr_with_value(self):
        node = HTMLNode("<p>", "testing with value", None, {"href":"https://www.boot.dev", "name":"link"})
        expected_result = "HTMLNode(tag=<p>, value=testing with value, props= href=https://www.boot.dev name=link)"

        result = repr(node)

        self.assertEqual(result, expected_result)

    def test_repr_with_children(self):
        child_node = [HTMLNode("<p>", "child-node", None, {"href":"https://www.boot.dev", "name":"link"})]
        parent_node = HTMLNode("<p>", "testing with child-node", child_node, {"name":"parent"})
        
        expected_result = "HTMLNode(tag=<p>, value=testing with child-node, child=HTMLNode(tag=<p>, value=child-node, props= href=https://www.boot.dev name=link), props= name=parent)"
        
        result = repr(parent_node)

        self.assertEqual(result, expected_result)
    
    def test_repr_with_no_props(self):
        node = HTMLNode("<p>", "testing with value", None, None)
        expected_result = "HTMLNode(tag=<p>, value=testing with value)"

        result = repr(node)

        self.assertEqual(result, expected_result)

    def test_repr_with_no_tag(self):
        node = HTMLNode(None, "testing with value", None, {"name":"test"})
        expected_result = "HTMLNode(value=testing with value, props= name=test)"

        result = repr(node)

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()