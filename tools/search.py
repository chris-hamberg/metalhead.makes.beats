import sys
import os


IGNORE = ["git", "__pycache__", ".db", "tools", "swp", "anaconda3"]


def search(term):
    for root, directories, files in os.walk("."):
        for file in files:
            try:
                path = os.path.join(root, file)
                for flag in IGNORE:
                    assert not flag in path
            except AssertionError:
                continue
            else:
                line_no = 1 

                try:
                    with open(path, "r") as fhand:
                        for line in fhand:
                            if term in line:
                                print(f" line #{line_no}: {path}")
                            line_no += 1
                except UnicodeDecodeError:
                    continue

if __name__ == "__main__":
    term = sys.argv[1]
    search(term)
