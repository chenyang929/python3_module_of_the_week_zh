# itertools_count.py

from itertools import count

for i in zip(count(1), ['a', 'b', 'c']):
    print(i)