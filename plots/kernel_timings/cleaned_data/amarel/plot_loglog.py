import os
import sys
import json

from matplotlib import pyplot as plt


pathname = sys.argv[1]
file_list = os.listdir(pathname)
keyword = sys.argv[2]

plot_id = ""
x = list()
labels = list()
avg = list()
confidence = list()
config = dict()

for fn in file_list:
    if keyword in fn:
        session_id = keyword.split('.csv')[0].split('_')[-1]

        with open(pathname+fn, 'r') as f:
            i = 0
            for row in f:
                row_list = row.split(',')
                print row

                if i == 0:
                    plot_id = row_list[0]
                    x = row_list[1:]
                    print x
                else:
                    if i % 4 == 1:
                        labels.append(session_id)
                        avg.append(map(float, row_list[1:]))
                    elif i % 4 == 3:
                        confidence.append(map(float, row_list[1:]))
                
                i += 1

with open("plot_config.json", 'r') as cf:
    config = json.load(cf) 


plt.close('all')

print plot_id

fig, ax = plt.subplots()
ax.set_title(config[plot_id]['title'], fontsize=24)

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(config[plot_id]['xlim'])
ax.set_ylim(config[plot_id]['ylim'])
ax.set_ylim([1000000, 100000000000000])
ax.set_xlabel(config[plot_id]['xlabel'], fontsize=20)
ax.set_ylabel(config[plot_id]['ylabel'], fontsize=20)
ax.tick_params(labelsize=20)
ax.grid(True)

for i in range(len(avg)):
    (_, caps, _) = ax.errorbar(x, avg[i], yerr=confidence[i], label=labels[i])
    for cap in caps:
        cap.set_linewidth(5)

ax.legend(loc='upper left')

plt.show()
