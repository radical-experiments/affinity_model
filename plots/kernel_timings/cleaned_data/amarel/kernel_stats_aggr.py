import os
import sys
import csv
import pprint

import calc_basic_stats as cbs


pathname = sys.argv[1]
print pathname
file_list = os.listdir(pathname)
print file_list

out_filename = sys.argv[2]

for filename in file_list:
    session_number = filename.split(".csv")[0].split('_')[-1]
    output_data = list()
    num_cycles = list()
    num_cycles_data = list()
    with open(pathname+filename, 'r') as f:
        for row in f:
            row_data = row.split(',')
            num_cycles.append(int(row_data[0]))
            num_cycles_data.append(map(float, row_data[1:]))

    title_data = [out_filename, 'Average', 'Std', 'CI']
    output_data = list()
    for i in range(len(num_cycles)):
        mean = cbs.average(num_cycles_data[i])
        samp_stdev = cbs.samp_std_dev(num_cycles_data[i])
        conf_intv = cbs.conf_interval(num_cycles_data[i])

        entry_data = [num_cycles[i], mean, samp_stdev, conf_intv]
        output_data.append(entry_data)

    output_data.sort(key=lambda x: x[0])
    output_data.insert(0, title_data)
    write_data = map(list, zip(*output_data))
    pprint.pprint(write_data)

    with open(out_filename+"_"+session_number+".csv", 'w') as f:
        writer = csv.writer(f)
        for row in write_data:
            writer.writerow(row)
