# itertools_chain.py

from itertools import chain

for i in chain([1, 2, 3], ['a', 'b', 'c']):
    print(i, end=' ')
print()