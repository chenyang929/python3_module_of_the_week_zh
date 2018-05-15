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
## Exponents and Logarithms
指数增长曲线出现在经济学、物理学和其他科学领域。
Python有一个内置的指数运算符(“**”)，但是当需要一个可调用函数作为另一个函数的参数时，pow()可能会有用。
<pre><code># math_pow.py

import math

INPUTS = [
    # Typical uses
    (2, 3),
    (2.1, 3.2),

    # Always 1
    (1.0, 5),
    (2.0, 0),

    # Not-a-number
    (2, float('nan')),

    # Roots
    (9.0, 0.5),
    (27.0, 1.0 / 3),
]

for x, y in INPUTS:
    print('{:5.1f} ** {:5.3f} = {:6.3f}'.format(
        x, y, math.pow(x, y)))</pre></code>
大多数非数字值的操作都是nan返回nan。如果指数小于1,pow()计算一个根。
<pre><code>$ python math_pow.py
  2.0 ** 3.000 =  8.000
  2.1 ** 3.200 = 10.742
  1.0 ** 5.000 =  1.000
  2.0 ** 0.000 =  1.000
  2.0 **   nan =    nan
  9.0 ** 0.500 =  3.000
 27.0 ** 0.333 =  3.000</pre></code>
由于方根(1/2的指数)被频繁地使用，因此有一个单独的计算它们的函数。
<pre><code># math_sqrt.py

import math

print(math.sqrt(9.0))
print(math.sqrt(3))
try:
    print(math.sqrt(-1))
except ValueError as err:
    print('Cannot compute sqrt(-1):', err)</pre></code>
计算负数的平方根需要复数，而不是由math模块来处理。任何试图计算负数的平方根的尝试都会产生一个ValueError。
<pre><code>$ python math_sqrt.py
3.0
1.7320508075688772
Cannot compute sqrt(-1): math domain error</pre></code>
在默认情况下，log()计算自然对数(底为e)，如果提供第二个参数，则将该值用作基础。
<pre><code># math_log.py

import math

print(math.log(8))
print(math.log(8, 2))
print(math.log(0.5, 2))</pre></code>
小于1的对数结果是负数。
<pre><code>$ python math_log.py
2.0794415416798357
3.0
-1.0</pre></code>
log()有三种变体。给定浮点表示法和舍入误差，log(x, b)所产生的计算值的精度有限，特别是在某些基础上。log10()计算log(x, 10)，使用比log()更精确的算法。
<pre><code># math_log10.py

import math

print('{:2} {:^12} {:^10} {:^20} {:8}'.format(
    'i', 'x', 'accurate', 'inaccurate', 'mismatch',
))
print('{:-^2} {:-^12} {:-^10} {:-^20} {:-^8}'.format(
    '', '', '', '', '',
))

for i in range(0, 10):
    x = math.pow(10, i)
    accurate = math.log10(x)
    inaccurate = math.log(x, 10)
    match = '' if int(inaccurate) == i else '*'
    print('{:2d} {:12.1f} {:10.8f} {:20.18f} {:^5}'.format(
        i, x, accurate, inaccurate, match,
    ))</pre></code>
输出末尾的行*突出了不准确的值。
<pre><code>$ python math_log10.py
i       x        accurate       inaccurate      mismatch
-- ------------ ---------- -------------------- --------
 0          1.0 0.00000000 0.000000000000000000      
 1         10.0 1.00000000 1.000000000000000000      
 2        100.0 2.00000000 2.000000000000000000      
 3       1000.0 3.00000000 2.999999999999999556   *  
 4      10000.0 4.00000000 4.000000000000000000      
 5     100000.0 5.00000000 5.000000000000000000      
 6    1000000.0 6.00000000 5.999999999999999112   *  
 7   10000000.0 7.00000000 7.000000000000000000      
 8  100000000.0 8.00000000 8.000000000000000000      
 9 1000000000.0 9.00000000 8.999999999999998224   * </pre></code>
类似于log10()， log2()计算等价于math.log(x,2)。
<pre><code># math_log2.py

import math

print('{:>2} {:^5} {:^5}'.format(
    'i', 'x', 'log2',
))
print('{:-^2} {:-^5} {:-^5}'.format(
    '', '', '',
))

for i in range(0, 10):
    x = math.pow(2, i)
    result = math.log2(x)
    print('{:2d} {:5.1f} {:5.1f}'.format(
        i, x, result,
    ))</pre></code>
根据底层平台的不同，使用内置的和特殊目的的函数可以提供更好的性能和准确性，使用的是在更通用的功能中没有找到的基础2的专用算法。
<pre><code>$ python math_log2.py
 i   x   log2 
-- ----- -----
 0   1.0   0.0
 1   2.0   1.0
 2   4.0   2.0
 3   8.0   3.0
 4  16.0   4.0
 5  32.0   5.0
 6  64.0   6.0
 7 128.0   7.0
 8 256.0   8.0
 9 512.0   9.0</pre></code>
log1p()计算Newton-Mercator系列(1+x的自然对数)。
<pre><code># math_log1p.py

import math

x = 0.0000000000000000000000001
print('x       :', x)
print('1 + x   :', 1 + x)
print('log(1+x):', math.log(1 + x))
print('log1p(x):', math.log1p(x))</pre></code>
log1p()对于x非常接近于零的值更精确，因为它使用一种算法来补偿初始添加的舍入错误。
<pre><code>$ python math_log1p.py
x       : 1e-25
1 + x   : 1.0
log(1+x): 0.0
log1p(x): 1e-25</pre></code>
exp()计算指数函数(e**x)。
<pre><code># math_exp.py

import math

x = 2

fmt = '{:.20f}'
print(fmt.format(math.e ** 2))
print(fmt.format(math.pow(math.e, 2)))
print(fmt.format(math.exp(2)))</pre></code>
与其他特殊情况函数一样，它使用一种算法来产生比通用等效的math.pow(math.e, x)更精确的结果。
<pre><code>$ python math_exp.py
7.38905609893064951876
7.38905609893064951876
7.38905609893065040694</pre></code>
expm1()是log1p()的倒数，并计算e**x - 1。
<pre><code># math_expm1.py

import math

x = 0.0000000000000000000000001

print(x)
print(math.exp(x) - 1)
print(math.expm1(x))</pre></code>
当单独执行减法时，小的x值会失去精度，比如log1p()。
<pre><code>$ python math_expm1.py
1e-25
0.0
1e-25</pre></code>
## Angles
虽然角度在日常讨论中更常用，但弧度是科学和数学中角测量的标准单位。弧度是由两条线在圆的中心相交形成的角度，它们的两端在圆的圆周上，间距为一个半径。

周长计算为2πr，因此弧度与π之间存在一种关系，这一数值在三角计算中经常出现。这种关系导致了在三角学和微积分中使用的弧度，因为它们会产生更紧凑的公式。

角度要转换成弧度，使用radians()函数。
<pre><code># math_radians.py

import math

print('{:^7} {:^7} {:^7}'.format(
    'Degrees', 'Radians', 'Expected'))
print('{:-^7} {:-^7} {:-^7}'.format(
    '', '', ''))

INPUTS = [
    (0, 0),
    (30, math.pi / 6),
    (45, math.pi / 4),
    (60, math.pi / 3),
    (90, math.pi / 2),
    (180, math.pi),
    (270, 3 / 2.0 * math.pi),
    (360, 2 * math.pi),
]

for deg, expected in INPUTS:
    print('{:7d} {:7.2f} {:7.2f}'.format(
        deg,
        math.radians(deg),
        expected,
    ))</pre></code>
转换公式为rad = deg * π / 180。
<pre><code>$ python math_radians.py
Degrees Radians Expected
------- ------- -------
      0    0.00    0.00
     30    0.52    0.52
     45    0.79    0.79
     60    1.05    1.05
     90    1.57    1.57
    180    3.14    3.14
    270    4.71    4.71
    360    6.28    6.28</pre></code>
要从弧度转换成角度，请使用degrees()。
<pre><code># math_degrees.py

import math

INPUTS = [
    (0, 0),
    (math.pi / 6, 30),
    (math.pi / 4, 45),
    (math.pi / 3, 60),
    (math.pi / 2, 90),
    (math.pi, 180),
    (3 * math.pi / 2, 270),
    (2 * math.pi, 360),
]

print('{:^8} {:^8} {:^8}'.format(
    'Radians', 'Degrees', 'Expected'))
print('{:-^8} {:-^8} {:-^8}'.format('', '', ''))
for rad, expected in INPUTS:
    print('{:8.2f} {:8.2f} {:8.2f}'.format(
        rad,
        math.degrees(rad),
        expected,
    ))</pre></code>
公式为deg = rad * 180 / π 。
<pre><code>$ python math_degrees.py
Radians  Degrees  Expected
-------- -------- --------
    0.00     0.00     0.00
    0.52    30.00    30.00
    0.79    45.00    45.00
    1.05    60.00    60.00
    1.57    90.00    90.00
    3.14   180.00   180.00
    4.71   270.00   270.00
    6.28   360.00   360.00</pre></code>
## Trigonometry
三角函数把三角形中的角与边的长度联系起来。它们出现在具有周期性特性的公式中，如谐波、圆周运动，或在处理角度时。标准库中的所有三角函数都以弧度表示。

在一个直角三角形中，正弦是边的长度与斜边的比(sin a =对边/斜边)。cos是邻边长度与斜边的比值(cos A =邻边/斜边)。tan等于对边与邻边的比值(tan A =对边/邻边)
<pre><code># math_trig.py

import math

print('{:^7} {:^7} {:^7} {:^7} {:^7}'.format(
    'Degrees', 'Radians', 'Sine', 'Cosine', 'Tangent'))
print('{:-^7} {:-^7} {:-^7} {:-^7} {:-^7}'.format(
    '-', '-', '-', '-', '-'))

fmt = '{:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'

for deg in range(0, 361, 30):
    rad = math.radians(deg)
    if deg in (90, 270):
        t = float('inf')
    else:
        t = math.tan(rad)
    print(fmt.format(deg, rad, math.sin(rad), math.cos(rad), t))</pre></code>
<pre><code>$ python math_trig.py
切的比例也可以被定义为角度的正弦余弦,既然cos = 0为π/ 2和3π/ 2弧度,切是无限的。
<pre><code>$ python math_trig.py
Degrees Radians  Sine   Cosine  Tangent
------- ------- ------- ------- -------
   0.00    0.00    0.00    1.00    0.00
  30.00    0.52    0.50    0.87    0.58
  60.00    1.05    0.87    0.50    1.73
  90.00    1.57    1.00    0.00     inf
 120.00    2.09    0.87   -0.50   -1.73
 150.00    2.62    0.50   -0.87   -0.58
 180.00    3.14    0.00   -1.00   -0.00
 210.00    3.67   -0.50   -0.87    0.58
 240.00    4.19   -0.87   -0.50    1.73
 270.00    4.71   -1.00   -0.00     inf
 300.00    5.24   -0.87    0.50   -1.73
 330.00    5.76   -0.50    0.87   -0.58
 360.00    6.28   -0.00    1.00   -0.00</pre></code>
给定一个点(x, y)，在点\[(0,0)，(x, 0)， (x, y)]三角形斜边的长度为(x ** 2 + y ** 2) ** 1/2，可以用hypot()计算。
<pre><code># math_hypot.py

import math

print('{:^7} {:^7} {:^10}'.format('X', 'Y', 'Hypotenuse'))
print('{:-^7} {:-^7} {:-^10}'.format('', '', ''))

POINTS = [
    # simple points
    (1, 1),
    (-1, -1),
    (math.sqrt(2), math.sqrt(2)),
    (3, 4),  # 3-4-5 triangle
    # on the circle
    (math.sqrt(2) / 2, math.sqrt(2) / 2),  # pi/4 rads
    (0.5, math.sqrt(3) / 2),  # pi/3 rads
]

for x, y in POINTS:
    h = math.hypot(x, y)
    print('{:7.2f} {:7.2f} {:7.2f}'.format(x, y, h))</pre></code>
圆上的点总是有斜边等于1。
<pre><code>$ python math_hypot.py
   X       Y    Hypotenuse
------- ------- ----------
   1.00    1.00    1.41
  -1.00   -1.00    1.41
   1.41    1.41    2.00
   3.00    4.00    5.00
   0.71    0.71    1.00
   0.50    0.87    1.00</pre></code>
同样的函数可以用来求两点之间的距离。
<pre><code># math_distance_2_points.py

import math

print('{:^8} {:^8} {:^8} {:^8} {:^8}'.format(
    'X1', 'Y1', 'X2', 'Y2', 'Distance',
))
print('{:-^8} {:-^8} {:-^8} {:-^8} {:-^8}'.format(
    '', '', '', '', '',
))

POINTS = [
    ((5, 5), (6, 6)),
    ((-6, -6), (-5, -5)),
    ((0, 0), (3, 4)),  # 3-4-5 triangle
    ((-1, -1), (2, 3)),  # 3-4-5 triangle
]

for (x1, y1), (x2, y2) in POINTS:
    x = x1 - x2
    y = y1 - y2
    h = math.hypot(x, y)
    print('{:8.2f} {:8.2f} {:8.2f} {:8.2f} {:8.2f}'.format(
        x1, y1, x2, y2, h,
    ))</pre></code>
使用x和y值的差异将一个端点移动到原点，然后将结果传递给hypot()。
<pre><code>$ python math_distance_2_points.py
   X1       Y1       X2       Y2    Distance
-------- -------- -------- -------- --------
    5.00     5.00     6.00     6.00     1.41
   -6.00    -6.00    -5.00    -5.00     1.41
    0.00     0.00     3.00     4.00     5.00
   -1.00    -1.00     2.00     3.00     5.00</pre></code>
数学也定义了反三角函数。
<pre><code># math_inverse_trig.py

import math

for r in [0, 0.5, 1]:
    print('arcsine({:.1f})    = {:5.2f}'.format(r, math.asin(r)))
    print('arccosine({:.1f})  = {:5.2f}'.format(r, math.acos(r)))
    print('arctangent({:.1f}) = {:5.2f}'.format(r, math.atan(r)))
    print()</pre></code>
1.57约等于π/2,或90度角, 正弦值是1的余弦值是0。
<pre><code>$ python math_inverse_trig.py
arcsine(0.0)    =  0.00
arccosine(0.0)  =  1.57
arctangent(0.0) =  0.00

arcsine(0.5)    =  0.52
arccosine(0.5)  =  1.05
arctangent(0.5) =  0.46

arcsine(1.0)    =  1.57
arccosine(1.0)  =  0.00
arctangent(1.0) =  0.79</pre></code>
## Hyperbolic Functions
双曲函数出现在线性微分方程中，在使用电磁场、流体力学、狭义相对论和其他高等物理和数学时使用。
<pre><code># math_hyperbolic.py

import math

print('{:^6} {:^6} {:^6} {:^6}'.format(
    'X', 'sinh', 'cosh', 'tanh',
))
print('{:-^6} {:-^6} {:-^6} {:-^6}'.format('', '', '', ''))

fmt = '{:6.4f} {:6.4f} {:6.4f} {:6.4f}'

for i in range(0, 11, 2):
    x = i / 10.0
    print(fmt.format(
        x,
        math.sinh(x),
        math.cosh(x),
        math.tanh(x),
    ))</pre></code>
而余弦函数和正弦函数是一个圆，双曲余弦和双曲正弦函数是双曲线的一半。
<pre><code>$ python math_hyperbolic.py
  X     sinh   cosh   tanh 
------ ------ ------ ------
0.0000 0.0000 1.0000 0.0000
0.2000 0.2013 1.0201 0.1974
0.4000 0.4108 1.0811 0.3799
0.6000 0.6367 1.1855 0.5370
0.8000 0.8881 1.3374 0.6640
1.0000 1.1752 1.5431 0.7616</pre></code>
反双曲函数acosh()、asinh()和atanh()也可用。
## Special Functions
高斯误差函数用于统计。
<pre><code># math_erf.py

import math

print('{:^5} {:7}'.format('x', 'erf(x)'))
print('{:-^5} {:-^7}'.format('', ''))

for x in [-3, -2, -1, -0.5, -0.25, 0, 0.25, 0.5, 1, 2, 3]:
    print('{:5.2f} {:7.4f}'.format(x, math.erf(x)))</pre></code>
对于误差函数，erf(-x) == -erf(x)。
<pre><code>$ python math_erf.py
  x   erf(x) 
----- -------
-3.00 -1.0000
-2.00 -0.9953
-1.00 -0.8427
-0.50 -0.5205
-0.25 -0.2763
 0.00  0.0000
 0.25  0.2763
 0.50  0.5205
 1.00  0.8427
 2.00  0.9953
 3.00  1.0000</pre></code>
互补误差函数为1 - erf(x)。
<pre><code># math_erfc.py

import math

print('{:^5} {:7}'.format('x', 'erfc(x)'))
print('{:-^5} {:-^7}'.format('', ''))

for x in [-3, -2, -1, -0.5, -0.25, 0, 0.25, 0.5, 1, 2, 3]:
    print('{:5.2f} {:7.4f}'.format(x, math.erfc(x)))</pre></code>
erfc()的实现避免了从1中减去x的小值的精度错误。
<pre><code>$ python math_erfc.py
  x   erfc(x)
----- -------
-3.00  2.0000
-2.00  1.9953
-1.00  1.8427
-0.50  1.5205
-0.25  1.2763
 0.00  1.0000
 0.25  0.7237
 0.50  0.4795
 1.00  0.1573
 2.00  0.0047
 3.00  0.0000</pre></code>


