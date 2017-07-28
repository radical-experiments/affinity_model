import os
import sys
import csv
from pprint import pprint
from operator import itemgetter

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

        pprint(actual_data)

pprint(graph_labels)
iter_labels.sort()

x = [i for i in range(len(iter_labels))]

fig, axes = plt.subplots(4, sharex=True, sharey=True)
for label_id in range(len(graph_labels)):
    i = 0
    for data_list in actual_data[graph_labels[label_id]]:
        x_iter = [i for j in range(len(data_list) - 1)]
        axes[label_id].scatter(x_iter, data_list[1:])
        i += 1

plt.show()
