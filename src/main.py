import os
import shutil
from textnode import TextNode, TextType
from copy_static import copy_files_recursive
from generate_page import generate_page, generate_pages_recursive


def main():
#  *** CONFIG  ***
    static_path = "./static"
    public_path = "./public"
    content_path = "./content"
    template_path = "./template.html"

    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)
    copy_files_recursive(static_path, public_path)

    # 2. Generate all pages recursively
    print(f"Generating pages from {content_path} to {public_path}...")
    generate_pages_recursive(content_path, template_path, public_path)



if __name__ == "__main__":
    main()
