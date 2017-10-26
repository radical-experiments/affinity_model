import sys
import csv
from pprint import pprint

from stats import *


input_path = sys.argv[1]
path_parts = [path_part for path_part in input_path.split('/') if path_part]
resource = path_parts[-1]

cycles_dict = dict()

with open("./cycles__"+resource+".csv") as f_in:
    reader = csv.reader(f_in)
    for row in reader:
        cycles_dict[row[0]] = map(float, row[1:])


avg_cycles_dict = dict()

for timestep, cycles_list in cycles_dict.iteritems():
    pprint(timestep)
    pprint(cycles_list)
    avg_cycles_dict[timestep] = [avg(cycles_list), samp_std(cycles_list), conf_itv(cycles_list)]


with open("avg_cycles__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, cycles_list in avg_cycles_dict.iteritems():
        row = [timestep]
        row.extend(cycles_list)
        pprint(row)
        writer.writerow(row)


