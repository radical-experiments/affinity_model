import sys
import csv
from pprint import pprint

from stats import *


cycles_dict = dict()
instr_rate_dict = dict()

with open("./cycles__amarel.csv") as f_in:
    reader = csv.reader(f_in)
    for row in reader:
        cycles_dict[row[0]] = map(float, row[1:])

with open("./instr_rate__amarel.csv") as f_in:
    reader = csv.reader(f_in)
    for row in reader:
        instr_rate_dict[row[0]] = map(float, row[1:])


pred_cycles_dict = dict()
avg_pred_cycles_dict = dict()

for timestep in cycles_dict.keys():
    pred_cycles_dict[timestep] = [int((cycles_dict[timestep][i] * instr_rate_dict[timestep][i])) for i in range(len(cycles_dict[timestep]))]

pprint(pred_cycles_dict)


for timestep, pred_cycles_list in pred_cycles_dict.iteritems():
    pprint(timestep)
    pprint(pred_cycles_list)
    avg_pred_cycles_dict[timestep] = [avg(pred_cycles_list), samp_std(pred_cycles_list), conf_itv(pred_cycles_list)]

pprint(avg_pred_cycles_dict)

with open("pred_cycles.csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, pred_cycle in pred_cycles_dict.iteritems():
        row = [timestep]
        row.extend(pred_cycle)
        pprint(row)
        writer.writerow(row)

with open("avg_pred_cycles.csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, avg_pred_cycle in avg_pred_cycles_dict.iteritems():
        row = [timestep]
        row.extend(avg_pred_cycle)
        pprint(row)
        writer.writerow(row)

