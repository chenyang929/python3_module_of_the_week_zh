# array -- Sequence of Fixed-type Data
> 目的: 有效地管理固定类型数值数据的序列。

数组模块定义了一个序列数据结构，它看起来非常像一个列表，只是所有的成员都必须是相同的原始类型。所支持的类型都是数字或其他固定大小的基本类型，如字节。
请参考下面的表，了解一些支持的类型。数组的标准库文档包括一个完整的类型代码列表。

## Initialization
数组用一个描述要允许的数据类型，以及可能存储在数组中的初始数据序列的参数来实例化。
<pre><code># array_string.py

import array
import binascii

s = b'This is the array'
a = array.array('b', s)

print('As byte string:', s)
print('As array      :', a)
print('As hex        :', binascii.hexlify(a))</pre></code>
在本例中，数组被配置为持有一个字节序列，并使用一个简单的字节字符串初始化。
<pre><code>$ python array_string.py
As byte string: b'This is the array'
As array      : array('b', [84, 104, 105, 115, 32, 105, 115, 32, 116, 104, 101, 32, 97, 114, 114, 97, 121])
As hex        : b'5468697320697320746865206172726179'</pre></code>
## Manipulating Arrays
可以使用与其他Python序列相同的方式扩展和处理一个数组。
<pre><code># array_sequence.py

import array

a = array.array('i', range(3))
print('Initial:', a)

a.extend(range(3))
print('Extended:', a)

print('Slice  :', a[2:5])

print('Iterator:')
print(list(enumerate(a)))</pre></code>
支持的操作包括:切片、迭代和追加元素。
<pre><code>$ python array_sequence.py
Initial: array('i', [0, 1, 2])
Extended: array('i', [0, 1, 2, 0, 1, 2])
Slice  : array('i', [2, 0, 1])
Iterator:
[(0, 0), (1, 1), (2, 2), (3, 0), (4, 1), (5, 2)]</pre></code>
## Arrays and Files
一个数组的内容可以用内置的方法从文件中写入和读取。

tofile()使用tobytes()来格式化数据，fromfile()使用frombytes()将它转换回一个数组实例。
<pre><code># array_tobytes.py

import array
import binascii

a = array.array('i', range(5))
print('A1:', a)

as_bytes = a.tobytes()
print('Bytes:', binascii.hexlify(as_bytes))

a2 = array.array('i')
a2.frombytes(as_bytes)
print('A2:', a2)</pre></code>
tobytes()和frombytes()都使用字节字符串，而不是Unicode字符串。
<pre><code>$ python array_tobytes.py
A1: array('i', [0, 1, 2, 3, 4])
Bytes: b'0000000001000000020000000300000004000000'
A2: array('i', [0, 1, 2, 3, 4])</pre></code>
## Alternative Byte Ordering

