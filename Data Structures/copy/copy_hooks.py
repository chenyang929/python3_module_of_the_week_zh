# copy_hooks.py

import copy
import functools


@functools.total_ordering
class MyClass:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name

    def __copy__(self):
        print('__copy__()')
        return MyClass(self.name)

    def __deepcopy__(self, memodict={}):
        print('__deepcopy__({})'.format(memodict))
        return MyClass(copy.deepcopy(self.name, memodict))


a = MyClass('a')

sc = copy.copy(a)
dc = copy.deepcopy(a)
