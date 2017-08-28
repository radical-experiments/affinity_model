import csv
import os
import sys
from pprint import pprint

from files_dir_mod import *


avg_instr_d = dict()
avg_cycles_d = dict()


def aggr_data(src_path, aggr_by_transpose_path, aggr_by_measurement_path, create_avg_dicts=False, cycles_to_iter=None):

    files = os.listdir(src_path)
    data_files = list()

    for ff in files:

        if not ff.startswith("timings_"):
            continue
        data_file = list()
        title = list()
        utils_l = list()
        cycles_l = list()
        clk_speed_l = list()
        instr_l = list()
        instr_rate_l = list()
        time_l = list()
        est_instr_l = list()
        est_instr_err_l = list()
        pred_cycles_l = list()
        pred_cycles_err_l = list()
        p2a_ratio_l = list()
        p2a_instr_rate_err_l = list() 
        instr_rate_err_l = list()
        cycles_speedup_cpi_l = list()
        p2a_cycles_speedup_err_cpi_l = list() 

        with open(src_path+'/'+ff, 'r') as f:
            num_iter = float(ff.split('_')[-1].split('.')[0])
            if num_iter > 100000.:
                continue

            i = 0
            for row in f:
                title = row.split(',')
                if i == 0:
                    utils_l = [title[0]]
                    cycles_l = [title[1]]
                    clk_speed_l = [title[2]]
                    instr_l = [title[3]]
                    instr_rate_l = [title[4]]
                    time_l = [title[5].strip()]
                    est_instr_l = ['instr_pred']
                    est_instr_err_l = ['instr_prederr']
                    pred_cycles_l = ['cycles_pred']
                    pred_cycles_err_l = ['cycles_prederr']
                    p2a_ratio_l = ['p2a_cycles']
                    p2a_instr_rate_err_l = ['p2a_cycles_prederr']
                    instr_rate_err_l = ['instr_rate_prederr']
                    cycles_speedup_cpi_l = ['cycles_speedup_cpi_adj']
                    p2a_cycles_speedup_err_cpi_l = ['p2a_cycles_speedup_prederr_cpi_adj']

                else:
                    row_data = row.split(',')
                    utils = float(row_data[0])
                    cycles = float(row_data[1])
                    clk_speed = float(row_data[2])
                    instr = float(row_data[3])
                    instr_rate = float(row_data[4])
                    time = float(row_data[5])
                    
                    if time <= 1.0:
                        continue

                    if not avg_instr_d or int(num_iter) not in avg_instr_d or type(avg_instr_d[int(num_iter)]) != float:
                        est_instr = -1
                        est_instr_err = -1
                    else:
                        est_instr = avg_instr_d[int(num_iter)]
                        est_instr_err = abs(est_instr - instr) / instr * 100.

                    if not avg_cycles_d or int(num_iter) not in avg_cycles_d or type(avg_cycles_d[int(num_iter)]) != float:
                        pred_cycles = int(num_iter)
                        pred_cycles_err = -1
                        p2a_ratio = -1
                        p2a_instr_rate_err = -1
                    else:
                        pred_cycles = avg_cycles_d[num_iter]
                        pred_cycles_err = abs(pred_cycles - cycles) / cycles * 100.
                        p2a_ratio = pred_cycles / cycles
                        p2a_instr_rate_err = abs(p2a_ratio - instr_rate) / p2a_ratio * 100

                    instr_rate_err = -1
                    cycles_speedup_cpi = -1
                        
                    #p2a_cycles_speedup_err_cpi = abs(p2a_ratio - cycles_speedup_cpi) / cycles_speedup_cpi * 100.
                    p2a_cycles_speedup_err_cpi = -1

                    utils_l.append(utils)
                    cycles_l.append(cycles)
                    clk_speed_l.append(clk_speed)
                    instr_l.append(instr)
                    instr_rate_l.append(instr_rate)
                    time_l.append(time)
                    est_instr_l.append(est_instr)
                    est_instr_err_l.append(est_instr_err)
                    pred_cycles_l.append(pred_cycles)
                    pred_cycles_err_l.append(pred_cycles_err)
                    p2a_ratio_l.append(p2a_ratio)
                    p2a_instr_rate_err_l.append(p2a_instr_rate_err)
                    instr_rate_err_l.append(instr_rate_err)
                    cycles_speedup_cpi_l.append(cycles_speedup_cpi)
                    p2a_cycles_speedup_err_cpi_l.append(p2a_cycles_speedup_err_cpi)

                    num_iter_key = int(num_iter)
                    if create_avg_dicts:
                        if num_iter_key not in avg_cycles_d.keys():
                            avg_cycles_d[num_iter_key] = [cycles * instr_rate]
                        else:
                            avg_cycles_d[num_iter_key].append(cycles * instr_rate)

                        if num_iter_key not in avg_instr_d.keys():
                            avg_instr_d[num_iter_key] = [instr]
                        else:
                            avg_instr_d[num_iter_key].append(instr)

                i += 1

        #pprint(int(num_iter))

        data_file.append(utils_l)
        data_file.append(cycles_l)
        data_file.append(clk_speed_l)
        data_file.append(instr_l)
        data_file.append(instr_rate_l)
        data_file.append(time_l)
        data_file.append(est_instr_l)
        data_file.append(est_instr_err_l)
        data_file.append(pred_cycles_l)
        data_file.append(pred_cycles_err_l)
        data_file.append(p2a_ratio_l)
        data_file.append(p2a_instr_rate_err_l)
        data_file.append(instr_rate_err_l)
        data_file.append(cycles_speedup_cpi_l)
        data_file.append(p2a_cycles_speedup_err_cpi_l)
        
        #pprint(data_file)

        data_files.append(data_file)

        #num_iter_key = int(num_iter)
        #if create_avg_dicts:
        #    if num_iter_key not in avg_cycles_d.keys():
        #        if len(cycles_l) > 1:
        #            avg_cycles_d[num_iter_key] = [(sum(cycles_l[1:]), len(cycles_l)-1)]
        #    else:
        #        avg_cycles_d[num_iter_key].append((sum(cycles_l[1:]), len(cycles_l)-1))
        #    
        #    if num_iter_key not in avg_instr_d.keys():
        #        if len(instr_l) > 1:
        #            avg_instr_d[num_iter_key] = [(sum(instr_l[1:]), len(instr_l)-1)]
        #    else:
        #        avg_instr_d[num_iter_key].append((sum(instr_l[1:]), len(instr_l)-1))

        #pprint(data_file[0])
        if len(data_file) > 1:
            with open(aggr_by_transpose_path+'/'+'t_'+ff, 'w') as f:
                writer = csv.writer(f)
                for line in data_file:
                    writer.writerow(line)

    #pprint(data_files)
    for i in range(len(data_files[0])):
        #pprint(data_files)
        with open(aggr_by_measurement_path+'/'+data_files[0][i][0]+'.csv', 'w') as f:
            writer = csv.writer(f)
            for run_data in data_files:
                if len(run_data[8]) > 1:
                    if not cycles_to_iter:
                        run_data[i][0] = int(run_data[8][1])
                    else:
                        pprint(cycles_to_iter)
                        print int(run_data[8][1])
                        run_data[i][0] = cycles_to_iter[int(run_data[8][1])]
                    print run_data[i][0]
                    writer.writerow(run_data[i])


def aggr_data_all_dir(src_path, transpose_path, measurement_path):

    amarel_dirnames = [dirname for dirname in gromacs_dirs if "amarel" in dirname and "compute" in dirname]
    pprint(amarel_dirnames)
    not_amarel_dirnames = [dirname for dirname in gromacs_dirs if not ("amarel" in dirname and "compute" in dirname)]
    pprint(not_amarel_dirnames)

    for dirname in amarel_dirnames:
        if not os.path.isdir(src_path+'/'+dirname):
            print "test"
            continue

        dir_keywords = dirname.split('/')
        kernel = dir_keywords[0]
        hostenv = dir_keywords[1]

        s_path = src_path + '/' + dirname
        t_path = transpose_path + '/' + dirname
        m_path = measurement_path + '/' + dirname
        aggr_data(s_path, t_path, m_path, create_avg_dicts=True)

    pprint(avg_cycles_d)
    pprint(avg_instr_d)

    for key, sum_list in avg_cycles_d.iteritems():
        total_sum = sum(sum_list)
        count = len(sum_list)
        average = total_sum / count
        avg_cycles_d[key] = average

    for key, sum_list in avg_instr_d.iteritems():
        total_sum = sum(sum_list)
        count = len(sum_list)
        average = total_sum / count
        avg_instr_d[key] = average

    pprint(avg_cycles_d)
    pprint(avg_instr_d)

    cycles_to_iter_map = {int(v): k for k, v in avg_cycles_d.iteritems()}
    pprint(cycles_to_iter_map)
    #sys.exit()

    for dirname in not_amarel_dirnames:
        if not os.path.isdir(src_path+'/'+dirname):
            print "test"
            continue

        dir_keywords = dirname.split('/')
        kernel = dir_keywords[0]
        hostenv = dir_keywords[1]

        s_path = src_path + '/' + dirname
        t_path = transpose_path + '/' + dirname
        m_path = measurement_path + '/' + dirname
        aggr_data(s_path, t_path, m_path, cycles_to_iter=cycles_to_iter_map)



if __name__ == "__main__":
    
   src_path = sys.argv[1]
   transpose_path = sys.argv[2]
   measurement_path = sys.argv[3]
   aggr_data_all_dir(src_path, transpose_path, measurement_path)
   print "test"
