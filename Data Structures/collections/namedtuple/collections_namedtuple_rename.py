# collections_namedtuple_rename.py

import collections

with_class = collections.namedtuple('Person', 'name class age', rename=True)
print(with_class._fields)

two_ages = collections.namedtuple('Person', 'name age age', rename=True)
print(two_ages._fields)
