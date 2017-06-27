import math
import csv

import numpy
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
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

bridges = sorted(bridges)
comet = sorted(comet)
gordon = sorted(comet)
stampede = sorted(stampede)
supermic = sorted(supermic)
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

fig, axes = plt.subplots(nrows=3, ncols=2)
ax_bridges = axes[0, 0]
ax_comet = axes[0, 1]
ax_gordon = axes[1, 0]
ax_stampede = axes[1, 1]
ax_supermic = axes[2, 0]

density_bridges = stats.kde.gaussian_kde(bridges)
density_comet = stats.kde.gaussian_kde(comet)
density_gordon = stats.kde.gaussian_kde(gordon)
density_stampede = stats.kde.gaussian_kde(stampede)
density_supermic = stats.kde.gaussian_kde(supermic)

df_bridges = pd.Series(bridges)
df_comet = pd.Series(comet)
df_gordon = pd.Series(gordon)
df_stampede = pd.Series(stampede)
df_supermic = pd.Series(supermic)

df_bridges.hist(cumulative=True, normed=1, bins=100, ax=ax_bridges, color='green', alpha=0.3)
df_comet.hist(cumulative=True, normed=1, bins=100, ax=ax_comet, color='blue', alpha=0.3)
df_gordon.hist(cumulative=True, normed=1, bins=100, ax=ax_gordon, color='red', alpha=0.3)
df_stampede.hist(cumulative=True, normed=1, bins=100, ax=ax_stampede, color='orange', alpha=0.3)
df_supermic.hist(cumulative=True, normed=1, bins=100, ax=ax_supermic, color='black', alpha=0.3)

#df = pd.DataFrame([bridges, comet, gordon, stampede, supermic])
#df = df.transpose()
#df.columns = ['bridges', 'comet', 'gordon', 'stampede', 'supermic']
#df.hist(bins=50)

print axes[0, 0]

"""
df_bridges.plot(kind='density')
df_comet.plot(kind='density')
df_gordon.plot(kind='density')
df_stampede.plot(kind='density')
df_supermic.plot(kind='density')
"""

tx = numpy.arange(0., 1500, 10)
"""
pdf_bridges = density_bridges(tx)
pdf_comet = density_comet(tx)
pdf_gordon = density_gordon(tx)
pdf_stampede = density_stampede(tx)
pdf_supermic = density_supermic(tx)

cdf_bridges = [sum(pdf_bridges[0:i]) for i in range(len(pdf_bridges))]
cdf_comet = [sum(pdf_comet[0:i]) for i in range(len(pdf_comet))]
cdf_gordon = [sum(pdf_gordon[0:i]) for i in range(len(pdf_gordon))]
cdf_stampede = [sum(pdf_stampede[0:i]) for i in range(len(pdf_stampede))]
cdf_supermic = [sum(pdf_supermic[0:i]) for i in range(len(pdf_supermic))]

print cdf_bridges

#plt.plot(tx, density_bridges(tx), label='bridges (actual)', color='green', linestyle='solid', linewidth=1)
#plt.plot(tx, density_comet(tx), label='comet (actual)', color='blue', linestyle='solid', linewidth=1)
#plt.plot(tx, density_gordon(tx), label='gordon (actual)', color='red', linestyle='solid', linewidth=1)
#plt.plot(tx, density_stampede(tx), label='stampede (actual)', color='orange', linestyle='solid', linewidth=1)
#plt.plot(tx, density_supermic(tx), label='supermic (actual)', color='black', linestyle='solid', linewidth=1)

plt.plot(tx, cdf_bridges, label='bridges (actual)', color='green', linestyle='solid', linewidth=1)
plt.plot(tx, cdf_comet, label='comet (actual)', color='blue', linestyle='solid', linewidth=1)
plt.plot(tx, cdf_gordon, label='gordon (actual)', color='red', linestyle='solid', linewidth=1)
plt.plot(tx, cdf_stampede, label='stampede (actual)', color='orange', linestyle='solid', linewidth=1)
plt.plot(tx, cdf_supermic, label='supermic (actual)', color='black', linestyle='solid', linewidth=1)
"""

ax_bridges.axvline(x=predictions['bridges'], label='bridges (predicted)', color='green', linestyle='dashed', linewidth=2.5)
ax_comet.axvline(x=predictions['comet'], label='comet (predicted)', color='blue', linestyle='dashed', linewidth=2.5)
ax_gordon.axvline(x=predictions['gordon'], label='gordon (predicted)', color='red', linestyle='dashed', linewidth=2.5)
ax_stampede.axvline(x=predictions['stampede'], label='stampede (predicted)', color='orange', linestyle='dashed', linewidth=2.5)
ax_supermic.axvline(x=predictions['supermic'], label='supermic (predicted)', color='black', linestyle='dashed', linewidth=2.5)



matplotlib.rcParams.update({'font.size': 18})
plt.axis([0, 1500, 0, 1.1])
plt.xlabel(r'$T_x$' + ', (s)', fontsize=18)
plt.ylabel('Density', fontsize=18)
plt.title('Histogram of ' + r'$T_x$', fontsize=24)
plt.legend(loc='upper left')
plt.grid(True)

plt.show()
