import os
import sys
import shutil
import marko


class md2www:
    def __init__(self, src_folder, www_folder, project) -> None:
        self.project = project
        self.src = src_folder
        self.www = www_folder
        self.struct = {}

        if not os.path.exists(self.www):
            os.makedirs(self.www)

    def get_weigth(self):
        weigth = {}
        counter = 0
        try:
            with open(self.src + "order.txt") as f:
                for line in f.readlines():
                    weigth[line.replace("\n", "")] = counter
                    counter += 1

            return weigth
        except:
            print("Missing order.txt file in the root of the src")
            sys.exit(0)

    def order_struct(self):
        ordered_struct = dict(
            sorted(self.struct.items(), key=lambda item: item[1]["weigth"])
        )

        for key, value in ordered_struct.items():
            if "content" in value:
                value["content"] = sorted(value["content"], key=lambda x: x["weigth"])

        self.struct = ordered_struct

    def generate_structure(self):
        weigth = self.get_weigth()
        missing = False
        self.assets = []
        for directory in os.listdir(self.src):
            if (
                os.path.isdir(self.src + directory)
                and directory[0] != "."
                and directory != "www"
            ):
                content = []
                chapter_weigth = 10000000
                for file in os.listdir(self.src + directory):
                    if not os.path.isdir(self.src + directory + "/" + file):
                        try:
                            if weigth[file] < chapter_weigth:
                                chapter_weigth = weigth[file]

                            content.append({"name": file, "weigth": weigth[file]})
                        except:
                            print("Missing file {} in order.txt".format(file))
                            missing = True
                    else:
                        if file == "assets":
                            for f in os.listdir(self.src + directory + "/assets"):
                                self.assets.append(
                                    self.src + directory + "/assets/" + f
                                )
                self.struct[directory] = {"content": content, "weigth": chapter_weigth}

        if missing:
            sys.exit(0)

        self.order_struct()

    def file2name(self, file):
        return " ".join(file.replace(".md", "").split("-")).capitalize().strip()

    def file2link(self, file):
        return file.replace("?", "").replace(".md", ".html")

    def generate_link(self, file):
        name = self.file2name(file)

        return '<a href="{}">{}</a>'.format(self.file2link(file), name)

    def generate_section(self, key, value):
        section = "<section><h2>"
        section += self.file2name(key)
        section += "</h2>"

        for file in value["content"]:
            section += self.generate_link(file["name"])

        section += "</section>"

        return section

    def generate_navigation(self):
        nav = "<nav><section class='title'><h1>{}</h1></section>".format(self.project)
        for key, value in self.struct.items():
            nav += self.generate_section(key, value)
        nav += "</nav>"

        return nav

    def generate_page(self, template, nav, chapter, content):
        name = self.file2name(content)

        with open(self.src + chapter + "/" + content) as f:
            parsed = marko.convert(f.read())

        page = (
            template.replace("<!--title-->", "{} | {}".format(name, self.project))
            .replace("<!--nav-->", nav)
            .replace("<!--content-->", parsed)
        )

        with open(self.www + self.file2link(content), "w") as f:
            f.write(page)

    def generate_index(self, template, nav):
        pass

    def generate_pages(self):
        nav = self.generate_navigation()

        templatefile = "template.html"
        if os.path.exists(self.src + "template.html"):
            templatefile = self.src + "template.html"
        else:
            print("Missing template.html file in the root of the src, use default")
            templatefile = (
                os.path.dirname(os.path.realpath(__file__)) + "/template.html"
            )

        with open(templatefile) as f:
            template = f.read()

        for key, value in self.struct.items():
            for p in value["content"]:
                self.generate_page(template, nav, key, p["name"])

    def move_assets(self):
        for asset in self.assets:
            if os.path.isfile(asset):
                if not os.path.exists(self.www + "assets"):
                    os.makedirs(self.www + "assets")
                shutil.copy(asset, self.www + "assets")
            else:
                print(f"File {asset} does not exist.")
        print("Assets moved successfully.")

    def move_css(self):
        pass

    def move_js(self):
        pass

    def move(self):
        self.move_assets()
        self.move_css()
        self.move_js()

    def generate(self):
        self.generate_structure()
        self.generate_pages()
        self.move()
