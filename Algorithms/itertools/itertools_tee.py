# itertools_tee.py

from itertools import islice, tee, count

r = islice(count(), 5)
i1, i2 = tee(r)

print('i1:', list(i1))
print('i2:', list(i2))