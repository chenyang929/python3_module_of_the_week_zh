# itertools_chain_from_iterable.py

from itertools import chain


def make_iterables_to_chain():
    yield [1, 2, 3]
    yield ['a', 'b', 'c']


for i in chain.from_iterable(make_iterables_to_chain()):
    print(i, end=' ')
print()