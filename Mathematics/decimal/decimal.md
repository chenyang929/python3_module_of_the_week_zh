# decimal -- Fixed and Floating Point Math
>目的：使用固定和浮点数的十进制运算。

十进制模块使用大多数人熟悉的模型来实现固定和浮点运算，而不是大多数计算机硬件实现的IEEE浮点版本。
一个十进制的实例可以精确地表示任何数字，上下左右，并对有效数字的数目施加一个限制。
## Decimal
十进制值被表示为小数类的实例。构造函数以一个整数或字符串作为参数。
浮点数可以被转换成一个字符串，然后被用来创建一个小数，让调用者显式地处理不能用硬件浮点表示法表示的值的位数。
另外，类方法from_float()转换为精确的十进制表示。
<pre><code># decimal_create.py

import decimal

fmt = '{0:<25} {1:<25}'

print(fmt.format('Input', 'Output'))
print(fmt.format('-'*25, '-'*25))

# Integer
print(fmt.format(5, decimal.Decimal(5)))

# String
print(fmt.format('3.14', decimal.Decimal('3.14')))

# Float
f = 0.1
print(fmt.format(repr(f), decimal.Decimal(str(f))))
print('{:<0.23g} {:<25}'.format(
    f,
    str(decimal.Decimal.from_float(f))[:25])
)</pre></code>
0.1的浮点值不表示为二进制的精确值，因此浮点数的表示形式与十进制值不同。
在输出的最后一行中，完整的字符串表示被截断为25个字符。
<pre><code>$ python decimal_create.py
Input                     Output                   
------------------------- -------------------------
5                         5                        
3.14                      3.14                     
0.1                       0.1                      
0.10000000000000000555112 0.10000000000000000555111</pre></code>
也可以从包含符号标志的元组(0为正数，1为负数)、一组数字和整数指数创建十进制。
<pre><code># decimal_tuple.py

import decimal

# Tuple
t = (1, (1, 1), -2)
print('Input   :', t)
print('Decimal :', decimal.Decimal(t))</pre></code>
基于元组的表示法创建起来不太方便，但是它提供了一种输出十进制值而不丢失精度的便携式方法。
元组表单可以通过网络传输，或者存储在不支持精确的十进制值的数据库中，然后再返回到一个十进制实例。
## Formatting
Decimal响应Python的字符串格式化协议，使用与其他数值类型相同的语法和选项。
<pre><code># decimal_format.py

import decimal

d = decimal.Decimal(1.1)
print('Precision:')
print('{:.1}'.format(d))
print('{:.2}'.format(d))
print('{:.3}'.format(d))
print('{:.18}'.format(d))

print('\nWidth and precision combined:')
print('{:5.1f} {:5.1g}'.format(d, d))
print('{:5.2f} {:5.2g}'.format(d, d))
print('{:5.2f} {:5.2g}'.format(d, d))

print('\nZero padding:')
print('{:05.1}'.format(d))
print('{:05.2}'.format(d))
print('{:05.3}'.format(d))</pre></code>
格式字符串可以控制输出的宽度、精度(有效数字的数量)以及如何填充该值以填充宽度。
<pre><code>$ python decimal_format.py
Precision:
1
1.1
1.10
1.10000000000000009

Width and precision combined:
  1.1     1
 1.10   1.1
 1.10   1.1

Zero padding:
00001
001.1
01.10</pre></code>
## Arithmetic
十进制重载了简单的算术运算符，所以实例可以和内置的数值类型一样被操作。
<pre><code># decimal_operators.py

import decimal

a = decimal.Decimal('5.1')
b = decimal.Decimal('3.14')
c = 4
d = 3.14

print('a     =', repr(a))
print('b     =', repr(b))
print('c     =', repr(c))
print('d     =', repr(d))
print()

print('a + b =', a + b)
print('a - b =', a - b)
print('a * b =', a * b)
print('a / b =', a / b)
print()

print('a + c =', a + c)
print('a - c =', a - c)
print('a * c =', a * c)
print('a / c =', a / c)
print()

print('a + d =', end=' ')
try:
    print(a + d)
except TypeError as e:
    print(e)</pre></code>
十进制运算符也接受整数参数，但浮点值必须转换为十进制实例。
<pre><code>$ python decimal_operators.py
a     = Decimal('5.1')
b     = Decimal('3.14')
c     = 4
d     = 3.14

a + b = 8.24
a - b = 1.96
a * b = 16.014
a / b = 1.624203821656050955414012739

a + c = 9.1
a - c = 1.1
a * c = 20.4
a / c = 1.275

a + d = unsupported operand type(s) for +: 'decimal.Decimal' and 'float'</pre></code>
## Special Values
除了期望的数值，十进制还可以表示几个特殊的值，包括无穷大的正值和负值，“不是一个数字”和“零”。
<pre><code># decimal_special.py

import decimal

for value in ['Infinity', 'NaN', '0']:
    print(decimal.Decimal(value), decimal.Decimal('-' + value))
print()

# Math with infinity
print('Infinity + 1:', (decimal.Decimal('Infinity') + 1))
print('-Infinity + 1:', (decimal.Decimal('-Infinity') + 1))

# Print comparing NaN
print(decimal.Decimal('NaN') == decimal.Decimal('Infinity'))
print(decimal.Decimal('NaN') != decimal.Decimal(1))</pre></code>
无限值的加法将返回另一个无限值。与NaN的相等比较总是返回false，而不等比较总是返回true。
比较对NaN的排序顺序是没有定义的，结果是错误的。
<pre><code>$ python decimal_special.py
Infinity -Infinity
NaN -NaN
0 -0

Infinity + 1: Infinity
-Infinity + 1: -Infinity
False
True</pre></code>
## Context
到目前为止，所有的示例都使用了decimal模块的默认行为。通过使用上下文，可以覆盖诸如精确维护、如何执行舍入、错误处理等设置。
上下文可以应用于线程中的所有十进制实例，或者在一个小的代码区域内本地应用。
### Current Context
要检索当前全局上下文，请使用getcontext。
<pre><code># decimal_getcontext.py

import decimal

context = decimal.getcontext()

print('Emax     =', context.Emax)
print('Emin     =', context.Emin)
print('capitals =', context.capitals)
print('prec     =', context.prec)
print('rounding =', context.rounding)
print('flags    =')
for f, v in context.flags.items():
    print('  {}: {}'.format(f, v))
print('traps    =')
for t, v in context.traps.items():
    print('  {}: {}'.format(t, v))</pre></code>
这个示例脚本展示了上下文的公共属性。
<pre><code>$ python decimal_getcontext.py
Emax     = 999999
Emin     = -999999
capitals = 1
prec     = 28
rounding = ROUND_HALF_EVEN
flags    =
  <class 'decimal.InvalidOperation'>: False
  <class 'decimal.FloatOperation'>: False
  <class 'decimal.DivisionByZero'>: False
  <class 'decimal.Overflow'>: False
  <class 'decimal.Underflow'>: False
  <class 'decimal.Subnormal'>: False
  <class 'decimal.Inexact'>: False
  <class 'decimal.Rounded'>: False
  <class 'decimal.Clamped'>: False
traps    =
  <class 'decimal.InvalidOperation'>: True
  <class 'decimal.FloatOperation'>: False
  <class 'decimal.DivisionByZero'>: True
  <class 'decimal.Overflow'>: True
  <class 'decimal.Underflow'>: False
  <class 'decimal.Subnormal'>: False
  <class 'decimal.Inexact'>: False
  <class 'decimal.Rounded'>: False
  <class 'decimal.Clamped'>: False</pre></code>
## Precision
上下文的prec属性控制由于算术而产生的新值的精度。文字值按描述保持。
<pre><code># decimal_precision.py

import decimal

d = decimal.Decimal('0.123456')

for i in range(1, 5):
    decimal.getcontext().prec = i
    print(i, ':', d, d*1)</pre></code>
要更改精度，请在1和decimal.MAX_PREC 之间分配一个新值。
<pre><code>$ python decimal_precision.py
1 : 0.123456 0.1
2 : 0.123456 0.12
3 : 0.123456 0.123
4 : 0.123456 0.1235</pre></code>
### Rounding
对于舍入，有几个选项可以使值保持在预期的精度范围内。
- ROUND_CEILING 一直向上到无穷大。
- ROUND_DOWN 总是朝着零。
- ROUND_FLOOR 一直到负无穷。
- ROUND_HALF_DOWN 如果最后一个有效数字大于或等于5，则从0开始，否则为0。
- ROUND_HALF_EVEN 类似于ROUND_HALF_DOWN，但如果值是5，则检查前面的数字。即使是值，也会导致结果被圆滑，而奇数位会导致结果被集中。
- ROUND_HALF_UP 像ROUND_HALF_DOWN，除非最后一个重要的数字是5，它的值从0开始。
- ROUND_UP 离开零。
- ROUND_05UP 如果最后一个数字为0或5，则离开0，否则朝向0。
<pre><code># decimal_rounding.py

import decimal

context = decimal.getcontext()

ROUNDING_MODES = [
    'ROUND_CEILING',
    'ROUND_DOWN',
    'ROUND_FLOOR',
    'ROUND_HALF_DOWN',
    'ROUND_HALF_EVEN',
    'ROUND_HALF_UP',
    'ROUND_UP',
    'ROUND_05UP',
]

header_fmt = '{:10} ' + ' '.join(['{:^8}'] * 6)

print(header_fmt.format(
    ' ',
    '1/8 (1)', '-1/8 (1)',
    '1/8 (2)', '-1/8 (2)',
    '1/8 (3)', '-1/8 (3)',
))
for rounding_mode in ROUNDING_MODES:
    print('{0:10}'.format(rounding_mode.partition('_')[-1]),
          end=' ')
    for precision in [1, 2, 3]:
        context.prec = precision
        context.rounding = getattr(decimal, rounding_mode)
        value = decimal.Decimal(1) / decimal.Decimal(8)
        print('{0:^8}'.format(value), end=' ')
        value = decimal.Decimal(-1) / decimal.Decimal(8)
        print('{0:^8}'.format(value), end=' ')
    print()</pre></code>
这个程序显示了用不同的算法将相同的值舍入不同的精度等级的效果。
<pre><code>$ python decimal_rounding.py
           1/8 (1)  -1/8 (1) 1/8 (2)  -1/8 (2) 1/8 (3)  -1/8 (3)
CEILING      0.2      -0.1     0.13    -0.12    0.125    -0.125  
DOWN         0.1      -0.1     0.12    -0.12    0.125    -0.125  
FLOOR        0.1      -0.2     0.12    -0.13    0.125    -0.125  
HALF_DOWN    0.1      -0.1     0.12    -0.12    0.125    -0.125  
HALF_EVEN    0.1      -0.1     0.12    -0.12    0.125    -0.125  
HALF_UP      0.1      -0.1     0.13    -0.13    0.125    -0.125  
UP           0.2      -0.2     0.13    -0.13    0.125    -0.125  
05UP         0.1      -0.1     0.12    -0.12    0.125    -0.125  </pre></code>

### Local Context
可以使用with语句将上下文应用到代码块中。
<pre><code># decimal_context_manager.py

import decimal

with decimal.localcontext() as c:
    c.prec = 2
    print('Local precision:', c.prec)
    print('3.14 / 3 =', (decimal.Decimal('3.14') / 3))

print()
print('Default precision:', decimal.getcontext().prec)
print('3.14 / 3 =', (decimal.Decimal('3.14') / 3))</pre></code>
上下文支持使用的上下文管理器API，因此设置只应用于块中。
<pre><code>$ python decimal_context_manager.py
Local precision: 2
3.14 / 3 = 1.0

Default precision: 28
3.14 / 3 = 1.046666666666666666666666667</pre></code>
### Pre-Instance Context
上下文还可以用于构建十进制实例，它继承了从上下文转换到转换的精确性和舍入参数。
<pre><code># decimal_instance_context.py

import decimal

c = decimal.getcontext().copy()
c.prec = 3

pi = c.create_decimal('3.1415')

print('PI   :', pi)

print('RESULT:', decimal.Decimal('2.01') * pi)</pre></code>
这让应用程序可以分别从用户数据的精度中选择常量值的精度。
<pre><code>$ python decimal_instance_context.py
PI   : 3.14
RESULT: 6.3114</pre></code>
### Threads
“全局”上下文实际上是线程本地的，因此每个线程都可以使用不同的值进行配置。
<pre><code># decimal_thread_context.py

import decimal
import threading
from queue import PriorityQueue


class Multiplier(threading.Thread):
    def __init__(self, a, b, prec, q):
        self.a = a
        self.b = b
        self.prec = prec
        self.q = q
        threading.Thread.__init__(self)

    def run(self):
        c = decimal.getcontext().copy()
        c.prec = self.prec
        decimal.setcontext(c)
        self.q.put((self.prec, a * b))


a = decimal.Decimal('3.14')
b = decimal.Decimal('1.234')

q = PriorityQueue()
threads = [Multiplier(a, b, i, q) for i in range(1, 6)]
for t in threads:
    t.start()
for t in threads:
    t.join()
for i in range(5):
    prec, value = q.get()
    print('{} {}'.format(prec, value))</pre></code>
这个例子使用指定的方法创建一个新的上下文，然后在每个线程中安装它。
<pre><code>$ python decimal_thread_context.py
1 4
2 3.9
3 3.87
4 3.875
5 3.8748</pre></code>


