import os
import sys
import csv
import json
from pprint import pprint

from matplotlib import pyplot as plt


def plot_data(filename, title, ymin, ymax, yinc):

    plot_id = ""
    x = list()
    labels = list()
    avg = list()
    confidence = list()
    config = dict()

    
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

    pprint(model_data)
    pprint(baseline_data)
    pprint(move_to_osg_data)

    #with open("plot_config.json", 'r') as cf:
    #    config = json.load(cf) 

    plt.close('all')
    print plot_id

    fig = plt.figure(figsize=(12,5))
    ax = fig.add_subplot(111)
    ax.set_title(title, fontsize=20)

    x = [i for i in range(len(model_data[0]))]
    ax.errorbar(x, baseline_data[1], yerr=baseline_data[2], label='baseline', color='blue', marker='v', capsize=3, alpha=0.6)
    ax.errorbar(x, move_to_osg_data[1], yerr=move_to_osg_data[2], label='reselection', color='green', marker='^', capsize=3, alpha=0.6, linestyle='--')
    ax.errorbar(x, model_data[1], yerr=model_data[2], label='model', color='orange', marker='o', capsize=3)

    ax.set_xticklabels(model_data[0])
    ax.set_xlim(-0.1, 4.1)
    ax.set_ylim(ymin, ymax)
    ax.xaxis.set_ticks(x, minor=False)
    ax.yaxis.set_ticks([i for i in range(ymin, ymax+1, yinc)], minor=False)

    ax.set_xlabel('Number of Tasks', fontsize=14)
    ax.set_ylabel('Time (s)', fontsize=14)
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)

    #ax.set_title(config[kernel][plot_id]['title'], fontsize=24)

    #ax.set_xlim(config[kernel][plot_id]['xlim'])
    #ax.set_ylim(config[kernel][plot_id]['ylim'])
    #ax.set_xlabel(config[kernel][plot_id]['xlabel'], fontsize=20)
    #ax.set_ylabel(config[kernel][plot_id]['ylabel'], fontsize=20)
    #ax.tick_params(labelsize=20)

    leg = ax.legend(loc='upper left')

    #fig.set_size_inches(9.5, 7)
    #plt.show()
    
    plot_name = filename.split('.')[0]
    plt.savefig(plot_name+'.pdf', bbox_inches='tight', dpi=144)
    plt.savefig(plot_name+'.png', bbox_inches='tight', dpi=144)
        

if __name__ == "__main__":


    plot_data('avg_ttc_wkd.csv', 'a) TTC from baseline, reselection and model runs', -10000, 100000, 20000)
    plot_data('avg_ttq_wkd.csv', 'b) Tq from baseline, reselection and model runs', -10000, 80000, 20000)
    plot_data('avg_ttx_wkd.csv', 'c) Tx from baseline, reselection and model runs', 0, 40000, 10000)

