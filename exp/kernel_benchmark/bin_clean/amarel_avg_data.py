import os
import sys
import csv
from pprint import pprint
from operator import itemgetter

import calc_basic_stats as cbs
from files_dir_mod import *



def data_stats_amarel(src_path, dst_path, kernel):

    for meas in measurements:
        has_title = 0

        fd_out = open(dst_path+'/'+kernel+'_'+meas+'.csv', 'w') 
        writer = csv.writer(fd_out)

        for dirname in dirnames:
            if not os.path.isdir(src_path+'/'+dirname):
                continue
            
            if not os.listdir(src_path+'/'+dirname):
                continue

            dir_keywords = dirname.split('/')
            
            if kernel != dir_keywords[0]:
                continue

            node_type = dir_keywords[-2]
            usage = dir_keywords[-1]

            data_list = list()
            with open(src_path+'/'+dirname+'/'+meas+'.csv') as f:
                reader = csv.reader(f)
                for row in reader:
                    data_list.append(row)

            pprint(data_list)

            data_aggr_run = dict()
            for data_row in data_list:
                iter_num = int(data_row[0].split('__')[-1])
                if iter_num in data_aggr_run.keys():
                    data_aggr_run[iter_num].extend(map(float, data_row[1:]))
                else:
                    data_aggr_run[iter_num] = map(float, data_row[1:])
            
            #pprint(data_aggr_run)

            data_stats = list()
            for iter_num, iter_data in data_aggr_run.iteritems():
                minimum = min(iter_data)
                maximum = max(iter_data)
                rng = maximum - minimum
                avg = cbs.average(iter_data)
                std = cbs.samp_std_dev(iter_data)
                ci = cbs.conf_interval(iter_data)
                count = len(iter_data)
                data_stats.append([iter_num, minimum, maximum, rng, avg, std, ci, count])

            
            data_stats = sorted(data_stats, key=itemgetter(0))
            data_stats = zip(*data_stats)
            data_stats = map(list, data_stats)
            
            pprint(data_stats)
            data_stats[0].insert(0, meas)
            data_stats[1].insert(0, "min" + "__" + node_type[:3] + "_" + usage[:3])
            data_stats[2].insert(0, "max" + "__" + node_type[:3] + "_" + usage[:3])
            data_stats[3].insert(0, "range" + "__" + node_type[:3] + "_" + usage[:3])
            data_stats[4].insert(0, "avg" + "__" + node_type[:3] + "_" + usage[:3])
            data_stats[5].insert(0, "std" + "__" + node_type[:3] + "_" + usage[:3])
            data_stats[6].insert(0, "ci" + "__" + node_type[:3] + "_" + usage[:3])
            data_stats[7].insert(0, "count" + "__" + node_type[:3] + "_" + usage[:3])

            pprint(data_stats)

            if has_title:
                writer.writerows(data_stats[1:])
            else:
                writer.writerows(data_stats)

            has_title += 1

        fd_out.close()



def data_stats_amarel_all(src_path, dst_path):
    
    kernel_list = ['adder', 'matmult']
    for kernel in kernel_list:
        data_stats_amarel(src_path, dst_path, kernel)



if __name__ == '__main__':

    src_path = sys.argv[1]
    dst_path = sys.argv[2]
    data_stats_amarel_all(src_path, dst_path)
