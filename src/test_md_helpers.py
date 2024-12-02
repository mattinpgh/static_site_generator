import unittest

from md_helpers import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_empty_node_list(self):
        result = split_nodes_delimiter([])
        self.assertEqual(result, [])

    def test_single_node_no_delimiters(self):
        nodes = [TextNode("example text from single_node_no_delimiters", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes)
        expected = [TextNode("example text from single_node_no_delimiters", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_single_node_with_simple_delimiters(self):
        nodes = [TextNode("*bold text*", TextType.BOLD)]
        result = split_nodes_delimiter(nodes)
        expected = [TextNode("*bold text*", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_multiple_nodes_mixed_content(self):
        nodes = [
            TextNode("plain text from test_multiple_nodes_mixed_content",TextType.NORMAL),
            TextNode("**bold text from test_multiple_nodes_mixed_content**",TextType.BOLD),
            TextNode("*italic text from test_multiple_nodes_mixed_content*", TextType.ITALIC)
        ]
        result = split_nodes_delimiter(nodes)
        expected = [
            TextNode("plain text from test_multiple_nodes_mixed_content",TextType.NORMAL),
            TextNode("**bold text from test_multiple_nodes_mixed_content**", TextType.BOLD),
            TextNode("*italic text from test_multiple_nodes_mixed_content*",TextType.ITALIC)
        ]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
