# itertools_combinations_with_replacement.py

from itertools import combinations_with_replacement


def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print(''.join(item), end=' ')
    print()


print('Unique pairs:\n')
show(combinations_with_replacement('abcd', r=2))