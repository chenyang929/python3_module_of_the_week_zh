# csv_reader.py

import csv
import sys

with open(sys.argv[1], 'rt', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)