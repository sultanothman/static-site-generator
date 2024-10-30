from textnode import TextNode
from inline_makrdown import *
from block_markdown import *
from static_data import *
from page_generator import *

import os


# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths relative to the script directory
source_path = os.path.join(SCRIPT_DIR, "..", "static")
destination_path = os.path.join(SCRIPT_DIR, "..", "public")
content_path = os.path.join(SCRIPT_DIR, "..", "content","index.md")
template_path = os.path.join(SCRIPT_DIR, "..", "template.html")

def main():
    deleteContent(destination_path)
    copyContent(source_path, destination_path)
    generate_page(content_path, template_path, destination_path)


if __name__ == "__main__":
    main()