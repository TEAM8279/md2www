import sys
from md2www import md2www

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <src_folder> <www_folder> <project name>")
        sys.exit(1)

    SRC_FOLDER = sys.argv[1]
    WWW_FOLDER = sys.argv[2]
    NAME = sys.argv[3]

    m2w = md2www(SRC_FOLDER, WWW_FOLDER, NAME)
    m2w.generate()
