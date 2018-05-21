# heapq_heapify.py

import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data


print('random    :', data)
heapq.heapify(data)
print('heapified :')
show_tree(data)
