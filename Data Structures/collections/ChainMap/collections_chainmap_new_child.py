# collections_chainmap_new_child.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}

m1 = collections.ChainMap(d1, d2)
m2 = m1.new_child()
print('before:')
print('m1 ', m1)
print('m2 ', m2)
m2['c'] = 'C1'
print('after:')
print('m1 ', m1)
print('m2 ', m2)
