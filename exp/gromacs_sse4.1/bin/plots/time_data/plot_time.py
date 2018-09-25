import csv
import sys
from pprint import pprint
from matplotlib import pyplot as plt


act_comet_data = list()
act_bridges_data = list()
act_supermic_data = list()
act_osg_data = list()

pred_base_comet_data = list()
pred_base_bridges_data = list()
pred_base_supermic_data = list()
pred_base_osg_data = list()

pred_max_comet_data = list()
pred_max_bridges_data = list()
pred_max_supermic_data = list()
pred_max_osg_data = list()

with open('avg_time__bridges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        act_bridges_data.append(fmt_row)

with open('avg_time__comet.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        act_comet_data.append(fmt_row)

with open('avg_time__supermic.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        act_supermic_data.append(fmt_row)

with open('avg_time__osg_no_perf.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        act_osg_data.append(fmt_row)



with open('avg_time_pred_base__bridges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_base_bridges_data.append(fmt_row)

with open('avg_time_pred_base__comet.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_base_comet_data.append(fmt_row)

with open('avg_time_pred_base__supermic.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_base_supermic_data.append(fmt_row)

with open('avg_time_pred_base__osg_no_perf.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_base_osg_data.append(fmt_row)



with open('avg_time_pred_max__bridges.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_max_bridges_data.append(fmt_row)

with open('avg_time_pred_max__comet.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_max_comet_data.append(fmt_row)

with open('avg_time_pred_max__supermic.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_max_supermic_data.append(fmt_row)

with open('avg_time_pred_max__osg_no_perf.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fmt_row = [int(row[0])]
        fmt_row.extend(map(float, row[1:]))
        pred_max_osg_data.append(fmt_row)


act_bridges_data.sort(key=lambda x: x[0])
z_act_bridges_data = map(list, zip(*act_bridges_data))
act_comet_data.sort(key=lambda x: x[0])
z_act_comet_data = map(list, zip(*act_comet_data))
act_supermic_data.sort(key=lambda x: x[0])
z_act_supermic_data = map(list, zip(*act_supermic_data))
act_osg_data.sort(key=lambda x: x[0])
z_act_osg_data = map(list, zip(*act_osg_data))

pred_base_bridges_data.sort(key=lambda x: x[0])
z_pred_base_bridges_data = map(list, zip(*pred_base_bridges_data))
pred_base_comet_data.sort(key=lambda x: x[0])
z_pred_base_comet_data = map(list, zip(*pred_base_comet_data))
pred_base_supermic_data.sort(key=lambda x: x[0])
z_pred_base_supermic_data = map(list, zip(*pred_base_supermic_data))
pred_base_osg_data.sort(key=lambda x: x[0])
z_pred_base_osg_data = map(list, zip(*pred_base_osg_data))

pred_max_bridges_data.sort(key=lambda x: x[0])
z_pred_max_bridges_data = map(list, zip(*pred_max_bridges_data))
pred_max_comet_data.sort(key=lambda x: x[0])
z_pred_max_comet_data = map(list, zip(*pred_max_comet_data))
pred_max_supermic_data.sort(key=lambda x: x[0])
z_pred_max_supermic_data = map(list, zip(*pred_max_supermic_data))
pred_max_osg_data.sort(key=lambda x: x[0])
z_pred_max_osg_data = map(list, zip(*pred_max_osg_data))


plt.close('all')

plt.rcParams['figure.figsize'] = [12, 5]
fig, ax = plt.subplots()
ax.set_title(r"a) Actual and Predicted Execution Time, predicted using $base$", fontsize=20)

x = z_act_bridges_data[0]

ax.errorbar(x, z_act_bridges_data[1], yerr=z_act_bridges_data[2], label='Bridges_Actual', color='blue', linestyle='-')
ax.errorbar(x, z_act_comet_data[1], yerr=z_act_comet_data[2], label='Comet_Actual', color='green', linestyle='-')
ax.errorbar(x, z_act_supermic_data[1], yerr=z_act_supermic_data[2], label='SuperMIC_Actual', color='red', linestyle='-')
ax.errorbar(x, z_act_osg_data[1], yerr=z_act_osg_data[2], label='OSG_Actual', color='darkcyan', linestyle='-')

ax.errorbar(x, z_pred_base_bridges_data[1], yerr=z_pred_base_bridges_data[2], label='Bridges_Pred_base', color='blue', linestyle='--')
ax.errorbar(x, z_pred_base_comet_data[1], yerr=z_pred_base_comet_data[2], label='Comet_Pred_base', color='green', linestyle='--')
ax.errorbar(x, z_pred_base_supermic_data[1], yerr=z_pred_base_supermic_data[2], label='SuperMIC_Pred_base', color='red', linestyle='--')
ax.errorbar(x, z_pred_base_osg_data[1], yerr=z_pred_base_osg_data[2], label='OSG_Pred_base', color='darkcyan', linestyle='--')

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlim(950, 105000)
ax.set_ylim(30, 15000)

ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)

ax.set_xlabel('Number of Timesteps', fontsize=14)
ax.set_ylabel('Time (s)', fontsize=14)

ax.legend(loc='upper left', fontsize=13, ncol=2)

#fig.set_size_inches(9.5, 7)
#plt.show()

plt.savefig('avg_time_pred_base.pdf', bbox_inches='tight', dpi=144)
plt.savefig('avg_time_pred_base.png', bbox_inches='tight', dpi=144)


plt.close('all')
fig, ax = plt.subplots()
ax.set_title(r"b) Actual and Predicted Execution Time, predicted using $max$", fontsize=20)

x = z_act_bridges_data[0]

ax.errorbar(x, z_act_bridges_data[1], yerr=z_act_bridges_data[2], label='Bridges_Actual', color='blue', linestyle='-')
ax.errorbar(x, z_act_comet_data[1], yerr=z_act_comet_data[2], label='Comet_Actual', color='green', linestyle='-')
ax.errorbar(x, z_act_supermic_data[1], yerr=z_act_supermic_data[2], label='SuperMIC_Actual', color='red', linestyle='-')
ax.errorbar(x, z_act_osg_data[1], yerr=z_act_osg_data[2], label='OSG_Actual', color='darkcyan', linestyle='-')

ax.errorbar(x, z_pred_max_bridges_data[1], yerr=z_pred_max_bridges_data[2], label='Bridges_Pred_max', color='blue', linestyle=':')
ax.errorbar(x, z_pred_max_comet_data[1], yerr=z_pred_max_comet_data[2], label='Comet_Pred_max', color='green', linestyle=':')
ax.errorbar(x, z_pred_max_supermic_data[1], yerr=z_pred_max_supermic_data[2], label='SuperMIC_Pred_max', color='red', linestyle=':')
ax.errorbar(x, z_pred_max_osg_data[1], yerr=z_pred_max_osg_data[2], label='OSG_Pred_max', color='darkcyan', linestyle=':')

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlim(950, 105000)
ax.set_ylim(30, 15000)

ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)

ax.set_xlabel('Number of Timesteps', fontsize=14)
ax.set_ylabel('Time (s)', fontsize=14)

ax.legend(loc='upper left', fontsize=13, ncol=2)

#fig.set_size_inches(9.5, 7)
#plt.show()

plt.savefig('avg_time_pred_max.pdf', bbox_inches='tight', dpi=144)
plt.savefig('avg_time_pred_max.png', bbox_inches='tight', dpi=144)
