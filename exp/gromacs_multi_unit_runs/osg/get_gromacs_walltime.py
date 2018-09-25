import sys
import csv


run_times = [100000]
with open("osg_timing.txt") as f_in:
    for line in f_in:
        run_time = [entry for entry in line.split(' ') if entry]
        run_times.append(run_time[3])


with open("time__osg.csv", "w") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(run_times)
