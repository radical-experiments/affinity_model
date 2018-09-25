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

with open('./baseline/comet_to_osg_all_pct_tx_reds_time_ranges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        stripped_row = [elem for elem in row if elem]
        comet_data[int(stripped_row[0])] = map(float, stripped_row[1:])

with open('./baseline/bridges_to_osg_all_pct_tx_reds_time_ranges.csv') as f:
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
    avg_red_tx_comet = sum(comet_data[cores]) / len(comet_data[cores])
    avg_red_tx_bridges = sum(bridges_data[cores]) / len(bridges_data[cores])
    
    comet_plotting_data.append(avg_red_tx_comet)
    bridges_plotting_data.append(avg_red_tx_bridges)

    samp_std_comet = samp_std(comet_data[cores])
    samp_std_bridges = samp_std(bridges_data[cores])

    comet_plotting_yerr.append(samp_std_comet)
    bridges_plotting_yerr.append(samp_std_bridges)

x = [i for i in range(len(cores_list))]


plt.close('all')
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(12, 6)

plot_inputs = [{"title": "a) - ",
                "ymin"      : -10000, 
                "ymax"      : 100000, 
                "yinc"      : 20000
                },

                {"title": "b) - Tq from baseline, reselection and  model runs", 
                "ymin"      : -10000, 
                "ymax"      : 80000,
                "yinc"      : 20000
                },

                {"title": "c) - Improvment when tasks from Comet or from Bridges to OSG", 
                 "ylabel"   : r'Percentage Reduction in $T_{x,task}$'
                "ymin"      : -300, 
                "ymax"      : 0,
                "yinc"      : 20
                }]

for i in range(len(plot_inputs)):
    ax[i].set_title(plot_inputs[i]['title'], fontsize=20)

    ax[i].errorbar(x[2:], bridges_plotting_data[i][2:], yerr=bridges_plotting_yerr[i][2:], marker='d', alpha=0.6, linestyle='--',linewidth=1.5, label='Bridges', color='green', capsize=5, capthick=1)
    ax[i].errorbar(x[0], comet_plotting_data[i][0], yerr=comet_plotting_yerr[i][0], marker='d', alpha=0.6, linestyle='--', linewidth=1.5, color='red', capsize=5, capthick=1)
    ax[i].errorbar(x[2:], comet_plotting_data[i][2:], yerr=comet_plotting_yerr[i][2:], marker='d', alpha=0.6, linestyle='--', linewidth=1.5, label='Comet', color='red', capsize=5, capthick=1)

    ax[i].set_xticklabels(cores_list, fontsize=16)
    ax[i].set_xticks(x, minor=False)
    ax[i].set_yticklabels([i for i in range(plot_inputs[i]['ymin'], plot_inputs[i]['ymax'], plot_inputs[i]['yinc'])], fontsize=16)
    ax[i].set_xlim(x[0] - 0.1, x[-1] + 0.1)
    ax[i].set_ylim(plot_inputs[i]['ymin'], plot_inputs[i]['ymax'])

    ax[i].legend()
    ax[i].set_title(plot_inputs[i]['ylabel'], fontsize=20)
    ax[i].set_xlabel('Number of cores', fontsize=18)
    ax[i].set_ylabel(plot_inputs[i]['ylabel'], fontsize=18)

fig.tight_layout()

#plt.show()
plt.savefig('all_red_to_osg.pdf', bbox_inches='tight', dpi=144)
plt.savefig('all_red_to_osg.png', bbox_inches='tight', dpi=144)
