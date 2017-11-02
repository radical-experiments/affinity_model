import sys
import csv
from pprint import pprint


input_path = sys.argv[1]
path_parts = [path_part for path_part in input_path.split('/') if path_part]
resource = path_parts[-1]

instr_dict = dict()
instr_rate_dict = dict()

with open(input_path+"/instr_act__instr_rate.txt") as f_in:

    for line in f_in:
        col_split = line.split(':')
        timesteps = int(col_split[0].split('_')[-1].split('.')[0])
        instr = int("".join(col_split[1].lstrip().split(' ')[0].split(',')))
        instr_rate = float(col_split[1].split('#')[-1].lstrip().split(' ')[0])

        print timesteps, instr, instr_rate

        if timesteps > 50000 and instr < 1000000000:
            continue
        if timesteps not in instr_dict.keys():
            instr_dict[timesteps] = [instr]
            instr_rate_dict[timesteps] = [instr_rate]
        else:
            instr_dict[timesteps].append(instr)
            instr_rate_dict[timesteps].append(instr_rate)

pprint(instr_dict)
pprint(instr_rate_dict)

with open("instr_act__"+resource+".csv", "w") as f_out:

    writer = csv.writer(f_out)
    for timestep, instr in instr_dict.iteritems():
        row = [timestep]
        row.extend(instr)
        pprint(row)
        writer.writerow(row)

with open("instr_rate__"+resource+".csv", "w") as f_out:

    writer = csv.writer(f_out)
    for timestep, instr_rate in instr_rate_dict.iteritems():
        row = [timestep]
        row.extend(instr_rate)
        pprint(row)
        writer.writerow(row)
