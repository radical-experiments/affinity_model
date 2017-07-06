import csv
import os
import sys

path = sys.argv[1]
files = os.listdir(sys.argv[1])

data_files = list()
session_id_l = list()

for ff in files:
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


    with open(path+ff, 'r') as f:
        session_name = float(ff.split('_')[-1].split('.')[0])
        session_id_l.append(session_name)
        print sys.argv
        number_of_cycles = float(sys.argv[2])
        print number_of_cycles
        num_iter = number_of_cycles / 8
        i = 0
        for row in f:
            title = row.split(',')
            if i == 0:
                utils_l = [title[0]]
                cycles_l = [title[1]]
                clk_speed_l = [title[2]]
                instr_l = [title[3]]
                instr_rate_l = [title[4]]
                time_l = [title[5]]
                est_instr_l = ['estimated number of instructions']
                est_instr_err_l = ['instruction calculation error']
                pred_cycles_l = ['predicted cycles']
                pred_cycles_err_l = ['cycles prediction error']
                p2a_ratio_l = ['prediction to actual cycles']
                p2a_instr_rate_err_l = ['p2a ratio to instruction rate error']

            else:
                row_data = row.split(',')
                utils = float(row_data[0])
                cycles = float(row_data[1])
                clk_speed = float(row_data[2])
                instr = float(row_data[3])
                instr_rate = float(row_data[4])
                time = float(row_data[5])
                est_instr = instr_rate * cycles
                est_instr_err = (est_instr - instr) / instr
                pred_cycles = 8. * num_iter
                pred_cycles_err = (pred_cycles - cycles) / pred_cycles
                p2a_ratio = pred_cycles / cycles
                p2a_instr_rate_err = (p2a_ratio - instr_rate) / instr_rate

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

	data_files.append(data_file)
	with open(path+'t_'+ff, 'w') as f:
		writer = csv.writer(f)
		for line in data_file:
			writer.writerow(line)

from pprint import pprint
pprint(data_files[0])

for i in range(len(data_files[0])):
    session_id_counter = 0
    with open(path+data_files[0][i][0]+'.csv', 'w') as f:
        print data_files[0][i][0]
        writer = csv.writer(f)
        for run_data in data_files:
            #print run_data
            #print session_id_l
            run_data[i][0] = int(session_id_l[session_id_counter])
            writer.writerow(run_data[i])
            session_id_counter += 1
