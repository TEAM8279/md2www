from md2www import md2www


if __name__ == "__main__":
    SRC_FOLDER = "../../saturn-documentation/"
    WWW_FOLDER = "../www/"

    m2w = md2www(SRC_FOLDER, WWW_FOLDER, "Project")
    m2w.generate()