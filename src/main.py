import os
import shutil
from textnode import TextNode, TextType
from copy_static import copy_files_recursive
from generate_page import generate_page


def main():
    static_path = "./static"
    public_path = "./public"
    content_path = "./content/index.md"
    template_path = "./template.html"
    output_path = "./public/index.html"

    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)
    
    print("Copying static files...")
    copy_files_recursive(static_path, public_path)


    print("Generating index page...")
    generate_page(content_path, template_path, output_path)



if __name__ == "__main__":
    main()
