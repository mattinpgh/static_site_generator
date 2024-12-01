"""
    Unit test for htmlnode.py
"""

import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    """
    A set of unit tests for the HTMLNode class, which verifies its construction,
    equality,representation, and conversion to HTML.
    """
    def test_default_constructor(self):
        """
        Raises AssertionError: If any of the HTMLNode attributes are not None
        upon instantiation without parameters.
        """
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_equality_with_value_only(self):
        """
            Test the constructor with only the tag and its value
        """
        node = HTMLNode(tag="p", value='Hello')
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'Hello')
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_equality_with_children(self):
        """
            Test the constructor with children
        """
        children = [HTMLNode(tag='li', value='One'),
                    HTMLNode(tag='li', value='Two')]
        node = HTMLNode(tag='ul', children=children)
        self.assertEqual(node.tag, 'ul')
        self.assertIsNone(node.value)
        self.assertEqual(node.children, children)
        self.assertIsNone(node.props)

    def test_inequality_with_different_properties(self):
        """
            Test the constructor with properties
        """
        node1 = HTMLNode(tag='div', props={'class': 'one'})
        node2 = HTMLNode(tag='div', props={'class': 'two'})
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        """
            Test the __repr__ method
        """
        node = HTMLNode(tag='p', value='Text')
        expected_repr = "HTMLNode('p', Text, None, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html(self):
        """
            Test the to_html method
        """
        node = HTMLNode(tag='p', value='Text')
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        """
            Test the props_to_html method
        """
        node = HTMLNode(tag='div', props={'class': 'one', 'id': 'two'})
        node2 = HTMLNode(tag='a', value="Google", props={
            'href': 'https://www.google.com', 'target': '_blank'})
        self.assertEqual(node.props_to_html(), 'class="one" id="two"')
        self.assertEqual(node2.props_to_html(), 'href="https://www.google.com" target="_blank"')


class TestLeafNode(unittest.TestCase):
    def test_default_constructor(self):
        node = LeafNode(value="Hello")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_constructor_with_no_value(self):
        with self.assertRaises(ValueError) as context:
            node = LeafNode(value=None)
        self.assertEqual(str(context.exception),
                         "Value is required for leaf nodes")

    def test_equality_with_tag_and_value(self):
        node = LeafNode(tag="p", value="Hello")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_inequality_with_different_tag(self):
        node1 = LeafNode(tag="p", value="Hello")
        node2 = LeafNode(tag="div", value="Hello")
        self.assertNotEqual(node1, node2)

    def test_inequality_with_different_value(self):
        node1 = LeafNode(tag="p", value="Hello")
        node2 = LeafNode(tag="p", value="Goodbye")
        self.assertNotEqual(node1, node2)

    def test_inequality_with_different_properties(self):
        node1 = LeafNode(tag="p", value="Hello", props={'class': 'one'})
        node2 = LeafNode(tag="p", value="Hello", props={'class': 'two'})
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = LeafNode(tag="p", value="Hello")
        expected_repr = "LeafNode('p', Hello, None, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html(self):
        node1 = LeafNode(tag="p", value="Hello")
        node2 = LeafNode(tag="a", value="Google", props={
            'href': 'https://www.google.com'})
        self.assertEqual(node1.to_html(), "<p>Hello</p>")
        self.assertEqual(node2.to_html(),
                         '<a href="https://www.google.com">Google</a>')


class TestParentNode(unittest.TestCase):
    def test_default_constructor(self):
        Node = ParentNode(tag="div", children=[LeafNode(tag="p", value="Hello")])
        self.assertEqual(Node.tag, "div")
        self.assertIsNone(Node.value)
        self.assertEqual(Node.children, [LeafNode(tag="p", value="Hello")])
        self.assertIsNone(Node.props)

    def test_error_children_is_none(self):
        with self.assertRaises(ValueError) as context:
            Node = ParentNode(tag="div", children=None)
        self.assertEqual(str(context.exception),
                         "Children are required for parent nodes")

    def test_error_children_is_empty(self):
        with self.assertRaises(ValueError) as context:
            Node = ParentNode(tag="div", children=[])
        self.assertEqual(str(context.exception),
                         "Children are required for parent nodes")

    def test_error_tag_is_none(self):
        with self.assertRaises(ValueError) as context:
            Node = ParentNode(tag=None, children=[LeafNode(tag="p", value="Hello")])
        self.assertEqual(str(context.exception),
                         "Tag is required for parent nodes")

    def test_equality_with_tag_and_children(self):
        node = ParentNode(tag="div", children=[LeafNode(tag="p", value="Hello")])
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [LeafNode(tag="p", value="Hello")])
        self.assertIsNone(node.props)

    def test_inequality_with_different_tag(self):
        node1 = ParentNode(tag="div", children=[LeafNode(tag="p", value="Hello")])
        node2 = ParentNode(tag="ul", children=[LeafNode(tag="p", value="Hello")])
        self.assertNotEqual(node1, node2)

    def test_to_html_with_correct_parameters(self):
        children = [LeafNode(tag="p", value="Hello"),
                    LeafNode(tag="p", value="Goodbye"),
                    LeafNode(tag="a", value="Google", props={'href': 'https://www.google.com'})]
        node = ParentNode(tag="div", children=children)
        self.assertEqual(node.to_html(),
                         '<div><p>Hello</p><p>Goodbye</p><a href="https://www.google.com">Google</a></div>')

    def test_to_html_with_empty_children_list(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(tag="div", children=[])
        self.assertEqual(str(context.exception),
                         "Children are required for parent nodes")

    def test_to_html_with_none_children(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(tag="div", children=None)
        self.assertEqual(str(context.exception),
                         "Children are required for parent nodes")

    def test_to_html_with_none_tag(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(tag=None, children=[LeafNode(tag="p", value="Hello")])
        self.assertEqual(str(context.exception),
                         "Tag is required for parent nodes")

    def test_to_html_with_empty_tag(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(tag="", children=[LeafNode(tag="p", value="Hello")])
        self.assertEqual(str(context.exception),
                         "Tag is required for parent nodes")

    def test_to_html_with_one_child(self):
        node = ParentNode(tag="div", children=[LeafNode(tag="p", value="Hello")])
        self.assertEqual(node.to_html(), "<div><p>Hello</p></div>")

    def test_to_html_with_child_with_no_value(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(tag="div", children=[LeafNode(tag="p")])
        self.assertEqual(str(context.exception),
                         "Value is required for leaf nodes")

if __name__ == "__main__":
    unittest.main()
