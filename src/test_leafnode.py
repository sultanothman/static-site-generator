import unittest

from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_all_arguments(self):
        leafnode = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        
        expected_result = "<a href=\"https://www.google.com\">Click me!</a>"

        result = leafnode.to_html()

        self.assertEqual(result, expected_result)
        
    def test_no_tag(self):
        leafnode = LeafNode(None, "text of test", {"name":"test"})

        expected_result = "text of test"

        result = leafnode.to_html()

        self.assertEqual(result, expected_result)

    def test_no_props(self):
        Leafnode = LeafNode("p", "this is a paragraph")

        expected_result = "<p>this is a paragraph</p>"

        result = Leafnode.to_html()

        self.assertEqual(result, expected_result)

    def test_no_value(self):
        leafnode = LeafNode("b", None, {"name":"should fail"})

        self.assertRaises(ValueError, leafnode.to_html)