import sys
import csv
from pprint import pprint

from stats import *


input_path = sys.argv[1]
path_parts = [path_part for path_part in input_path.split('/') if path_part]
resource = path_parts[-1]

cycles_dict = dict()

with open("./pred_cycles.csv") as f_in:
    reader = csv.reader(f_in)
    for row in reader:
        cycles_dict[row[0]] = map(float, row[1:])
pprint(cycles_dict)

instr_rate_dict = dict()

with open("./instr_rate__"+resource+".csv") as f_in:
    reader = csv.reader(f_in)
    for row in reader:
        instr_rate_dict[row[0]] = map(float, row[1:])


cycles_instr_rate_adj_dict = dict()

for timestep in cycles_dict.keys():
    cycles_instr_rate_adj_dict[timestep] = list()
    for i in range(len(cycles_dict[timestep])):
        adj_num_cycles = cycles_dict[timestep][i] / instr_rate_dict[timestep][i]
        cycles_instr_rate_adj_dict[timestep].append(adj_num_cycles)
        
pprint(cycles_instr_rate_adj_dict)


avg_cycles_instr_rate_adj_dict = dict()

for timestep, adj_cycles_list in cycles_instr_rate_adj_dict.iteritems():
    pprint(timestep)
    pprint(adj_cycles_list)
    avg_cycles_instr_rate_adj_dict[timestep] = [avg(adj_cycles_list), samp_std(adj_cycles_list), conf_itv(adj_cycles_list)]


with open("pred_cycles_instr_rate_adj__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, adj_cycles_list in cycles_instr_rate_adj_dict.iteritems():
        row = [timestep]
        row.extend(adj_cycles_list)
        pprint(row)
        writer.writerow(row)

with open("avg_pred_cycles_instr_rate_adj__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, adj_cycles_list in avg_cycles_instr_rate_adj_dict.iteritems():
        row = [timestep]
        row.extend(adj_cycles_list)
        pprint(row)
        writer.writerow(row)

