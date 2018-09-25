import csv
import sys
from pprint import pprint
from matplotlib import pyplot as plt


amarel_data = list()
pred_data = list()
comet_data = list()
bridges_data = list()
supermic_data = list()
osg_data = list()

with open('avg_cycles__amarel.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        amarel_data.append(fmt_row)

with open('avg_cycles__bridges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        bridges_data.append(fmt_row)

with open('avg_cycles__comet.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        comet_data.append(fmt_row)

with open('avg_cycles__supermic.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        supermic_data.append(fmt_row)

with open('avg_cycles__osg.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        osg_data.append(fmt_row)

with open('avg_pred_cycles.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_data.append(fmt_row)

amarel_data.sort(key=lambda x: x[0])
z_amarel_data = map(list, zip(*amarel_data))
bridges_data.sort(key=lambda x: x[0])
z_bridges_data = map(list, zip(*bridges_data))
comet_data.sort(key=lambda x: x[0])
z_comet_data = map(list, zip(*comet_data))
supermic_data.sort(key=lambda x: x[0])
z_supermic_data = map(list, zip(*supermic_data))
osg_data.sort(key=lambda x: x[0])
z_osg_data = map(list, zip(*osg_data))
pred_data.sort(key=lambda x: x[0])
z_pred_data = map(list, zip(*pred_data))


plt.close('all')
plt.rcParams["figure.figsize"] = [12, 8]
fig, ax = plt.subplots()
ax.set_title("Average Number of Cycles, for each simulation timesteps", fontsize=20)

x = z_amarel_data[0]
ax.errorbar(x, z_amarel_data[1], yerr=z_amarel_data[2], label='Amarel', color='darkgoldenrod')
ax.errorbar(x, z_pred_data[1], yerr=z_pred_data[2], label='Predicted', color='black')
ax.errorbar(x, z_bridges_data[1], yerr=z_bridges_data[2], label='Bridges',color='blue')
ax.errorbar(x, z_comet_data[1], yerr=z_comet_data[2], label='Comet', color='green')
ax.errorbar(x, z_supermic_data[1], yerr=z_supermic_data[2], label='SuperMIC', color='red')
ax.errorbar(x, z_osg_data[1], yerr=z_osg_data[2], label='OSG', color='c')

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlim(950, 105000)
ax.set_ylim(100000000000, 50000000000000)

ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)

ax.set_xlabel('Number of Timesteps', fontsize=14)
ax.set_ylabel('Number of cycles', fontsize=14)

ax.legend(loc='upper left')

#ax.set_aspect(1.0 / 2)
#print aspect

#fig.set_size_inches(8, 6)
#plt.show()

plt.savefig('avg_cycles.pdf', bbox_inches='tight', dpi=144)
plt.savefig('avg_cycles.png', bbox_inches='tight', dpi=144)
