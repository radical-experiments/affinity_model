import os
import sys
import csv
from pprint import pprint

from files_dir_mod import *

def collect_avg_gromacs(src_path):

    dirs_d = dict()
    num_meas = len(measurements)
    num_sessions = dict()
    for set3_dir in set3_dirs:
        if not os.path.exists(src_path+'/'+set3_dir):
            print src_path+'/'+set3_dir
            continue
        set3_files = sorted(os.listdir(src_path+'/'+set3_dir))
        if len(set3_files) > 0:
            dirs_d[set3_dir] = [f for f in set3_files if os.path.isdir(src_path+'/'+set3_dir+'/'+f)]
            num_sessions[set3_dir] = len(dirs_d[set3_dir])
        #print dirs_d[set3_dir]

    #pprint(dirs_d)
    #pprint(num_sessions)
    for m in range(num_meas):
        for set3_dir in dirs_d.keys():
            data_dirs_l = list()
            dir_keywords = set3_dir.split('/')
            node_type = dir_keywords[-1]
            num_ses_dir = num_sessions[set3_dir]
            
            #pprint(node_type)
            #pprint(num_ses_dir)
            for sidx in range(num_ses_dir):
                
                #pprint(dirs_d[set3_dir]) 
                #print dirs_d[set3_dir][sidx]
                #fn = dirs_d[set3_dir][m * num_ses_dir + sidx]
                fn = 'avg_' + measurements[m] + "_run_" + str(sidx+1) + ".csv"
                src_file_path = src_path+'/'+set3_dir+'/'+dirs_d[set3_dir][sidx] + '/' + fn

                pprint(fn)
                pprint(src_file_path)
                #continue

                dir_keywords = set3_dir.split('/')
                #node_type = dir_keywords[2][:3]

                #pprint(dir_keywords)
                #pprint(node_type)

                tmp = fn.split('.csv')[0].split('_')
                session = tmp[-1]
                print session
                meas_filename = "_".join(tmp[:-1])
                #print meas_filename, session

                is_title_row = 0
                #pprint(set3_dir)
            

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
        
            pprint(out_data_l)
            pprint(measurements)
            print(num_meas)
            measurement = measurements[m]
            
            outfile_name = node_type + '/' + measurement + '.csv'
            with open('plotting_data/set3/gromacs/'+outfile_name, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(out_data_l)
        

def collect_avg(src_path):
    collect_avg_gromacs(src_path)


if __name__ == "__main__":
    
    src_path = sys.argv[1]
    collect_avg(src_path)
