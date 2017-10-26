import sys
import csv
from pprint import pprint

from stats import *


instr_dict = dict()

with open("./instr_act__amarel.csv") as f_in:
    reader = csv.reader(f_in)
    for row in reader:
        instr_dict[row[0]] = map(int, row[1:])


avg_instr_dict = dict()

for timestep, instr_list in instr_dict.iteritems():
    pprint(timestep)
    pprint(instr_list)
    avg_instr_dict[timestep] = [avg(instr_list), samp_std(instr_list), conf_itv(instr_list)]


with open("avg_instr_act.csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, instr in avg_instr_dict.iteritems():
        row = [timestep]
        row.extend(instr)
        pprint(row)
        writer.writerow(row)

