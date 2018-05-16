# statistics -- Statistical Calculations
> 目的：常见统计计算的实现。

统计模块使用Python的各种数值类型(整数、浮点数、小数和小数)实现了许多常用的统计公式。
## Averages
有三种形式的平均支持，平均，中位数和模式。用mean()计算算术平均数。
<pre><code># statistics_mean.py

from statistics import *

data = [1, 2, 2, 5, 10, 12]

print('{:0.2f}'.format(mean(data)))</pre></code>
整数和浮点数的返回值始终是一个浮点数。对于Decimal和分数输入数据，结果与输入的类型相同。
<pre><code>$ python statistics_mean.py
5.33</pre></code>
使用mode()在数据集中计算最常用的数据点。
<pre><code># statistics_mode.py

from statistics import *

data = [1, 2, 2, 5, 10, 12]
print(mode(data))</pre></code>
返回值始终是输入数据集的成员，因为mode()将输入视为一组离散值，并计数递归，输入实际上不需要是数值。
<pre><code>$ python statistics_mode.py
2</pre></code>
计算中值有四种不同形式，前三种类似如下
<pre><code># statistics_median.py

from statistics import *

data = [1, 2, 2, 5, 10, 12]
data1 = [1, 2, 2, 8, 5, 10, 12]
print(data)
print('median   : {:0.2f}'.format(median(data)))
print('low      : {:0.2f}'.format(median_low(data)))
print('high     : {:0.2f}'.format(median_high(data)))
print(data1)
print('median   : {:0.2f}'.format(median(data1)))
print('low      : {:0.2f}'.format(median_low(data1)))
print('high     : {:0.2f}'.format(median_high(data1)))</pre></code>
包含偶数个元素的三种中值计算形式可能是不同的结果
<pre><code>$ python statistics_median.py
[1, 2, 2, 5, 10, 12]
median   : 3.50
low      : 2.00
high     : 5.00
[1, 2, 2, 8, 5, 10, 12]
median   : 5.00
low      : 5.00
high     : 5.00</pre></code>
第四种的中值计算,使用median_grouped(),将输入连续的数据,计算出50%百分位值首先发现使用提供的区间中值范围宽,然后插值,范围内使用的位置实际值(s)的数据集,这个范围。
<pre><code># statistics_median_grouped.py

from statistics import *

data = [10, 20, 30, 40]

print('1: {:0.2f}'.format(median_grouped(data, interval=1)))
print('2: {:0.2f}'.format(median_grouped(data, interval=2)))
print('3: {:0.2f}'.format(median_grouped(data, interval=3)))</pre></code>
随着区间宽度的增加，相同数据集的计算值会发生变化。
<pre><code>$ python statistics_median_grouped.py
1: 29.50
2: 29.00
3: 28.50</pre></code>

