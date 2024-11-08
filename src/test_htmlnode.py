import unittest

from htmlnode import *
from textnode import *


class TestHTMLNode(unittest.TestCase):
    pass

class TestParentNode(unittest.TestCase):
    def test_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
         
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

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
        with self.assertRaises(ValueError) as e:
            exception = e
            self.assertEqual(node.to_html(), exception)
        self.assertIsNone(node.tag)

    def test_double_parents(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "b",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Noraml text"),
                    ]
                ),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text")
            ]
        )
        self.assertEqual(node.to_html(), "<p><b><b>Bold text</b>Noraml text</b><i>Italic text</i>Normal text</p>")
    
    def test_no_parents(self):
        node = ParentNode("p", [])
        with self.assertRaises(ValueError) as e:
            exception = e
            self.assertEqual(node.to_html(), exception)

    def test_super_nest(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold", {"href": 'https://boot.dev.com'}),
                                LeafNode(None, "Normal text")
                            ]
                        ),
                        LeafNode("i", "Italic", {"href": 'https://google.come'})
                    ]
                ),
                LeafNode("c", "Code"),
                LeafNode(None, "Normal text")
            ]
        )
        self.assertEqual(node.to_html(), '<p><p><p><b href="https://boot.dev.com">Bold</b>Normal text</p><i href="https://google.come">Italic</i></p><c>Code</c>Normal text</p>')
    
    def test_no_tag_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "Normal text "),
                LeafNode(None, "This is a test "),
                LeafNode(None, "None")
            ]
        )
        self.assertEqual(node.to_html(), "<p>Normal text This is a test None</p>")

class TestTransformation(unittest.TestCase):
    def test_Normal(self):
        node = TextNode("Nothing here", TextType.NORMAL)
        Html = text_node_to_html_node(node)
        self.assertEqual(Html.to_html(), "<>Nothing here</>")
    
    def test_Bold(self):
        node = TextNode("im bold",TextType.BOLD)
        Html = text_node_to_html_node(node)
        self.assertEqual(Html.to_html(), "<b>im bold</b>")


if __name__ == "__main__":
    unittest.main()