# weakref -- Impermanent References to Objects
> 目的：引用一个“昂贵的”对象，但如果没有其他非弱引用，则允许垃圾收集器回收其内存。

weakref模块支持对对象的弱引用。一个正常的引用增加了对象的引用计数，并防止它被垃圾收集。这个结果并不总是可取的，
特别是当一个循环引用可能出现或者当内存需要删除对象缓存时。弱引用是一个对象的句柄，它不会阻止它自动被清除。
## References
对对象的弱引用通过ref类进行管理。要检索原始对象，请调用引用对象。
<pre><code># weakref_ref.py

import weakref


class ExpensiveObject:

    def __del__(self):
        print('(Deleting {})'.format(self))


obj = ExpensiveObject()
r = weakref.ref(obj)

print('obj:', obj)
print('ref:', r)
print('r():', r())

print('deleting obj')
del obj
print('r():', r())</pre></code>
在本例中，由于obj在第二次调用引用之前被删除，因此ref没有返回任何值。
<pre><code>$ python weakref_ref.py
obj: <__main__.ExpensiveObject object at 0x000002346F9985F8>
ref: <weakref at 0x000002346F98CF98; to 'ExpensiveObject' at 0x000002346F9985F8>
r(): <__main__.ExpensiveObject object at 0x000002346F9985F8>
deleting obj
(Deleting <__main__.ExpensiveObject object at 0x000002346F9985F8>)
r(): None</pre></code>
## Reference Callbacks
ref构造函数接受一个可选的回调函数，该函数在被引用的对象被删除时调用。
<pre><code># weakref_ref_callback.py

import weakref


class ExpensiveObject:

    def __del__(self):
        print('(Deleting {})'.format(self))


def callback(reference):
    print('callback({!r})'.format(reference))


obj = ExpensiveObject()
r = weakref.ref(obj, callback)

print('obj:', obj)
print('ref:', r)
print('r():', r())

print('deleting obj')
del obj
print('r():', r())</pre></code>
在引用死后，回调接收引用对象作为参数，并不再引用原始对象。此特性的一个用途是将弱引用对象从缓存中删除。
<pre><code>$ python weakref_ref_callback.py
obj: <__main__.ExpensiveObject object at 0x0000018C18D2E400>
ref: <weakref at 0x0000018C18D1CF98; to 'ExpensiveObject' at 0x0000018C18D2E400>
r(): <__main__.ExpensiveObject object at 0x0000018C18D2E400>
deleting obj
(Deleting <__main__.ExpensiveObject object at 0x0000018C18D2E400>)
callback(<weakref at 0x0000018C18D1CF98; dead>)
r(): None</pre></code>
## Finalizing Objects
为了在清除弱引用时对资源进行更健壮的管理，使用finalize将回调与对象关联起来。
即使应用程序没有保留对finalizer的引用，也会保留一个finalize实例，直到被附加的对象被删除为止。
</pre></code># weakref_finalize.py

import weakref


class ExpensiveObject:

    def __del__(self):
        print('(Deleting {})'.format(self))


def on_finalize(*args):
    print('on_finalize({!r})'.format(args))
    

obj = ExpensiveObject()
weakref.finalize(obj, on_finalize, 'extra argument')

del obj</pre></code>
finalize的参数是跟踪的对象，当对象被垃圾收集时调用该对象，会将任何位置或命名的参数传递给callable。
<pre><code>$ python weakref_finalize.py
(Deleting <__main__.ExpensiveObject object at 0x000001E11FFA85C0>)
on_finalize(('extra argument',))</pre></code>
finalize实例有一个可写的适当的atexit来控制回调是否在程序退出时被调用，如果该回调还没有被调用的话。
<pre><code># weakref_finalize_atexit.py

import sys
import weakref


class ExpensiveObject:

    def __del__(self):
        print('(Deleting) {}'.format(self))


def on_finalize(*args):
    print('on_finalize({!r})'.format(args))


obj = ExpensiveObject()
f = weakref.finalize(obj, on_finalize, 'extra argument')
f.atexit = bool(int(sys.argv[1]))</pre></code>
默认情况是调用回调。设置atexit为false禁用默认行为。
<pre><code>$ python weakref_finalize_atexit.py 1
on_finalize(('extra argument',))
(Deleting) <__main__.ExpensiveObject object at 0x0000020DE82BE2B0>

$ python weakref_finalize_atexit.py 0

</pre></code>
给finalize实例一个指向它所跟踪的对象的引用会导致引用被保留，所以对象不会被垃圾收集。
<pre><code># weakref_finalize_reference.py

import gc
import weakref


class ExpensiveObject:

    def __del__(self):
        print('(Deleting {})'.format(self))


def on_finalize(*args):
    print('on_finalize({!r})'.format(args))


obj = ExpensiveObject()
obj_id = id(obj)

f = weakref.finalize(obj, on_finalize, obj)
f.atexit = False

del obj

for o in gc.get_objects():
    if id(o) == obj_id:
        print('found uncollected object in gc')</pre></code>
如本示例所示，即使删除了对obj的显式引用，该对象仍然保留并通过f对垃圾收集器可见。
<pre><code>$ python weakref_finalize_reference.py
found uncollected object in gc</pre></code>
使用被跟踪对象的方法作为callable也可以阻止对象被垃圾回收。
<pre><code># weakref_finalize_reference_method.py


import gc
import weakref


class ExpensiveObject:

    def __del__(self):
        print('(Deleting {})'.format(self))

    def do_finalize(self):
        print('do_finalize')


obj = ExpensiveObject()
obj_id = id(obj)

f = weakref.finalize(obj, obj.do_finalize)
f.atexit = False

del obj

for o in gc.get_objects():
    if id(o) == obj_id:
        print('found uncollected object in gc')</pre></code>
由于给finalize的回调是对象绑定的方法，finalize对象保存了对obj的引用，故obj不能被删除和垃圾回收。
<pre><code>$ python weakref_finalize_reference_method.py
found uncollected object in gc</pre></code>
## Proxies
有时使用代理更方便，而不是弱引用。代理可以像原对象一样使用，不需要在对象可访问之前被调用。因
此，它们可以被传递给一个库，它不知道自己接收的是一个引用而不是实际对象。
<pre><code># weakref_proxy.py


import weakref


class ExpensiveObject:

    def __init__(self, name):
        self.name = name

    def __del__(self):
        print('(Delete {})'.format(self))


obj = ExpensiveObject('My Object')
r = weakref.ref(obj)
p = weakref.proxy(obj)

print('via obj:', obj.name)
print('via ref:', r().name)
print('via proxy:', p.name)
del obj
print('via proxy:', p.name)</pre></code>
如果在删除了referent对象之后访问代理，则会引发一个ReferenceError异常。
<pre><code>$ python weakref_proxy.py
via obj: My Object
via ref: My Object
via proxy: My Object
(Delete <__main__.ExpensiveObject object at 0x00000180C10E84A8>)
Traceback (most recent call last):
  File "weakref_proxy.py", line 24, in <module>
    print('via proxy:', p.name)
ReferenceError: weakly-referenced object no longer exists</pre></code>
## Caching Objects

