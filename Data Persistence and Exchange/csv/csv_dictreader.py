# csv_dictreader.py

import csv
import sys

with open(sys.argv[1], 'rt', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)