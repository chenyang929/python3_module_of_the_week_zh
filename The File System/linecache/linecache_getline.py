# linecache_getline.py

import linecache
from linecache_data import lorem, make_tempfile, cleanup

filename = make_tempfile()

print('SOURCE:')
print('{!r}'.format(lorem.split('\n')[4]))
print()
print('CACHE:')
print('{!r}'.format(linecache.getline(filename, 5)))

cleanup(filename)