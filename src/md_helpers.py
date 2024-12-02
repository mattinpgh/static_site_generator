"""
Helper functions for markdown files
"""

import logging


from textnode import TextType, TextNode


logging.basicConfig(
    filename='src.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def char_iterator(string):
    """
    Generator that yields each character in a string.
    """
    yield from string


def pull_substring(open_delimiter, close_delimiter, initial_char, char_stream):
    """
    Extracts a substring from a character stream, starting with an initial
    character and ending when a specified closing delimiter is found. The
    function verifies that the stream begins with a specified opening delimiter.
    After extracting the substring, any remaining characters in the stream
    are appended to the result list.

    Parameters:
    open_delimiter: str
        The string that must appear at the beginning of the stream as a
        delimiter to start the extraction process.
    close_delimiter: str
        The string that signals the end of the substring to be extracted.
    initial_char: str
        The first character of the stream, which is already read and provided
        outside of this function.
    char_stream: iterator
        An iterator providing characters from a stream sequentially.

    Returns:
    list of str
        A list containing the extracted substring followed by any remaining
        characters in the stream.

    Raises:
    ValueError
        If the opening delimiter is not found at the beginning of the stream,
        or if the closing delimiter is not found by the end of the stream.
    """
    if not open_delimiter and not close_delimiter:
        return [''.join([initial_char] + list(char_stream))]

    buffer = [initial_char]

    for _ in range(len(open_delimiter) - 1):
        try:
            buffer.append(next(char_stream))
        except StopIteration as exc:
            raise ValueError("Stream ended before completing the opening delimiter") from exc

    if open_delimiter and ''.join(buffer) != open_delimiter:
        raise ValueError("Opening delimiter does not match")

    # Extract characters until the closing delimiter is found
    output = []
    buffer = []  # Reuse buffer for closing delimiter matching

    for char in char_stream:
        buffer.append(char)

        # Keep only the characters needed for matching the closing delimiter
        if len(buffer) > len(close_delimiter):
            output.append(buffer.pop(0))

        # Check if the buffer matches the closing delimiter
        if ''.join(buffer) == close_delimiter:
            break
    else:
        raise ValueError("Stream ended before finding the closing delimiter")

    # Remaining characters after the closing delimiter
    remaining_chars = ''.join(char_stream)  # Consume any leftover characters

    result = [''.join(output)]  # Add the extracted substring
    if remaining_chars:
        result.append(remaining_chars)  # Add remaining characters if any

    return result


def validate_nodes(nodes):
    """
    Validate a list of TextNodes and their delimiters.
    Receives nodes: List of nodes to validate
    Returns valid_nodes: List of valid TextNodes with proper
    text types and delimiters
    Logs errors for invalid nodes instead of raising exceptions.
    """
    valid_nodes = []

    for node in nodes:
        if not isinstance(node, TextNode):
            logging.error("Invalid node type: %s. Expected TextNode.", type(node))
            continue

        try:
            if node.text_type != TextType.NORMAL:
                # Just access the property - if it raises an error, the node is invalid
                node.get_delimiters
            valid_nodes.append(node)
        except (AttributeError, ValueError) as e:
            logging.error(
                "Error validating delimiters for node: %s. "
                "Error: %s", node, str(e)
            )

    return valid_nodes



def split_nodes_delimiter(old_nodes):
    """
    Splits nodes based on a specified delimiter, processing them into new nodes.
    The function iterates over each node, extracting substrings using defined opening
    and closing delimiters, and reassembles processed sections into a set of new nodes.
    It handles character-by-character analysis of node texts and reconstructs them
    when necessary.

    Args:
        old_nodes (list): A list of nodes to be processed, where each node contains
                          text information and a corresponding text type specifying
                          delimiter details.

    Returns:
        list: A new list of processed nodes where each node represents a text section
              either as a regular text node or as a substring captured between
              specified delimiters.
    """
    new_nodes = []
    nodes_to_review = validate_nodes(old_nodes)

    for item in nodes_to_review:

        get_char = char_iterator(item.text)
        open_delimiter, close_delimiter = item.get_delimiters

        buffer = []
        try:
            char = next(get_char)
        except StopIteration:
            continue

        if char and open_delimiter and char != open_delimiter[0]:
            buffer.append(char)
        else:
            if buffer:
                new_nodes.append(TextNode(''.join(buffer), text_type=TextType.NORMAL))
                buffer = []
                char = next(get_char)
            new_nodes.append(pull_substring(open_delimiter, close_delimiter, char,
                                           get_char))
    return_nodes = []
    for node in new_nodes:
        node_text = node[0]  # Assuming every node has at least one element
        if len(node) > 1 and node[1] != "":
            node_type = node[1]
        else:
            node_type = TextType.NORMAL  # Default value if node[1] doesn't exist or is empty
        return_nodes.append(TextNode(node_text, node_type))

    return return_nodes

