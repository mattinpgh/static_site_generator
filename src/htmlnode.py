'''
Defines the HTMLNode class
'''


class HTMLNode():
    '''
        Class to represent a node in an HTML document
    '''

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        '''
            Placeholder for later child class behavior
        '''
        raise NotImplementedError

    def props_to_html(self):
        '''
            Returns the properties as an HTML string
        '''
        return None if self.props is None else \
            ' '.join([f'{key}="{value}"' for key, value in self.props.items()])

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and \
            self.children == other.children and self.props == other.props:
            return True
        return False

    def __repr__(self):
        return f"HTMLNode('{self.tag}', {self.value},\
            {self.children}, {self.props})"