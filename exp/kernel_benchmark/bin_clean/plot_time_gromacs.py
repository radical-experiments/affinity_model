import os
import sys
import csv
from pprint import pprint
from operator import itemgetter
from decimal import Decimal
from copy import deepcopy

from matplotlib import pyplot as plt


dirpath = sys.argv[1]
#setting = sys.argv[2]

graph_labels = list()
iter_labels = list()

actual_data = dict()

with open(dirpath+'/'+"time_act_norm.csv") as c:
    reader = csv.reader(c)
    for row in reader:
        stripped_row = [entry for entry in row if entry]
        keywords = stripped_row[0].split("__")
        node_type, nsteps = keywords[0], keywords[1]
        if nsteps not in actual_data.keys():
            actual_data[nsteps] = dict()
        actual_data[nsteps][node_type] = map(float, stripped_row[1:])

pprint(actual_data)

min_pred = dict()
max_pred = dict()
avg_clk_pred = dict()

with open(dirpath+'/'+"time_pred_norm.csv") as c:
    reader = csv.reader(c)
    for row in reader:
        stripped_row = [entry for entry in row if entry]
        keywords = stripped_row[0].split("__")
        node_type, nsteps = keywords[0], keywords[1]
        if nsteps not in max_pred.keys():
            max_pred[nsteps] = list()
            min_pred[nsteps] = list()
            avg_clk_pred[nsteps] = list()
        max_pred[nsteps].append((node_type, float(stripped_row[1])))
        min_pred[nsteps].append((node_type, float(stripped_row[2])))
        avg_clk_pred[nsteps].append((node_type, float(stripped_row[3])))

node_labels = None
for num_iter in max_pred.keys():
    if node_labels == None:
        tmp = zip(*sorted(max_pred[num_iter], key=itemgetter(0)))
        node_labels = list(tmp[0])
        max_pred[num_iter] = list(tmp[1])
    else:
        max_pred[num_iter] = list(zip(*sorted(max_pred[num_iter], key=itemgetter(0)))[1])
    min_pred[num_iter] = list(zip(*sorted(min_pred[num_iter], key=itemgetter(0)))[1])
    avg_clk_pred[num_iter] = list(zip(*sorted(avg_clk_pred[num_iter], key=itemgetter(0)))[1])

print node_labels
pprint(min_pred)
pprint(max_pred)
pprint(avg_clk_pred)

num_steps = sorted(map(int, actual_data.keys()))
graph_labels = [str(nsteps)+" timesteps" for nsteps in num_steps]
pprint(graph_labels)

x = [i for i in range(len(iter_labels))]

fig, axes = plt.subplots(len(graph_labels), sharex=True, sharey=True)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.suptitle(r"Error between Predcited and Actual $T_x$, Normalized by $T_{x, max}$ of measured on Amarel High Memory Nodes", size=30, wrap=True)

i = 0
for label_id in range(len(graph_labels)):

    #for nst in num_steps:
    #nsteps = str(nst)
    nsteps = graph_labels[label_id].split(" ")[0]
    data_list = actual_data[nsteps]

    node_idxx = range(len(max_pred[nsteps]))

    pprint(nsteps)
    if i == 0:
        axes[label_id].scatter(node_idxx, max_pred[nsteps], marker="^", s=30, color="green", label="max pred")
        axes[label_id].scatter(node_idxx, min_pred[nsteps], marker="v", s=30, color="green", label="min pred")
        axes[label_id].scatter(node_idxx, avg_clk_pred[nsteps], marker="*", s=30, color="red", label="avg clkspeed pred")
    else:
        axes[label_id].scatter(node_idxx, max_pred[nsteps], marker="^", s=30, color="green")
        axes[label_id].scatter(node_idxx, min_pred[nsteps], marker="v", s=30, color="green")
        axes[label_id].scatter(node_idxx, avg_clk_pred[nsteps], marker="*", s=30, color="red")


    ii = 0
    for node in node_labels:
        idx_list = [ii for j in range(len(data_list[node]))]
        if i == 0 and ii == 0:
            axes[label_id].scatter(idx_list, data_list[node], s=15, alpha=0.5, label="actual runs")
        else:
            axes[label_id].scatter(idx_list, data_list[node], s=15, alpha=0.5)
        ii += 1

    xticklabels = deepcopy(node_labels)

    axes[label_id].set_title(graph_labels[label_id], fontsize=24)
    axes[label_id].set_xlim(-0.5, 3.5)
    axes[label_id].set_ylim(0.2, 1.05)
    axes[label_id].set_xlabel("Node Type", fontsize=20)
    axes[label_id].set_ylabel(r"Normalized $T_x$", fontsize=20)
    axes[label_id].set_xticklabels(xticklabels)
    axes[label_id].tick_params(labelsize=20)
    axes[label_id].set_xticks([j for j in range(len(node_labels))])
    axes[label_id].set_yticks([0.2*j for j in range(1, 6)])
    
    if label_id == 0:
        axes[label_id].legend(loc="upper right")
        axes[label_id].legend(fontsize=16)
        
    axes[label_id].grid(True)

    i += 1

plt.setp(plt.xticks()[-1], rotation=30)
plt.show()
