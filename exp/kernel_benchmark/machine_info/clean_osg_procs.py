from pprint import pprint
import sys
import csv


fn = sys.argv[1]
f = open(fn)

procs = dict()
proc_company = ["Intel", "AMD"]

for line in f:
    for proc_manufact in proc_company:
        proc_start = line.find(proc_manufact)
        if line.find(proc_manufact) >= 0:
            proc = line[proc_start:].strip()
            proc_name_list = [info for info in proc.split(" ") if info]
            cleaned_proc = " ".join(proc_name_list)
            if cleaned_proc not in procs.keys():
                procs[cleaned_proc] = 1
            else:
                procs[cleaned_proc] += 1
            break

f.close()

with open("proc_list.csv", "w") as g:
    writer = csv.writer(g)
    for proc, occ in procs.iteritems():
        writer.writerow([proc, occ])


pprint(procs)
pprint(len(procs))


