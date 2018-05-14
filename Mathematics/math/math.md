# math -- Mathematical Functions
> 目的：为专门的数学运算提供函数。

数学模块实现了许多IEEE函数，这些功能通常可以在本机平台C库中找到，用于使用浮点值(包括对数和三角运算)进行复杂的数学运算。
## Special Constants
许多数学运算依赖于特殊的常数。例如π的值(π), e, nan(不是一个数字), 和无穷。
<pre><code># math_constants.py

import math

print('  π: {:.30f}'.format(math.pi))
print('  e: {:.30f}'.format(math.e))
print('nan: {:.30f}'.format(math.nan))
print('inf: {:.30f}'.format(math.inf))</pre></code>
仅在平台的浮点C库中，π和e的精度都是有限的。
<pre><code>$ python math_constants.py
  π: 3.141592653589793115997963468544
  e: 2.718281828459045090795598298428
nan: nan
inf: inf</pre></code>
## Testing for Exceptional Values
浮点计算可以产生两种特殊值。其中的第一个，inf(无穷大)，当用于持有浮点值的双值从一个具有较大绝对值的值溢出时出现。
<pre><code># math_isinf.py

import math

print('{:^3} {:6} {:6} {:6}'.format(
    'e', 'x', 'x**2', 'isinf'))
print('{:-^3} {:-^6} {:-^6} {:-^6}'.format(
    '', '', '', ''))

for e in range(0, 201, 20):
    x = 10.0 ** e
    y = x * x
    print('{:3d} {:<6g} {:<6g} {!s:6}'.format(e, x, y, math.isinf(y)))</pre></code>
当这个例子中的指数足够大时，x的平方就不再是一个双精度型的，而是这个值被记录为无穷大。
<pre><code>$ python math_isinf.py
 e  x      x**2   isinf 
--- ------ ------ ------
  0 1      1      False 
 20 1e+20  1e+40  False 
 40 1e+40  1e+80  False 
 60 1e+60  1e+120 False 
 80 1e+80  1e+160 False 
100 1e+100 1e+200 False 
120 1e+120 1e+240 False 
140 1e+140 1e+280 False 
160 1e+160 inf    True  
180 1e+180 inf    True  
200 1e+200 inf    True </pre></code>
然而，并非所有浮点数溢出都会导致(inf)无穷值。计算带有浮点值的指数，可能会引起溢出错误，而不是保存inf结果。
<pre><code># math_overflow.py

x = 10.0 ** 200

print('x    =', x)
print('x*x  =', x * x)
print('x**2 =', end=' ')
try:
    print(x ** 2)
except OverflowError as err:
    print(err)</pre></code>
这种差异是由C Python使用的库中的实现差异造成的。
<pre><code>$ python math_overflow.py
x    = 1e+200
x*x  = inf
x**2 = (34, 'Result too large')</pre></code>
使用无限值的除法运算是没有定义的。将一个数字除以无穷的结果是nan(不是一个数字)。
<pre><code># math_isnan.py

import math

x = (10.0 ** 200) * (10.0 ** 200)
y = x / x

print('x =', x)
print('isnan(x) =', math.isnan(x))
print('y = x / x =', x / x)
print('y == nan =', y == float('nan'))
print('isnan(y) =', math.isnan(y))</pre></code>
nan不等于任何值，甚至本身，所以要检查nan使用isnan()。
<pre><code>$ python math_isnan.py
x = inf
isnan(x) = False
y = x / x = nan
y == nan = False
isnan(y) = True</pre></code>
使用isfinite()来检查常规数字，或者是inf或nan的特殊值。
<pre><code># math_isfinite.py

import math

for f in [0.0, 1.0, math.pi, math.e, math.inf, math.nan]:
    print('{:5.2f} {!s}'.format(f, math.isfinite(f)))</pre></code>
isfinite()对于异常情况返回False，反之True。
<pre><code>$ python math_isfinite.py
 0.00 True
 1.00 True
 3.14 True
 2.72 True
  inf False
  nan False</pre></code>
## Comparing
对浮点值的比较可能是错误的，因为计算的每一步都可能由于数字表示而引入错误。
isclose()函数使用一个稳定的算法来最小化这些错误，并为相对和绝对比较提供了一种方法。所用的公式是等价的。
> abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

在默认情况下，isclose()使用相对比较，将公差设置为1e-09，这意味着值之间的差值必须小于或等于1e-09倍于a和b之间的较大绝对值。
通过一个关键字参数rel_tol()来改变容错。在本例中，值必须在彼此的10%以内。
<pre><code># math_isclose.py

import math

INPUTS = [
    (1000, 900, 0.1),
    (100, 90, 0.1),
    (10, 9, 0.1),
    (1, 0.9, 0.1),
    (0.1, 0.09, 0.1),
]

print('{:^8} {:^8} {:^8} {:^8} {:^8} {:^8}'.format(
    'a', 'b', 'rel_tol', 'abs(a-b)', 'tolerance', 'close')
)
print('{:-^8} {:-^8} {:-^8} {:-^8} {:-^8} {:-^8}'.format(
    '-', '-', '-', '-', '-', '-'),
)

fmt = '{:8.2f} {:8.2f} {:8.2f} {:8.2f} {:8.2f} {!s:>8}'

for a, b, rel_tol in INPUTS:
    close = math.isclose(a, b, rel_tol=rel_tol)
    tolerance = rel_tol * max(abs(a), abs(b))
    abs_diff = abs(a - b)
    print(fmt.format(a, b, rel_tol, abs_diff, tolerance, close))</pre></code>
0.1和0.09之间的比较失败是因为彼此的差距在容错范围外。
<pre><code>$ python math_isclose.py
   a        b     rel_tol  abs(a-b) tolerance  close  
-------- -------- -------- -------- -------- --------
 1000.00   900.00     0.10   100.00   100.00     True
  100.00    90.00     0.10    10.00    10.00     True
   10.00     9.00     0.10     1.00     1.00     True
    1.00     0.90     0.10     0.10     0.10     True
    0.10     0.09     0.10     0.01     0.01    False</pre></code>
要使用一个固定的或“绝对”的公差，用abs_tol代替rel_tol。
<pre><code># math_isclose_abs_tol.py

import math


INPUTS = [
    (1.0, 1.0 + 1e-07, 1e-08),
    (1.0, 1.0 + 1e-08, 1e-08),
    (1.0, 1.0 + 1e-09, 1e-08),
]

print('{:^8} {:^11} {:^8} {:^10} {:^8}'.format(
    'a', 'b', 'abs_tol', 'abs(a-b)', 'close')
)
print('{:-^8} {:-^11} {:-^8} {:-^10} {:-^8}'.format(
    '-', '-', '-', '-', '-'),
)

for a, b, abs_tol in INPUTS:
    close = math.isclose(a, b, abs_tol=abs_tol)
    abs_diff = abs(a - b)
    print('{:8.2f} {:11} {:8} {:0.9f} {!s:>8}'.format(
        a, b, abs_tol, abs_diff, close))</pre></code>
对于绝对公差，输入值之间的差值必须小于给定的公差。
<pre><code>$ python math_isclose_abs_tol.py
   a          b      abs_tol   abs(a-b)   close  
-------- ----------- -------- ---------- --------
    1.00   1.0000001    1e-08 0.000000100    False
    1.00  1.00000001    1e-08 0.000000010     True
    1.00 1.000000001    1e-08 0.000000001     True</pre></code>
nan和inf是特殊情况。
<pre><code># math_isclose_inf.py

import math

print('nan, nan:', math.isclose(math.nan, math.nan))
print('nan, 1.0:', math.isclose(math.nan, 1.0))
print('inf, inf:', math.isclose(math.inf, math.inf))
print('inf, 1.0:', math.isclose(math.inf, 1.0))</pre></code>
nan永远不会接近另一个值，包括它自己。inf只接近它自己。
<pre><code>$ python math_isclose_inf.py
nan, nan: False
nan, 1.0: False
inf, inf: True
inf, 1.0: False</pre></code>
## Converting Floating Point Values to Integers
math模块包含三个函数，用于将浮点值转换为整数。每个人都采取不同的方法，并且在不同的情况下会有用。

最简单的是trunc()，它截断了小数点后面的数字，只留下有效的数字组成了整个数值的一部分。
floor()将其输入转换为最大的前整数，而ceil()(天花板)在输入值之后按顺序产生最大的整数。
<pre><code># math_integers.py

import math

HEADINGS = ('i', 'int', 'trunk', 'floor', 'ceil')
print('{:^5} {:^5} {:^5} {:^5} {:^5}'.format(*HEADINGS))
print('{:-^5} {:-^5} {:-^5} {:-^5} {:-^5}'.format(
    '', '', '', '', '',
))

fmt = '{:5.1f} {:5.1f} {:5.1f} {:5.1f} {:5.1f}'

TEST_VALUES = [
    -1.5,
    -0.8,
    -0.5,
    -0.2,
    0,
    0.2,
    0.5,
    0.8,
    1,
]

for i in TEST_VALUES:
    print(fmt.format(
        i,
        int(i),
        math.trunc(i),
        math.floor(i),
        math.ceil(i),
    ))</pre></code>
trunc()相当于直接转换为int。
<pre><code>$ python math_integers.py
  i    int  trunk floor ceil 
----- ----- ----- ----- -----
 -1.5  -1.0  -1.0  -2.0  -1.0
 -0.8   0.0   0.0  -1.0   0.0
 -0.5   0.0   0.0  -1.0   0.0
 -0.2   0.0   0.0  -1.0   0.0
  0.0   0.0   0.0   0.0   0.0
  0.2   0.0   0.0   0.0   1.0
  0.5   0.0   0.0   0.0   1.0
  0.8   0.0   0.0   0.0   1.0
  1.0   1.0   1.0   1.0   1.0</pre></code>
## Alternate Representations of Floating Point Values
modf()取一个浮点数，返回包含输入值的分数和整数部分的元组。
<pre><code># math_modf.py

import math

for i in range(6):
    print(' {}/2 = {}'.format(i, math.modf(i / 2.0)))</pre></code>
返回的值都是浮点数。
<pre><code>$ python math_modf.py
 0/2 = (0.0, 0.0)
 1/2 = (0.5, 0.0)
 2/2 = (0.0, 1.0)
 3/2 = (0.5, 1.0)
 4/2 = (0.0, 2.0)
 5/2 = (0.5, 2.0)</pre></code>
frexp()返回一个浮点数的尾数和指数，可以用来创建一个更便于携带的值表示。
<pre><code># math_frexp.py

import math

print('{:^7} {:^7} {:^7}'.format('x', 'm', 'e'))
print('{:-^7} {:-^7} {:-^7}'.format('', '', ''))

for x in [0.1, 0.5, 4.0]:
    m, e = math.frexp(x)
    print('{:7.2f} {:7.2f} {:7d}'.format(x, m, e))</pre></code>
frexp公式()使用x = m * 2 * * e,并返回值m和e。
<pre><code>$ python math_frexp.py
   x       m       e   
------- ------- -------
   0.10    0.80      -3
   0.50    0.50       0
   4.00    0.50       3</pre></code>
ldexp()是frexp()的倒数。
<pre><code># math_ldexp.py

import math

print('{:^7} {:^7} {:^7}'.format('m', 'e', 'x'))
print('{:-^7} {:-^7} {:-^7}'.format('', '', ''))

INPUTS = [
    (0.8, -3),
    (0.5, 0),
    (0.5, 3),
]

for m, e in INPUTS:
    x = math.ldexp(m, e)
    print('{:7.2f} {:7d} {:7.2f}'.format(m, e, x))</pre></code>
使用与frexp()相同的公式，ldexp()将尾数和指数值作为参数，并返回一个浮点数。
<pre><code>$ python math_ldexp.py
   m       e       x   
------- ------- -------
   0.80      -3    0.10
   0.50       0    0.50
   0.50       3    4.00</pre></code>
## Positive and Negative Signs
数字的绝对值是没有符号的值。使用fabs()计算浮点数的绝对值。
<pre><code># math_fabs.py

import math

print(math.fabs(-1.1))
print(math.fabs(-0.0))
print(math.fabs(0.0))
print(math.fabs(1.1))</pre></code>
在实际中，浮点数的绝对值被表示为正值。
<pre><code>$ python math_fabs.py
1.1
0.0
0.0
1.1</pre></code>
要确定一个值的符号，可以给一组值相同的符号，或者比较两个值，使用copysign()来设置已知的好值的符号。
<pre><code># math_copysign.py

import math

HEADINGS = ('f', 's', '< 0', '> 0', '= 0')
print('{:^5} {:^5} {:^5} {:^5} {:^5}'.format(*HEADINGS))
print('{:-^5} {:-^5} {:-^5} {:-^5} {:-^5}'.format(
    '', '', '', '', '',
))

VALUES = [
    -1.0,
    0.0,
    1.0,
    float('-inf'),
    float('inf'),
    float('-nan'),
    float('nan'),
]

for f in VALUES:
    s = int(math.copysign(1, f))
    print('{:5.1f} {:5d} {!s:5} {!s:5} {!s:5}'.format(
        f, s, f < 0, f > 0, f == 0,
    ))</pre></code>
需要一个额外的函数，例如copysign()，因为将nan和-nan直接与其他值进行比较不会起作用。
<pre><code>$ python math_copysign.py
  f     s    < 0   > 0   = 0 
----- ----- ----- ----- -----
 -1.0    -1 True  False False
  0.0     1 False False True 
  1.0     1 False True  False
 -inf    -1 True  False False
  inf     1 False True  False
  nan    -1 False False False
  nan     1 False False False</pre></code>
## Commonly Used Calculations
表示二进制浮点内存中的精确值具有挑战性。有些值不能精确地表示，而且一个值越经常通过重复计算来操作，就越有可能引入表示错误。
math包含一个函数，用于计算一系列浮点数的和，使用一种有效的算法来最小化这些错误。
<pre><code># math_fsum.py

import math

values = [0.1] * 10

print('Input values:', values)

print('sum()       : {:.20f}'.format(sum(values)))

s = 0.0
for i in values:
    s += i
print('for-loop    : {:.20f}'.format(s))
print('math.fsum() : {:.20f}'.format(math.fsum(values)))</pre></code>
给定一个10个值的序列，每个值都等于0.1，序列和的期望值是1.0。
由于0.1不能精确地表示为浮点值，除非用fsum()计算，否则求和计算将会引入错误。
<pre><code>$ python math_fsum.py
Input values: [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
sum()       : 0.99999999999999988898
for-loop    : 0.99999999999999988898
math.fsum() : 1.00000000000000000000</pre></code>
factorial()通常用于计算一系列对象的排列组合数。一个正整数n的阶乘，表示n!，递归地定义为(n-1)!* n，使用0!= = 1停止递归。
<pre><code># math_factorial.py

import math

for i in [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.1]:
    try:
        print('{:2.0f} {:6.0f}'.format(i, math.factorial(i)))
    except ValueError as err:
        print('Error computing factorial({}): {}'.format(i, err))</pre></code>
factorial()只对整数起作用，但只要它们可以转换为整数而不失去值，就可以接受浮点参数。
<pre><code>$ python math_factorial.py
 0      1
 1      1
 2      2
 3      6
 4     24
 5    120
Error computing factorial(6.1): factorial() only accepts integral values</pre></code>
gamma()就像factorial()，但它可以接受正实数。
<pre><code># math_gamma.py

import math

for i in [0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6]:
    try:
        print('{:2.1f} {:6.2f}'.format(i, math.gamma(i)))
    except ValueError as err:
        print('Error computing gamma({}): {}'.format(i, err))</pre></code>
由于零导致开始值为负，因此不允许。
<pre><code>$ python math_gamma.py
1.1   0.95
2.2   1.10
3.3   2.68
4.4  10.14
5.5  52.34
6.6 344.70</pre></code>
lgamma()返回输入值的gmma绝对值的自然对数。
<pre><code># math_lgamma.py

import math

for i in [0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6]:
    try:
        print('{:2.1f} {:.20f} {:.20f}'.format(i, math.lgamma(i), math.log(math.gamma(i))))
    except ValueError as err:
        print('Error computing lgamma({}): {}'.format(i, err))</pre></code>
使用lgamma()比使用gamma()的结果单独计算对数要更精确。
<pre><code>$ python math_lgamma.py
Error computing lgamma(0): math domain error
1.1 -0.04987244125984036103 -0.04987244125983997245
2.2 0.09694746679063825923 0.09694746679063866168
3.3 0.98709857789473387513 0.98709857789473409717
4.4 2.31610349142485727469 2.31610349142485727469
5.5 3.95781396761871651080 3.95781396761871606671
6.6 5.84268005527463252236 5.84268005527463252236</pre></code>
模运算符(%)计算除法表达式的其余部分(例如:5 % 2 = 1).内置的运算符与整数很好地工作，但是，与其他许多浮点运算一样，中间计算导致了数据丢失的代表性问题。
fmod()为浮点值提供了更精确的实现。
<pre><code># math_fmod.py

import math


print('{:^4} {:^4} {:^5} {:^5}'.format(
    'x', 'y', '%', 'fmod'))
print('{:-^4} {:-^4} {:-^5} {:-^5}'.format(
    '-', '-', '-', '-'))

INPUTS = [
    (5, 2),
    (5, -2),
    (-5, 2),
]

for x, y in INPUTS:
    print('{:4.1f} {:4.1f} {:5.2f} {:5.2f}'.format(
        x,
        y,
        x % y,
        math.fmod(x, y),
    ))</pre></code>
一个更常见的混淆来源是fmod()用于计算模块的算法与%的不同，因此结果的符号是不同的。
<pre><code>$ python math_fmod.py
 x    y     %   fmod 
---- ---- ----- -----
 5.0  2.0  1.00  1.00
 5.0 -2.0 -1.00  1.00
-5.0  2.0  1.00 -1.00</pre></code>
使用gcd()找到最大的整数，可以将其平均分为两个整数，最大公约数。
<pre><code># math_gcd.py

import math

print(math.gcd(10, 8))
print(math.gcd(10, 0))
print(math.gcd(50, 225))
print(math.gcd(11, 9))
print(math.gcd(0, 0))</pre></code>
如果两个值都为0，则结果为0。
<pre><code>$ python math_gcd.py
2
10
25
1
0</pre></code>

