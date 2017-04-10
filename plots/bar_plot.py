import sys
import csv
import matplotlib.pyplot as plt
import numpy as np


filename_model = sys.argv[1]
filename_exp = sys.argv[2]

resource_model = list()
affinity = list()

with open(filename_model, "rb") as csvfile:
    c = csv.reader(csvfile)
    for row in c:
        resource_model.append(row[0])
        affinity.append(row[1])

resource_exp = list()
tx_avg = list()
tx_stderr = list()
tx_count = list()

with open(filename_exp, "rb") as csvfile:
    c = csv.reader(csvfile)
    for row in c:
        print row
        resource_exp.append(row[0])
        tx_avg.append(float(row[1]))
        tx_stderr.append(float(row[2]))
        tx_count.append(int(row[3]))

#print resource
#print affinity

ind = np.arange(len(resource_model))
width = 0.2

fig, ax = plt.subplots()
bar1 = ax.bar(ind, affinity, width, color='b')
bar2 = ax.bar(ind + width, tx_avg, width, color='r', yerr=tx_stderr)

ax.set_title(r'$T_x$ by Resource', size=24)

ax.set_xticks(ind + width)
ax.set_xticklabels(resource_model, size=16)

ax.set_ylabel(r'$T_x$', size=18)
ax.set_ylim([0, 1000])
ax.tick_params(axis='y', which='major', labelsize=16)

ax.legend((bar1, bar2), (r'Predicted T_x', r'Actual T_x'))

plt.show()
