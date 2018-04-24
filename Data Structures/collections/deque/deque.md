# deque -- Double-Ended Queue
一个双端队列，或deque，支持添加和移除队列两端的元素。更常用的栈和队，其的输入和输出被限制在一端上。
<pre><code># collections_deque.py

import collections

d = collections.deque('abcdefg')
print('Deque:', d)
print('Length:', len(d))
print('Left end:', d[0])
print('Right end:', d[-1])

d.remove('c')
print('remove(c):', d)</pre></code>
由于deques是一种类型的序列容器，所以它们支持一些与list相同的操作，比如用__getitem__()检查内容，确定长度，并通过匹配标识从队列中间删除元素。
<pre><code>$ python collections_deque.py
Deque: deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
Length: 7
Left end: a
Right end: g
remove(c): deque(['a', 'b', 'd', 'e', 'f', 'g'])</pre></code>
## Populating
在Python实现中，可以从任何一端填充一个deque，称为“左”和“右”。
<pre><code># collections_deque_populating.py

import collections

# Add to the right
d1 = collections.deque()
d1.extend('abcdefg')
print('extend    :', d1)
d1.append('h')
print('append    :', d1)

# Add to the left
d2 = collections.deque()
d2.extendleft(range(6))
print('extendleft:', d2)
d2.appendleft(6)
print('appendleft:', d2)</pre></code>
extendleft()函数遍历它的输入，并对每个条目执行等效的appendleft()。最终的结果是deque包含了相反顺序的输入序列。
<pre><code>$ python collections_deque_populating.py
extend    : deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
append    : deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
extendleft: deque([5, 4, 3, 2, 1, 0])
appendleft: deque([6, 5, 4, 3, 2, 1, 0])</pre></code>
## Consuming
类似地，deque的元素可以从两端消费，这取决于所应用的算法。
<pre><code># collections_deque_consuming.py

import collections

print('From the right:')
d = collections.deque('abcdefg')
while True:
    try:
        print(d.pop(), end='')
    except IndexError:
        break
print()

print('\nFrom the left:')
d = collections.deque(range(6))
while True:
    try:
        print(d.popleft(), end='')
    except IndexError:
        break
print()</pre></code>
使用pop()从deque“右”端删除返回一个元素，popleft()从“左”端删除返回一个元素。
<pre><code>$ python collections_deque_consuming.py
From the right:
gfedcba

From the left:
012345</pre></code>
由于deque是线程安全的，所以不同线程可以同时消费一个deque
<pre><code># collections_deque_both_ends.py

import collections
import threading
import time

candle = collections.deque(range(5))


def burn(direction, nextSource):
    while True:
        try:
            next = nextSource()
        except IndexError:
            break
        else:
            print('{:>8}: {}'.format(direction, next))
            time.sleep(0.1)
    print('{:>8} done'.format(direction))
    return


left = threading.Thread(target=burn, args=('Left', candle.popleft))
right = threading.Thread(target=burn, args=('Right', candle.pop))
left.start()
right.start()
left.join()
right.join()</pre></code>
这个示例中的线程在两端交替删除项目，直到deque为空。
<pre><code>$ python collections_deque_both_ends.py
    Left: 0
   Right: 4
   Right: 3
    Left: 1
   Right: 2
    Left done
   Right done</pre></code>
## Rotating
deque的另一个有用的方面是可以在任意方向旋转它，从而跳过一些项。
<pre><code># collections_deque_rotate.py

import collections

d = collections.deque(range(10))
print('Normal        :', d)

d = collections.deque(range(10))
d.rotate(2)
print('Right rotation:', d)

d = collections.deque(range(10))
d.rotate(-2)
print('Left rotation :', d)</pre></code>
将deque旋转到右边(使用正旋转)从右端取出物品并将其移动到左端。向左旋转(带一个负值)从左端取物品并将其移动到右端。它可能有助于将deque上的物品形象化，就像刻在表盘边缘一样。
<pre><code>$ python collections_deque_rotate.py
Normal        : deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Right rotation: deque([8, 9, 0, 1, 2, 3, 4, 5, 6, 7])
Left rotation : deque([2, 3, 4, 5, 6, 7, 8, 9, 0, 1])</pre></code>
## Constraining the Queue Size
一个deque实例可以配置一个最大长度，这样它就不会超出这个大小。当队列达到指定长度时，将丢弃现有的项，添加新项。这种行为有助于在未确定长度的流中查找最后的n项。
<pre><code># collections_deque_maxlen.py

import collections
import random

# 设置random seed这样每次执行都是相同结果
random.seed(1) 

d1 = collections.deque(maxlen=3)
d2 = collections.deque(maxlen=3)

for i in range(5):
    n = random.randint(0, 100)
    print('n =', n)
    d1.append(n)
    d2.appendleft(n)
    print('D1:', d1)
    print('D2:', d2)</pre></code>
不管添加了哪些项，都保持了deque长度。
<pre><code>$ python collections_deque_maxlen.py
n = 17
D1: deque([17], maxlen=3)
D2: deque([17], maxlen=3)
n = 72
D1: deque([17, 72], maxlen=3)
D2: deque([72, 17], maxlen=3)
n = 97
D1: deque([17, 72, 97], maxlen=3)
D2: deque([97, 72, 17], maxlen=3)
n = 8
D1: deque([72, 97, 8], maxlen=3)
D2: deque([8, 97, 72], maxlen=3)
n = 32
D1: deque([97, 8, 32], maxlen=3)
D2: deque([32, 8, 97], maxlen=3)</pre></code>
### See also
+ [Deque Recipes](https://docs.python.org/3.6/library/collections.html#deque-recipes) -- Examples of using deques in algorithms from the standard library documentation.