import os


from extract_title import extract_title
# Assuming your markdown conversion logic is in src/markdown_blocks.py
from markdown_blocks import markdown_to_html_node 

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read Markdown
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    # Read Template
    with open(template_path, 'r') as f:
        template = f.read()

    # Convert Markdown to HTML
    node = markdown_to_html_node(markdown_content)
    html_content = node.to_html()

    # Get Title
    title = extract_title(markdown_content)

    # Inject into Template
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    # Write to file
    with open(dest_path, 'w') as f:
        f.write(full_html)

import os

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Log what we are doing for debugging
    print(f"Walking from {dir_path_content} to {dest_dir_path}")

    # We list the CURRENT directory
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        # Check if the ITEM is a file
        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                # Logic to convert .md to .html path
                # Use .replace or os.path.splitext
                dest_html_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_html_path)
        else:
            # ONLY if it's a directory do we recurse
            # Ensure the directory exists in public/
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, dest_path)