# OrderedDict -- Remember the Order Keys are Added to a Dictionary
OrderedDict是dictionary的子类，它记住元素被添加的顺序。
<pre><code># collections_ordereddict_iter.py

import collections

print('Regular dictionary:')
d = dict()
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)

print('\nOrderedDict:')
d = collections.OrderedDict()
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)</pre></code>
Python3.6的dictionary是有序的，但不能依赖。
<pre><code>$ python collections_ordereddict_iter.py
Regular dictionary:
a A
b B
c C

OrderedDict:
a A
b B
c C</pre></code>
## Equality
在测试是否相等时，常规的dictionary只查看它的内容。OrderedDict还考虑添加条目的顺序。
<pre><code># collections_ordereddict_equality

import collections

print('dict:', end='')
d1 = dict()
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = dict()
d2['b'] = 'B'
d2['a'] = 'A'
d2['c'] = 'C'
print(d1 == d2)

print('OrderedDict:', end='')
d1 = collections.OrderedDict()
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = collections.OrderedDict()
d2['b'] = 'B'
d2['a'] = 'A'
d2['c'] = 'C'
print(d1 == d2)</pre></code>
OrderedDict由于元素添加的顺序不同，故两者不相等。
<pre><code>$ python collections_ordereddict_equality.py
dict:True
OrderedDict:False</pre></code>
## Reordering
通过使用move_to_end()可以更改OrderedDict中的键的顺序。
<pre><code># collections_ordereddict_move_to_end.py

import collections

d = collections.OrderedDict([('a', 'A'), ('b', 'B'), ('c', 'C')])
print('Before:')
for k, v in d.items():
    print(k, v)

d.move_to_end('b')

print('\nmove_to_end():')
for k, v in d.items():
    print(k, v)

d.move_to_end('b', last=False)  # last默认为True,最末尾的不会移动到头部

print('\nmove_to_end(last=False):')
for k, v in d.items():
    print(k, v)</pre></code>
<pre><code>$ python collections_ordereddict_move_to_end.py
Before:
a A
b B
c C

move_to_end():
a A
c C
b B

move_to_end(last=False):
b B
a A
c C</pre></code>