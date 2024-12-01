"""
Defines the TextNode class and TextType enum.
"""
from enum import Enum

class TextType(Enum):
    """
    The TextType class is an enumeration that defines
    various types of text formatting.
    """
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    """
    Represents a text element with an optional URL and a specific type.

    The TextNode class is designed to encapsulate a piece of text along with its
    type and an optional URL. It provides basic functionality to compare two text
    nodes for equality based on their attributes and to generate a representational
    string of the text node for debugging and logging purposes.
    """
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode('{self.text}', {self.text_type.value}, '{self.url}')"
