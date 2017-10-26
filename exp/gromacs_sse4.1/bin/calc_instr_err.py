import sys
import csv
from pprint import pprint

from stats import *


input_path = sys.argv[1]
path_parts = [path_part for path_part in input_path.split('/') if path_part]
resource = path_parts[-1]

est_instr_dict = dict()
res_instr_dict = dict()

with open("./avg_instr_act.csv") as f_base:
    reader = csv.reader(f_base)
    for row in reader:
        est_instr_dict[row[0]] = float(row[1])

with open("./instr_act__"+resource+".csv") as f_res:
    reader = csv.reader(f_res)
    for row in reader:
        res_instr_dict[row[0]] = map(float, row[1:])


instr_pct_err_dict = dict()
for timestep in est_instr_dict.keys():
    instr_pct_err_dict[timestep] = pct_err(res_instr_dict[timestep], est_instr_dict[timestep])

avg_instr_pct_err_dict = dict()
for timestep, pct_err_list in instr_pct_err_dict.iteritems():
    avg_instr_pct_err_dict[timestep] = [avg(pct_err_list), samp_std(pct_err_list), conf_itv(pct_err_list)]

with open("./instr_err__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, instr_err in instr_pct_err_dict.iteritems():
        row = [timestep]
        row.extend(instr_err)
        pprint(row)
        writer.writerow(row)

with open("./avg_instr_err__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, instr_err in avg_instr_pct_err_dict.iteritems():
        row = [timestep]
        row.extend(instr_err)
        pprint(row)
        writer.writerow(row)

