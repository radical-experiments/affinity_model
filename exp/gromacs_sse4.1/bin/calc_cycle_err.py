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


cycles_pct_err_dict = dict()
for timestep in est_cycles_dict.keys():
    cycles_pct_err_dict[timestep] = pct_err(res_cycles_dict[timestep], est_cycles_dict[timestep])

avg_cycles_pct_err_dict = dict()
for timestep, pct_err_list in cycles_pct_err_dict.iteritems():
    avg_cycles_pct_err_dict[timestep] = [avg(pct_err_list), samp_std(pct_err_list), conf_itv(pct_err_list)]

with open("./cycles_err__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, cycles_err in cycles_pct_err_dict.iteritems():
        row = [timestep]
        row.extend(cycles_err)
        pprint(row)
        writer.writerow(row)

with open("./avg_cycles_err__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    for timestep, cycles_err in avg_cycles_pct_err_dict.iteritems():
        row = [timestep]
        row.extend(cycles_err)
        pprint(row)
        writer.writerow(row)

