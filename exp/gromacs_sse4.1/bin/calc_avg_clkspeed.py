import sys
import csv
from pprint import pprint

from stats import *


input_path = sys.argv[1]
path_parts = [path_part for path_part in input_path.split('/') if path_part]
resource = path_parts[-1]

clkspeed_dict = dict()

with open("./clkspeed__"+resource+".csv") as f_in:
    reader = csv.reader(f_in)
    for row in reader:
        clkspeed_dict[row[0]] = map(float, row[1:])


avg_clkspeed_dict = dict()

for timestep, clkspeed_list in clkspeed_dict.iteritems():
    pprint(timestep)
    pprint(clkspeed_list)
    avg_clkspeed_dict[timestep] = [avg(clkspeed_list), samp_std(clkspeed_list), conf_itv(clkspeed_list)]


with open("avg_clkspeed__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, clkspeed_list in avg_clkspeed_dict.iteritems():
        row = [timestep]
        row.extend(clkspeed_list)
        pprint(row)
        writer.writerow(row)


