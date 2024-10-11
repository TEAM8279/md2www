from md2www import md2www


if __name__ == "__main__":
    SRC_FOLDER = "/home/tom/git/saturn-documentation/"
    WWW_FOLDER = "/home/tom/git/saturn-documentation/www/"

    m2w = md2www(SRC_FOLDER, WWW_FOLDER, "Saturn documentation")
    m2w.generate()
