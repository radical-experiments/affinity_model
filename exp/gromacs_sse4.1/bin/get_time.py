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
        #timesteps = int(col_split[0].split('_')[-1].split('.')[0])
        timesteps = int(col_split[0].split('/')[0].split('_')[-1])
        #run_time = float(col_split[1].lstrip().split(' ')[0])
        print col_split
        run_time = float([elem for elem in col_split[2].lstrip().split(' ') if elem][1])
        print timesteps, run_time

        if timesteps > 50000 and run_time < 600.0:
            continue
        if timesteps not in input_dict.keys():
            input_dict[timesteps] = [run_time]
        else:
            input_dict[timesteps].append(run_time)

#pprint(input_dict)


with open("time__"+resource+".csv", "w") as f_out:

    writer = csv.writer(f_out)
    for timestep, runtime in input_dict.iteritems():
        row = [timestep]
        row.extend(runtime)
        #pprint(row)
        writer.writerow(row)
