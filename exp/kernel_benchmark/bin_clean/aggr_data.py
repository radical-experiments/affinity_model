import csv
import os
import sys

from files_dir_mod import *


def aggr_data(src_path, aggr_by_transpose_path, aggr_by_measurement_path, kernel):

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

                    if kernel == "matmult":
                        est_instr = INSTRUCTIONS_MATMULT * num_iter**3
                        pred_cycles = CYCLES_MATMULT * num_iter**3
                        instr_rate_err = abs(instr_rate - INSTR_RATE_MATMULT) / instr_rate * 100.
                    elif kernel == "adder":
                        est_instr = INSTRUCTIONS_ADDER * num_iter
                        pred_cycles = CYCLES_ADDER * num_iter
                        instr_rate_err = abs(instr_rate - INSTR_RATE_ADDER) / instr_rate * 100.
                    
                    est_instr_err = abs(est_instr - instr) / instr * 100.
                    pred_cycles_err = abs(pred_cycles - cycles) / cycles * 100.
                    p2a_ratio = pred_cycles / cycles
                    p2a_instr_rate_err = abs(p2a_ratio - instr_rate) / instr_rate * 100.

                    if kernel == "matmult":
                        cycles_speedup_cpi = instr_rate * CPI_MATMULT
                    elif kernel == "adder":
                        cycles_speedup_cpi = instr_rate * CPI_ADDER
                        
                    p2a_cycles_speedup_err_cpi = abs(p2a_ratio - cycles_speedup_cpi) / cycles_speedup_cpi * 100.

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

                i += 1

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

        data_files.append(data_file)
        with open(aggr_by_transpose_path+'/'+'t_'+ff, 'w') as f:
            writer = csv.writer(f)
            for line in data_file:
                writer.writerow(line)

    for i in range(len(data_files[0])):
        with open(aggr_by_measurement_path+'/'+data_files[0][i][0]+'.csv', 'w') as f:
            writer = csv.writer(f)
            for run_data in data_files:
                run_data[i][0] = int(run_data[8][1])
                writer.writerow(run_data[i])


def aggr_data_all_dir(src_path, transpose_path, measurement_path):

    for dirname in dirnames:
        if not os.path.isdir(src_path+'/'+dirname):
            print "test"
            continue

        dir_keywords = dirname.split('/')
        kernel = dir_keywords[0]
        hostenv = dir_keywords[1]

        if hostenv == "amarel":
            session_dirs = os.listdir(src_path+'/'+dirname)
            for session in session_dirs:
                s_path = src_path + '/' + dirname + '/' + session
                t_path = transpose_path + '/' + dirname + '/' + session
                m_path = measurement_path + '/' + dirname + '/' + session
                aggr_data(s_path, t_path, m_path, kernel)

        elif (hostenv == "laptop") or (hostenv == "desktop"):
            s_path = src_path + '/' + dirname
            t_path = transpose_path + '/' + dirname
            m_path = measurement_path + '/' + dirname
            aggr_data(s_path, t_path, m_path, kernel)



if __name__ == "__main__":
    
   src_path = sys.argv[1]
   transpose_path = sys.argv[2]
   measurement_path = sys.argv[3]
   aggr_data_all_dir(src_path, transpose_path, measurement_path)
   print "test"
