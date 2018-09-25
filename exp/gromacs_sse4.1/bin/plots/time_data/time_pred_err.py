import csv
import sys
from pprint import pprint

from stats import *

resource = sys.argv[1]
pred_method = sys.argv[2]

pred_data = list()
act_data = list()

with open('time__{}.csv'.format(resource)) as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        act_data.append(fmt_row)

act_data.sort(key=lambda x: x[0])

with open('avg_time_pred_{}__{}.csv'.format(pred_method, resource)) as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_data.append(fmt_row)

pred_data.sort(key=lambda x: x[0])
pprint(pred_data)

pred_err_data = list()
for i in range(len(pred_data)):
    row = [pred_data[i][0]]
    print len(act_data[i][1:]), len(pred_data[i][1:])
    pred_errs = pct_err(act_data[i][1:], pred_data[i][1])
    row.extend(pred_errs)
    pred_err_data.append(row)

pprint(row)


with open('time_prederr_{0}__{1}.csv'.format(pred_method, resource), 'w') as f:
    writer = csv.writer(f)
    for row in pred_err_data:
        writer.writerow(row)

stat_data = list()
for sample_data in pred_err_data:
    row = [sample_data[0], avg(sample_data[1:]), samp_std(sample_data[1:]), conf_itv(sample_data[1:])]
    stat_data.append(row)

pprint(stat_data)

filename = 'time_prederr_{0}__{1}.csv'.format(pred_method, resource)
with open(filename, 'w') as f:
    writer = csv.writer(f)
    for row in stat_data:
        writer.writerow(row)
