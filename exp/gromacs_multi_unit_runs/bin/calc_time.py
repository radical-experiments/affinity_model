import sys
import csv
from pprint import pprint

from stats import *


input_path = sys.argv[1]
path_parts = [path_part for path_part in input_path.split('/') if path_part]
resource = path_parts[-1]

time_dict = dict()

with open("./time__"+resource+".csv") as f_in:
    reader = csv.reader(f_in)
    for row in reader:
        time_dict[row[0]] = map(float, row[1:])


avg_time_dict = dict()

for timestep, time_list in time_dict.iteritems():
    pprint(timestep)
    pprint(time_list)
    avg_time_dict[timestep] = [avg(time_list), samp_std(time_list), conf_itv(time_list)]


with open("avg_time__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, time in avg_time_dict.iteritems():
        row = [timestep]
        row.extend(time)
        pprint(row)
        writer.writerow(row)

