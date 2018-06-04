# linecache_empty_line.py
import linecache
from linecache_data import make_tempfile, cleanup

filename = make_tempfile()

print('BLANK : {!r}'.format(linecache.getline(filename, 8)))

cleanup(filename)