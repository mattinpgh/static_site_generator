import unittest
from textnode import TextNode, TextType
from md_helpers import split_nodes_delimiter

class TestMarkdownParser(unittest.TestCase):
    def test_bold_at_start(self):
        """Test bold text at the start of the string"""
        node = TextNode("**Bold text** after", TextType.TEXT)
        expected = [
            TextNode("Bold text", TextType.BOLD),
            TextNode(" after", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_bold_in_middle(self):
        """Test bold text in the middle of the string"""
        node = TextNode("Text with **bold words** here", TextType.TEXT)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold words", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_bold_at_end(self):
        """Test bold text at the end of the string"""
        node = TextNode("Text with **bold text**", TextType.TEXT)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_multiple_bold_starting_at_beginning(self):
        """Test multiple bold sections starting at the beginning"""
        node = TextNode("**First bold** middle **second bold** end", TextType.TEXT)
        expected = [
            TextNode("First bold", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("second bold", TextType.BOLD),
            TextNode(" end", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_multiple_bold_starting_in_middle(self):
        """Test multiple bold sections starting in the middle"""
        node = TextNode("Start **first bold** middle **second bold** end", TextType.TEXT)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("first bold", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("second bold", TextType.BOLD),
            TextNode(" end", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_italic_at_start(self):
        """Test italic text at the start of the string"""
        node = TextNode("*Italic text* after", TextType.TEXT)
        expected = [
            TextNode("Italic text", TextType.ITALIC),
            TextNode(" after", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_code_in_middle(self):
        """Test code block in the middle of the string"""
        node = TextNode("Text with `code block` here", TextType.TEXT)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_error_cases(self):
        """Test error cases with invalid delimiter counts"""
        # Test odd number of delimiters
        node = TextNode("Text with **bold but no closing", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

        # Test no delimiters
        node = TextNode("Text with no delimiters", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Text with no delimiters")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_empty_delimited_text(self):
        """Test handling of empty delimited text"""
        node = TextNode("Before ** ** after", TextType.TEXT)
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode(" after", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_non_text_node_passthrough(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        node = TextNode("Already bold text", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Already bold text")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_multiple_nodes_simple(self):
        """Test handling multiple nodes where only some contain delimiters"""
        nodes = [
            TextNode("First **bold** text", TextType.TEXT),
            TextNode("No delimiters here", TextType.TEXT),
            TextNode("More **bold** text", TextType.TEXT)
        ]
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("No delimiters here", TextType.TEXT),
            TextNode("More ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_multiple_nodes_mixed_types(self):
        """Test handling multiple nodes including non-TEXT nodes"""
        nodes = [
            TextNode("Start **bold**", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More **bold** here", TextType.TEXT),
            TextNode("Code block", TextType.CODE)
        ]
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
            TextNode("Code block", TextType.CODE)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_multiple_nodes_empty_and_whitespace(self):
        """Test handling multiple nodes with empty delimited text and whitespace"""
        nodes = [
            TextNode("Start ** **", TextType.TEXT),
            TextNode("Middle **  ** here", TextType.TEXT),
            TextNode("End ****", TextType.TEXT)
        ]
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode("Middle ", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
            TextNode("End ", TextType.TEXT),
            TextNode("", TextType.BOLD)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_multiple_nodes_with_errors(self):
        """Test handling multiple nodes where one node has invalid delimiters"""
        nodes = [
            TextNode("Valid **bold**", TextType.TEXT),
            TextNode("Invalid **bold", TextType.TEXT),  # Missing closing delimiter
            TextNode("More **bold** text", TextType.TEXT)
        ]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_multiple_empty_nodes(self):
        """Test handling multiple empty or whitespace-only nodes"""
        nodes = [
            TextNode("", TextType.TEXT),
            TextNode("  ", TextType.TEXT),
            TextNode("**bold**", TextType.TEXT),
            TextNode("", TextType.TEXT)
        ]
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("  ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_multiple_nodes_cross_delimiter(self):
        """Test that delimiters can't cross node boundaries"""
        nodes = [
            TextNode("Start **bold", TextType.TEXT),
            TextNode("not bold** end", TextType.TEXT)
        ]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

if __name__ == "__main__":
    unittest.main()