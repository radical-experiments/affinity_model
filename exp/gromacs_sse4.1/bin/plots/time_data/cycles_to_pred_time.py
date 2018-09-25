import csv
import sys
from pprint import pprint

from stats import *

resource = sys.argv[1]
pred_method = sys.argv[2]
clkspeed = float(sys.argv[3]) * 1000000000

data = list()
filename = 'cycles__{}.csv'.format(resource)

with open('pred_cycles.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        for i in range(1, len(fmt_row)):
            fmt_row[i] /= clkspeed
        data.append(fmt_row)

data.sort(key=lambda x: x[0])

with open('time_pred_{0}__{1}.csv'.format(pred_method, resource), 'w') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)

stat_data = list()
for sample_data in data:
    row = [sample_data[0], avg(sample_data[1:]), samp_std(sample_data[1:]), conf_itv(sample_data[1:])]
    stat_data.append(row)

pprint(stat_data)

filename = 'avg_time_pred_{0}__{1}.csv'.format(pred_method, resource)
with open(filename, 'w') as f:
    writer = csv.writer(f)
    for row in stat_data:
        writer.writerow(row)
