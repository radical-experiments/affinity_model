import os
import sys

filename = sys.argv[1]

data_array = list()
title = ['CPU utilized', 'cycles', 'clock speed', 'instructions', 'instructions per cycle','time (s)']
data_array.append(title)

with open(filename, 'r') as f:

    txt_block = 14
    cpu_utilized = 3
    cycles = 7
    instructions = 8
    time = 12

    i = 0
    for row in f:
        if (row != '' and row != '\n') and i == 0:
            #txt_block -= 1
            cpu_utilized -= 1
            cycles -= 1
            instructions -= 1
            time -= 1
            print "enters once\n"

        tmp_row = row.strip()
        if i % txt_block == 0:
            tmp_list = list()

        if i % txt_block == cpu_utilized:
            pass
            #print tmp_row
            #print tmp_row.split('#')[1]
            cpu_util = row.strip().split('#')[1].lstrip().split()[0]
            tmp_list.append(float(cpu_util))

        if i % txt_block == cycles:
            cycles_str = tmp_row.split('#')
            #print row.strip()
            total_cycles_commas = cycles_str[0].rstrip().split()[0]
            split_comma = total_cycles_commas.split(',')
            total_cycles = ''.join(split_comma)
            #print i
            #print total_cycles
            #print cycles_str
            clock_speed = cycles_str[1].lstrip().split()[0]
            #print clock_speed
            tmp_list.append(int(total_cycles))
            tmp_list.append(float(clock_speed))

        if i % txt_block == instructions:
            instr_str = tmp_row.split('#')
            total_instr_comma = instr_str[0].lstrip().split()[0]
            split_comma = total_instr_comma.split(',')
            total_instr = ''.join(split_comma)
            instr_rate = instr_str[1].rstrip().split()[0]
            tmp_list.append(int(total_instr))
            tmp_list.append(float(instr_rate))

        if i % txt_block == time:
            run_time = tmp_row.split()[0]
            tmp_list.append(float(run_time))

        if i % txt_block == (txt_block - 1):
            data_array.append(tmp_list)
        
        i += 1

#from pprint import pprint
#pprint(data_array)

num_iterations = filename.split('/')[-1].split('_')[-1]
#print num_iterations

out_filename = "timings_" + num_iterations + ".csv"

import csv
with open(out_filename, 'w') as f:
    writer = csv.writer(f)
    for row in data_array:
        writer.writerow(row)
    
