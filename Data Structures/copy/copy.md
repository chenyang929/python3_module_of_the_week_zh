## copy -- Duplicate Objects
> 目的：提供使用浅拷贝或深拷贝语义复制对象的功能。

## Shallow Copies
copy()创建的浅拷贝是一个新的容器，它包含对原始对象的内容的引用。
当创建一个列表对象的浅拷贝时，将构造一个新的列表，并将原始对象的元素附加到它。
<pre><code># copy_shallow.py

import copy
import functools


@functools.total_ordering
class MyClass:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name


a = MyClass('a')
my_list = [a]
dup = copy.copy(my_list)

print('             my_list:', my_list)
print('                 dup:', dup)
print('      dup is my_list:', (dup is my_list))
print('      dup == my_list:', (dup == my_list))
print('dup[0] is my_list[0]:', (dup[0] is my_list[0]))
print('dup[0] == my_list[0]:', (dup[0] == my_list[0]))</pre></code>
对于浅拷贝，MyClass实例不是复制的，所以在dup列表中的引用与my_list中的对象是同一个。
<pre><code>$ python copy_shallow.py
             my_list: [<__main__.MyClass object at 0x00000206204284E0>]
                 dup: [<__main__.MyClass object at 0x00000206204284E0>]
      dup is my_list: False
      dup == my_list: True
dup[0] is my_list[0]: True
dup[0] == my_list[0]: True</pre></code>
## Deep Copies
deepcopy()创建的深拷贝是一个新的容器，该容器中填充了原始对象的内容的副本。
要创建一个列表的深拷贝，构造一个新的列表，复制原始列表的元素，然后将这些副本添加到新列表中。

用deepcopy()替换copy()的调用会使输出的差异明显。
<pre><code># copy_deep.py

import copy
import functools


@functools.total_ordering
class MyClass:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name


a = MyClass('a')
my_list = [a]
dup = copy.deepcopy(my_list)

print('             my_list:', my_list)
print('                 dup:', dup)
print('      dup is my_list:', (dup is my_list))
print('      dup == my_list:', (dup == my_list))
print('dup[0] is my_list[0]:', (dup[0] is my_list[0]))
print('dup[0] == my_list[0]:', (dup[0] == my_list[0]))</pre></code>
列表的第一个元素不再是相同的对象引用，但是当两个对象被比较时，它们仍然会被认为是相等的。
<pre><code>$ python copy_deep.py
             my_list: [<__main__.MyClass object at 0x0000016FC2C684A8>]
                 dup: [<__main__.MyClass object at 0x0000016FC2C7B470>]
      dup is my_list: False
      dup == my_list: True
dup[0] is my_list[0]: False
dup[0] == my_list[0]: True</pre></code>
## Customizing Copy Behavior
可以通过使用__copy__()和__deepcopy__()特殊方法来控制拷贝。
+ __copy__()无需任何参数调用，应该返回对象的一个浅拷贝。
+ __deepcopy__()是用一个memo dictionary调用的，它应该返回一个对象的深拷贝。
需要进行深拷贝的任何成员属性都应该和memo dictionary一起传递给copy.deepcopy()，以控制递归。
(稍后将详细解释memo dictionary。)
下面的示例演示如何调用这些方法。
<pre><code># copy_hooks.py

import copy
import functools


@functools.total_ordering
class MyClass:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name

    def __copy__(self):
        print('__copy__()')
        return MyClass(self.name)

    def __deepcopy__(self, memodict={}):
        print('__deepcopy__({})'.format(memodict))
        return MyClass(copy.deepcopy(self.name, memodict))


a = MyClass('a')

sc = copy.copy(a)
dc = copy.deepcopy(a)</pre></code>
memo dictionary用于跟踪已经复制的值，以避免无限递归。
<pre><code>$ python copy_hooks.py
__copy__()
__deepcopy__({})</pre></code>
## Recursion in Deep Copy
为了避免复制递归数据结构的问题，deepcopy()使用字典来跟踪已经复制的对象。
这个字典被传递给__deepcopy__()方法，因此它也可以在那里进行检查。

下一个示例展示了一个相互关联的数据结构(如有向图)如何通过实现__deepcopy__()方法来帮助防止递归。
<pre><code># copy_recursion.py

import copy


class Graph:
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    def add_connection(self, other):
        self.connections.append(other)

    def __repr__(self):
        return 'Graph(name={}, id={})'.format(self.name, id(self))

    def __deepcopy__(self, memodict={}):
        print('\nCalling __deepcopy__ for {!r}'.format(self))
        if self in memodict:
            existing = memodict.get(self)
            print('  Already copied to {!r}'.format(existing))
            return existing
        print('  Memo dictionary')
        if memodict:
            for k, v in memodict.items():
                print('  {}:{}'.format(k, v))
        else:
            print('  (empty)')
        dup = Graph(copy.deepcopy(self.name, memodict), [])
        print('  Coping to new object {}'.format(dup))
        memodict[self] = dup
        for c in self.connections:
            dup.add_connection(copy.deepcopy(c, memodict))
        return dup


root = Graph('root', [])
a = Graph('a', [root])
b = Graph('b', [a, root])
root.add_connection(a)
root.add_connection(b)

dup = copy.deepcopy(root)</pre></code>
图类包括一些基本的有向图方法。一个实例可以用一个名称和它所连接的现有节点的列表来初始化。add_connection()方法用于设置双向连接。它也被深层复制操作符使用。

__deepcopy__()方法打印消息以显示它是如何调用的，并根据需要管理备忘录字典内容。它不会复制整个连接列表，而是创建一个新的列表，并将单个连接的副本附加到它。
这确保在每个新节点被复制时更新备忘录字典，并且避免递归问题或额外的节点副本。与以前一样，该方法在完成时返回复制的对象。

图中显示的图形包含几个循环，但是使用memo字典处理递归会防止遍历导致堆栈溢出错误。当复制根节点时，它会产生以下输出。
<pre><code>$ python copy_recursion.py

Calling __deepcopy__ for Graph(name=root, id=2559359878648)
  Memo dictionary
  (empty)
  Coping to new object Graph(name=root, id=2559359948056)

Calling __deepcopy__ for Graph(name=a, id=2559359878704)
  Memo dictionary
  Graph(name=root, id=2559359878648):Graph(name=root, id=2559359948056)
  Coping to new object Graph(name=a, id=2559359948112)

Calling __deepcopy__ for Graph(name=root, id=2559359878648)
  Already copied to Graph(name=root, id=2559359948056)

Calling __deepcopy__ for Graph(name=b, id=2559359905632)
  Memo dictionary
  Graph(name=root, id=2559359878648):Graph(name=root, id=2559359948056)
  Graph(name=a, id=2559359878704):Graph(name=a, id=2559359948112)
  2559359878648:Graph(name=root, id=2559359948056)
  2559361408600:[Graph(name=root, id=2559359878648), Graph(name=a, id=2559359878704)]
  2559359878704:Graph(name=a, id=2559359948112)
  Coping to new object Graph(name=b, id=2559359991592)</pre></code>
  
第二次遇到根节点时，当一个节点被复制时，__deepcopy__()检测递归，并从memo字典中重用现有的值，而不是创建一个新对象。