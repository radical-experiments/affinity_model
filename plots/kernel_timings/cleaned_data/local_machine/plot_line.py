import sys

from matplotlib import pyplot as plt


filename = sys.argv[1]

title = ""
x = list()
labels = list()
avg = list()
confidence = list()

with open(filename, 'r') as f:
    i = 0
    for row in f:
        row_list = row.strip().split(',')

        if i == 0:
            title = row_list[0]
            x = row_list[1:]
            print x
        else:
            if i % 2 == 1:
                labels.append(row_list[0])
                avg.append(map(float, row_list[1:]))
            else:
                confidence.append(map(float, row_list[1:]))
        
        i += 1


plt.close('all')

fig, ax = plt.subplots()
ax.set_title(title)
ax.set_xscale('log')
ax.grid(True)

for i in range(len(avg)):
    (_, caps, _) = ax.errorbar(x, avg[i], yerr=confidence[i], label=labels[i])
    for cap in caps:
        cap.set_linewidth(5)

ax.legend(loc='upper left')

plt.show()
