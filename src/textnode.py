'''
Defines the TextNode class and TextType enum.
'''
from enum import Enum

class TextType(Enum):
    '''
        Enum for the type of text
    '''
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    '''
        Class to represent a node in a text document
    '''
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
