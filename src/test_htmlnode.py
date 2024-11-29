'''
    Unit test for htmlnode.py
'''

import unittest
from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    '''
        Unit test for htmlnode.py
    '''
    def test_default_constructor(self):
        '''
            Test the default constructor. All fields should None
        '''
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_equality_with_value_only(self):
        '''
            Test the constructor with only the tag and its value
        '''
        node = HTMLNode(tag="p", value='Hello')
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'Hello')
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_equality_with_children(self):
        '''
            Test the constructor with children
        '''
        children = [HTMLNode(tag='li', value='One'),
                    HTMLNode(tag='li', value='Two')]
        node = HTMLNode(tag='ul', children=children)
        self.assertEqual(node.tag, 'ul')
        self.assertIsNone(node.value)
        self.assertEqual(node.children, children)
        self.assertIsNone(node.props)

    def test_inequality_with_different_proprties(self):
        '''
            Test the constructor with properties
        '''
        node1 = HTMLNode(tag='div', props={'class': 'one'})
        node2 = HTMLNode(tag='div', props={'class': 'two'})
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        '''
            Test the __repr__ method
        '''
        node = HTMLNode(tag='p', value='Text')
        expected_repr = "HTMLNode('p', Text, None, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html(self):
        '''
            Test the to_html method
        '''
        node = HTMLNode(tag='p', value='Text')
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        '''
            Test the props_to_html method
        '''
        node = HTMLNode(tag='div', props={'class': 'one', 'id': 'two'})
        node2 = HTMLNode(tag='a', value="Google", props={
            'href': 'https://www.google.com', 'target': '_blank'})
        self.assertEqual(node.props_to_html(), 'class="one" id="two"')
        self.assertEqual(node2.props_to_html(), 'href="https://www.google.com" target="_blank"')


if __name__ == "__main__":
    unittest.main()
