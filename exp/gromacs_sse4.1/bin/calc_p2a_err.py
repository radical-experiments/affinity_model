import sys
import csv
from pprint import pprint

from stats import *


input_path = sys.argv[1]
path_parts = [path_part for path_part in input_path.split('/') if path_part]
resource = path_parts[-1]

est_cycles_dict = dict()
res_cycles_dict = dict()

with open("./avg_pred_cycles.csv") as f_base:
    reader = csv.reader(f_base)
    for row in reader:
        est_cycles_dict[row[0]] = float(row[1])

with open("./cycles__"+resource+".csv") as f_res:
    reader = csv.reader(f_res)
    for row in reader:
        res_cycles_dict[row[0]] = map(float, row[1:])


p2a_dict = dict()
for timestep in est_cycles_dict.keys():
    p2a_dict[timestep] = [(est_cycles_dict[timestep] / elem) for elem in res_cycles_dict[timestep]]


instr_rate_dict = dict()
with open("./instr_rate__"+resource+".csv") as f_res:
    reader = csv.reader(f_res)
    for row in reader:
        instr_rate_dict[row[0]] = map(float, row[1:])


p2a_pct_err_dict = dict()
for timestep in est_cycles_dict.keys():
    p2a_pct_err_dict[timestep] = pct_err_list(p2a_dict[timestep], instr_rate_dict[timestep])

avg_p2a_pct_err_dict = dict()
for timestep, pct_err_list in p2a_pct_err_dict.iteritems():
    avg_p2a_pct_err_dict[timestep] = [avg(pct_err_list), samp_std(pct_err_list), conf_itv(pct_err_list)]

with open("./p2a__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, p2a in p2a_dict.iteritems():
        row = [timestep]
        row.extend(p2a)
        pprint(row)
        writer.writerow(row)

with open("./p2a_instr_rate_err__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, p2a_err in p2a_pct_err_dict.iteritems():
        row = [timestep]
        row.extend(p2a_err)
        pprint(row)
        writer.writerow(row)

with open("./avg_p2a_instr_rate_err__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, p2a_err in avg_p2a_pct_err_dict.iteritems():
        row = [timestep]
        row.extend(p2a_err)
        pprint(row)
        writer.writerow(row)

