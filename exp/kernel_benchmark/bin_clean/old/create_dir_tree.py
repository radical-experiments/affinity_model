import os
import sys
import json
from pprint import pprint

struct_json = "./dir_struct.json"

dirnames = [
            "adder/laptop/clkspeed_2-6",
            "adder/laptop/clkspeed_3-5",
            "adder/desktop/clkspeed_2-6",
            "adder/desktop/clkspeed_3-5",
            "matmult/laptop/clkspeed_2-6",
            "matmult/laptop/clkspeed_3-5",
            "matmult/desktop/clkspeed_2-6",
            "matmult/desktop/clkspeed_3-5",
            "adder/amarel/shared/compute",
            "adder/amarel/shared/mem",
            "adder/amarel/exclusive/compute",
            "adder/amarel/exclusive/mem",
            "matmult/amarel/shared/compute",
            "matmult/amarel/shared/mem",
            "matmult/amarel/exclusive/compute",
            "matmult/amarel/exclusive/mem"
            ]

def create_dir(pathname, dirs):

    if type(dirs) == list:
        for d in dirs:
            os.mkdir(pathname+'/'+d)
    else:
        for d, subdirs in dirs.iteritems():
            if not os.path.isdir(pathname+'/'+d):
                os.mkdir(pathname+'/'+d)
            create_dir(pathname+'/'+d, subdirs)

def create_dir_tree(dirname):

    root_dir = os.mkdir(dirname)
    dir_struct = dict()
    with open(struct_json, 'r') as j:
        dir_struct = json.load(j)
        pprint(dir_struct)

    create_dir(dirname, dir_struct)


if __name__ == "__main__":
    
    src_tree_rootname = sys.argv[1]
    dst_tree_rootname = sys.argv[2]
    create_dir_tree(tree_rootname)
