import os
import sys
import csv
from pprint import pprint

from files_dir_mod import *

def collect_avg_set1(src_path, kernel):


    if kernel == "adder":
        set1_dirs = set1_adder_dirs
    elif kernel == "matmult":
        set1_dirs = set1_matmult_dirs

    dirs_d = dict()
    num_meas = 0
    for set1_dir in set1_dirs:
        set1_files = sorted(os.listdir(src_path+'/'+set1_dir))
        num_meas = len(set1_files)
        dirs_d[set1_dir] = set1_files

    pprint(dirs_d)

    for m in range(num_meas):
        data_dirs_l = list()
        for set1_dir in set1_dirs:
            fn = dirs_d[list(dirs_d.keys())[0]][0]
            session_keywords = fn.split('.csv')[0].split('_')[-2:]
            session = "_".join(session_keywords)

            is_title_row = 0
            pprint(set1_dir)
            with open(src_path+'/'+set1_dir+'/'+dirs_d[set1_dir][m]) as f:
                reader = csv.reader(f)
                data_dir_l = list()
                for row in reader:
                    if is_title_row:
                        row[0] = row[0] + "__" + session
                    data_dir_l.append(row)
                    is_title_row += 1

            data_dirs_l.append(data_dir_l)
            is_title_row = 0

        pprint(data_dirs_l)
        out_data_l = list()
        out_data_l.append(data_dirs_l[0][0])
        
        for data_dir in data_dirs_l:
            print "\n\n\n"
            for data_row in range(1, len(data_dir)):
                out_data_l.append(data_dir[data_row])
        
        pprint(out_data_l)
        measurement = measurements[m]
        
        with open('plotting_data/set1/'+kernel+'/'+measurement+'.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(out_data_l)
        


if __name__ == "__main__":
    
    src_path = sys.argv[1]
    kernel = sys.argv[2]
    collect_avg_set1(src_path, kernel)
