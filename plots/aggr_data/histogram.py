import csv

import numpy
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats

bridges = list()
comet = list()
gordon = list()
stampede = list()
supermic = list()

predictions = dict()

with open('bridges_1024.csv') as csvfile:
    c = csv.reader(csvfile)
    for row in c:
        bridges.append(float(row[0]))

with open('comet_1024.csv') as csvfile:
    c = csv.reader(csvfile)
    for row in c:
        comet.append(float(row[0]))

with open('gordon_1024.csv') as csvfile:
    c = csv.reader(csvfile)
    for row in c:
        gordon.append(float(row[0]))

with open('stampede_1024.csv') as csvfile:
    c = csv.reader(csvfile)
    for row in c:
        stampede.append(float(row[0]))

with open('supermic_1024.csv') as csvfile:
    c = csv.reader(csvfile)
    for row in c:
        supermic.append(float(row[0]))

with open('pred_max_tx_converted.csv') as csvfile:
    c = csv.reader(csvfile)
    for row in c:
        predictions[row[0]] = float(row[1])

#print bridges
#print comet
#print gordon
#print stampede
#print supermic

#plt.hist(bridges, 50, normed=1, facecolor='green', alpha=0.5)
#plt.hist(comet, 50, normed=1, facecolor='blue', alpha=0.5)
#plt.hist(gordon, 50, normed=1, facecolor='red', alpha=0.5)
#plt.hist(stampede, 50, normed=1, facecolor='orange', alpha=0.5)
#plt.hist(supermic, 50, normed=1, facecolor='black', alpha=0.5)

density_bridges = stats.kde.gaussian_kde(bridges)
density_comet = stats.kde.gaussian_kde(comet)
density_gordon = stats.kde.gaussian_kde(gordon)
density_stampede = stats.kde.gaussian_kde(stampede)
density_supermic = stats.kde.gaussian_kde(supermic)

tx = numpy.arange(0., 1500, 10)

plt.plot(tx, density_bridges(tx), label='bridges (actual)', color='green', linestyle='solid', linewidth=1)
plt.plot(tx, density_comet(tx), label='comet (actual)', color='blue', linestyle='solid', linewidth=1)
plt.plot(tx, density_gordon(tx), label='gordon (actual)', color='red', linestyle='solid', linewidth=1)
plt.plot(tx, density_stampede(tx), label='stampede (actual)', color='orange', linestyle='solid', linewidth=1)
plt.plot(tx, density_supermic(tx), label='supermic (actual)', color='black', linestyle='solid', linewidth=1)

plt.axvline(x=predictions['bridges'], label='bridges (predicted)', color='green', linestyle='dashed', linewidth=1.5)
plt.axvline(x=predictions['comet'], label='comet (predicted)', color='blue', linestyle='dashed', linewidth=1.5)
plt.axvline(x=predictions['gordon'], label='gordon (predicted)', color='red', linestyle='dashed', linewidth=1.5)
plt.axvline(x=predictions['stampede'], label='stampede (predicted)', color='orange', linestyle='dashed', linewidth=1.5)
plt.axvline(x=predictions['supermic'], label='supermic (predicted)', color='black', linestyle='dashed', linewidth=1.5)



matplotlib.rcParams.update({'font.size': 18})
plt.axis([0, 1000, 0, 0.025])
plt.xlabel(r'$T_x$' + ' (s)', fontsize=18)
plt.ylabel('Density', fontsize=18)
plt.title('Histogram of ' + r'$T_x$', fontsize=24)
plt.legend(loc='upper left')
plt.grid(True)

plt.show()
