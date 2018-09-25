import sys
import csv
from pprint import pprint


input_path = sys.argv[1]
path_parts = [path_part for path_part in input_path.split('/') if path_part]
resource = path_parts[-1]

input_dict = dict()

with open(input_path+"/time.txt") as f_in:

    for line in f_in:
        col_split = line.split(':')
        timesteps = 100000
        print col_split
        fields = [field for field in col_split[2].split(' ') if field]
        run_time = fields[1]
        print timesteps, run_time

        if timesteps > 50000 and run_time < 600.0:
            continue
        if timesteps not in input_dict.keys():
            input_dict[timesteps] = [run_time]
        else:
            input_dict[timesteps].append(run_time)

pprint(input_dict)


with open("time__"+resource+".csv", "w") as f_out:

    writer = csv.writer(f_out)
    for timestep, runtime in input_dict.iteritems():
        row = [timestep]
        row.extend(runtime)
        pprint(row)
        writer.writerow(row)
