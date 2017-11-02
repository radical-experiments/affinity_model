import sys
import csv
from pprint import pprint


input_path = sys.argv[1]
path_parts = [path_part for path_part in input_path.split('/') if path_part]
resource = path_parts[-1]

input_dict = dict()

with open(input_path+"/cpu_util.txt") as f_in:

    for line in f_in:
        col_split = line.split(':')
        timesteps = int(col_split[0].split('_')[-1].split('.')[0])
        cpu_util = float(col_split[1].lstrip().split('#')[1].lstrip().split(' ')[0])
        print timesteps, cpu_util

        if timesteps > 50000 and cpu_util < 0.9:
            continue
        if timesteps not in input_dict.keys():
            input_dict[timesteps] = [cpu_util]
        else:
            input_dict[timesteps].append(cpu_util)

pprint(input_dict)


with open("cpu_util__"+resource+".csv", "w") as f_out:

    writer = csv.writer(f_out)
    for timestep, util in input_dict.iteritems():
        row = [timestep]
        row.extend(util)
        pprint(row)
        writer.writerow(row)
