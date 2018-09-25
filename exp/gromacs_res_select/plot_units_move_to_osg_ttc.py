import os
import sys
import csv
import math
from pprint import pprint

from matplotlib import pyplot as plt


def samp_std(input_list):

    if len(input_list) == 1:
        return 0

    mean = sum(input_list) / len(input_list)
    samp_std = 0

    for elem in input_list:
        samp_std = (elem - mean) * (elem - mean)
    samp_std /= len(input_list) - 1
    samp_std = math.sqrt(samp_std)
    return samp_std

def conf_itv(samp_std, num_samps):
    return 2.576 * samp_std / math.sqrt(num_samps)


comet_data = dict()
bridges_data = dict()

with open('./baseline/comet_to_osg_all_pct_ttc_reds_time_ranges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        stripped_row = [elem for elem in row if elem]
        comet_data[int(stripped_row[0])] = map(float, stripped_row[1:])

with open('./baseline/bridges_to_osg_all_pct_ttc_reds_time_ranges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        stripped_row = [elem for elem in row if elem]
        bridges_data[int(stripped_row[0])] = map(float, stripped_row[1:])

pprint(comet_data)
pprint(bridges_data)

comet_plotting_data = list()
bridges_plotting_data = list()
comet_plotting_yerr = list()
bridges_plotting_yerr = list()

cores_list = sorted(comet_data.keys())
for cores in cores_list:
    avg_red_ttc_comet = sum(comet_data[cores]) / len(comet_data[cores])
    avg_red_ttc_bridges = sum(bridges_data[cores]) / len(bridges_data[cores])
    
    comet_plotting_data.append(avg_red_ttc_comet)
    bridges_plotting_data.append(avg_red_ttc_bridges)

    samp_std_comet = samp_std(comet_data[cores])
    samp_std_bridges = samp_std(bridges_data[cores])

    comet_plotting_yerr.append(samp_std_comet)
    bridges_plotting_yerr.append(samp_std_bridges)

x = [i for i in range(len(cores_list))]


plt.close('all')
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(12, 6)


ax.errorbar(x[2:], bridges_plotting_data[2:], yerr=bridges_plotting_yerr[2:], marker='d', alpha=0.6, linestyle='--',linewidth=1.5, label='Bridges', color='green', capsize=5, capthick=1)
ax.errorbar(x[0], comet_plotting_data[0], yerr=comet_plotting_yerr[0], marker='d', alpha=0.6, linestyle='--', linewidth=1.5, color='red', capsize=5, capthick=1)
ax.errorbar(x[2:], comet_plotting_data[2:], yerr=comet_plotting_yerr[2:], marker='d', alpha=0.6, linestyle='--', linewidth=1.5, label='Comet', color='red', capsize=5, capthick=1)

ax.set_xticklabels(cores_list, fontsize=16)
ax.set_xticks(x, minor=False)
ax.set_yticklabels([i for i in range(-20, 101, 20)], fontsize=16)
ax.set_xlim(x[0] - 0.1, x[-1] + 0.1)
ax.set_ylim(-20, 100)

ax.legend()
ax.set_title('Improvement when tasks from Comet or from Bridges to OSG', fontsize=20)
ax.set_xlabel('Number of cores', fontsize=18)
ax.set_ylabel(r'Percentage Reduction in $TTC_{task}$', fontsize=18)

#plt.show()
plt.savefig('ttc_red_to_osg.pdf', bbox_inches='tight', dpi=144)
plt.savefig('ttc_red_to_osg.png', bbox_inches='tight', dpi=144)
