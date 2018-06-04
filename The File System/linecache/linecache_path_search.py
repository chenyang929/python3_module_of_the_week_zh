# linecache_path_search.py

import linecache
import os

module_line = linecache.getline('linecache.py', 3)
print('MODULE:')
print(repr(module_line))

file_src = linecache.__file__
if file_src.endswith('.pyc'):
    file_src = file_src[:-1]
print('\nFILE:')
with open(file_src, 'r') as f:
    file_line = f.readlines()[2]
print(repr(file_line))