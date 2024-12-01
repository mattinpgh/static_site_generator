"""
Defines the HTMLNode class
"""



class HTMLNode:
    """
    Represents a node in an HTML structure with tag, value, children, and properties.

    This class serves as a basic representation of an HTML node. It encapsulates
    the core attributes of an HTML element such as the tag name, its textual content,
    list of child nodes, and a dictionary of properties (attributes). The class
    provides methods to work with these attributes, such as converting properties
    to an HTML-compatible attribute string. It also defines standard methods for
    comparison and representation. Intended to be used as a base class for more
    specific types of HTML nodes.
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
            Placeholder for later child class behavior
        """
        raise NotImplementedError

    def props_to_html(self):
        """
        Converts the properties (props) dictionary into a string of HTML attributes.

        If the 'props' attribute is None, it returns None. Otherwise, it generates
        a string of key-value pairs formatted as HTML attributes, joined by spaces.

        Returns
        -------
        str or None
            A string of HTML attributes if 'props' is not None and contains attributes,
            otherwise None.
        """
        return None if self.props is None else \
            ' '.join([f'{key}="{value}"' for key, value in self.props.items()])

    def generate_tag_with_props(self):
        """Helper method to generate a tag with optional properties."""
        props_html = self.props_to_html()
        return f"<{self.tag} {props_html}>" if props_html else f"<{self.tag}>"

    def __eq__(self, other):
        """
        Compares this HTMLNode with another for equality based on tag, value,
        children, and props attributes.

        Parameters:
            other: The object to compare against.

        Returns:
            bool: True if the two objects are equal, False otherwise.
        """
        return self.tag == other.tag and \
            self.value == other.value and \
            self.children == other.children and \
            self.props == other.props

    def __repr__(self):
        return f"HTMLNode('{self.tag}', {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """Represents a leaf node in an HTML document structure.

    A LeafNode is a terminal node in the HTML document tree that cannot
    have any children. It encapsulates simple HTML elements with optional
    attributes and a required textual value. This class is useful for
    creating elements like <span>, <a>, <img> (without children), or
    text nodes.

    Attributes
    ----------
    tag : str, optional
        The HTML tag of the element. If None, the node will be treated
        as a text node without any tag encapsulation.
    value : str
        The textual content or value of the HTML element. This attribute
        is mandatory to create a valid LeafNode and should never be None.
    props : dict, optional
        A dictionary of HTML attributes for the node. This can include
        any key-value pairs representing valid HTML properties.
    Examples
    --------
    >>> node = LeafNode(tag="span", value="Hello, world!", props={"class": "highlight"})
    >>> print(node.to_html())
    <span class="highlight">Hello, world!</span>

    >>> text_node = LeafNode(value="Just text")
    >>> print(text_node.to_html())
    Just text
    """
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("Value is required for leaf nodes")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value is required for leaf nodes")
        if self.tag is None:
            return self.value

        return f"{self.generate_tag_with_props()}{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode('{self.tag}', {self.value}, {self.children}, {self.props})"


class ParentNode(HTMLNode):
    """
    Represents a parent HTML node with a tag and children nodes.

    This class is used for creating an HTML node that contains child nodes.
    It requires a tag and a list of children nodes upon initialization, and
    provides a method to generate an HTML string representation of the node
    and its children. The class inherits from HTMLNode, ensuring it has
    properties and common behaviors of an HTML node.

    Attributes:
        tag: The HTML tag for the node. Required for parent nodes.
        children: A list of child nodes. Required for parent nodes.

    Methods:
        __init__(tag, children, props):
            Initializes a ParentNode with a specified tag, children, and optional properties.
        to_html():
            Converts the node and its children into an HTML string representation.
        __repr__():
            Provides a string representation of the ParentNode.

    Raises:
        ValueError: If 'tag' or 'children' is not provided during initialization or
                    when converting to HTML.
    """
    def __init__(self, tag=None, children=None, props=None):
        if not children:
            raise ValueError("Children are required for parent nodes")
        if not tag:
            raise ValueError("Tag is required for parent nodes")

        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        """
        Converts the current node and its child nodes into HTML string representation.
        """
        # Generate HTML for all children without re-wrapping their tags
        children_html = "".join(child.to_html() for child in self.children)

        # Generate the tag with properties for the parent node
        parent_tag_with_props = self.generate_tag_with_props()
        return f"{parent_tag_with_props}{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode('{self.tag}', {self.value}, {self.children}, {self.props})"
