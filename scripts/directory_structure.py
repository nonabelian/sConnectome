import os
import sys


def create_dstruct(root, level=0):
    tree = root + "\n"
    for d, subdirs, files in os.walk(root):
        dlist = d.split(os.sep)

        if "" in dlist:
            dlist.remove('')

        level = len(dlist)-1

        head = dlist[-1]

        if level > 0:
            tree += "|" + "    " * (level-1) + "+--" + head + "/\n"

        for f in files:
            tree += "|" + "    " * level + "+--" + f + "\n"

    return tree


def usage():
    print 'USAGE:'
    print '\t\tpython directory_structure.py <filename>\n\n'


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "Error: Must pass an argument"
        usage()
        sys.exit()

    if not isinstance(sys.argv[1], str):
        print "Error: Must pass a string"
        usage()
        sys.exit()

    path = sys.argv[1]

    if not os.path.exists(path):
        print "Error: Path does not exist!"
        usage()
        sys.exit()

    dir_tree = create_dstruct(path)

    print dir_tree
