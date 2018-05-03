# pprint_arbitrary_object.py

from pprint import pprint


class Node:

    def __init__(self, name, contents=[]):
        self.name = name
        self.contents = contents[:]

    def __repr__(self):
        return (
                'node(' + repr(self.name) + ', ' +
                repr(self.contents) + ')'
        )


trees = [
    Node('node-1'),
    Node('node-2', [Node('node-2-1')]),
    Node('node-3', [Node('node-3-1')]),
]
pprint(trees)
