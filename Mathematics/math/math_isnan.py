# math_isnan.py

import math

x = (10.0 ** 200) * (10.0 ** 200)
y = x / x

print('x =', x)
print('isnan(x) =', math.isnan(x))
print('y = x / x =', x / x)
print('y == nan =', y == float('nan'))
print('isnan(y) =', math.isnan(y))
