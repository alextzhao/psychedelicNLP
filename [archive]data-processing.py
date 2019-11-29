import csv
with open('trips.csv') as f:
  csv_reader = csv.reader(f)
  for line in csv_reader:
    if printed < 10:
        print(line)
        printed += 1
    else:
        break
