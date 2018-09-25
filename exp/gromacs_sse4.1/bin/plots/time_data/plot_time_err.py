import csv
import sys
from pprint import pprint
from matplotlib import pyplot as plt


pred_base_comet_data = list()
pred_base_bridges_data = list()
pred_base_supermic_data = list()
pred_base_osg_data = list()

pred_max_comet_data = list()
pred_max_bridges_data = list()
pred_max_supermic_data = list()
pred_max_osg_data = list()


with open('time_prederr_base__bridges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_base_bridges_data.append(fmt_row)

with open('time_prederr_base__comet.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_base_comet_data.append(fmt_row)

with open('time_prederr_base__supermic.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_base_supermic_data.append(fmt_row)

with open('time_prederr_base__osg_no_perf.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_base_osg_data.append(fmt_row)


pred_base_bridges_data.sort(key=lambda x: x[0])
z_pred_base_bridges_data = map(list, zip(*pred_base_bridges_data))
pred_base_comet_data.sort(key=lambda x: x[0])
z_pred_base_comet_data = map(list, zip(*pred_base_comet_data))
pred_base_supermic_data.sort(key=lambda x: x[0])
z_pred_base_supermic_data = map(list, zip(*pred_base_supermic_data))
pred_base_osg_data.sort(key=lambda x: x[0])
z_pred_base_osg_data = map(list, zip(*pred_base_osg_data))


with open('time_prederr_max__bridges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_max_bridges_data.append(fmt_row)

with open('time_prederr_max__comet.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_max_comet_data.append(fmt_row)

with open('time_prederr_max__supermic.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_max_supermic_data.append(fmt_row)

with open('time_prederr_max__osg_no_perf.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_max_osg_data.append(fmt_row)


pred_max_bridges_data.sort(key=lambda x: x[0])
z_pred_max_bridges_data = map(list, zip(*pred_max_bridges_data))
pred_max_comet_data.sort(key=lambda x: x[0])
z_pred_max_comet_data = map(list, zip(*pred_max_comet_data))
pred_max_supermic_data.sort(key=lambda x: x[0])
z_pred_max_supermic_data = map(list, zip(*pred_max_supermic_data))
pred_max_osg_data.sort(key=lambda x: x[0])
z_pred_max_osg_data = map(list, zip(*pred_max_osg_data))

plt.close('all')

plt.rcParams["figure.figsize"] = [12, 5]
fig, ax = plt.subplots()
ax.set_title("Execution Time Prediction Error", fontsize=20)

x = z_pred_base_bridges_data[0]
ax.errorbar(x, z_pred_base_bridges_data[1], yerr=z_pred_base_bridges_data[2], label='Bridges', color='blue', linestyle='--', capsize=2)
ax.errorbar(x, z_pred_base_comet_data[1], yerr=z_pred_base_comet_data[2], label='Comet', color='green', linestyle='--', capsize=2)
ax.errorbar(x, z_pred_base_supermic_data[1], yerr=z_pred_base_supermic_data[2], label='SuperMIC', color='red', linestyle='--', capsize=2)
ax.errorbar(x, z_pred_base_osg_data[1], yerr=z_pred_base_osg_data[2], label='OSG', color='c', linestyle='--', capsize=2)

#ax.errorbar(x, z_pred_max_bridges_data[1], yerr=z_pred_max_bridges_data[2], label='Bridges_max', color='blue', linestyle=':')
#ax.errorbar(x, z_pred_max_comet_data[1], yerr=z_pred_max_comet_data[2], label='Comet_max', color='green', linestyle=':')
#ax.errorbar(x, z_pred_max_supermic_data[1], yerr=z_pred_max_supermic_data[2], label='SuperMIC_max', color='red', linestyle=':')
#ax.errorbar(x, z_pred_max_osg_data[1], yerr=z_pred_max_osg_data[2], label='OSG_max', color='darkcyan', linestyle=':')

ax.set_xscale('log')

ax.set_xlim(950, 105000)
ax.set_ylim(0, 225)

ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)

ax.set_xlabel('Number of Timesteps', fontsize=14)
ax.set_ylabel('Prediction Error (%)', fontsize=14)

ax.legend(loc='upper left', fontsize=14, ncol=2)

#fig.set_size_inches(9.5, 7)
#plt.show()

plt.savefig('avg_time_err.pdf', bbox_inches='tight', dpi=144)
plt.savefig('avg_time_err.png', bbox_inches='tight', dpi=144)
