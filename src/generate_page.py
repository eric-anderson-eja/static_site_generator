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