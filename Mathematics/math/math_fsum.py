# math_fsum.py

import math

values = [0.1] * 10

print('Input values:', values)

print('sum()       : {:.20f}'.format(sum(values)))

s = 0.0
for i in values:
    s += i
print('for-loop    : {:.20f}'.format(s))
print('math.fsum() : {:.20f}'.format(math.fsum(values)))
