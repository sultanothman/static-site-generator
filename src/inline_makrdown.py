from textnode import TextNode
import re

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

def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    for image in images:
        if image[1] == "":
            raise ValueError("Inavlid markdown - missing url")

    return images

def extract_markdown_links(text):
    links =  re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

    for link in links:
        if link[1] == "":
            raise ValueError("Invalid markdown - missing link")
        
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if (len(images) == 0):
            new_nodes.append(old_node)
            continue

        for img in images:
            sections = original_text.split(f"![{img[0]}]({img[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(
                    TextNode(
                        sections[0], 
                        text_type_text
                    )
                )
            new_nodes.append(
                TextNode(
                    img[0],
                    text_type_image,
                    img[1],
                )
            )
            original_text = sections[1]
    if original_text != "":
        new_nodes.append(
            TextNode(
                original_text,
                text_type_text
            )
        )
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if (len(links) == 0):
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
    
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(
                    TextNode(
                        sections[0], 
                        text_type_text
                    )
                )
            new_nodes.append(
                TextNode(
                    link[0],
                    text_type_link,
                    link[1],
                )
            )
            original_text = sections[1]
    if original_text != "":
        new_nodes.append(
            TextNode(
                original_text,
                text_type_text
            )
        )
    return new_nodes
    
def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    
    if check_for_double_asterisks_occurrences(nodes):
        nodes = split_nodes_delimiter( nodes, "**", text_type_bold)

    if check_for_single_asterisks_occurrences(nodes):
        nodes = split_nodes_delimiter(nodes, "*", text_type_italic)

    if check_for_backticks_occurrences(nodes):
        nodes = split_nodes_delimiter(nodes, "`", text_type_code)

    if check_for_images_occurrences(nodes):
        nodes = split_nodes_image(nodes)
        
    if check_for_links_occurrences(nodes):
        nodes = split_nodes_link(nodes)
    
    return nodes

def check_for_single_asterisks_occurrences(nodes):
    for node in nodes:
        text = node.text
        single_asterisks = re.findall(r'(?<!\*)\*(?!\*)', text)
        if len(single_asterisks) % 2 == 0 and len(single_asterisks) > 0:
            return True

    return False

def check_for_double_asterisks_occurrences(nodes):
    for node in nodes:
        text = node.text
        double_asterisks = re.findall(r'\*\*', text)
    
        if len(double_asterisks) > 0 and len(double_asterisks) % 2 == 0:
            return True

    return False

def check_for_backticks_occurrences(nodes):
    for node in nodes:
        text = node.text
        backticks_count = text.count("`")
    
        if backticks_count > 0 and backticks_count % 2 == 0:
            return True

    return False

def check_for_images_occurrences(nodes):
    for node in nodes:
        text = node.text
        images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    
        if len(images) > 0:
            return True

    return False

def check_for_links_occurrences(nodes):
    for node in nodes:
        text = node.text
        links = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    
        if len(links) > 0:
            return True

    return False