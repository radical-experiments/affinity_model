import csv
import sys

filename_model = sys.argv[1]
filename_exp = sys.argv[2]

resource = list()
predicted = list()
actual = list()

with open(filename_model, "rb") as csvfile:
    c = csv.reader(csvfile)
    for row in c:
        resource.append(row[0])
        predicted.append(float(row[1]))

with open(filename_exp, "rb") as csvfile:
    c = csv.reader(csvfile)
    for row in c:
        actual.append(float(row[1]))

print predicted
print actual

pct_err = list()

for i in range(len(predicted)):
    err = abs(predicted[i] - actual[i]) / actual[i] * 100
    pct_err.append(err)

with open("prediction_percent_errors.csv", "wb") as csvfile:
    c = csv.writer(csvfile, delimiter=',')
    
    for i in range(len(predicted)):
        c.writerow(resource[i] + "," + str(pct_err[i]))

print pct_err
