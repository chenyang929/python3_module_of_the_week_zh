# datetime_datetime.py

import datetime

print('Now    :', datetime.datetime.now())
print('Today  :', datetime.datetime.today())
print('UTC Now:', datetime.datetime.utcnow())

FIELDS = [
    'year', 'month', 'day',
    'hour', 'minute', 'second',
    'microsecond',
]

d = datetime.datetime.now()
for attr in FIELDS:
    print('{:15} {}'.format(attr, getattr(d, attr)))

