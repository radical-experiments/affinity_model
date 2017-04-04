import sys
import csv
import matplotlib.pyplot as plt
import numpy as np


filename = sys.argv[1]

resource = list()
affinity = list()

with open(filename, "rb") as csvfile:
    c = csv.reader(csvfile)
    for row in c:
        resource.append(row[0])
        affinity.append(row[1])

print resource
print affinity

ind = np.arange(len(resource))
width = 0.35

fig, ax = plt.subplots()
bar1 = ax.bar(ind, affinity, width, color='r')

ax.set_ylabel(r'min $T_x$')
ax.set_title(r'min $T_x$ by Resource')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(resource)

#ax.legend((bar1), (r'max T_x'))

plt.show()
