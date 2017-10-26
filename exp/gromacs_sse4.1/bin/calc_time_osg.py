import sys
import csv
from pprint import pprint

from stats import *


BIN_SIZE = 500
resource = 'osg'

time_dict = dict()

with open("./time__"+resource+".csv") as f_in:
    reader = csv.reader(f_in)
    for row in reader:
        time_dict[row[0]] = map(float, row[1:])


time_bins_dict = dict()
for i in range(1000, 18001, BIN_SIZE):
    time_bins_dict[i] = 0

for elem in time_dict['100000']:
    for bin_range in time_bins_dict.keys():
        if elem >= bin_range and elem < (bin_range + BIN_SIZE):
            time_bins_dict[bin_range] += 1
            break

pprint(time_bins_dict)

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

with open("time_dist__"+resource+".csv", "w") as f_out:
    writer = csv.writer(f_out)
    bins_sorted = sorted(time_bins_dict.keys())
    pprint(bins_sorted)
    for bin_range in bins_sorted:
        row = [bin_range, time_bins_dict[bin_range]]
        pprint(row)
        writer.writerow(row)
