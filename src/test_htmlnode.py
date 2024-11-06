import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        print(node)

    def test_props2(self):
        node2 = HTMLNode(props={"href": "https://google.com", "target": "_help"})
        print(node2)
    
    def test_props3(self):
        node3 = HTMLNode(props={"href": "https://boot.dev.com", "target": "_cool"})
        print(node3)

class TestLeafNode(unittest.TestCase):
    def test_leaf(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
    
    def test_leaf2(self):
        node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_with_no_value_raises_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode("b", None)
            node.to_html()

if __name__ == "__main__":
    unittest.main()