# collections_chainmap_update_directly.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(d1, d2)
print('Before:')
print(m)
m['c'] = 'C1'
m['b'] = 'B1'
m['e'] = 'E'
print('After:')
print(m)
print('d1', d1)
print('d2', d2)


