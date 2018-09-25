import os
import sys
import csv
import json
from pprint import pprint

from matplotlib import pyplot as plt


def read_data(filename):
    model_data = list()
    with open('model_pred/'+filename, 'r') as f:
        data = list()
        reader = csv.reader(f)
        for row in reader:
            fmt_row = [int(row[0])]
            fmt_row.extend(map(float, row[1:]))
            data.append(fmt_row)
        model_data = map(list, zip(*data))

    baseline_data = list()
    with open('baseline/'+filename, 'r') as f:
        data = list()
        reader = csv.reader(f)
        for row in reader:
            fmt_row = [int(row[0])]
            fmt_row.extend(map(float, row[1:]))
            data.append(fmt_row)
        baseline_data = map(list, zip(*data))

    move_to_osg_data = list()
    with open('move_to_osg/'+filename, 'r') as f:
        data = list()
        reader = csv.reader(f)
        for row in reader:
            fmt_row = [int(row[0])]
            fmt_row.extend(map(float, row[1:]))
            data.append(fmt_row)
        move_to_osg_data = map(list, zip(*data))

    return model_data, baseline_data, move_to_osg_data


def plot_all_data(inputs):

    model_data = list()
    baseline_data = list()
    move_to_osg_data = list()
    for i in range(len(inputs)):
        m_data, b_data, v_data = read_data(inputs[i]["filename"])
        model_data.append(m_data)
        baseline_data.append(b_data)
        move_to_osg_data.append(v_data)

    plt.close('all')
    fig, ax = plt.subplots(3, 1)
    fig.set_size_inches(12, 12)

    x = [i for i in range(len(model_data[0][0]))]

    for i in range(len(inputs)):
        ax[i].set_title(inputs[i]['title'], fontsize=20)

        ax[i].errorbar(x, baseline_data[i][1], yerr=baseline_data[i][2], label='random', color='blue', marker='v', capsize=3, alpha=0.6)
        #ax[i].errorbar(x, move_to_osg_data[i][1], yerr=baseline_data[i][2], label='reselection', color='green', marker='^', capsize=3, alpha=0.6, linestyle='--')
        ax[i].errorbar(x, model_data[i][1], yerr=model_data[i][2], label='model', color='orange', marker='o', capsize=3)

        ax[i].set_xticklabels(model_data[i][0])
        ax[i].set_xlim(-0.1, 4.1)
        ax[i].set_ylim(inputs[i]['ymin'], inputs[i]['ymax'])
        ax[i].xaxis.set_ticks(x, minor=False)
        ax[i].yaxis.set_ticks([ii for ii in range(inputs[i]['ymin'], inputs[i]['ymax']+1, inputs[i]['yinc'])], minor=False)

        ax[i].set_xlabel('Number of Tasks', fontsize=14)
        ax[i].set_ylabel('Time (s)', fontsize=14)
        ax[i].xaxis.set_tick_params(labelsize=14)
        ax[i].yaxis.set_tick_params(labelsize=14)

        ax[i].legend(loc='upper left')

        #aspect = 4.0 / (inputs[i]['ymax'] - inputs[i]['ymin'])
        #ax[i].set_aspect(aspect / 2)
        #print aspect

    fig.tight_layout()
    #fig.subplots_adjust(hspace=0.2)
    #fig.set_size_inches(9.5, 7)
    #plt.show()
    
    plot_name = "avg_wkd_res_select"
    plt.savefig(plot_name+'.pdf', bbox_inches='tight', dpi=144)
    plt.savefig(plot_name+'.png', bbox_inches='tight', dpi=144)
        

if __name__ == "__main__":


    plot_inputs = [{"filename"  : "avg_ttc_wkd.csv",
                    "title": "a) - TTC from baseline and model runs",
                    "ymin"      : -10000, 
                    "ymax"      : 100000, 
                    "yinc"      : 20000
                    },

                   {"filename"  : "avg_ttq_wkd.csv", 
                    "title": "b) - Tq from baseline and model runs", 
                    "ymin"      : -10000, 
                    "ymax"      : 80000,
                    "yinc"      : 20000
                    },
                   {"filename"  : "avg_ttx_wkd.csv", 
                    "title": "c) - Tx from baseline and model runs", 
                    "ymin"      : 0, 
                    "ymax"      : 40000,
                    "yinc"      : 10000
                    }]

    plot_all_data(plot_inputs)
