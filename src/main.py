import sys
import os
import shutil
from copy_static import copy_files_recursive
from generate_page import generate_page, generate_pages_recursive


def main():
#  *** CONFIG  ***
    # Default to "/" if no argument is provided
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    static_path = "./static"
    output_path = "./docs"
    content_path = "./content"
    template_path = "./template.html"

    print(f"Cleaning {output_path}...")
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)

    print(f"Copying static files to {output_path}...")
    copy_files_recursive(static_path, output_path)

    print(f"Generating pages to {output_path} with basepath: {basepath}...")
    generate_pages_recursive(content_path, template_path, output_path, basepath)



if __name__ == "__main__":
    main()
