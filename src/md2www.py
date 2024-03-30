import os
import sys
import marko

class md2www:
    def __init__(self, src_folder, www_folder, project) -> None:
        self.project = project
        self.src = src_folder
        self.www = www_folder
        self.struct = {}

    def get_weigth(self):
        weigth = {}
        counter = 0
        try:
            with open(self.src+"order.txt") as f:
                for line in f.readlines():
                    weigth[line.replace("\n", "")] = counter
                    counter+=1

            return weigth
        except:
            print("Missing order.txt file in the root of the src")
            sys.exit(0)
    
    def order_struct(self):
        ordered_struct = dict(sorted(self.struct.items(), key=lambda item: item[1]['weigth']))

        for key, value in ordered_struct.items():
            if 'content' in value:
                value['content'] = sorted(value['content'], key=lambda x: x['weigth'])

        self.struct = ordered_struct

    def generate_structure(self):
        weigth = self.get_weigth()
        missing = False
        for directory in os.listdir(self.src):
            if os.path.isdir(self.src+directory) and directory[0] != ".":
                content = []
                chapter_weigth = 10000000
                for file in os.listdir(self.src+directory):
                    if not os.path.isdir(self.src+directory+"/"+file):
                        try:
                            if weigth[file] < chapter_weigth:
                                chapter_weigth = weigth[file]
                            
                            content.append({
                            "name": file,
                            "weigth": weigth[file]
                            })
                        except:
                            print("Missing file {} in order.txt".format(file))
                            missing = True
                self.struct[directory] = {
                    "content": content,
                    "weigth": chapter_weigth
                }
        
        if missing:
            sys.exit(0)
        
        self.order_struct()

    def file2name(self, file):
        return " ".join(file.split("-")).capitalize().strip()

    def generate_link(self, file):
        name = self.file2name(file.replace(".md", " "))

        return '<a href="{}">{}</a>'.format(name+".html", name)

    def generate_section(self, key, value):
        section = "<section><h2>"
        section += self.file2name(key)
        section += "</h2>"

        for file in value['content']:
            section+=self.generate_link(file['name'])

        section += "</section>"

        return section

    def generate_navigation(self):
        nav = "<nav><section class='title'><h1>{}</h1></section>".format(self.project)
        for key, value in self.struct.items():
            nav += self.generate_section(key, value)
        nav += "</nav>"

        return nav
            
    def generate_page(self, template, nav, chapter, content):
        name = self.file2name(content.replace(".md", ""))
        

        with open(self.src + chapter + "/" + content) as f:
            parsed = marko.convert(f.read())

        page = template.replace("<!--title-->", "{} | {}".format(name, self.project)).replace("<!--nav-->", nav).replace("<!--content-->", parsed)

        with open(self.www + content.replace(".md", ".html"), "w") as f:
            f.write(page)

    def generate_pages(self):
        nav = self.generate_navigation()

        templatefile="template.html"
        if os.path.exists(self.src+"template.html"):
            templatefile = self.src+"template.html"

        with open(templatefile) as f:
            template = f.read()

        for key, value in self.struct.items():
            for p in value['content']:
                self.generate_page(template, nav, key, p['name'])

    def generate(self):
        self.generate_structure()
        self.generate_pages()
