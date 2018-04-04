# ChainMap -- Search Multiple Dictionaries
ChainMap类管理一个字典序列，并按照它们给出的顺序对它们进行搜索，以找到与键关联的值。
ChainMap是一个很好的“上下文”容器，因为它可以被当作栈来处理，对于随着堆栈的增长而发生的改变，而随着堆栈的收缩，这些改变又被丢弃。
## Accessing Values
ChainMap有着和常规字典访问存在的值相同的API
<pre><code># collections_chainmap_read.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(d1, d2)   # d1, d2换位下面的'c'值就是'D'
print(m)
print('a={}'.format(m['a']))
print('b={}'.format(m['b']))
print('c={}'.format(m['c']))
print('Keys={}'.format(list(m.keys())))
print('Values={}'.format(list(m.values())))
print('Items:')
for k, v in m.items():
    print('{}={}'.format(k, v))
print('"d" in m: {}'.format('d' in m))</code></pre>
子映射按照传递给构造函数的顺序进行搜索，因此为键'c'的值来自于d1字典。
<pre><code>$ python3 collections_chain_read.py
ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
a=A
b=B
c=C
Keys=['c', 'b', 'a']
Values=['C', 'B', 'A']
Items:
c=C
b=B
a=A
"d" in m: False</code></pre>
## Reordering
ChainMap在其map属性存贮映射列表并按照这个列表来搜索查找。
由于列表是可变的，因此可以通过对这个映射列表添加新映射或更改元素的顺序来控制查更新和查找的行为。
<pre><code># collections_chainmap_reorder.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(d1, d2)
print(m.maps)
print('c={}'.format(m['c']))

# 反向列表
m.maps = list(reversed(m.maps))
print(m.maps)
print('c={}'.format(m['c']))</code></pre>
当映射列表被反向时，'c'的值改变了。
<pre><code>$ python3 collectins_chainmap_reorder.py
[{'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'}]
c=C
[{'b': 'B', 'c': 'D'}, {'a': 'A', 'c': 'C'}]
c=D</code></pre>
# Updating Values
ChainMap不缓存子映射中的值。因此，如果对其内容进行了修改，则会在访问ChainMap时反映修改后的结果。
<pre><code># collections_chainmap_update_behind.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(d1, d2)
print('Before:')
print(m)
print('c={}'.format(m['c']))
d1['c'] = 'C1'
d2['e'] = 'E'
print('After:')
print(m)
print('c={}'.format(m['c']))</code></pre>
对原字典的修改和新增都会实时改变ChainMap
<pre><code>$ python3 collections_chainmap_update_behind.py
Before:
ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
c=C
After:
ChainMap({'a': 'A', 'c': 'C1'}, {'b': 'B', 'c': 'D', 'e': 'E'})
c=C1</pre></code>
也可以直接通过ChainMap进行修改和新增操作，但这些都只会作用在第一个字典上
<pre><code># collections_chainmap_update_directly.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(d1, d2)
print('Before:')
print(m)
m['c'] = 'C1'
m['b'] = 'B1'
m['e'] = 'E'
print('After:')
print(m)
print('d1', d1)
print('d2', d2)</code></pre>
可以看到，对m的修改都只反映在d1上
<pre><code>$ python3 collections_chainmap_update_directly.py
Before:
ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
After:
ChainMap({'a': 'A', 'c': 'C1', 'b': 'B1', 'e': 'E'}, {'b': 'B', 'c': 'D'})
d1 {'a': 'A', 'c': 'C1', 'b': 'B1', 'e': 'E'}
d2 {'b': 'B', 'c': 'D'}</code></pre>
ChainMap提供了一个方法new_child，实例调用后可以创建一个新的实例，该新实例的映射列表会在原来的基础上在头部新增一个空字典，这样就可以避免修改现有的底层数据结构。
<pre><code># collections_chainmap_new_child.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}

m1 = collections.ChainMap(d1, d2)
m2 = m1.new_child()
print('before:')
print('m1 ', m1)
print('m2 ', m2)
m2['c'] = 'C1'
print('after:')
print('m1 ', m1)
print('m2 ', m2)</code></pre>
这种类似堆栈的行为让ChainMap实例很方便的作为模板或应用程序上下文。具体地说，在一次迭代中添加或更新值，然后下一次迭代放弃这些更改。
<pre><code>$ python3 collections_chainmap_new_child.py
before:
m1  ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m2  ChainMap({}, {'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
after:
m1  ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m2  ChainMap({'c': 'C1'}, {'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})</code></pre>
对于已知或预先构建好新上下文的情况，可以通过直接传递映射到new_child()中。
<pre><code># collections_chainmap_new_child_explicit.py

import collections

d1 = {'a': 'A', 'c': 'C'}
d2 = {'b': 'B', 'c': 'D'}
d3 = {'e': 'E'}

m1 = collections.ChainMap(d1, d2)
m2 = m1.new_child(d3)   # 等价下面的
m3 = collections.ChainMap(d3, *m1.maps)
print('before:')
print('m1', m1)
print('m2', m2)
print('m3', m3)
m2['a'] = 'A1'
print('after')
print('m1', m1,)
print('m2', m2,)
print('m3', m3)</pre></code>
<pre><code>$ python3 collections_chainmap_new_child_explicit.py
before:
m1 ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m2 ChainMap({'e': 'E'}, {'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m3 ChainMap({'e': 'E'}, {'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
after
m1 ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m2 ChainMap({'e': 'E', 'a': 'A1'}, {'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m3 ChainMap({'e': 'E', 'a': 'A1'}, {'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})</pre></code>
可以发现对m2修改，m3也变化，我的理解是m2和m3都只是对映射列表的引用。大家可以把上面的代码复制到
[http://www.pythontutor.com/](http://www.pythontutor.com/)网站，看执行的情况。如下图所示


