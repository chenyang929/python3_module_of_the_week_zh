# functools -- Tools for Manipulating Functions
> 目的：作用于其他函数的函数。

functools模块提供用于调整或扩展函数和其他可调用对象的工具，而不会完全重写它们。
## Decorators
functools模块提供的主要工具是类分部，它可用于“包装”具有默认参数的可调用对象。结果对象本身是可调用的，可以将其视为原始函数。它接受与原始参数相同的所有参数，并且可以使用额外的位置参数或命名参数进行调用。可以使用部分参数代替lambda为函数提供默认参数，而不指定某些参数。
### Partial Objects
这个示例展示了函数myfunc()的两个简单的局部对象。show_details()的输出包括局部对象的func、args和关键字属性。
```
# functools_partial.py

import functools


def myfunc(a, b=2):
    "Docstring for myfunc()."
    print('  called myfunc with:', (a, b))


def show_details(name, f, is_partial=False):
    "Show details of a callable object."
    print('{}:'.format(name))
    print('  object:', f)
    if not is_partial:
        print('  __name__:', f.__name__)
    if is_partial:
        print('  func:', f.func)
        print('  args:', f.args)
        print('  keywords:', f.keywords)
    return


show_details('myfunc', myfunc)
myfunc('a', 3)
print()

# Set a different default value for 'b', but require
# the caller to provide 'a'.
p1 = functools.partial(myfunc, b=4)
show_details('partial with named default', p1, True)
p1('passing a')
p1('override b', b=5)
print()

# Set default values for both 'a' and 'b'.
p2 = functools.partial(myfunc, 'default a', b=99)
show_details('partial with defaults', p2, True)
p2()
p2(b='override b')
print()

print('Insufficient arguments:')
p1()
```
在示例的末尾，第一个部分创建的部分被调用，而不传递a的值，从而导致异常。
```
$ python functools_partial.py

myfunc:
  object: <function myfunc at 0x0000023A2D083F28>
  __name__: myfunc
  called myfunc with: ('a', 3)

partial with named default:
  object: functools.partial(<function myfunc at 0x0000023A2D083F28>, b=4)
  func: <function myfunc at 0x0000023A2D083F28>
  args: ()
  keywords: {'b': 4}
  called myfunc with: ('passing a', 4)
  called myfunc with: ('override b', 5)

partial with defaults:
  object: functools.partial(<function myfunc at 0x0000023A2D083F28>, 'default a', b=99)
  func: <function myfunc at 0x0000023A2D083F28>
  args: ('default a',)
  keywords: {'b': 99}
  called myfunc with: ('default a', 99)
  called myfunc with: ('default a', 'override b')

Insufficient arguments:
Traceback (most recent call last):
  File "d:/python3_module_of_the_week_zh/Algorithms/functools/functools_partial.py", line 44, in <module>
    p1()
TypeError: myfunc() missing 1 required positional argument: 'a'
```
### Acquiring Function Properties
部分对象在默认情况下没有__name__或__doc__属性，如果没有这些属性，修饰过的函数将更难调试。使用update_wrapper()，将原始函数的属性复制或添加到部分对象。
```
# functools_update_wrapper.py

import functools


def myfunc(a, b=2):
    "Docstring for myfunc()."
    print('  called myfunc with:', (a, b))


def show_details(name, f):
    "Show details of a callable object."
    print('{}:'.format(name))
    print('  object:', f)
    print('  __name__:', end=' ')
    try:
        print(f.__name__)
    except AttributeError:
        print('(no __name__)')
    print('  __doc__', repr(f.__doc__))
    print()


show_details('myfunc', myfunc)

p1 = functools.partial(myfunc, b=4)
show_details('raw wrapper', p1)

print('Updating wrapper:')
print('  assign:', functools.WRAPPER_ASSIGNMENTS)
print('  update:', functools.WRAPPER_UPDATES)
print()

functools.update_wrapper(p1, myfunc)
show_details('updated wrapper', p1)
```
添加到包装器的属性在WRAPPER_ASSIGNMENTS中定义，而WRAPPER_UPDATES列出要修改的值。
```
$ python functools_update_wrapper.py

myfunc:
  object: <function myfunc at 0x0000022FC326BBF8>
  __name__: myfunc
  __doc__ 'Docstring for myfunc().'

raw wrapper:
  object: functools.partial(<function myfunc at 0x0000022FC326BBF8>, b=4)
  __name__: (no __name__)
  __doc__ 'partial(func, *args, **keywords) - new function with partial application\n    of the given arguments and keywords.\n'

Updating wrapper:
  assign: ('__module__', '__name__', '__qualname__', '__doc__', '__annotations__')
  update: ('__dict__',)

updated wrapper:
  object: functools.partial(<function myfunc at 0x0000022FC326BBF8>, b=4)
  __name__: myfunc
  __doc__ 'Docstring for myfunc().'
```
### Other Callables
Partials可以处理任何可调用对象，而不仅仅是独立函数。
```
# functools_callable.py

import functools


class MyClass:
    "Demonstration class for functools"

    def __call__(self, e, f=6):
        "Docstring for MyClass.__call__"
        print('  called object with:', (self, e, f))


def show_details(name, f):
    "Show details of a callable object."
    print('{}:'.format(name))
    print('  object:', f)
    print('  __name__:', end=' ')
    try:
        print(f.__name__)
    except AttributeError:
        print('(no __name__)')
    print('  __doc__', repr(f.__doc__))
    return


o = MyClass()

show_details('instance', o)
o('e goes here')
print()

p = functools.partial(o, e='default for e', f=8)
functools.update_wrapper(p, o)
show_details('instance wrapper', p)
p()
```
这个示例使用__call__()方法从类的实例创建partials。
```
$ python functools_callable.py

instance:
  object: <__main__.MyClass object at 0x0000026AE9441390>
  __name__: (no __name__)
  __doc__ 'Demonstration class for functools'
  called object with: (<__main__.MyClass object at 0x0000026AE9441390>, 'e goes here', 6)

instance wrapper:
  object: functools.partial(<__main__.MyClass object at 0x0000026AE9441390>, e='default for e', f=8)
  __name__: (no __name__)
  __doc__ 'Demonstration class for functools'
  called object with: (<__main__.MyClass object at 0x0000026AE9441390>, 'default for e', 8)
```
### Methods and Functions
虽然partial()返回一个可直接使用的调用对象，partialmethod()返回一个作为对象的未绑定方法的调用对象。在下面的例子中，同样的独立函数作为MyClass的属性添加两次，一次使用partialmethod()作为method1()，再一次使用partial()作为method2()。
```
# functools_partialmethod.py

import functools


def standalone(self, a=1, b=2):
    "Standalone function"
    print('  called standalone with:', (self, a, b))
    if self is not None:
        print('  self.attr =', self.attr)


class MyClass:
    "Demonstration class for functools"

    def __init__(self):
        self.attr = 'instance attribute'

    method1 = functools.partialmethod(standalone)
    method2 = functools.partial(standalone)


o = MyClass()

print('standalone')
standalone(None)
print()

print('method1 as partialmethod')
o.method1()
print()

print('method2 as partial')
try:
    o.method2()
except TypeError as err:
    print('ERROR: {}'.format(err))
```
method1()可以从MyClass的实例中调用，实例作为第一个参数传递，就像通常定义的方法一样。method2()不是作为绑定方法设置的，因此必须显式地传递self参数，否则调用将导致一个TypeError。
```
$ python functools_partialmethod.py

standalone
  called standalone with: (None, 1, 2)

method1 as partialmethod
  called standalone with: (<__main__.MyClass object at 0x000001C0FF631390>, 1, 2)
  self.attr = instance attribute

method2 as partial
ERROR: standalone() missing 1 required positional argument: 'self'
```
### Acquiring Function Properties for Decorators
更新包装可调用的属性在decorator中尤其有用，因为转换后的函数最终具有原始“裸”函数的属性。
```
# functools_wraps.py

import functools


def show_details(name, f):
    "Show details of a callable object."
    print('{}:'.format(name))
    print('  object:', f)
    print('  __name__:', end=' ')
    try:
        print(f.__name__)
    except AttributeError:
        print('(no __name__)')
    print('  __doc__', repr(f.__doc__))
    print()


def simple_decorator(f):
    @functools.wraps(f)
    def decorated(a='decorated defaults', b=1):
        print('  decorated:', (a, b))
        print('  ', end=' ')
        return f(a, b=b)
    return decorated


def myfunc(a, b=2):
    "myfunc() is not complicated"
    print('  myfunc:', (a, b))
    return


# The raw function
show_details('myfunc', myfunc)
myfunc('unwrapped, default b')
myfunc('unwrapped, passing b', 3)
print()

# Wrap explicitly
wrapped_myfunc = simple_decorator(myfunc)
show_details('wrapped_myfunc', wrapped_myfunc)
wrapped_myfunc()
wrapped_myfunc('args to wrapped', 4)
print()


# Wrap with decorator syntax
@simple_decorator
def decorated_myfunc(a, b):
    myfunc(a, b)
    return


show_details('decorated_myfunc', decorated_myfunc)
decorated_myfunc()
decorated_myfunc('args to decorated', 4)
```
functools提供了一个装饰器，wraps()，它将update_wrapper()应用到修饰函数。
```
$ python functools_wraps.py

myfunc:
  object: <function myfunc at 0x00000200C0CCF2F0>
  __name__: myfunc
  __doc__ 'myfunc() is not complicated'

  myfunc: ('unwrapped, default b', 2)
  myfunc: ('unwrapped, passing b', 3)

wrapped_myfunc:
  object: <function myfunc at 0x00000200C0CCF378>
  __name__: myfunc
  __doc__ 'myfunc() is not complicated'

  decorated: ('decorated defaults', 1)
     myfunc: ('decorated defaults', 1)
  decorated: ('args to wrapped', 4)
     myfunc: ('args to wrapped', 4)

decorated_myfunc:
  object: <function decorated_myfunc at 0x00000200C0CCF488>
  __name__: decorated_myfunc
  __doc__ None

  decorated: ('decorated defaults', 1)
     myfunc: ('decorated defaults', 1)
  decorated: ('args to decorated', 4)
     myfunc: ('args to decorated', 4)
```
## Comparison
在Python 2下，类可以定义__cmp__()方法，该方法返回-1、0或1，基于对象是否小于、等于或大于被比较的项。Python 2.1引入了丰富的比较方法API 
```
__lt__()、__le__()、__eq__()、__ne__()、__gt__()和__ge__()
```
它们执行单个比较操作并返回一个布尔值。Python 3不赞成使用__cmp__()来支持这些新方法，而functools提供的工具可以使编写符合Python 3中新的比较需求的类变得更容易。
### Rich Comparison
丰富的比较API允许具有复杂比较的类以尽可能有效的方式实现每个测试。但是，对于比较简单的类，手工创建每个丰富的比较方法是没有意义的。total_orders()类装饰器使用一个类来提供一些方法，并添加其余的方法。
```
# functools_total_ordering.py

import functools
import inspect
from pprint import pprint


@functools.total_ordering
class MyObject:

    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        print('  testing __eq__({}, {})'.format(
            self.val, other.val))
        return self.val == other.val

    def __gt__(self, other):
        print('  testing __gt__({}, {})'.format(
            self.val, other.val))
        return self.val > other.val


print('Methods:\n')
pprint(inspect.getmembers(MyObject, inspect.isfunction))

a = MyObject(1)
b = MyObject(2)

print('\nComparisons:')
for expr in ['a < b', 'a <= b', 'a == b', 'a >= b', 'a > b']:
    print('\n{:<6}:'.format(expr))
    result = eval(expr)
    print('  result of {}: {}'.format(expr, result))
```
该类必须提供__eq__()的实现和另一种丰富的比较方法。装饰器通过使用提供的比较添加了其他方法的实现。如果无法进行比较，则该方法应该返回NotImplemented，以便在完全失败之前使用反向比较运算符对另一个对象进行比较。
```
$ python functools_total_ordering.py

Methods:

[('__eq__', <function MyObject.__eq__ at 0x000001E71D21F378>),
 ('__ge__', <function _ge_from_gt at 0x000001E71D156378>),
 ('__gt__', <function MyObject.__gt__ at 0x000001E71D21F400>),
 ('__init__', <function MyObject.__init__ at 0x000001E71D21F2F0>),
 ('__le__', <function _le_from_gt at 0x000001E71D156400>),
 ('__lt__', <function _lt_from_gt at 0x000001E71D1562F0>)]

Comparisons:

a < b :
  testing __gt__(1, 2)
  testing __eq__(1, 2)
  result of a < b: True

a <= b:
  testing __gt__(1, 2)
  result of a <= b: True

a == b:
  testing __eq__(1, 2)
  result of a == b: False

a >= b:
  testing __gt__(1, 2)
  testing __eq__(1, 2)
  result of a >= b: False

a > b :
  testing __gt__(1, 2)
  result of a > b: False
```
### Collation Order
由于旧式的比较函数在Python 3中不被使用，所以也不再支持sort()函数的cmp参数。使用比较函数的旧程序可以使用cmp_to_key()将它们转换为返回排序键的函数，该函数用于确定最终序列中的位置。
```
# functools_cmp_to_key.py

import functools


class MyObject:

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return 'MyObject({})'.format(self.val)


def compare_obj(a, b):
    """Old-style comparison function.
    """
    print('comparing {} and {}'.format(a, b))
    if a.val < b.val:
        return -1
    elif a.val > b.val:
        return 1
    return 0


# Make a key function using cmp_to_key()
get_key = functools.cmp_to_key(compare_obj)

def get_key_wrapper(o):
    "Wrapper function for get_key to allow for print statements."
    new_key = get_key(o)
    print('key_wrapper({}) -> {!r}'.format(o, new_key))
    return new_key


objs = [MyObject(x) for x in range(5, 0, -1)]

for o in sorted(objs, key=get_key_wrapper):
    print(o)
```
通常会直接使用cmp_to_key()，但是在本例中引入了一个额外的包装器函数，以便在调用键函数时输出更多信息。

输出显示sort()首先为序列中的每个项调用get_key_wrapper()来生成一个键。cmp_to_key()返回的键是在functools中定义的类的实例，该类使用传入的旧式比较函数实现丰富的比较API。在创建所有键之后，通过比较键对序列进行排序。
```
$ python functools_cmp_to_key.py

key_wrapper(MyObject(5)) -> <functools.KeyWrapper object at 0x000001612F989610>
key_wrapper(MyObject(4)) -> <functools.KeyWrapper object at 0x000001612F989330>
key_wrapper(MyObject(3)) -> <functools.KeyWrapper object at 0x000001612F989230>
key_wrapper(MyObject(2)) -> <functools.KeyWrapper object at 0x000001612F9895F0>
key_wrapper(MyObject(1)) -> <functools.KeyWrapper object at 0x000001612F9895D0>
comparing MyObject(4) and MyObject(5)
comparing MyObject(3) and MyObject(4)
comparing MyObject(2) and MyObject(3)
comparing MyObject(1) and MyObject(2)
MyObject(1)
MyObject(2)
MyObject(3)
MyObject(4)
MyObject(5)
```
## Caching
lru_cache()装饰器将函数封装在最近最少使用的缓存中。函数的参数用于构建一个散列键，然后映射到结果。具有相同参数的后续调用将从缓存中获取值，而不是调用函数。装饰器还向函数添加了一些方法来检查缓存的状态(cache_info())并清空缓存(cache_clear())。
```
# functools_lru_cache.py

import functools


@functools.lru_cache()
def expensive(a, b):
    print('expensive({}, {})'.format(a, b))
    return a * b


MAX = 2

print('First set of calls:')
for i in range(MAX):
    for j in range(MAX):
        expensive(i, j)
print(expensive.cache_info())

print('\nSecond set of calls:')
for i in range(MAX + 1):
    for j in range(MAX + 1):
        expensive(i, j)
print(expensive.cache_info())

print('\nClearing cache:')
expensive.cache_clear()
print(expensive.cache_info())

print('\nThird set of calls:')
for i in range(MAX):
    for j in range(MAX):
        expensive(i, j)
print(expensive.cache_info())
```
这个例子在一组嵌套循环中对expensive()进行了多次调用。第二次调用使用相同的值时，结果出现在缓存中。当清除缓存并再次运行循环时，必须重新计算值。
```
$ python functools_lru_cache.py

First set of calls:
expensive(0, 0)
expensive(0, 1)
expensive(1, 0)
expensive(1, 1)
CacheInfo(hits=0, misses=4, maxsize=128, currsize=4)

Second set of calls:
expensive(0, 2)
expensive(1, 2)
expensive(2, 0)
expensive(2, 1)
expensive(2, 2)
CacheInfo(hits=4, misses=9, maxsize=128, currsize=9)

Clearing cache:
CacheInfo(hits=0, misses=0, maxsize=128, currsize=0)

Third set of calls:
expensive(0, 0)
expensive(0, 1)
expensive(1, 0)
expensive(1, 1)
CacheInfo(hits=0, misses=4, maxsize=128, currsize=4)
```
为了防止缓存在长时间运行的进程中无边界地增长，给它一个最大的大小。默认值是128个条目，但是可以使用maxsize参数对每个缓存进行更改。
```
# functools_lru_cache_expire.py

import functools


@functools.lru_cache(maxsize=2)
def expensive(a, b):
    print('called expensive({}, {})'.format(a, b))
    return a * b


def make_call(a, b):
    print('({}, {})'.format(a, b), end=' ')
    pre_hits = expensive.cache_info().hits
    expensive(a, b)
    post_hits = expensive.cache_info().hits
    if post_hits > pre_hits:
        print('cache hit')


print('Establish the cache')
make_call(1, 2)
make_call(2, 3)

print('\nUse cached items')
make_call(1, 2)
make_call(2, 3)

print('\nCompute a new value, triggering cache expiration')
make_call(3, 4)

print('\nCache still contains one old item')
make_call(2, 3)

print('\nOldest item needs to be recomputed')
make_call(1, 2)
```
在本例中，缓存大小设置为2个条目。当使用了第三组惟一参数(3,4)时，缓存中最老的项将被删除并替换为新的结果。
```
$ python functools_lru_cache_expire.py

Establish the cache
(1, 2) called expensive(1, 2)
(2, 3) called expensive(2, 3)

Use cached items
(1, 2) cache hit
(2, 3) cache hit

Compute a new value, triggering cache expiration
(3, 4) called expensive(3, 4)

Cache still contains one old item
(2, 3) cache hit

Oldest item needs to be recomputed
(1, 2) called expensive(1, 2)
```
lru_cache()管理的缓存的键必须是可清洗的，因此与缓存查找一起包装的函数的所有参数必须是可清洗的。
```
# functools_lru_cache_arguments.py

import functools


@functools.lru_cache(maxsize=2)
def expensive(a, b):
    print('called expensive({}, {})'.format(a, b))
    return a * b


def make_call(a, b):
    print('({}, {})'.format(a, b), end=' ')
    pre_hits = expensive.cache_info().hits
    expensive(a, b)
    post_hits = expensive.cache_info().hits
    if post_hits > pre_hits:
        print('cache hit')


make_call(1, 2)

try:
    make_call([1], 2)
except TypeError as err:
    print('ERROR: {}'.format(err))

try:
    make_call(1, {'2': 'two'})
except TypeError as err:
    print('ERROR: {}'.format(err))
```
如果任何不能被散列的对象被传递给函数，则会引发一个TypeError。
```
$ python functools_lru_cache_arguments.py

(1, 2) called expensive(1, 2)
([1], 2) ERROR: unhashable type: 'list'
(1, {'2': 'two'}) ERROR: unhashable type: 'dict'
```
## Reducing a Data Set
reduce()函数接受一个可调用的和一系列的数据作为输入，并根据从序列中的值调用可调用的值并积累产生的输出来生成一个单一的值。
```
# functools_reduce.py

import functools


def do_reduce(a, b):
    print('do_reduce({}, {})'.format(a, b))
    return a + b


data = range(1, 5)
print(data)
result = functools.reduce(do_reduce, data)
print('result: {}'.format(result))
```
这个例子把输入序列中的数字加起来。
```
$ python functools_reduce.py

range(1, 5)
do_reduce(1, 2)
do_reduce(3, 3)
do_reduce(6, 4)
result: 10
```
可选初始化参数放在序列的前面，并与其他项一起处理。这可以用于使用新的输入更新先前计算的值。
```
# functools_reduce_initializer.py

import functools


def do_reduce(a, b):
    print('do_reduce({}, {})'.format(a, b))
    return a + b


data = range(1, 5)
print(data)
result = functools.reduce(do_reduce, data, 99)
print('result: {}'.format(result))
```
在本例中，使用前一个99的和来初始化reduce()计算的值。
```
$ python functools_reduce_initializer.py

range(1, 5)
do_reduce(99, 1)
do_reduce(100, 2)
do_reduce(102, 3)
do_reduce(105, 4)
result: 109
```
当没有初始值设定项时，带有单个项目的序列会自动降低到该值。空列表生成错误，除非提供了初始化器。
```
# functools_reduce_short_sequences.py

import functools


def do_reduce(a, b):
    print('do_reduce({}, {})'.format(a, b))
    return a + b


print('Single item in sequence:',
      functools.reduce(do_reduce, [1]))

print('Single item in sequence with initializer:',
      functools.reduce(do_reduce, [1], 99))

print('Empty sequence with initializer:',
      functools.reduce(do_reduce, [], 99))

try:
    print('Empty sequence:', functools.reduce(do_reduce, []))
except TypeError as err:
    print('ERROR: {}'.format(err))
```
因为初始化器参数作为默认值，但是如果输入序列不是空的，那么也会与新值相结合，所以必须仔细考虑是否使用它。当将默认值与新值组合起来没有意义时，最好是捕获类型错误，而不是传递初始化器。
```
$ python functools_reduce_short_sequences.py

Single item in sequence: 1
do_reduce(99, 1)
Single item in sequence with initializer: 100
Empty sequence with initializer: 99
ERROR: reduce() of empty sequence with no initial value
```
## Generic Functions
在像Python这样的动态类型化语言中，通常需要根据参数的类型执行稍微不同的操作，特别是在处理项目列表和单个项目之间的差异时。是简单的直接检查参数的类型,但在行为差异的情况下可以分离成单独的函数functools提供singledispatch()装饰器注册一组通用函数自动切换基于函数的第一个参数的类型。
```
# functools_singledispatch.py

import functools


@functools.singledispatch
def myfunc(arg):
    print('default myfunc({!r})'.format(arg))


@myfunc.register(int)
def myfunc_int(arg):
    print('myfunc_int({})'.format(arg))


@myfunc.register(list)
def myfunc_list(arg):
    print('myfunc_list()')
    for item in arg:
        print('  {}'.format(item))


myfunc('string argument')
myfunc(1)
myfunc(2.3)
myfunc(['a', 'b', 'c'])
```
新函数的register()属性用作注册其他实现的另一个装饰器。如果没有找到其他类型特定的函数，则使用singledispatch()包装的第一个函数是默认实现，如本例中的float例子所示。
```
$ python functools_singledispatch.py

default myfunc('string argument')
myfunc_int(1)
default myfunc(2.3)
myfunc_list()
  a
  b
  c
```
当没有找到类型的精确匹配时，将计算继承顺序，并使用最接近的匹配类型。
```
# functools_singledispatch_mro.py

import functools


class A:
    pass


class B(A):
    pass


class C(A):
    pass


class D(B):
    pass


class E(C, D):
    pass


@functools.singledispatch
def myfunc(arg):
    print('default myfunc({})'.format(arg.__class__.__name__))


@myfunc.register(A)
def myfunc_A(arg):
    print('myfunc_A({})'.format(arg.__class__.__name__))


@myfunc.register(B)
def myfunc_B(arg):
    print('myfunc_B({})'.format(arg.__class__.__name__))


@myfunc.register(C)
def myfunc_C(arg):
    print('myfunc_C({})'.format(arg.__class__.__name__))


myfunc(A())
myfunc(B())
myfunc(C())
myfunc(D())
myfunc(E())
```
在本例中，类D和E不完全匹配任何已注册的泛型函数，所选择的函数取决于类层次结构。
```
$ python functools_singledispatch_mro.py

myfunc_A(A)
myfunc_B(B)
myfunc_C(C)
myfunc_B(D)
myfunc_C(E)
```



