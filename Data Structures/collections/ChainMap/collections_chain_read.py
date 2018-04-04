# collections_chainmap_read.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(d1, d2)   # d1, d2换位下面的'c'值就是'D'
print(m)
print('a={}'.format(m['a']))
print('b={}'.format(m['b']))
print('c={}'.format(m['c']))
print('Keys={}'.format(list(m.keys())))
print('Values={}'.format(list(m.values())))
print('Items:')
for k, v in m.items():
    print('{}={}'.format(k, v))
print('"d" in m: {}'.format('d' in m))
