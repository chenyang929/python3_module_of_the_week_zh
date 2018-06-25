# dbm_intvalue.py

import dbm

with dbm.open('example.db', 'w') as db:
    try:
        db['one'] = 1
    except TypeError as err:
        print(err)