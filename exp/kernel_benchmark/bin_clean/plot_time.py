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

actual_data = dict()
graph_labels = list()
iter_labels = list()

with open(dirpath+'/'+"time_act_norm.csv") as c:
    reader = csv.reader(c)
    for row in reader:
        stripped_row = [entry for entry in row if entry]
        graph_label, run_label = row[0].split('__')[0], int(row[0].split('__')[1])
        stripped_row[0] = run_label
        stripped_row = [float(entry) for entry in stripped_row]
        stripped_row[0] = int(stripped_row[0])

        if stripped_row[0] not in iter_labels:
            iter_labels.append(stripped_row[0])

        if graph_label not in graph_labels:
            graph_labels.append(graph_label)

        if graph_label not in actual_data.keys():
            actual_data[graph_label] = [stripped_row]
        else:
            actual_data[graph_label].append(stripped_row)

        for keys, data_list in actual_data.iteritems():
            data_list = data_list.sort(key=lambda x: x[0])


#pprint(actual_data)

#pprint(graph_labels)
#iter_labels.sort()

predictions = dict()

with open(dirpath+'/'+"time_pred_norm.csv") as c:
    reader = csv.reader(c)
    is_title = 0
    tmp_list = list() 
    run_label = ""
    for row in reader:
        pprint(row)
        stripped_row = [entry for entry in row if entry]
       
        if is_title == 0:
            pass
        else:
            run_label, iter_label = stripped_row[0].split('__')[0], int(stripped_row[0].split('__')[1])
            print run_label, iter_label
            stripped_row[0] = iter_label

            if run_label not in predictions.keys():
                predictions[run_label] = [stripped_row]
            else:
                predictions[run_label].append(stripped_row)
        is_title += 1 

pprint(predictions)

for run_label, prediction in predictions.iteritems():
    tmp_list = sorted(prediction, key=itemgetter(0))
    #pprint(tmp_list)
    tmp_list = map(list, zip(*tmp_list))
    predictions[run_label] = tmp_list

#pprint(predictions)




x = [i for i in range(len(iter_labels))]

fig, axes = plt.subplots(4, sharex=True, sharey=True)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.suptitle(r"Error between Predcited and Actual $T_x$, Normalized by $T_{x, max}$", size=30)

for label_id in range(len(graph_labels)):
    i = 0

    for data_list in actual_data[graph_labels[label_id]]:
        x_iter = [i for j in range(len(data_list) - 1)]

        if '_' in graph_labels[label_id]:
            pred_key = graph_labels[label_id].split('_')[1]

        if pred_key in predictions.keys():
            #pprint(predictions[pred_key][1])
            #pprint(predictions[pred_key][2])
            if i == 0:
                axes[label_id].scatter([i], predictions[pred_key][1][i], marker="^", s=30, color="green", label="max pred")
                axes[label_id].scatter([i], predictions[pred_key][2][i], marker="v", s=30, color="green", label="min pred")
            else:
                pprint(i)
                axes[label_id].scatter([i], predictions[pred_key][1][i], marker="^", s=30, color="green")
                axes[label_id].scatter([i], predictions[pred_key][2][i], marker="v", s=30, color="green")
        
        if i == 0:
            axes[label_id].scatter(x_iter, data_list[1:], s=15, alpha=0.5, label="actual data")
        else:
            axes[label_id].scatter(x_iter, data_list[1:], s=15, alpha=0.5)

        pred_key = graph_labels[label_id].split('_')[1]
        pprint(predictions[pred_key][0])
        num_runs = len(predictions[pred_key][0])
        if label_id == 0 and i == 0:
            xticklabels = deepcopy(predictions[pred_key][0])
            for k in range(len(xticklabels)):
                xticklabels[k] = "%.2E" % Decimal(xticklabels[i])
            xticklabels.insert(0, "")
        pprint(xticklabels)

        axes[label_id].set_xticklabels(xticklabels)
        axes[label_id].set_title(graph_labels[label_id], fontsize=24)
        axes[label_id].set_xlim(-0.5, num_runs - 0.5)
        axes[label_id].set_ylim(0.2, 1.5)
        axes[label_id].set_xlabel("Number of Predicted Cycles", fontsize=20)
        axes[label_id].set_ylabel(r"Normalized $T_x$", fontsize=20)
        axes[label_id].tick_params(labelsize=20)
        axes[label_id].legend(loc='upper right')
        axes[label_id].legend(fontsize=16)
        axes[label_id].grid(True)
        i += 1

plt.setp(plt.xticks()[-1], rotation=30)
plt.show()
