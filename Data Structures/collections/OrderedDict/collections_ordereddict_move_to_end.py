# collections_ordereddict_move_to_end.py

import collections

d = collections.OrderedDict([('a', 'A'), ('b', 'B'), ('c', 'C')])
print('Before:')
for k, v in d.items():
    print(k, v)

d.move_to_end('b')

print('\nmove_to_end():')
for k, v in d.items():
    print(k, v)

d.move_to_end('b', last=False)   # last默认为True,最末尾的不会移动到头部

print('\nmove_to_end(last=False):')
for k, v in d.items():
    print(k, v)
