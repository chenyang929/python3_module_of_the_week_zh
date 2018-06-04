# linecache_out_of_range.py

import linecache
from linecache_data import make_tempfile, cleanup

filename = make_tempfile()

not_there = linecache.getline(filename, 500)
print('NOT THERE: {!r} include {} characters'.format(not_there, len(not_there)))

cleanup(filename)
