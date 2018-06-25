# pickle -- Object Serialization
> 目的：对象序列化

pickle模块实现了一种将任意Python对象转换成一系列字节的算法。这个过程也称为对象序列化。然后，可以传输或存储表示对象的字节流，然后重新构建以创建具有相同特征的新对象。

警告：pickle的文档表明，它没有提供安全保证。事实上，unpickle数据可以执行任意代码。使用pickle进行进程间通信或数据存储时要小心，不要信任不能被验证为安全的数据。参见hmac模块，了解验证pickle数据源的安全方法示例。

## Encoding and Decoding Data in Strings
第一个示例使用dumps()将数据结构编码为字符串，然后将字符串打印到控制台。它使用完全内置类型组成的数据结构。可以对任何类的实例进行pickle，后面的示例将对此进行说明。
```
# pickle_string.py

import pickle
import pprint

data = [{'a': 'A', 'b': 2, 'c': 3.0}]
print('DATA:', end=' ')
pprint.pprint(data)

data_string = pickle.dumps(data)
print('PICKLE: {!r}'.format(data_string))
```
默认情况下，当在Python 3程序之间共享时，pickle将以最兼容的二进制格式编写。
```
$ python pickle_string.py

DATA: [{'a': 'A', 'b': 2, 'c': 3.0}]
PICKLE: b'\x80\x03]q\x00}q\x01(X\x01\x00\x00\x00aq\x02X\x01\x00\x00\x00Aq\x03X\x01\x00\x00\x00bq\x04K\x02X\x01\x00\x00\x00cq\x05G@\x08\x00\x00\x00\x00\x00\x00ua.'
```
数据序列化后，可以将其写入文件、套接字、管道等。之后可以从文件中读取并对数据进行unpickle，以构造具有相同值的新对象。
```
# pickle_unpickle.py

import pickle
import pprint

data1 = [{'a': 'A', 'b': 2, 'c': 3.0}]
print('BEFORE: ', end=' ')
pprint.pprint(data1)

data1_string = pickle.dumps(data1)

data2 = pickle.loads(data1_string)
print('AFTER : ', end=' ')
pprint.pprint(data2)

print('SAME? :', (data1 is data2))
print('EQUAL?:', (data1 == data2))
```
新构造对象的值等于原始对象的值，但不是原始对象。
```
$ python pickle_unpickle.py

BEFORE:  [{'a': 'A', 'b': 2, 'c': 3.0}]
AFTER :  [{'a': 'A', 'b': 2, 'c': 3.0}]
SAME? : False
EQUAL?: True
```
## Working with Streams
除了dumps()和loads()之外，pickle还提供了处理类文件流的便利函数。可以将多个对象写入流中，然后从流中读取它们，而不事先知道有多少对象被写入，或者它们有多大。
```
# pickle_stream.py

import io
import pickle
import pprint


class SimpleObject:

    def __init__(self, name):
        self.name = name
        self.name_backwards = name[::-1]
        return


data = []
data.append(SimpleObject('pickle'))
data.append(SimpleObject('preserve'))
data.append(SimpleObject('last'))

# Simulate a file.
out_s = io.BytesIO()

# Write to the stream
for o in data:
    print('WRITING : {} ({})'.format(o.name, o.name_backwards))
    pickle.dump(o, out_s)
    out_s.flush()

# Set up a read-able stream
in_s = io.BytesIO(out_s.getvalue())

# Read the data
while True:
    try:
        o = pickle.load(in_s)
    except EOFError:
        break
    else:
        print('READ    : {} ({})'.format(
            o.name, o.name_backwards))
```
该示例使用两个BytesIO缓冲区模拟流。第一个接收pickle的对象，并将其值提供给load()读取的第二个对象。简单的数据库格式也可以使用pickle来存储对象。shelve模块就是这样一个实现。
```
$ python pickle_stream.py

WRITING : pickle (elkcip)
WRITING : preserve (evreserp)
WRITING : last (tsal)
READ    : pickle (elkcip)
READ    : preserve (evreserp)
READ    : last (tsal)
```
除了存储数据之外，pickle还可以方便地进行进程间通信。例如，os.fork()和os.pipe()可用于建立worker进程，该进程从一个管道读取作业指令并将结果写到另一个管道。管理工作程序池、发送作业和接收响应的核心代码可以重用，因为作业和响应对象不必基于特定的类。在使用管道或套接字时，不要忘记在转储每个对象之后进行刷新，以便通过连接将数据推到另一端。请参阅可重用的工作池管理器的multiprocessing模块。
## Problems Reconstructing Objects
在使用自定义类时，被pickle的类必须出现在读取pickle的进程的名称空间中。只有实例的数据被pickle，而不是类定义。类名用于找到在unpickle时创建新对象的构造函数。下面的示例将类的实例写入文件。
```
# pickle_dump_to_file_1.py

import pickle
import sys


class SimpleObject:

    def __init__(self, name):
        self.name = name
        l = list(name)
        l.reverse()
        self.name_backwards = ''.join(l)


if __name__ == '__main__':
    data = []
    data.append(SimpleObject('pickle'))
    data.append(SimpleObject('preserve'))
    data.append(SimpleObject('last'))

    filename = sys.argv[1]

    with open(filename, 'wb') as out_s:
        for o in data:
            print('WRITING: {} ({})'.format(
                o.name, o.name_backwards))
            pickle.dump(o, out_s)
```
运行时，脚本根据命令行上的参数创建一个文件。
```
$ python pickle_dump_to_file_1.py test.dat

WRITING: pickle (elkcip)
WRITING: preserve (evreserp)
WRITING: last (tsal)
```
加载结果pickle对象的简单尝试失败。
```
# pickle_load_from_file_1.py

import pickle
import pprint
import sys

filename = sys.argv[1]

with open(filename, 'rb') as in_s:
    while True:
        try:
            o = pickle.load(in_s)
        except EOFError:
            break
        else:
            print('READ: {} ({})'.format(
                o.name, o.name_backwards))
```
这个版本失败是因为没有SimpleObject类可用。
```
$ python3 pickle_load_from_file_1.py

Traceback (most recent call last):
  File "pickle_load_from_file_1.py", line 12, in <module>
    o = pickle.load(in_s)
AttributeError: Can't get attribute 'SimpleObject' on <module '_
_main__' from 'pickle_load_from_file_1.py'>
```
从原始脚本中导入SimpleObject的修正版本成功了。将此导入语句添加到导入列表的末尾，允许脚本找到类并构造对象。
```
from pickle_dump_to_file_1 import SimpleObject
```
运行修改后的脚本现在将生成所需的结果。
```
$ python pickle_load_from_file_2.py test.dat

READ: pickle (elkcip)
READ: preserve (evreserp)
READ: last (tsal
```
## Unpicklable Objects
不是所有的对象都可以被pickle。套接字、文件句柄、数据库连接和其他运行时状态依赖于操作系统或其他进程的对象可能无法以有意义的方式保存。具有非pickle属性的对象可以定义__getstate__()和__setstate__()来返回要pickle的实例的状态的子集。

__ getstate__()方法必须返回包含对象内部状态的对象。表示该状态的一种方便的方法是使用字典，但值可以是任何可picklable对象。当对象从pickle中加载时，状态被存储并传递给__setstate__()。
```
# pickle_state.py

import pickle


class State:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'State({!r})'.format(self.__dict__)


class MyClass:

    def __init__(self, name):
        print('MyClass.__init__({})'.format(name))
        self._set_name(name)

    def _set_name(self, name):
        self.name = name
        self.computed = name[::-1]

    def __repr__(self):
        return 'MyClass({!r}) (computed={!r})'.format(
            self.name, self.computed)

    def __getstate__(self):
        state = State(self.name)
        print('__getstate__ -> {!r}'.format(state))
        return state

    def __setstate__(self, state):
        print('__setstate__({!r})'.format(state))
        self._set_name(state.name)


inst = MyClass('name here')
print('Before:', inst)

dumped = pickle.dumps(inst)

reloaded = pickle.loads(dumped)
print('After:', reloaded)
```
这个示例使用一个单独的状态对象来保存MyClass的内部状态。当从pickle加载MyClass实例时，__ setstate__()将传递一个用于初始化对象的状态实例。
```
$ python pickle_state.py

MyClass.__init__(name here)
Before: MyClass('name here') (computed='ereh eman')
__getstate__ -> State({'name': 'name here'})
__setstate__(State({'name': 'name here'}))
After: MyClass('name here') (computed='ereh eman')
```
警告：如果返回值为false，则当对象未被pickle时，__ setstate__()不会被调用。
## Circular References
pickle协议自动处理对象之间的循环引用，因此复杂的数据结构不需要任何特殊处理。考虑图中的有向图。它包含几个循环，但是正确的结构可以被pickle，然后重新加载。
```
# pickle_cycle.py

import pickle


class Node:
    """A simple digraph
    """
    def __init__(self, name):
        self.name = name
        self.connections = []

    def add_edge(self, node):
        "Create an edge between this node and the other."
        self.connections.append(node)

    def __iter__(self):
        return iter(self.connections)


def preorder_traversal(root, seen=None, parent=None):
    """Generator function to yield the edges in a graph.
    """
    if seen is None:
        seen = set()
    yield (parent, root)
    if root in seen:
        return
    seen.add(root)
    for node in root:
        recurse = preorder_traversal(node, seen, root)
        for parent, subnode in recurse:
            yield (parent, subnode)


def show_edges(root):
    "Print all the edges in the graph."
    for parent, child in preorder_traversal(root):
        if not parent:
            continue
        print('{:>5} -> {:>2} ({})'.format(
            parent.name, child.name, id(child)))


# Set up the nodes.
root = Node('root')
a = Node('a')
b = Node('b')
c = Node('c')

# Add edges between them.
root.add_edge(a)
root.add_edge(b)
a.add_edge(b)
b.add_edge(a)
b.add_edge(c)
a.add_edge(a)

print('ORIGINAL GRAPH:')
show_edges(root)

# Pickle and unpickle the graph to create
# a new set of nodes.
dumped = pickle.dumps(root)
reloaded = pickle.loads(dumped)

print('\nRELOADED GRAPH:')
show_edges(reloaded)
```
重新加载的节点不是同一个对象，但是节点之间的关系是维护的，只有一个具有多个引用的对象的副本被重新加载。通过检查在pickle之前和之后的节点的id()值，可以验证这两个语句。
```
$ python pickle_cycle.py

ORIGINAL GRAPH:
 root ->  a (2396517899848)
    a ->  b (2396517899960)
    b ->  a (2396517899848)
    b ->  c (2396517933912)
    a ->  a (2396517899848)
 root ->  b (2396517899960)

RELOADED GRAPH:
 root ->  a (2396518024640)
    a ->  b (2396518024696)
    b ->  a (2396518024640)
    b ->  c (2396518024752)
    a ->  a (2396518024640)
 root ->  b (2396518024696)
```

