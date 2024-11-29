'''
This is the main file for the project. No logic so far, just a print statement.
'''
from textnode import TextType, TextNode


def main():
    '''
        Main function for the project
    '''
    dummy_node = TextNode('Here is the text string.', TextType.ITALIC,
                         'http://www.mallardmariner.com')
    tod_node = TextNode('Here is the text string.', TextType.ITALIC,
                       'http://www.mallardmariner.com')
    print(f'{dummy_node} \n{tod_node}')
    print(tod_node == dummy_node)

main()
