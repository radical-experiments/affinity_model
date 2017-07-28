import csv
from pprint import pprint


cleaned_data = list()
with open("condor_status_cpu", 'r') as c_i:
    reader = csv.reader(c_i)
    for row in reader:
        stripped_row = [entry for entry in row if entry and entry != '0']
        if stripped_row[1] == "undefined":
            continue
        entry = [stripped_row[0], " ".join(stripped_row[1:])]
        cleaned_data.append(entry)

with open('condor_status_cpu_cleaned.csv', 'w') as c_o:
    writer = csv.writer(c_o)
    writer.writerows(cleaned_data)


unq_proc_type = list()
with open('condor_status_cpu_cleaned.csv', 'r') as c_i:
    reader = csv.reader(c_i)
    for row in reader:
        if row[1] not in unq_proc_type:
            unq_proc_type.append(row[1])

unq_proc_type = sorted(unq_proc_type)
with open('condor_unique_cpu_type.csv', 'w') as c_o:
    writer = csv.writer(c_o)
    for proc_type in unq_proc_type:
        writer.writerow([proc_type])
