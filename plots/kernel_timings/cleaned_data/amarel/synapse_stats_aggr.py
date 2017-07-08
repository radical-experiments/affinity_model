import os
import sys
import csv

import calc_basic_stats as cbs


pathname = sys.argv[1]
print pathname
file_list = os.listdir(pathname)
print file_list

out_filename = sys.argv[2]

session_id = list()
session_data = list()

with open(pathname+file_list[0], 'r') as f:
    for row in f:
        row_data = row.split(',')
        session_id.append(int(row_data[0]))
        session_data.append(map(float, row_data[1:]))

output_data = [[out_filename, 'Average', 'Std', 'CI']]
for i in range(len(session_id)):
    mean = cbs.average(session_data[i])
    samp_stdev = cbs.samp_std_dev(session_data[i])
    conf_intv = cbs.conf_interval(session_data[i])

    entry_data = [session_id[i], mean, samp_stdev, conf_intv]
    output_data.append(entry_data)

output_data = map(list, zip(*output_data))

with open(out_filename+".csv", 'w') as f:
    writer = csv.writer(f)
    for row in output_data:
        writer.writerow(row)
