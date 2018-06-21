# operator -- Functional Interface to Built-in Operators
> 目的：内置操作符的功能接口。

使用迭代器编程有时需要为简单表达式创建小函数。有时，这些函数可以实现为lambda函数，但对于某些操作，根本不需要新的函数。操作员模块定义了对应于标准对象api的算术、比较和其他操作的内置操作的函数。
## Logical Operations
有一些函数用于确定值的布尔等价性，将其否定以创建相反的布尔值，并比较对象以查看它们是否相同。
```
# operator_boolean.py

from operator import not_, truth, is_, is_not

a = -1
b = 5

print('a =', a)
print('b =', b)
print()

print('not_(a)     :', not_(a))
print('truth(a)    :', truth(a))
print('is_(a, b)   :', is_(a, b))
print('is_not(a, b):', is_not(a, b))
```
not_()包含尾下划线，因为not是Python关键字。truth()应用与在if语句中测试表达式或将表达式转换为bool时相同的逻辑。is_()实现了is关键字使用的相同检查，is_not()执行相同的测试并返回相反的答案。
```
$ python operator_boolean.py

a = -1
b = 5

not_(a)     : False
truth(a)    : True
is_(a, b)   : False
is_not(a, b): True
```
## Comparison Operators
所有丰富的比较运算符都得到了支持。
```
# operator_comparisons.py

from operator import lt, le, eq, ne, ge, gt

a = 1
b = 5.0

print('a =', a)
print('b =', b)
for func in (lt, le, eq, ne, ge, gt):
    print('{}(a, b): {}'.format(func.__name__, func(a, b)))
```
函数的作用相当于使用<、<=、==、>=和>的表达式语法。
```
$ python operator_comparisons.py

a = 1
b = 5.0
lt(a, b): True
le(a, b): True
eq(a, b): False
ne(a, b): True
ge(a, b): False
gt(a, b): False
```
## Arithmetic Operators
还支持操作数值的算术运算符。
```
# operator_math.py

from operator import *

a = -1
b = 5.0
c = 2
d = 6

print('a =', a)
print('b =', b)
print('c =', c)
print('d =', d)

print('\nPositive/Negative:')
print('abs(a):', abs(a))
print('neg(a):', neg(a))
print('neg(b):', neg(b))
print('pos(a):', pos(a))
print('pos(b):', pos(b))

print('\nArithmetic:')
print('add(a, b)     :', add(a, b))
print('floordiv(a, b):', floordiv(a, b))
print('floordiv(d, c):', floordiv(d, c))
print('mod(a, b)     :', mod(a, b))
print('mul(a, b)     :', mul(a, b))
print('pow(c, d)     :', pow(c, d))
print('sub(b, a)     :', sub(b, a))
print('truediv(a, b) :', truediv(a, b))
print('truediv(d, c) :', truediv(d, c))

print('\nBitwise:')
print('and_(c, d)  :', and_(c, d))
print('invert(c)   :', invert(c))
print('lshift(c, d):', lshift(c, d))
print('or_(c, d)   :', or_(c, d))
print('rshift(d, c):', rshift(d, c))
print('xor(c, d)   :', xor(c, d))
```
有两个独立的除法操作符:floordiv(在3.0版本之前在Python中实现的整数除法)和truediv()(浮点除法)。
```
$ python operator_math.py

a = -1
b = 5.0
c = 2
d = 6

Positive/Negative:
abs(a): 1
neg(a): 1
neg(b): -5.0
pos(a): -1
pos(b): 5.0

Arithmetic:
add(a, b)     : 4.0
floordiv(a, b): -1.0
floordiv(d, c): 3
mod(a, b)     : 4.0
mul(a, b)     : -5.0
pow(c, d)     : 64
sub(b, a)     : 6.0
truediv(a, b) : -0.2
truediv(d, c) : 3.0

Bitwise:
and_(c, d)  : 2
invert(c)   : -3
lshift(c, d): 128
or_(c, d)   : 6
rshift(d, c): 1
xor(c, d)   : 4
```
## Sequence Operators
处理序列的操作符可分为四组:构建序列、搜索项、访问内容和从序列中删除项。
```
# operator_sequences.py

from operator import *

a = [1, 2, 3]
b = ['a', 'b', 'c']

print('a =', a)
print('b =', b)

print('\nConstructive:')
print('  concat(a, b):', concat(a, b))

print('\nSearching:')
print('  contains(a, 1)  :', contains(a, 1))
print('  contains(b, "d"):', contains(b, "d"))
print('  countOf(a, 1)   :', countOf(a, 1))
print('  countOf(b, "d") :', countOf(b, "d"))
print('  indexOf(a, 5)   :', indexOf(a, 1))

print('\nAccess Items:')
print('  getitem(b, 1)                  :',
      getitem(b, 1))
print('  getitem(b, slice(1, 3))        :',
      getitem(b, slice(1, 3)))
print('  setitem(b, 1, "d")             :', end=' ')
setitem(b, 1, "d")
print(b)
print('  setitem(a, slice(1, 3), [4, 5]):', end=' ')
setitem(a, slice(1, 3), [4, 5])
print(a)

print('\nDestructive:')
print('  delitem(b, 1)          :', end=' ')
delitem(b, 1)
print(b)
print('  delitem(a, slice(1, 3)):', end=' ')
delitem(a, slice(1, 3))
print(a)
```
其中的一些操作，如setitem()和delitem()，修改了序列并没有返回值。
```
$ python operator_sequences.py

a = [1, 2, 3]
b = ['a', 'b', 'c']

Constructive:
  concat(a, b): [1, 2, 3, 'a', 'b', 'c']

Searching:
  contains(a, 1)  : True
  contains(b, "d"): False
  countOf(a, 1)   : 1
  countOf(b, "d") : 0
  indexOf(a, 5)   : 0

Access Items:
  getitem(b, 1)                  : b
  getitem(b, slice(1, 3))        : ['b', 'c']
  setitem(b, 1, "d")             : ['a', 'd', 'c']
  setitem(a, slice(1, 3), [4, 5]): [1, 4, 5]

Destructive:
  delitem(b, 1)          : ['a', 'c']
  delitem(a, slice(1, 3)): [1]
```
## In-place Operators
除了标准操作符之外，许多类型的对象通过特殊操作符(如+=)支持“就地”修改。也有相同的功能进行就地修改:
```
# operator_inplace.py

from operator import *

a = -1
b = 5.0
c = [1, 2, 3]
d = ['a', 'b', 'c']
print('a =', a)
print('b =', b)
print('c =', c)
print('d =', d)
print()

a = iadd(a, b)
print('a = iadd(a, b) =>', a)
print()

c = iconcat(c, d)
print('c = iconcat(c, d) =>', c)
```
这些示例仅演示了其中的一些函数。有关详细信息，请参阅标准库文档。
```
$ python operator_inplace.py

a = -1
b = 5.0
c = [1, 2, 3]
d = ['a', 'b', 'c']

a = iadd(a, b) => 4.0

c = iconcat(c, d) => [1, 2, 3, 'a', 'b', 'c']
```
## Attribute and Item "Getters"
操作员模块最不寻常的特性之一是getter的概念。这些是在运行时构造的可调用对象，用于从序列中检索对象或内容的属性。当处理迭代器或生成器序列时，getter特别有用，它们的开销比lambda或Python函数要小。
```
# operator_attrgetter.py

from operator import *


class MyObj:
    """example class for attrgetter"""

    def __init__(self, arg):
        super().__init__()
        self.arg = arg

    def __repr__(self):
        return 'MyObj({})'.format(self.arg)


l = [MyObj(i) for i in range(5)]
print('objects   :', l)

# Extract the 'arg' value from each object
g = attrgetter('arg')
vals = [g(i) for i in l]
print('arg values:', vals)

# Sort using arg
l.reverse()
print('reversed  :', l)
print('sorted    :', sorted(l, key=g))
```
属性getters的工作方式为x, n='attrname': getattr(x, n):
```
$ python operator_attrgetter.py

objects   : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]
arg values: [0, 1, 2, 3, 4]
reversed  : [MyObj(4), MyObj(3), MyObj(2), MyObj(1), MyObj(0)]
sorted    : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]
```
项目getter的工作方式是x, y=5: x[y]:
```
# operator_itemgetter.py

from operator import *

l = [dict(val=-1 * i) for i in range(4)]
print('Dictionaries:')
print(' original:', l)
g = itemgetter('val')
vals = [g(i) for i in l]
print('   values:', vals)
print('   sorted:', sorted(l, key=g))

print()
l = [(i, i * -2) for i in range(4)]
print('\nTuples:')
print(' original:', l)
g = itemgetter(1)
vals = [g(i) for i in l]
print('   values:', vals)
print('   sorted:', sorted(l, key=g))
```
项目获取器使用映射和序列。
```
$ python operator_itemgetter.py

Dictionaries:
 original: [{'val': 0}, {'val': -1}, {'val': -2}, {'val': -3}]
   values: [0, -1, -2, -3]
   sorted: [{'val': -3}, {'val': -2}, {'val': -1}, {'val': 0}]


Tuples:
 original: [(0, 0), (1, -2), (2, -4), (3, -6)]
   values: [0, -2, -4, -6]
   sorted: [(3, -6), (2, -4), (1, -2), (0, 0)]
```
## Combining Operators and Custom Classes
运算符模块中的函数通过其操作的标准Python接口工作，因此它们与用户定义的类以及内置的类型一起工作。
```
# operator_classes.py

from operator import *


class MyObj:
    """Example for operator overloading"""

    def __init__(self, val):
        super(MyObj, self).__init__()
        self.val = val

    def __str__(self):
        return 'MyObj({})'.format(self.val)

    def __lt__(self, other):
        """compare for less-than"""
        print('Testing {} < {}'.format(self, other))
        return self.val < other.val

    def __add__(self, other):
        """add values"""
        print('Adding {} + {}'.format(self, other))
        return MyObj(self.val + other.val)


a = MyObj(1)
b = MyObj(2)

print('Comparison:')
print(lt(a, b))

print('\nArithmetic:')
print(add(a, b))
```
有关每个操作符使用的特殊方法的完整列表，请参阅Python参考指南。
```
$ python operator_classes.py

Comparison:
Testing MyObj(1) < MyObj(2)
True

Arithmetic:
Adding MyObj(1) + MyObj(2)
MyObj(3)
```