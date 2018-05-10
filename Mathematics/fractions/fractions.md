# fractions -- Rational Numbers
> 目的：实现一个类，用于处理有理数。

## Creating Fraction Instances
与十进制模块一样，可以通过多种方式创建新值。一种简单的方法是把它们从分子和分母中分离出来:
<pre><code># fractions_create_integers.py

import fractions

for n, d in [(1, 2), (2, 4), (3, 6)]:
    f = fractions.Fraction(n, d)
    print('{}/{} = {}'.format(n, d, f))</pre></code>
最小公分母保持为新值的计算。
<pre><code>$ python fractions_create_integers.py
1/2 = 1/2
2/4 = 1/2
3/6 = 1/2</pre></code>
另一种创建分数的方法是使用<分子> / <分母>:
<pre><code># fractions_create_strings.py

import fractions

for s in ['1/2', '2/4', '3/6']:
    f = fractions.Fraction(s)
    print('{} = {}'.format(s, f))</pre></code>
对字符串进行解析以找到分子和分母值。
<pre><code>$ python fractions_create_strings.py
1/2 = 1/2
2/4 = 1/2
3/6 = 1/2</pre></code>
字符串还可以使用更常用的十进制或浮点数的符号，这些数字在一段时间内被分隔。
支持任何可以通过float()解析的字符串，和不表示“不是一个数字”(NaN)或一个无限值。
<pre><code># fractions_create_strings_floats.py

import fractions

for s in ['0.5', '1.5', '2.0', '5e-1']:
    f = fractions.Fraction(s)
    print('{0:>4} = {1}'.format(s, f))</pre></code>
用浮点值表示的分子和分母值是自动计算的。
<pre><code>$ python fractions_create_strings_floats.py
 0.5 = 1/2
 1.5 = 3/2
 2.0 = 2
5e-1 = 1/2</pre></code>
还可以直接从其他rational值的表示(例如浮点数或小数)来创建分数实例。
<pre><code># fractions_from_float.py

import fractions

for v in [0.1, 0.5, 1.5, 2.0]:
    print('{} = {}'.format(v, fractions.Fraction(v)))</pre></code>
不能准确表达的浮点值可能会产生意想不到的结果。
<pre><code>$ python fractions_from_float.py
0.1 = 3602879701896397/36028797018963968
0.5 = 1/2
1.5 = 3/2
2.0 = 2</pre></code>
使用值的十进制表示给出了预期的结果。
<pre><code># fractions_from_decimal.py

import decimal
import fractions

values = [
    decimal.Decimal('0.1'),
    decimal.Decimal('0.5'),
    decimal.Decimal('1.5'),
    decimal.Decimal('2.0'),
]

for v in values:
    print('{} = {}'.format(v, fractions.Fraction(v)))</pre></code>
十进制的内部实现不受标准浮点表示法的精度错误的影响。
<pre><code>$ python fractions_from_decimal.py
0.1 = 1/10
0.5 = 1/2
1.5 = 3/2
2.0 = 2</pre></code>
## Arithmetic
一旦分数被实例化，它们就可以用于数学表达式。
<pre><code># fractions_arithmetic.py

import fractions

f1 = fractions.Fraction(1, 2)
f2 = fractions.Fraction(3, 4)

print('{} + {} = {}'.format(f1, f2, f1 + f2))
print('{} - {} = {}'.format(f1, f2, f1 - f2))
print('{} * {} = {}'.format(f1, f2, f1 * f2))
print('{} / {} = {}'.format(f1, f2, f1 / f2))</pre></code>
支持所有标准操作符。
<pre><code>$ python fractions_arithmetic.py
1/2 + 3/4 = 5/4
1/2 - 3/4 = -1/4
1/2 * 3/4 = 3/8
1/2 / 3/4 = 2/3</pre></code>
## Approximating Values
分数的一个有用特性是将浮点数转换为近似的合理值的能力。
<pre><code># fractions_limit_denominator.py

import fractions
import math

print('PI       =', math.pi)

f_pi = fractions.Fraction(str(math.pi))
print('No limit = ', f_pi)

for i in [1, 6, 11, 60, 70, 90, 100]:
    limited = f_pi.limit_denominator(i)
    print('{0:8} = {1}'.format(i, limited))</pre></code>
分数的值可以通过限制分母的大小来控制。
<pre><code>$ python fractions_limit_denominator.py
PI       = 3.141592653589793
No limit =  3141592653589793/1000000000000000
       1 = 3
       6 = 19/6
      11 = 22/7
      60 = 179/57
      70 = 201/64
      90 = 267/85
     100 = 311/99</pre></code>
