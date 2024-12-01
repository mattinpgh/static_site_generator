"""
Defines the TextNode class and TextType enum.
"""
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    """
    Represents the different types of text formatting options available.

    This enumeration is used to specify the type of text formatting that
    can be applied to text elements. It includes normal text as well as
    common formatting options such as bold, italic, and code. Additionally,
    it provides options for text links and image insertion. This can be used
    in text processing applications where such text transformations are
    needed.
    """
    NORMAL = None
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    """

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

    def text_node_to_html_node(self) -> LeafNode:
        """
        Converts the TextNode into an equivalent HTML LeafNode.
        """
        match self.text_type:
            case TextType.NORMAL:
                return LeafNode(tag=None, value=self.text, props=None)
            case TextType.BOLD:
                return LeafNode(tag="b", value=self.text, props=None)
            case TextType.ITALIC:
                return LeafNode(tag="i", value=self.text, props=None)
            case TextType.CODE:
                return LeafNode(tag="code", value=self.text, props=None)
            case TextType.LINK:
                if not self.url:
                    raise ValueError("URL is required for LINK text type.")
                return LeafNode(tag="a", value=self.text, props={"href": self.url})
            case TextType.IMAGE:
                if not self.url:
                    raise ValueError("URL is required for IMAGE text type.")
                return LeafNode(tag="img", value="", props={"src": self.url, "alt": self.text})
            case _:
                raise ValueError(f"Invalid text type: {self.text_type}")
