# copy_recursion.py

import copy


class Graph:
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    def add_connection(self, other):
        self.connections.append(other)

    def __repr__(self):
        return 'Graph(name={}, id={})'.format(self.name, id(self))

    def __deepcopy__(self, memodict={}):
        print('\nCalling __deepcopy__ for {!r}'.format(self))
        if self in memodict:
            existing = memodict.get(self)
            print('  Already copied to {!r}'.format(existing))
            return existing
        print('  Memo dictionary')
        if memodict:
            for k, v in memodict.items():
                print('  {}:{}'.format(k, v))
        else:
            print('  (empty)')
        dup = Graph(copy.deepcopy(self.name, memodict), [])
        print('  Coping to new object {}'.format(dup))
        memodict[self] = dup
        for c in self.connections:
            dup.add_connection(copy.deepcopy(c, memodict))
        return dup


root = Graph('root', [])
a = Graph('a', [root])
b = Graph('b', [a, root])
root.add_connection(a)
root.add_connection(b)

dup = copy.deepcopy(root)
