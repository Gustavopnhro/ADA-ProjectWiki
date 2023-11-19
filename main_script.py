import os
import markdown
from jinja2 import Environment, FileSystemLoader

def generate_html_post(title, content):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("post_template.html")
    return template.render(title=title, content=content)

def index_page(posts):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index_template.html")
    return template.render(posts=posts)

markdown_directory = "markdown_files"
output_directory = "pages"

markdown_files_list = [f for f in os.listdir(markdown_directory) if f.endswith(".md")]

posts = []

for markdown_file in markdown_files_list:
    with open(os.path.join(markdown_directory, markdown_file), "r", encoding="utf-8") as post:
        markdown_content = post.read()


    html_content = markdown.markdown(markdown_content, extensions=["markdown.extensions.fenced_code"])
    
    post_title = (os.path.splitext(markdown_file)[0])

    html_post = generate_html_post(post_title, html_content)

    with open(os.path.join(output_directory, f"{post_title}.html"), "w", encoding="utf-8") as output_file:
        output_file.write(html_post)

    posts.append({"title": post_title, "link":f"{post_title}.html", "preview":markdown_content[0:20]+"..."})


index_html = index_page(posts)
with open(os.path.join(output_directory, "index.html"), "w", encoding="utf-8") as index:
    index.write(index_html)
