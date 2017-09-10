import os
import sys
import csv
from pprint import pprint

from files_dir_mod import *

SPLIT_PHRASE = "NUMBER"


def extract_from_cleaned_perf(src_pathname, dst_pathname):

    title = ['cpu_util', 'cycles_act', 'clkspeed', 'instr_act', 'instr_rate', 'time']

    cpu_util = dict()
    cycles_act = dict()
    clkspeed = dict()
    instr_act = dict()
    instr_rate = dict()
    time = dict()

    with open(src_pathname+'/'+'cycles.txt', 'r') as f:
        run_length = 0
        for row in f: 
            if row[:len(SPLIT_PHRASE)] == SPLIT_PHRASE:
                run_length = int(row.split(':')[-1].strip())
                if run_length not in cycles_act.keys():
                    cycles_act[run_length] = None
                if run_length not in clkspeed.keys():
                    clkspeed[run_length] = None
            else:
                #print run_length
                row_words = row.split()
                row_keywords = [word for word in row_words if word]
                cyc = int(row_keywords[0].replace(',',''))
                clk = float(row_keywords[-2])

                if cycles_act[run_length] == None:
                    cycles_act[run_length] = [cyc]
                else:
                    cycles_act[run_length].append(cyc)

                if clkspeed[run_length] == None:
                    clkspeed[run_length] = [clk]
                else:
                    clkspeed[run_length].append(clk)


    with open(src_pathname+'/'+'instructions.txt', 'r') as f:
        run_length = 0
        for row in f: 
            if row[:len(SPLIT_PHRASE)] == SPLIT_PHRASE:
                run_length = int(row.split(':')[-1].strip())
                if run_length not in instr_act.keys():
                    instr_act[run_length] = None
                if run_length not in instr_rate.keys():
                    instr_rate[run_length] = None
            else:
                #print run_length
                row_words = row.split()
                row_keywords = [word for word in row_words if word]
                ins_act = int(row_keywords[0].replace(',',''))
                ins_rate = float(row_keywords[-4])

                if instr_act[run_length] == None:
                    instr_act[run_length] = [ins_act]
                else:
                    instr_act[run_length].append(ins_act)

                if instr_rate[run_length] == None:
                    instr_rate[run_length] = [ins_rate]
                else:
                    instr_rate[run_length].append(ins_rate)


    with open(src_pathname+'/'+'task_clock.txt', 'r') as f:
        run_length = 0
        for row in f: 
            if row[:len(SPLIT_PHRASE)] == SPLIT_PHRASE:
                run_length = int(row.split(':')[-1].strip())
                if run_length not in cpu_util.keys():
                    cpu_util[run_length] = None
            else:
                #print run_length
                row_words = row.split()
                row_keywords = [word for word in row_words if word]
                cpu = float(row_keywords[-3])

                if cpu_util[run_length] == None:
                    cpu_util[run_length] = [cpu]
                else:
                    cpu_util[run_length].append(cpu)


    with open(src_pathname+'/'+'time.txt', 'r') as f:
        run_length = 0
        for row in f: 
            if row[:len(SPLIT_PHRASE)] == SPLIT_PHRASE:
                run_length = int(row.split(':')[-1].strip())
                if run_length not in time.keys():
                    time[run_length] = None
            else:
                #print run_length
                row_words = row.split()
                row_keywords = [word for word in row_words if word]
                t = float(row_keywords[0])

                if time[run_length] == None:
                    time[run_length] = [t]
                else:
                    time[run_length].append(t)

    run_keys = cpu_util.keys()

    for run in run_keys:
        print run
        data_array = list()
       
        pprint(cycles_act)
        if run in cpu_util.keys() and cpu_util[run]:
            data_array.append(cpu_util[run])
        if run in cycles_act.keys() and cycles_act[run]:
            data_array.append(cycles_act[run])
        if run in clkspeed.keys() and clkspeed[run]:
            data_array.append(clkspeed[run])
        if run in instr_act.keys() and instr_act[run]:
            data_array.append(instr_act[run])
        if run in instr_rate.keys() and instr_rate[run]:
            data_array.append(instr_rate[run])
        if run in time.keys() and time[run]:
            data_array.append(time[run])

        data_array = map(list, zip(*data_array))
        
        #pprint(data_array)

        if data_array:
            out_filename = "timings_" + str(run) + ".csv"
            with open(dst_pathname+'/'+out_filename, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(title)
                for row in data_array:
                    writer.writerow(row)

def clean_gromacs_data(src_path, dst_path):

    for dirname in gromacs_dirs:
        print dirname
        if not os.path.isdir(src_path+'/'+dirname):
            continue

        print dirname.split()
        dir_keywords = dirname.split('/')
        extract_from_cleaned_perf(src_path+'/'+dirname, dst_path+'/'+dirname)

if __name__ == "__main__":
    src_path = sys.argv[1]
    dst_path = sys.argv[2]
    clean_gromacs_data(src_path, dst_path)
