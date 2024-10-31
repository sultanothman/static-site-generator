from block_markdown import *
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file_object = open(from_path, "r", encoding = "utf-8")
    template_file_object = open(template_path, "r+", encoding = "utf-8")
    page_name = f"{extract_file_name(from_path)}.html"
    result_path = os.path.join(dest_path, page_name)

    markdown_file = markdown_file_object.read()
    template_file = template_file_object.read()

    markdown_as_html_nodes = markdown_to_html_node(markdown_file)
    html_content =  markdown_as_html_nodes.to_html()
    
    title = extract_title(markdown_file)

    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html_content)

    with open(result_path, "w", encoding = "utf-8") as index_html_file:
        index_html_file.write(template_file)

    markdown_file_object.close()
    template_file_object.close()

def extract_title(markdown):
    lines = markdown.splitlines()
    if lines:
        first_row = lines[0]
        match = re.match(r'^#\s+', first_row)
        if match:
            return first_row.replace("#", "").strip()
    
    raise Exception("markdown does not contain H1 header")

def extract_file_name(path):
    delimiter = ""
    if "\\" in path:
        delimiter = "\\"
    elif "/" in path:
        delimiter = "/"
    else:
        raise Exception("Not a path")
    
    dirs = path.split(delimiter)

    file_name_and_extension = dirs[-1]
    
    return file_name_and_extension.split(".")[0]

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise ReferenceError("Invalid path")
    
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)


    for content in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, content)
    
        if os.path.isdir(content_path):
            dest_path = os.path.join(dest_dir_path, content)
            generate_pages_recursive(content_path, template_path, dest_path)
        
        else:
            generate_page(content_path, template_path, dest_dir_path)