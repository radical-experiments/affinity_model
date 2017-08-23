import os
import sys
import csv
from pprint import pprint

import calc_basic_stats as cbs
from files_dir_mod import *


def data_stats(src_path, dst_path, session):

    file_list = os.listdir(src_path)

    for filename in file_list:
        measurement = filename.split('.')[0]
        output_data = list()
        num_cycles = list()
        num_cycles_data = list()
        with open(src_path+'/'+filename, 'r') as f:
            for row in f:
                row_data = row.strip().split(',')
                row_data = [entry for entry in row_data if entry]
                num_cycles.append(int(row_data[0]))
                num_cycles_data.append(map(float, row_data[1:]))

        title_data = [measurement, 'Average', 'Std', 'CI']
        output_data = list()
        for i in range(len(num_cycles)):
            if len(num_cycles_data[i]) == 1:
                continue
            mean = cbs.average(num_cycles_data[i])
            samp_stdev = cbs.samp_std_dev(num_cycles_data[i])
            conf_intv = cbs.conf_interval(num_cycles_data[i])

            entry_data = [num_cycles[i], mean, samp_stdev, conf_intv]
            output_data.append(entry_data)

        output_data.sort(key=lambda x: x[0])
        output_data.insert(0, title_data)
        write_data = map(list, zip(*output_data))
        #pprint.pprint(write_data)

        with open(dst_path+'/'+"avg_"+measurement+"_"+session+".csv", 'w') as f:
            pprint(measurement+"_"+session)
            writer = csv.writer(f)
            writer.writerows(write_data)
#            for row in write_data:
#                pprint.pprint(row)
#                writer.writerow(row)


def data_stats_all(src_path, dst_path):

    for dirname in gromacs_dirs:
        if not os.path.isdir(src_path+'/'+dirname):
            continue

        dir_keywords = dirname.split('/')
        hostname = dir_keywords[1]
        session = dir_keywords[-1]

        pprint(dirname)
        for measurement in measurements:
            data_stats(src_path+'/'+dirname+'/', dst_path+'/'+dirname, session)


if __name__ == "__main__":

    src_path = sys.argv[1]
    dst_path = sys.argv[2]
    data_stats_all(src_path, dst_path)
