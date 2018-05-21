# heapq -- Heap Sort Algorithm
> 目的：heapq实现了一种适用于Python列表的min-heap排序算法。

堆是树状的数据结构，其中子节点与父节点有一个排序关系。
二进制堆可以使用一个列表或数组来表示，这样元素N的子元素就处于2 * N + 1和2 * N + 2的位置(对于从零开始的索引)。这种布局使得重新排列堆的位置成为可能，所以在添加或删除项目时不必重新分配内存。

max-heap确保父节点大于或等于它的两个子节点。min-heap要求父节点小于或等于其子节点。Python的heapq模块实现了一个min-heap。
## Example Data
这章的例子使用的数据来自heapq_heapdata.py
<pre><code># heapq_heapdata

data = [19, 9, 4, 10, 11]</pre></code>
堆的打印输出使用heapq_showtree.py
<pre><code># # heapq_showtree.py

import math
from io import StringIO


def show_tree(tree, total_width=36, fill=' '):
    """Pretty-print a tree."""
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i + 1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write('\n')
        columns = 2 ** row
        col_width = int(math.floor(total_width / columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print(output.getvalue())
    print('-' * total_width)
    print()</pre></code>
## Creating a Heap
创建一个堆有两种基本方式，使用heappush()和heapify()方法。
<pre><code># heapq_heapush.py

import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data

heap = []
print('random :', data)
print()

for n in data:
    print('add {:>3}:'.format(n))
    heapq.heappush(heap, n)
    show_tree(heap)</pre></code>
当使用heappush()时，当从数据源中添加新项时，将维护元素的堆排序顺序。
<pre><code>$ python heapq_heapush.py
random : [19, 9, 4, 10, 11]

add  19:

                 19                 
------------------------------------

add   9:

                 9                  
        19        
------------------------------------

add   4:

                 4                  
        19                9         
------------------------------------

add  10:

                 4                  
        10                9         
    19   
------------------------------------

add  11:

                 4                  
        10                9         
    19       11   
------------------------------------</pre></code>
如果数据已经在内存中，那么使用heapify()来重新排列列表中的项就更有效了。
<pre><code># heapq_heapify.py

import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data


print('random    :', data)
heapq.heapify(data)
print('heapified :')
show_tree(data)</pre></code>
在一次堆订单中构建一个列表的结果与构建无序列表并调用heapify()的结果相同。
<pre><code>$ python heapq_heapify.py
random    : [19, 9, 4, 10, 11]
heapified :

                 4                  
        9                 19        
    10       11   
------------------------------------</pre></code>
## Accessing the Contents of a Heap
一旦正确地组织了堆，使用heappop()来删除具有最低值的元素。
<pre><code># heapq_heappop.py


import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data


print('random   :', data)
heapq.heapify(data)
print('heapified :')
show_tree(data)
print()

for i in range(2):
    smallest = heapq.heappop(data)
    print('pop    {:>3}:'.format(smallest))
    show_tree(data)</pre></code>
在这个例子中，根据stdlib文档，heapify()和heappop()被用来排序一个数字列表。
<pre><code>$ python heapq_heappop.py
random   : [19, 9, 4, 10, 11]
heapified :

                 4                  
        9                 19        
    10       11   
------------------------------------


pop      4:

                 9                  
        10                19        
    11   
------------------------------------

pop      9:

                 10                 
        11                19        
------------------------------------</pre></code>
要删除现有的元素并在单个操作中替换为新的值，请使用heapreplace()。
<pre><code># heapq_heapreplace.py


import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data

heapq.heapify(data)
print('start:')
show_tree(data)

for n in [0, 13]:
    smallest = heapq.heapreplace(data, n)
    print('replace {:>2} with {:>2}:'.format(smallest, n))
    show_tree(data)</pre></code>
替换现有的元素使得维护固定大小的堆成为可能，例如优先排序的任务队列。
<pre><code>$ python heapq_heapreplace.py
start:

                 4                  
        9                 19        
    10       11   
------------------------------------

replace  4 with  0:

                 0                  
        9                 19        
    10       11   
------------------------------------

replace  0 with 13:

                 9                  
        10                19        
    13       11   
------------------------------------</pre></code>
## Data Extremes from a Heap
heapq还包含两个函数来检查一个可迭代对象，并找到它所包含的最大或最小值的范围。
<pre><code># heapq_extremes.py

import heapq
from heapq_heapdata import data


print('all       :', data)
print('3 largest :', heapq.nlargest(3, data))
print('from sort :', list(reversed(sorted(data)[-3:])))
print('3 smallest:', heapq.nsmallest(3, data))
print('from sort :', sorted(data)[:3])</pre></code>
对于n > 1的相对较小的值使用nlargest()和nsmallest()是有效的，但是在一些情况下仍然可以派上用场。
<pre><code>$ python heapq_extremes.py
all       : [19, 9, 4, 10, 11]
3 largest : [19, 11, 10]
from sort : [19, 11, 10]
3 smallest: [4, 9, 10]
from sort : [4, 9, 10]</pre></code>
## Efficiently Merging Sorted Sequences
将几个排序序列合并成一个新序列对于小数据集来说是很容易的。
> list(sorted(itertools.chain(*data)))

对于较大的数据集，该技术可以使用相当大的内存。
merge()不是对整个组合序列进行排序，而是使用堆来一次生成一个新的序列，用固定的内存来确定下一个项目。
<pre><code># heapq_merge.py

import heapq
import random


random.seed(2016)

data = []
for i in range(4):
    new_data = list(random.sample(range(1, 101), 5))
    new_data.sort()
    data.append(new_data)

for i, d in enumerate(data):
    print('{}: {}'.format(i, d))

print('\nMerged:')
for i in heapq.merge(*data):
    print(i, end=' ')
print()</pre></code>
因为merge()的实现使用了堆，所以它根据被合并的序列的数量来消耗内存，而不是这些序列中项目的数量。
<pre><code>$ python heapq_merge.py
0: [33, 58, 71, 88, 95]
1: [10, 11, 17, 38, 91]
2: [13, 18, 39, 61, 63]
3: [20, 27, 31, 42, 45]

Merged:
10 11 13 17 18 20 27 31 33 38 39 42 45 58 61 63 71 88 91 95 </pre></code>
