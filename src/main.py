import os
import shutil

from src.actions.convert import markdown_to_html_node
from pathlib import Path


def copy_static_to_public(src, dst):
    if os.path.isfile(src):
        shutil.copy(src, dst)
        return
    
    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.mkdir(dst)    
    files = os.listdir(src)

    for file_name in files:
        if not os.path.isfile(file_name):
            new_dst = os.path.join(dst, file_name)
            new_src = os.path.join(src, file_name)
            copy_static_to_public(new_src, new_dst)


def extract_title(markdown):
    header = markdown.split('\n', 1)

    if not header or not header[0].startswith('# '):
        raise Exception("No h1 header in markdown file.")
    
    return header[0][2:]


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path) as f:
        markdown = f.read()
    
    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)
    
    p = Path(dest_path)
    f = open(p.with_suffix(".html"), "x")
    f.write(template)
    f.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content) and dir_path_content[len(dir_path_content) - 3:] == '.md':
        generate_page(dir_path_content, template_path, dest_dir_path)
        return

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    files = os.listdir(dir_path_content)

    for file_name in files:
        if not os.path.isfile(file_name):
            new_dst = os.path.join(dest_dir_path, file_name)
            new_src = os.path.join(dir_path_content, file_name)
            generate_pages_recursive(new_src, template_path, new_dst)


def main():
    copy_static_to_public("static", "public")
    generate_pages_recursive("content", "./template.html", "public")


if __name__ == "__main__":
    main()
    
