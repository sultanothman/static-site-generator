from block_markdown import *
from inline_makrdown import extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file_object = open(from_path, "r", encoding = "utf-8")
    template_file_object = open(template_path, "r+", encoding = "utf-8")
    index_path = os.path.join(dest_path, "index.html")

    markdown_file = markdown_file_object.read()
    template_file = template_file_object.read()

    markdown_as_html_nodes = markdown_to_html_node(markdown_file)
    html_content =  markdown_as_html_nodes.to_html()
    
    title = extract_title(markdown_file)

    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html_content)

    with open(index_path, "w", encoding = "utf-8") as index_html_file:
        index_html_file.write(template_file)

    markdown_file_object.close()
    template_file_object.close()
