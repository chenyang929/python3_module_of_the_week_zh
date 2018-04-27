# heapq_heapush.py

import heapq
from heapq_heapdata import data
from heapq_showtree import show_tree

heap = []
print('random :', data)
print()

for n in data:
    print('add {:>3}:'.format(n))
    heapq.heappush(heap, n)
    show_tree(heap)
