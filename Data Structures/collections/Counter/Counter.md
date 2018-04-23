# Counter -- Count Hashable Objects
Counter是一个容器，它可以跟踪添相同的值出现的次数。它可以用于实现其他语言通常使用包或多集数据结构的相同算法。
## Initializing
Counter支持三种形式的初始化。可以传递元素的序列，一个包含键和计数的字典，或者使用键到计数的映射的关键字参数。
<pre><code># collections_counter_init

import collections

print(collections.Counter(['a', 'b', 'c', 'a', 'b', 'b']))
print(collections.Counter({'a': 2, 'b': 3, 'c': 1}))
print(collections.Counter(a=2, b=3, c=1))</pre></code>
3种初始化的方式结果一样
<pre><code>$ python collections_counter_init.py
Counter({'b': 3, 'a': 2, 'c': 1})
Counter({'b': 3, 'a': 2, 'c': 1})
Counter({'b': 3, 'a': 2, 'c': 1})</pre></code>
可以不传值给构造函数创建一个空Counter, 然后通过update方法填充内容
<pre><code># collections_counter_update.py

import collections

c = collections.Counter()
print('Initial:', c)

c.update('abcdaab')
print('Sequence:', c)

c.update({'a': 1, 'd': 5})
print('Dict:', c)</pre></code>
计数值是在原来的基础上增加，而不是替换
<pre><code>$ python collections_counter_update.py
Initial: Counter()
Sequence: Counter({'a': 3, 'b': 2, 'c': 1, 'd': 1})
Dict: Counter({'d': 6, 'a': 4, 'b': 2, 'c': 1})</pre></code>
## Accessing Counts
一旦Counter是有填充值的，这些值可以通过字典api形式检索
<pre><code># collections_counter_get_values.py

import collections

c = collections.Counter('abcdaab')
for letter in 'abcde':
    print('{}: {}'.format(letter, c[letter]))</pre></code>
对于没有的项，Counter不会触发KeyError, 而是把它的计数作为0
<pre><code>python collections_counter_get_values.py
a: 3
b: 2
c: 1
d: 1
e: 0</pre></code>
elements()方法返回一个迭代器，该迭代器生成计数器已知的所有项。
<pre><code># collections_counter_elements.py

import collections

c = collections.Counter('extremely')
c['z'] = 0
print(c)
print(list(c.elements()))</pre></code>
生成元素的顺序是没有保证的，计数值不大于0的元素也不包含在内
<pre><code>$ python collections_counter_elements.py
Counter({'e': 3, 'x': 1, 't': 1, 'r': 1, 'm': 1, 'l': 1, 'y': 1, 'z': 0})
['e', 'e', 'e', 'x', 't', 'r', 'm', 'l', 'y']</pre></code>
most_common()方法得到计数值最大的前n项
<pre><code># collections_counter_most_common.py

import collections

c = collections.Counter('ABCDGRIOGGHAJHNVUSBHAGYCDRSAA')
print(c.most_common(3))</pre></code>
<pre><code>python collections_counter_most_common.py
[('A', 5), ('G', 4), ('H', 3)]</pre></code>
## Arithmetic
Counter实例支持算术，并为聚合结果设置操作。这个示例显示了创建新的计数器实例的标准操作符，=、-=、&=和|=也得到了支持。
<pre><code># collections_counter_arithmetic.py

import collections

c1 = collections.Counter(['a', 'b', 'c', 'a', 'b', 'b'])
c2 = collections.Counter('alphabet')

print('C1:', c1)
print('C2:', c2)

print('\nCombined counts:')
print(c1 + c2)

print('\nSubtraction:')
print(c1 - c2)

print('\nIntersection (taking positive minimums):')
print(c1 & c2)

print('\nUnion (taking maximums):')
print(c1 | c2)</pre></code>
相关的操作都会产生一个新的Counter
<pre><code>$ python collections_counter_arithmetic.py
C1: Counter({'b': 3, 'a': 2, 'c': 1})
C2: Counter({'a': 2, 'l': 1, 'p': 1, 'h': 1, 'b': 1, 'e': 1, 't': 1})

Combined counts:
Counter({'a': 4, 'b': 4, 'c': 1, 'l': 1, 'p': 1, 'h': 1, 'e': 1, 't': 1})

Subtraction:
Counter({'b': 2, 'c': 1})

Intersection (taking positive minimums):
Counter({'a': 2, 'b': 1})

Union (taking maximums):
Counter({'b': 3, 'a': 2, 'c': 1, 'l': 1, 'p': 1, 'h': 1, 'e': 1, 't': 1})</pre></code>

