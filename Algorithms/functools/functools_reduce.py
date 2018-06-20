# functools_reduce.py

import functools


def do_reduce(a, b):
    print('do_reduce({}, {})'.format(a, b))
    return a + b


data = range(1, 5)
print(data)
result = functools.reduce(do_reduce, data)
print('result: {}'.format(result))