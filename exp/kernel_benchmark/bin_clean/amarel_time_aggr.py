import os
import sys
import csv
from pprint import pprint


dirname = sys.argv[1]
run_name = sys.argv[2]

time_data = dict()

with open(dirname+'/'+'time.csv') as c:
    reader = csv.reader(c)

    for row in reader:
        pprint(row)
        cleaned_row = [entry for entry in row if entry]

        run_id = cleaned_row[0].split('__')[-1]
        cleaned_row[0] = run_name + '__' + run_id

        if run_id not in time_data.keys():
            time_data[run_id] = cleaned_row
        else:
            time_data[run_id].extend(cleaned_row[1:])
 
with open(dirname+'/'+run_name+'_time.csv', 'w') as c:
    writer = csv.writer(c)
    for _, time_row in time_data.iteritems():
        writer.writerow(time_row)
