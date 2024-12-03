'''
    Unit tests for the TextNode class
'''
import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    '''
        Unit tests for the TextNode class
    '''
    def test_eq(self):
        '''
            Test the equality of two TextNode objects
        '''
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_url(self):
        '''
            Test the equality of two TextNode objects with different urls
        '''
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        node3 = TextNode("This is a text node", TextType.BOLD, "www.website.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node3)
    def test_text_type(self):
        '''
            Test the equality of two TextNode objects with different text types
        '''
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node2, node3)
        self.assertNotEqual(node, node2)
    def test_text(self):
        '''
            Test the equality of two TextNode objects with different text
        '''
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node.", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_to_html_normal(self):
        in_text_node = TextNode("This is some text", TextType.TEXT)
        out_leaf_node = in_text_node.text_node_to_html_node()
        self.assertIsInstance(out_leaf_node, LeafNode)
        self.assertEqual(out_leaf_node.value, in_text_node.text)
        self.assertIsNone(out_leaf_node.props)
        self.assertIsNone(out_leaf_node.children)
        self.assertIsNone(out_leaf_node.tag)

    def test_text_to_html_bold(self):
        in_text_node = TextNode("This is some text", TextType.BOLD)
        out_leaf_node = in_text_node.text_node_to_html_node()
        self.assertIsInstance(out_leaf_node, LeafNode)
        self.assertEqual(out_leaf_node.value, in_text_node.text)
        self.assertIsNone(out_leaf_node.props)
        self.assertIsNone(out_leaf_node.children)
        self.assertEqual(out_leaf_node.tag, "b")

    def test_text_to_html_italic(self):
        in_text_node = TextNode("This is some text", TextType.ITALIC)
        out_leaf_node = in_text_node.text_node_to_html_node()
        self.assertIsInstance(out_leaf_node, LeafNode)
        self.assertEqual(out_leaf_node.value, in_text_node.text)
        self.assertIsNone(out_leaf_node.props)
        self.assertIsNone(out_leaf_node.children)
        self.assertEqual(out_leaf_node.tag, "i")

    def test_text_to_html_code(self):
        in_text_node = TextNode("print('Hello world!)", TextType.CODE)
        out_leaf_node = in_text_node.text_node_to_html_node()
        self.assertIsInstance(out_leaf_node, LeafNode)
        self.assertEqual(out_leaf_node.value, in_text_node.text)
        self.assertIsNone(out_leaf_node.props)
        self.assertIsNone(out_leaf_node.children)
        self.assertEqual(out_leaf_node.tag, "code")

    def test_text_to_html_link(self):
        in_text_node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        out_leaf_node = in_text_node.text_node_to_html_node()
        self.assertIsInstance(out_leaf_node, LeafNode)
        self.assertEqual(out_leaf_node.value, in_text_node.text)
        self.assertEqual(out_leaf_node.props, {"href": in_text_node.url})
        self.assertIsNone(out_leaf_node.children)
        self.assertEqual(out_leaf_node.tag, "a")

    def test_text_to_html_link_no_url(self):
        in_text_node = TextNode("This is a link", TextType.LINK)
        with self.assertRaises(ValueError) as context:
            out_leaf_node = in_text_node.text_node_to_html_node()
        self.assertEqual(str(context.exception), "URL is required for LINK text type.")

    def test_text_to_html_link_empty_url(self):
        in_text_node = TextNode("This is a link", TextType.LINK, url="")
        with self.assertRaises(ValueError) as context:
            out_leaf_node = in_text_node.text_node_to_html_node()
        self.assertEqual(str(context.exception), "URL is required for LINK text type.")

    def test_text_to_html_link_valid_url(self):
        in_text_node = TextNode("This is a link", TextType.LINK, url="https://example.com")
        out_leaf_node = in_text_node.text_node_to_html_node()
        self.assertEqual(out_leaf_node.props, {"href": "https://example.com"})

    def test_text_to_image(self):
        in_text_node = TextNode("This is the alt text", TextType.IMAGE,
                                "https://example.com/image.png")
        out_leaf_node = in_text_node.text_node_to_html_node()
        self.assertIsInstance(out_leaf_node, LeafNode)
        self.assertEqual(out_leaf_node.props["alt"], in_text_node.text)
        self.assertEqual(out_leaf_node.props["src"], in_text_node.url)
        self.assertIsNone(out_leaf_node.children)
        self.assertEqual(out_leaf_node.tag, "img")
        self.assertEqual(out_leaf_node.value, "")

if __name__ == "__main__":
    unittest.main()
