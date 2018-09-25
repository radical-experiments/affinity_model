import csv
import sys
from pprint import pprint
from matplotlib import pyplot as plt


comet_data = list()
bridges_data = list()
supermic_data = list()
osg_data = list()

with open('avg_instr_rate__bridges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        bridges_data.append(fmt_row)

with open('avg_instr_rate__comet.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        comet_data.append(fmt_row)

with open('avg_instr_rate__supermic.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        supermic_data.append(fmt_row)

with open('avg_instr_rate__osg.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        osg_data.append(fmt_row)

bridges_data.sort(key=lambda x: x[0])
z_bridges_data = map(list, zip(*bridges_data))
comet_data.sort(key=lambda x: x[0])
z_comet_data = map(list, zip(*comet_data))
supermic_data.sort(key=lambda x: x[0])
z_supermic_data = map(list, zip(*supermic_data))
osg_data.sort(key=lambda x: x[0])
z_osg_data = map(list, zip(*osg_data))


plt.close('all')

plt.rcParams['figure.figsize'] = [12, 5]
fig, ax = plt.subplots()
ax.set_title("Average Instruction Executed Rate, for simulations of timesteps", fontsize=20)

x = z_bridges_data[0]
ax.errorbar(x, z_bridges_data[1], yerr=z_bridges_data[2], label='Bridges', color='blue')
ax.errorbar(x, z_comet_data[1], yerr=z_comet_data[2], label='Comet', color='green')
ax.errorbar(x, z_supermic_data[1], yerr=z_supermic_data[2], label='SuperMIC', color='red')
ax.errorbar(x, z_osg_data[1], yerr=z_osg_data[2], label='OSG', color='c')

ax.set_xlim(950, 105000)
ax.set_ylim(1, 2.75)

ax.set_xscale('log')

ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)

ax.set_xlabel('Number of Timesteps', fontsize=14)
ax.set_ylabel('Instructions Executed Per Cycle', fontsize=14)

ax.legend(loc='upper left', ncol=2)

#fig.set_size_inches(9.5, 7)
#plt.show()

plt.savefig('avg_instr_rate.pdf', bbox_inches='tight', dpi=144)
plt.savefig('avg_instr_rate.png', bbox_inches='tight', dpi=144)
