'''
    Unit tests for the TextNode class
'''
import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()
