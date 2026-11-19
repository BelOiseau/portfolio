import sys
import os
import shutil
import pathlib
from textnode import *
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_conversion import extract_title
from md_to_html import markdown_to_htmlnode


def main():
    argv = sys.argv
    if len(argv) == 1:
        basepath = "/"
    else:
        basepath = argv[1]
    cp_src_to_dest("static", "docs")
    generate_page_recursive("content", "template.html", "docs", basepath)

def generate_page_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    current_folder_path = pathlib.Path(dir_path_content)
    for child in current_folder_path.iterdir():
        dest = str(child).replace(str(dir_path_content), dest_dir_path)
        if child.is_file():
            dest_path = dest.replace(".md", ".html")
            generate_page(child, template_path, dest_path, basepath)
        else:
            if not os.path.exists(dest):
                os.mkdir(dest)
            generate_page_recursive(child, template_path, dest, basepath)

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        raw_template = f.read()
    title = extract_title(markdown)
    html = markdown_to_htmlnode(markdown).to_html()
    titled_template = raw_template.replace("{{ Title }}", title)
    content_filled_template = titled_template.replace("{{ Content }}", html)
    filled_and_basepath_replaced = content_filled_template.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as f:
        f.write(filled_and_basepath_replaced)

def cp_src_to_dest(src: str, dest: str) -> None:
    print(f"trying to remove '{dest}' folder")
    if os.path.exists(dest):
        try:
            dest_folder_content = os.listdir(dest)
            for file in dest_folder_content:
                print(f"deleting {file}")
            print(f"deleting '{dest}'")
            shutil.rmtree(dest)
        except Exception as e:
            print(f"ERROR: {e}")
    else:
        print(f"'{dest}' folder doesn't exist")

    print(f"creating folder '{dest}'")
    try:
        os.mkdir(dest)
        if os.path.exists(src):
            src_files = os.listdir(src)
            for basename_src_file in src_files:
                src_file = os.path.join(src, basename_src_file)
                if not os.path.isfile(src_file):
                    sub_folder = os.path.join(dest, basename_src_file)
                    cp_src_to_dest(src_file, sub_folder)
                else:
                    print(f"copying {src_file} to {dest}")
                    shutil.copy(src_file, dest)
    except Exception as e:
        print(f"ERROR: {e}")
    
if __name__ == "__main__":
    main()