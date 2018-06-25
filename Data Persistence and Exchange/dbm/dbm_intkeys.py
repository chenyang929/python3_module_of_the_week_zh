# dbm_intkeys.py

import dbm

with dbm.open('example.db', 'w') as db:
    try:
        db[1] = 'one'
    except TypeError as err:
        print(err)