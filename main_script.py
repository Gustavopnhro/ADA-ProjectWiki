import os
import markdown
from jinja2 import Environment, FileSystemLoader
import json

def generate_html_post(general, content):
    env = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(), "templates")))
    print("Current working directory:", os.getcwd())
    template = env.get_template("post_template.html")
    return template.render(title=general['title'], author=general['author'], description=general['description'], content=content)

def index_page(posts):
    env = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(), "templates")))
    print("Current working directory:", os.getcwd())
    template = env.get_template("index_template.html")
    return template.render(posts=posts)

markdown_directory = "markdown_files"
output_directory = ""
json_path = "json_path"

markdown_files_list = [f for f in os.listdir(markdown_directory) if f.endswith(".md")]

posts = []

for index, markdown_file in enumerate(markdown_files_list):
    with open(os.path.join(markdown_directory, markdown_file), "r", encoding="utf-8") as post:
        markdown_content = post.read()
        content_lines = markdown_content.split("\n")

    content_index = 0
    info_parts = []
    for i in range (0,3):
        split_text = content_lines[i].split(':')
        content_index += len(content_lines[i])+1
        info_parts.append(split_text[1].strip())
        
    general_info = {"title": str(info_parts[0]), "description": str((info_parts[1])), "author": str(info_parts[2])}

    with open(os.path.join(json_path, f"general_info[{index+1}].json") , "w+", encoding="utf-8") as json_file:
        json.dump(general_info, json_file)

    html_content = markdown.markdown(markdown_content[content_index::], extensions=["markdown.extensions.fenced_code"])
    post_title = general_info["title"]
    html_post = generate_html_post(general_info, html_content)
    with open(os.path.join(output_directory, f"{post_title}.html"), "w", encoding="utf-8") as output_file:
        output_file.write(html_post)
        posts.append({"title": general_info['title'], "link":f"{general_info['title']}.html", "preview": general_info['description']+"..."})




index_html = index_page(posts)
with open(os.path.join(output_directory, "index.html"), "w", encoding="utf-8") as index:
    index.write(index_html)