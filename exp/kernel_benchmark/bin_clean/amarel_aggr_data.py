import os
import sys
import csv
from pprint import pprint

from files_dir_mod import *


def amarel_aggregate(src_path, dst_path):

    for dirname in dirnames:
        if not os.path.isdir(src_path+'/'+dirname):
            print "{0} does not exist".format(dirname)
            continue

        dir_keywords = dirname.split('/')
        pprint(dir_keywords)

        machine = dir_keywords[1]
        if machine != "amarel":
            continue

        dir_list = os.listdir(src_path+'/'+dirname)
        if dir_list:
            kernel = dir_keywords[0]
            node_type = dir_keywords[2]
            usage = dir_keywords[3]

            for meas in measurements:
                fd_out = open(dst_path+'/'+dirname+'/'+meas+'.csv', 'w')
                writer = csv.writer(fd_out)

                for session in dir_list:
                    with open(src_path+'/'+dirname+'/'+session+'/'+meas+'.csv') as fd_in:
                        reader = csv.reader(fd_in)
                        for row in reader:
                            cleaned_row = row
                            cleaned_row[0] = session + "__" + cleaned_row[0]
                            writer.writerow(cleaned_row)
                fd_out.close()


            pprint(dirname)
            pprint(dir_list)

            

if __name__ == "__main__":
    
    src_path = sys.argv[1]
    dst_path = sys.argv[2]
    amarel_aggregate(src_path, dst_path)

