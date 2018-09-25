import os
import sys
import csv
import json
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


comet_ttc_data = dict()
bridges_ttc_data = dict()
comet_tq_data = dict()
bridges_tq_data = dict()
comet_tx_data = dict()
bridges_tx_data = dict()

with open('./baseline/comet_to_osg_all_pct_ttc_reds_time_ranges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        stripped_row = [elem for elem in row if elem]
        comet_ttc_data[int(stripped_row[0])] = map(float, stripped_row[1:])

with open('./baseline/bridges_to_osg_all_pct_ttc_reds_time_ranges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        stripped_row = [elem for elem in row if elem]
        bridges_ttc_data[int(stripped_row[0])] = map(float, stripped_row[1:])

with open('./baseline/comet_to_osg_all_pct_tq_reds_time_ranges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        stripped_row = [elem for elem in row if elem]
        comet_tq_data[int(stripped_row[0])] = map(float, stripped_row[1:])

with open('./baseline/bridges_to_osg_all_pct_tq_reds_time_ranges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        stripped_row = [elem for elem in row if elem]
        bridges_tq_data[int(stripped_row[0])] = map(float, stripped_row[1:])

with open('./baseline/comet_to_osg_all_pct_tx_reds_time_ranges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        stripped_row = [elem for elem in row if elem]
        comet_tx_data[int(stripped_row[0])] = map(float, stripped_row[1:])

with open('./baseline/bridges_to_osg_all_pct_tx_reds_time_ranges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        stripped_row = [elem for elem in row if elem]
        bridges_tx_data[int(stripped_row[0])] = map(float, stripped_row[1:])


comet_plotting_data = [list() for i in range(3)]
bridges_plotting_data = [list() for i in range(3)]
comet_plotting_yerr = [list() for i in range(3)]
bridges_plotting_yerr = [list() for i in range(3)]

cores_list = sorted(comet_ttc_data.keys())

for cores in cores_list:

    avg_red_ttc_comet = sum(comet_ttc_data[cores]) / len(comet_ttc_data[cores])
    avg_red_ttc_bridges = sum(bridges_ttc_data[cores]) / len(bridges_ttc_data[cores])
    comet_plotting_data[0].append(avg_red_ttc_comet)
    bridges_plotting_data[0].append(avg_red_ttc_bridges)

    samp_std_ttc_comet = samp_std(comet_ttc_data[cores])
    samp_std_ttc_bridges = samp_std(bridges_ttc_data[cores])

    comet_plotting_yerr[0].append(samp_std_ttc_comet)
    bridges_plotting_yerr[0].append(samp_std_ttc_bridges)


    avg_red_tq_comet = sum(comet_tq_data[cores]) / len(comet_tq_data[cores])
    avg_red_tq_bridges = sum(bridges_tq_data[cores]) / len(bridges_tq_data[cores])
    comet_plotting_data[1].append(avg_red_tq_comet)
    bridges_plotting_data[1].append(avg_red_tq_bridges)

    samp_std_tq_comet = samp_std(comet_tq_data[cores])
    samp_std_tq_bridges = samp_std(bridges_tq_data[cores])

    comet_plotting_yerr[1].append(samp_std_tq_comet)
    bridges_plotting_yerr[1].append(samp_std_tq_bridges)


    avg_red_tx_comet = sum(comet_tx_data[cores]) / len(comet_tx_data[cores])
    avg_red_tx_bridges = sum(bridges_tx_data[cores]) / len(bridges_tx_data[cores])
    comet_plotting_data[2].append(avg_red_tx_comet)
    bridges_plotting_data[2].append(avg_red_tx_bridges)

    samp_std_tx_comet = samp_std(comet_tx_data[cores])
    samp_std_tx_bridges = samp_std(bridges_tx_data[cores])

    comet_plotting_yerr[2].append(samp_std_tx_comet)
    bridges_plotting_yerr[2].append(samp_std_tx_bridges)

pprint(comet_plotting_data)
pprint(bridges_plotting_data)

plot_inputs = [{"title": r"a) - Improvement in $TTC_{task}$ when tasks from Comet or Bridges move to OSG",
                "ylabel": 'Percentage Reduction',
                "ymin"      : -20, 
                "ymax"      : 100, 
                "yinc"      : 20
                },

                {"title": r"b) - Improvement in $T_{q,task}$ when tasks from Comet or Bridges move to OSG", 
                "ylabel": 'Percentage Reduction',
                "ymin"      : 40, 
                "ymax"      : 101,
                "yinc"      : 10
                },

                {"title": r'c) - Improvement in $T_{x,task}$ when tasks from Comet or Bridges move to OSG', 
                "ylabel": 'Percentage Reduction',
                "ymin"      : -300, 
                "ymax"      : 1,
                "yinc"      : 20
                }]

plt.close('all')
fig, ax = plt.subplots(3, 1)
fig.set_size_inches(12, 12)

x = [i for i in range(len(cores_list))]


for i in range(len(plot_inputs)):
    ax[i].set_title(plot_inputs[i]['title'], fontsize=16)

    ax[i].errorbar(x[2:], bridges_plotting_data[i][2:], yerr=bridges_plotting_yerr[i][2:], marker='d', alpha=0.6, linestyle='--',linewidth=1.5, label='Bridges', color='green', capsize=5, capthick=1)
    ax[i].errorbar(x[0], comet_plotting_data[i][0], yerr=comet_plotting_yerr[i][0], marker='d', alpha=0.6, linestyle='--', linewidth=1.5, color='red', capsize=5, capthick=1)
    ax[i].errorbar(x[2:], comet_plotting_data[i][2:], yerr=comet_plotting_yerr[i][2:], marker='d', alpha=0.6, linestyle='--', linewidth=1.5, label='Comet', color='red', capsize=5, capthick=1)

    ax[i].set_xlim(x[0] - 0.1, x[-1] + 0.1)
    ax[i].set_ylim(plot_inputs[i]['ymin'], plot_inputs[i]['ymax'])
    ax[i].set_xticklabels(cores_list, fontsize=14)
    ax[i].xaxis.set_ticks(x, minor=False)
    ax[i].set_yticklabels([ii for ii in range(plot_inputs[i]['ymin'], plot_inputs[i]['ymax']+1, plot_inputs[i]['yinc'])], fontsize=16)

    ax[i].set_xlabel('Number of cores', fontsize=18)
    ax[i].set_ylabel(plot_inputs[i]['ylabel'], fontsize=18)

    ax[i].legend(loc='upper left')


fig.tight_layout()

plot_name = "all_red_to_osg"
plt.savefig(plot_name+'.pdf', bbox_inches='tight', dpi=144)
plt.savefig(plot_name+'.png', bbox_inches='tight', dpi=144)
