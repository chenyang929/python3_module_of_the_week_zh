# decimal_instance_context.py

import decimal

c = decimal.getcontext().copy()
c.prec = 3

pi = c.create_decimal('3.1415')

print('PI   :', pi)

print('RESULT:', decimal.Decimal('2.01') * pi)
