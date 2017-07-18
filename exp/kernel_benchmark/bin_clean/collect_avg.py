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
            fn = dirs_d[set1_dir][0]
            session_keywords = fn.split('.csv')[0].split('_')[-2:]
            session = "_".join(session_keywords)
            #print fn
            #print session

            is_title_row = 0
            #pprint(set1_dir)
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

        #pprint(data_dirs_l)
        out_data_l = list()
        out_data_l.append(data_dirs_l[0][0])
        
        for data_dir in data_dirs_l:
            for data_row in range(1, len(data_dir)):
                out_data_l.append(data_dir[data_row])
        
        #pprint(out_data_l)
        measurement = measurements[m]
        
        with open('plotting_data/set1/'+kernel+'/'+measurement+'.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(out_data_l)
        


def collect_avg_set2(src_path, kernel):

    if kernel == "adder":
        set2_dirs = set2_adder_dirs
    elif kernel == "matmult":
        set2_dirs = set2_matmult_dirs

    dirs_d = dict()
    num_meas = len(measurements)
    num_sessions = dict()
    for set2_dir in set2_dirs:
        if not os.path.exists(src_path+'/'+set2_dir):
            print src_path+'/'+set2_dir
            continue
        set2_files = sorted(os.listdir(src_path+'/'+set2_dir))
        if len(set2_files) > 0:
            dirs_d[set2_dir] = [f for f in set2_files if not os.path.isdir(src_path+'/'+set2_dir+'/'+f)]
            num_session = len(dirs_d[set2_dir]) / num_meas
            num_sessions[set2_dir] = num_session
        #print dirs_d[set2_dir]

    pprint(num_sessions)
    for m in range(num_meas):
        for set2_dir in dirs_d.keys():
            data_dirs_l = list()
            dir_keywords = set2_dir.split('/')
            node_type = dir_keywords[2][:3]
            tenancy = dir_keywords[3][:3]

            num_ses_dir = num_sessions[set2_dir]
            print num_ses_dir
            for sidx in range(num_ses_dir):
                
                print dirs_d[set2_dir][m * num_ses_dir + sidx]
                fn = dirs_d[set2_dir][m * num_ses_dir + sidx]
                src_file_path = src_path+'/'+set2_dir+'/'+dirs_d[set2_dir][m * num_ses_dir + sidx]

                dir_keywords = set2_dir.split('/')
                node_type = dir_keywords[2][:3]
                tenancy = dir_keywords[3][:3]

                tmp = fn.split('.csv')[0].split('_')
                session = tmp[-1]
                print session
                meas_filename = "_".join(tmp[:-1])
                #print meas_filename, session

                is_title_row = 0
                #pprint(set2_dir)
            

                with open(src_file_path) as f:
                    #print src_file_path
                    reader = csv.reader(f)
                    data_dir_l = list()
                    for row in reader:
                        if is_title_row:
                            row[0] = row[0] + "__" + session
                        data_dir_l.append(row)
                        is_title_row += 1

                data_dirs_l.append(data_dir_l)
                is_title_row = 0

            #pprint(data_dirs_l)
            out_data_l = list()
            out_data_l.append(data_dirs_l[0][0])
        
            for data_dir in data_dirs_l:
                #print "\n\n\n"
                for data_row in range(1, len(data_dir)):
                    out_data_l.append(data_dir[data_row])
        
            #pprint(out_data_l)
            #pprint(measurements)
            #print(num_meas)
            measurement = measurements[m]
            
            outfile_name = kernel+'/'+node_type+'_'+tenancy+'_'+measurement+'.csv'
            with open('plotting_data/set2/'+outfile_name, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(out_data_l)
        


def collect_avg(src_path, kernel, setting):
    if setting == '1':
        collect_avg_set1(src_path, kernel)
    elif setting == '2':
        collect_avg_set2(src_path, kernel)



if __name__ == "__main__":
    
    src_path = sys.argv[1]
    kernel = sys.argv[2]
    setting = sys.argv[3]
    collect_avg(src_path, kernel, setting)
