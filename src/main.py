from textnode import TextNode, TextType
from copy_static import copy_files_recursive
import os
import shutil


def main():
    node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    print(node)
    source_path = "./static"
    dest_path = "./public"

    print("Cleaning up public directory...")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    
    print("Creating public directory...")
    os.mkdir(dest_path)

    print("Copying static files to public directory...")
    copy_files_recursive(source_path, dest_path)




if __name__ == "__main__":
    main()
