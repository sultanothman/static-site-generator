from textnode import TextNode

from textnode import (
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            nodes.append(old_node)
            continue

        node_text = old_node.text.split(delimiter)
        if len(node_text) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        
        for i, text in enumerate(node_text):
            if (text == ""):
                continue
            if i % 2 == 0:
                new_node = TextNode(text, old_node.text_type)
                nodes.append(new_node)
            else :
                new_node = TextNode(text, text_type)
                nodes.append(new_node)
    return nodes