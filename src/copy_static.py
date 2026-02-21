import os
import shutil


def copy_files_recursive(source, destination):
    if not os.path.exists(source):
        raise Exception("Source path does not exist")
        
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dst_path = os.path.join(destination, item)
        
        if os.path.isfile(src_path):
            print(f" * {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            copy_files_recursive(src_path, dst_path)
