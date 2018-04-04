# collections_chainmap_reorder.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(d1, d2)
print(m.maps)
print('c={}'.format(m['c']))

# 反向列表
m.maps = list(reversed(m.maps))
print(m.maps)
print('c={}'.format(m['c']))
