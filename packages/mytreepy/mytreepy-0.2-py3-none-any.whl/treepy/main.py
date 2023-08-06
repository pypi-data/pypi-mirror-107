import os
import sys
import argparse

class Tree:
    def __init__(self, target_level=99):
        self.dirCount = 0
        self.fileCount = 0
        self.targetLevel = target_level

    def title(self, directory):
        return os.path.basename(os.path.abspath(directory))

    def register(self, absolute):
        if os.path.isdir(absolute):
            self.dirCount += 1
        else:
            self.fileCount += 1

    def summary(self):
        return str(self.dirCount) + " directories, " + str(self.fileCount) + " files"

    def walk(self, directory, prefix = "", level = 0):
        if level >= self.targetLevel:
            return
        
        filepaths = sorted([filepath for filepath in os.listdir(directory)])

        for index in range(len(filepaths)):
            if filepaths[index][0] == ".":
                continue

            absolute = os.path.join(directory, filepaths[index])
            self.register(absolute)

            if index == len(filepaths) - 1:
                print(prefix + "└── " + filepaths[index])
                if os.path.isdir(absolute):
                    self.walk(absolute, prefix + "    ", level+1)
            else:
                print(prefix + "├── " + filepaths[index])
                if os.path.isdir(absolute):
                    self.walk(absolute, prefix + "│   ", level+1)

def main():
    parser = argparse.ArgumentParser(description='tree')
    parser.add_argument('directory_list', help='directory list', nargs="?", default=".")
    parser.add_argument('-L', metavar="LEVEL", type=int, help='Descend only level directories deep.')
    args = parser.parse_args()

    if args.L is not None:
        tree = Tree(args.L)
    else:
        tree = Tree()

    print(tree.title(args.directory_list))
    tree.walk(args.directory_list)
    print("\n" + tree.summary())

if __name__ == "__main__":
    main()