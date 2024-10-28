from textnode import TextNode
from inline_makrdown import *
from block_markdown import *
from static_data import *
import os

source_path = "./static/"
destination_path = "./public/"

def main():
    deleteContent(destination_path)
    copyContent(source_path, destination_path)


main()