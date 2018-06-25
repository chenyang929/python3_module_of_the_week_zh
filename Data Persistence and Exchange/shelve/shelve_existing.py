# shelve_existing.py

import shelve

with shelve.open('test_shelf.db') as s:
    existing = s['key1']

print(existing)