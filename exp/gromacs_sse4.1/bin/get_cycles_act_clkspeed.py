import sys
import csv
from pprint import pprint


input_path = sys.argv[1]
path_parts = [path_part for path_part in input_path.split('/') if path_part]
resource = path_parts[-1]

cycles_dict = dict()
clkspeed_dict = dict()

with open(input_path+"/cycles_act__clkspeed.txt") as f_in:

    for line in f_in:
        col_split = line.split(':')
        timesteps = int(col_split[0].split('_')[-1])
        cycles = int("".join(col_split[1].lstrip().split(' ')[0].split(',')))
        clkspeed = float(col_split[1].split('#')[-1].lstrip().split(' ')[0])

        print timesteps, cycles, clkspeed

        if timesteps > 50000 and cycles < 1000000000:
            continue
        if timesteps not in cycles_dict.keys():
            cycles_dict[timesteps] = [cycles]
            clkspeed_dict[timesteps] = [clkspeed]
        else:
            cycles_dict[timesteps].append(cycles)
            clkspeed_dict[timesteps].append(clkspeed)

pprint(cycles_dict)
pprint(clkspeed_dict)

with open("cycles__"+resource+".csv", "w") as f_out:

    writer = csv.writer(f_out)
    for timestep, cycles in cycles_dict.iteritems():
        row = [timestep]
        row.extend(cycles)
        pprint(row)
        writer.writerow(row)

with open("clkspeed__"+resource+".csv", "w") as f_out:

    writer = csv.writer(f_out)
    for timestep, clkspeed in clkspeed_dict.iteritems():
        row = [timestep]
        row.extend(clkspeed)
        pprint(row)
        writer.writerow(row)
