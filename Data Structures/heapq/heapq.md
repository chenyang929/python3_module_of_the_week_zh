# heapq -- Heap Sort Algorithm
> 目的：heapq实现了一种适用于Python列表的min-heap排序算法。

堆是树状的数据结构，其中子节点与父节点有一个排序关系。二进制堆可以使用一个列表或数组来表示，这样元素N的子元素就处于2 * N + 1和2 * N + 2的位置(对于从零开始的索引)。这种布局使得重新排列堆的位置成为可能，所以在添加或删除项目时不必重新分配内存。

max-heap确保父节点大于或等于它的两个子节点。min-heap要求父节点小于或等于其子节点。Python的heapq模块实现了一个min-heap。
## Example Data
这章的例子使用的数据来自heapq_heapdata.py
<pre><code># heapq_heapdata

data = [19, 9, 4, 10, 11]</pre></code>
堆的打印输出使用heapq_showtree.py
<pre><code># heapq_showtree.py

import math
from io import StringIO


def show_tree(tree, total_width=36, fill=''):
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
创建一个堆有两种基本方式，使用heappush()和heapify()方法
