# collections_ordereddict_equality.py

import collections

print('dict:', end='')
d1 = dict()
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = dict()
d2['b'] = 'B'
d2['a'] = 'A'
d2['c'] = 'C'
print(d1 == d2)

print('OrderedDict:', end='')
d1 = collections.OrderedDict()
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = collections.OrderedDict()
d2['b'] = 'B'
d2['a'] = 'A'
d2['c'] = 'C'
print(d1 == d2)
