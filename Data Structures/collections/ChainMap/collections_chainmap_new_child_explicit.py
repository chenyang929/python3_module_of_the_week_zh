# collections_chainmap_new_child_explicit.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}
d3 = {'e': 'E'}

m1 = collections.ChainMap(d1, d2)
m2 = m1.new_child(d3)   # 等价下面的
m3 = collections.ChainMap(d3, *m1.maps)
print('before:')
print('m1', m1)
print('m2', m2)
print('m3', m3)
m2['a'] = 'A1'
print('after')
print('m1', m1,)
print('m2', m2,)
print('m3', m3)
