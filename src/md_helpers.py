"""
Helper functions to convert markdown to html
"""
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Takes a list of nodes, a delimiter, and a text type. Returns a new list of TextNodes where the text within the
    original node has been split into multiple new nodes with the delimiter between them.

    Args:
        old_nodes: List of TextNode objects to process
        delimiter: String delimiter that marks special text (e.g., "**" for bold, "`" for code)
        text_type: TextType enum value to apply to delimited sections

    Returns:
        list[TextNode]: New list of TextNode objects with text split at delimiters

    Raises:
        ValueError: If a node contains an odd number of delimiters or no delimiters

    Example:
        >>> node = TextNode("This is **bold text** and `code`.", TextType.TEXT)
        >>> split_nodes_delimiter([node], "**", TextType.BOLD)
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and `code`.", TextType.TEXT)
        ]
    """
    new_nodes = []
    delim_length = len(delimiter)

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Find all delimiter positions
        text = node.text
        delimiter_positions = []
        pos = 0
        while True:
            pos = text.find(delimiter, pos)
            if pos == -1:
                break
            delimiter_positions.append(pos)
            pos += delim_length

        # Validate delimiter pairs
        if len(delimiter_positions) % 2 != 0:
            raise ValueError(f"Node contains an odd number of '{delimiter}' delimiters: {text}")
        if not delimiter_positions:
            new_nodes.append(node)
            continue

        # Split text using delimiter positions
        current_pos = 0
        for i in range(0, len(delimiter_positions), 2):
            start_delim = delimiter_positions[i]
            end_delim = delimiter_positions[i + 1]

            # Add text before delimiter if it exists
            if current_pos < start_delim:
                new_nodes.append(TextNode(text[current_pos:start_delim], TextType.TEXT))

            # Add delimited text (excluding the delimiters themselves)
            delimited_text = text[start_delim + delim_length:end_delim].strip()
            new_nodes.append(TextNode(delimited_text, text_type))

            current_pos = end_delim + delim_length

        # Add remaining text after last delimiter if it exists
        if current_pos < len(text):
            new_nodes.append(TextNode(text[current_pos:], TextType.TEXT))

    return new_nodes