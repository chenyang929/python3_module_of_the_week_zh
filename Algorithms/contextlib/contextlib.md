# contextlib -- Context Manager Utilities
> 目的：用于创建和处理上下文管理器的实用程序。

contextlib模块包含用于处理上下文管理器和with语句的实用程序。
## Context Manager API
上下文管理器负责代码块中的资源，可能在输入块时创建它，然后在块退出后清理它。例如，文件支持上下文管理器API，以便确保在所有读写完成之后关闭它们。
```
# contextlib_file.py

with open('pymotw.txt', 'wt') as f:
    f.write('contents go here')
# file is automatically closed
```
上下文管理器由with语句启用，而API包含两种方法。__ enter__()方法在执行流进入with内部的代码块时运行。它返回要在上下文中使用的对象。当执行流离开with块时，调用上下文管理器的__exit__()方法来清理使用的任何资源。
```
# contextlib_api.py

class Context:

    def __init__(self):
        print('__init__()')

    def __enter__(self):
        print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__()')


with Context():
    print('Doing work in the context')
```
结合上下文管理器和with语句是编写try:finally block的一种更紧凑的方式，因为始终调用上下文管理器的__exit__()方法，即使引发了异常。
```
$ python contextlib_api.py

__init__()
__enter__()
Doing work in the context
__exit__()
```
__ enter__()方法可以返回任何对象，以便与with语句的as子句中指定的名称相关联。在本例中，上下文返回一个使用开放上下文的对象。
```
# contextlib_api_other_object.py

class WithinContext:

    def __init__(self, context):
        print('WithinContext.__init__({})'.format(context))

    def do_something(self):
        print('WithinContext.do_something()')

    def __del__(self):
        print('WithinContext.__del__')


class Context:

    def __init__(self):
        print('Context.__init__()')

    def __enter__(self):
        print('Context.__enter__()')
        return WithinContext(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Context.__exit__()')


with Context() as c:
    c.do_something()
```
与变量c关联的值是__enter__()返回的对象，它不一定是在with语句中创建的上下文实例。
```
$ python contextlib_api_other_object.py

Context.__init__()
Context.__enter__()
WithinContext.__init__(<__main__.Context object at 0x000001AF34651DA0>)
WithinContext.do_something()
Context.__exit__()
WithinContext.__del__
```
__ exit__()方法接收包含在with块中引发的任何异常细节的参数。
```
# contextlib_api_error.py

class Context:

    def __init__(self, handle_error):
        print('__init__({})'.format(handle_error))
        self.handle_error = handle_error

    def __enter__(self):
        print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__()')
        print('  exc_type =', exc_type)
        print('  exc_val  =', exc_val)
        print('  exc_tb   =', exc_tb)
        return self.handle_error


with Context(True):
    raise RuntimeError('error message handled')

print()

with Context(False):
    raise RuntimeError('error message propagated')
```
如果上下文管理器可以处理异常，__ exit__()应该返回一个真实值，以表明不需要传播异常。返回false会导致在__exit__()返回后重新引发异常。
```
$ python contextlib_api_error.py

__init__(True)
__enter__()
__exit__()
  exc_type = <class 'RuntimeError'>
  exc_val  = error message handled
  exc_tb   = <traceback object at 0x0000025BA42D4CC8>

__init__(False)
__enter__()
__exit__()
  exc_type = <class 'RuntimeError'>
  exc_val  = error message propagated
  exc_tb   = <traceback object at 0x0000025BA42D4CC8>
Traceback (most recent call last):
  File "contextlib_api_error.py", line 27, in <module>
    raise RuntimeError('error message propagated')
RuntimeError: error message propagated
```
## Context Managers as Function Decorators
ContextDecorator类添加了对常规上下文管理器类的支持，使它们可以用作函数修饰器和上下文管理器。
```
# contextlib_decorator.py

import contextlib


class Context(contextlib.ContextDecorator):

    def __init__(self, how_used):
        self.how_used = how_used
        print('__init__({})'.format(how_used))

    def __enter__(self):
        print('__enter__({})'.format(self.how_used))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__({})'.format(self.how_used))


@Context('as decorator')
def func(message):
    print(message)


print()
with Context('as context manager'):
    print('Doing work in the context')

print()
func('Doing work in the wrapped function')
```
使用上下文管理器作为装饰器的一个不同之处在于，__ enter__()返回的值在正在修饰的函数中不可用，这与使用with和as不同。传递给修饰函数的参数以通常的方式可用。
```
$ python contextlib_decorator.py

__init__(as decorator)

__init__(as context manager)
__enter__(as context manager)
Doing work in the context
__exit__(as context manager)

__enter__(as decorator)
Doing work in the wrapped function
__exit__(as decorator)
```
## From Generator to Context Manager
通过使用__enter__()和__exit__()方法编写类，以传统方式创建上下文管理器并不困难。但是，有时把所有的内容都写出来对于一些琐碎的上下文来说是额外的开销。在这种情况下，使用contextmanager()装饰器将生成器函数转换为上下文管理器。
```
# contextlib_contextmanager.py

import contextlib


@contextlib.contextmanager
def make_context():
    print('  entering')
    try:
        yield {}
    except RuntimeError as err:
        print('  ERROR:', err)
    finally:
        print('  exiting')


print('Normal:')
with make_context() as value:
    print('  inside with statement:', value)

print('\nHandled error:')
with make_context() as value:
    raise RuntimeError('showing example of handling an error')

print('\nUnhandled error:')
with make_context() as value:
    raise ValueError('this exception is not handled')
```
生成器应该初始化上下文，生成一次，然后清理上下文。得到的值(如果有的话)绑定到with语句的as子句中的变量。来自with块的异常在生成器中重新引发，因此可以在那里处理它们。
```
$ python contextlib_contextmanager.py

Normal:
  entering
  inside with statement: {}
  exiting

Handled error:
  entering
  ERROR: showing example of handling an error
  exiting

Unhandled error:
  entering
  exiting
Traceback (most recent call last):
  File "d:/python3_module_of_the_week_zh/Algorithms/contextlib/contextlib_contextmanager.py", line 27, in <module>
    raise ValueError('this exception is not handled')
ValueError: this exception is not handled
```
contextmanager()返回的上下文管理器派生自ContextDecorator，因此它也可以作为函数装饰器。
```
# contextlib_contextmanager_decorator.py

import contextlib


@contextlib.contextmanager
def make_context():
    print('  entering')
    try:
        # Yield control, but not a value, because any value
        # yielded is not available when the context manager
        # is used as a decorator.
        yield
    except RuntimeError as err:
        print('  ERROR:', err)
    finally:
        print('  exiting')


@make_context()
def normal():
    print('  inside with statement')


@make_context()
def throw_error(err):
    raise err


print('Normal:')
normal()

print('\nHandled error:')
throw_error(RuntimeError('showing example of handling an error'))

print('\nUnhandled error:')
throw_error(ValueError('this exception is not handled'))
```
在上面的ContextDecorator示例中，当上下文管理器用作装饰器时，生成器生成的值在正在修饰的函数中不可用。传递给修饰函数的参数仍然可用，如本例中的throw_error()所示。
```
$ python contextlib_contextmanager_decorator.py

Normal:
  entering
  inside with statement
  exiting

Handled error:
  entering
  ERROR: showing example of handling an error
  exiting

Unhandled error:
  entering
  exiting
Traceback (most recent call last):
  File "contextlib_contextmanager_decorator.py", line 37, in <module>
    throw_error(ValueError('this exception is not handled'))
  File "C:\python3\lib\contextlib.py", line 52, in inner
    return func(*args, **kwds)
  File "contextlib_contextmanager_decorator.py", line 27, in throw_error
    raise err
ValueError: this exception is not handled
```
## Closing Open Handles
file类直接支持上下文管理器API，但其他一些表示open句柄的对象则不支持。contextlib的标准库文档中给出的示例是从urllib.urlopen()返回的对象。还有其他遗留类使用close()方法，但不支持上下文管理器API。为了确保句柄是关闭的，使用close()来为它创建一个上下文管理器。
```
# contextlib_closing.py

import contextlib


class Door:

    def __init__(self):
        print('  __init__()')
        self.status = 'open'

    def close(self):
        print('  close()')
        self.status = 'closed'


print('Normal Example:')
with contextlib.closing(Door()) as door:
    print('  inside with statement: {}'.format(door.status))
print('  outside with statement: {}'.format(door.status))

print('\nError handling example:')
try:
    with contextlib.closing(Door()) as door:
        print('  raising from inside with statement')
        raise RuntimeError('error message')
except Exception as err:
    print('  Had an error:', err)
```
无论with块中是否有错误，句柄都是关闭的。
```
$ python contextlib_closing.py

Normal Example:
  __init__()
  inside with statement: open
  close()
  outside with statement: closed

Error handling example:
  __init__()
  raising from inside with statement
  close()
  Had an error: error message
```
## Ignoring Exceptions
忽略由库引发的异常通常是有用的，因为错误表明所期望的状态已经实现，或者它可以被忽略。忽略异常最常见的方法是尝试:except语句，在except块中只有pass语句。
```
# contextlib_ignore_error.py

import contextlib


class NonFatalError(Exception):
    pass


def non_idempotent_operation():
    raise NonFatalError(
        'The operation failed because of existing state'
    )


try:
    print('trying non-idempotent operation')
    non_idempotent_operation()
    print('succeeded!')
except NonFatalError:
    pass

print('done')
```
在这种情况下，操作失败，错误被忽略。
```
$ python contextlib_ignore_error.py

trying non-idempotent operation
done
```
try:except表单可以用contextli .suppress()替换，以更显式地抑制在with块中任何地方发生的异常。
```
# contextlib_suppress.py

import contextlib


class NonFatalError(Exception):
    pass


def non_idempotent_operation():
    raise NonFatalError(
        'The operation failed because of existing state'
    )


with contextlib.suppress(NonFatalError):
    print('trying non-idempotent operation')
    non_idempotent_operation()
    print('succeeded!')

print('done')
```
在这个更新的版本中，异常被完全丢弃。
```
$ python contextlib_suppress.py

trying non-idempotent operation
done
```
## Redirecting Output Streams
设计不良的库代码可以直接写入sys.stdout或sys.stderr，不提供参数来配置不同的输出目的地。可以使用redirect_stdout()和redirect_stderr()上下文管理器从这样的函数中捕获输出，对于这样的函数，不能更改源以接受新的输出参数。
```
# contextlib_redirect.py

from contextlib import redirect_stdout, redirect_stderr
import io
import sys


def misbehaving_function(a):
    sys.stdout.write('(stdout) A: {!r}\n'.format(a))
    sys.stderr.write('(stderr) A: {!r}\n'.format(a))


capture = io.StringIO()
with redirect_stdout(capture), redirect_stderr(capture):
    misbehaving_function(5)

print(capture.getvalue())
```
在本例中，misbehaving_function()将写入stdout和stderr，但两个上下文管理器将该输出发送到相同的io.StringIO实例，保存到稍后使用。
```
$ python contextlib_redirect.py

(stdout) A: 5
(stderr) A: 5
```
注意：redirect_stdout()和redirect_stderr()都通过替换sys模块中的对象来修改全局状态，应该小心使用。这些函数不是线程安全的，并且可能会干扰其他操作，这些操作期望将标准输出流附加到终端设备上。

## Dynamic Context Manager Stacks
大多数上下文管理器每次只对一个对象进行操作，例如单个文件或数据库句柄。在这些情况下，对象是预先知道的，使用上下文管理器的代码可以围绕该对象构建。在其他情况下，程序可能需要在上下文中创建未知数量的对象，同时希望在控制流退出上下文时清理所有对象。创建ExitStack来处理这些更动态的情况。

ExitStack实例维护一个清理回调的堆栈数据结构。回调被显式地填充在上下文中，当控制流退出上下文时，任何已注册的回调都以相反的顺序被调用。结果就像使用多元素嵌套语句一样，只是它们是动态建立的。
### Stacking Context Managers
有几种方法可以填充ExitStack。这个示例使用enter_context()向堆栈添加一个新的上下文管理器。
```
# contextlib_exitstack_enter_context.py

import contextlib


@contextlib.contextmanager
def make_context(i):
    print('{} entering'.format(i))
    yield {}
    print('{} exiting'.format(i))


def variable_stack(n, msg):
    with contextlib.ExitStack() as stack:
        for i in range(n):
            stack.enter_context(make_context(i))
        print(msg)


variable_stack(2, 'inside context')
```
enter_context()首先在上下文管理器上调用__enter__()，然后将其__exit__()方法注册为回调，以便在堆栈被撤消时调用。
```
$ python contextlib_exitstack_enter_context.py

0 entering
1 entering
inside context
1 exiting
0 exiting
```
给予ExitStack的上下文管理器被当作是嵌套在一系列语句中的。上下文中的任何地方发生的错误通过上下文管理器的正常错误处理传播。这些上下文管理器类说明了错误传播的方式。
```
# contextlib_context_managers.py

import contextlib


class Tracker:
    "Base class for noisy context managers."

    def __init__(self, i):
        self.i = i

    def msg(self, s):
        print('  {}({}): {}'.format(
            self.__class__.__name__, self.i, s))

    def __enter__(self):
        self.msg('entering')


class HandleError(Tracker):
    "If an exception is received, treat it as handled."

    def __exit__(self, *exc_details):
        received_exc = exc_details[1] is not None
        if received_exc:
            self.msg('handling exception {!r}'.format(
                exc_details[1]))
        self.msg('exiting {}'.format(received_exc))
        # Return Boolean value indicating whether the exception
        # was handled.
        return received_exc


class PassError(Tracker):
    "If an exception is received, propagate it."

    def __exit__(self, *exc_details):
        received_exc = exc_details[1] is not None
        if received_exc:
            self.msg('passing exception {!r}'.format(
                exc_details[1]))
        self.msg('exiting')
        # Return False, indicating any exception was not handled.
        return False


class ErrorOnExit(Tracker):
    "Cause an exception."

    def __exit__(self, *exc_details):
        self.msg('throwing error')
        raise RuntimeError('from {}'.format(self.i))


class ErrorOnEnter(Tracker):
    "Cause an exception."

    def __enter__(self):
        self.msg('throwing error on enter')
        raise RuntimeError('from {}'.format(self.i))

    def __exit__(self, *exc_info):
        self.msg('exiting')
```
### Arbitrary Context Callbacks
ExitStack还支持为关闭上下文而进行的任意回调，这使得清理通过上下文管理器无法控制的资源变得很容易。
```
# contextlib_exitstack_callbacks.py

import contextlib


def callback(*args, **kwds):
    print('closing callback({}, {})'.format(args, kwds))


with contextlib.ExitStack() as stack:
    stack.callback(callback, 'arg1', 'arg2')
    stack.callback(callback, arg3='val3')
```
就像使用完整上下文管理器的__exit__()方法一样，回调也会以它们注册的相反顺序调用。
```
$ python contextlib_exitstack_callbacks.py

closing callback((), {'arg3': 'val3'})
closing callback(('arg1', 'arg2'), {})
```
无论是否发生错误，都将调用回调函数，并且不会给出关于是否发生错误的任何信息。它们的返回值被忽略。
```
# contextlib_exitstack_callbacks_error.py

import contextlib


def callback(*args, **kwds):
    print('closing callback({}, {})'.format(args, kwds))


try:
    with contextlib.ExitStack() as stack:
        stack.callback(callback, 'arg1', 'arg2')
        stack.callback(callback, arg3='val3')
        raise RuntimeError('thrown error')
except RuntimeError as err:
    print('ERROR: {}'.format(err))
```
因为它们无法访问错误，所以回调无法抑制从上下文管理器堆栈的其余部分传播的异常。
```
$ python contextlib_exitstack_callbacks_error.py

closing callback((), {'arg3': 'val3'})
closing callback(('arg1', 'arg2'), {})
ERROR: thrown error
```
回调可以方便地定义清理逻辑，而不需要创建新的上下文管理器类。为了提高代码的可读性，可以将该逻辑封装在内联函数中，callback()可以用作装饰器。
```
# contextlib_exitstack_callbacks_decorator.py

import contextlib


with contextlib.ExitStack() as stack:

    @stack.callback
    def inline_cleanup():
        print('inline_cleanup()')
        print('local_resource = {!r}'.format(local_resource))

    local_resource = 'resource created in context'
    print('within the context')
```
无法指定使用callback()的装饰器形式注册的函数的参数。但是，如果清理回调是内联定义的，那么范围规则允许它访问调用代码中定义的变量。
```
$ python contextlib_exitstack_callbacks_decorator.py

within the context
inline_cleanup()
local_resource = 'resource created in context'
```
### Partial Stacks
有时，在构建复杂的上下文时，如果上下文不能完全构建，那么能够中止操作是非常有用的，但是，如果它们都能正确设置，则可以延迟对所有资源的清理工作。例如，如果一个操作需要几个长期存在的网络连接，那么最好不要在一个连接失败时启动该操作。但是，如果所有的连接都可以打开，那么它们需要比单个上下文管理器的持续时间更长。这个场景中可以使用ExitStack的pop_all()方法。

pop_all()从调用它的堆栈中清除所有上下文管理器和回调，并返回预填充了相同上下文管理器和回调的新堆栈。新的堆栈的close()方法可以在原始堆栈消失后稍后调用，以清理资源。
```
# contextlib_exitstack_pop_all.py

import contextlib

from contextlib_context_managers import *


def variable_stack(contexts):
    with contextlib.ExitStack() as stack:
        for c in contexts:
            stack.enter_context(c)
        # Return the close() method of a new stack as a clean-up
        # function.
        return stack.pop_all().close
    # Explicitly return None, indicating that the ExitStack could
    # not be initialized cleanly but that cleanup has already
    # occurred.
    return None


print('No errors:')
cleaner = variable_stack([
    HandleError(1),
    HandleError(2),
])
cleaner()

print('\nHandled error building context manager stack:')
try:
    cleaner = variable_stack([
        HandleError(1),
        ErrorOnEnter(2),
    ])
except RuntimeError as err:
    print('caught error {}'.format(err))
else:
    if cleaner is not None:
        cleaner()
    else:
        print('no cleaner returned')

print('\nUnhandled error building context manager stack:')
try:
    cleaner = variable_stack([
        PassError(1),
        ErrorOnEnter(2),
    ])
except RuntimeError as err:
    print('caught error {}'.format(err))
else:
    if cleaner is not None:
        cleaner()
    else:
        print('no cleaner returned')
```
这个示例使用前面定义的相同上下文管理器类，不同之处在于ErrorOnEnter在__enter__()而不是__exit__()上产生错误。在variable_stack()中，如果没有错误地输入所有上下文，则返回一个新的ExitStack的close()方法。如果发生处理错误，variable_stack()返回None，表示清理工作已经完成。如果发生未处理的错误，则清理部分堆栈并传播错误。
```
$ python contextlib_exitstack_pop_all.py

No errors:
  HandleError(1): entering
  HandleError(2): entering
  HandleError(2): exiting False
  HandleError(1): exiting False

Handled error building context manager stack:
  HandleError(1): entering
  ErrorOnEnter(2): throwing error on enter
  HandleError(1): handling exception RuntimeError('from 2',)
  HandleError(1): exiting True
no cleaner returned

Unhandled error building context manager stack:
  PassError(1): entering
  ErrorOnEnter(2): throwing error on enter
  PassError(1): passing exception RuntimeError('from 2',)
  PassError(1): exiting
caught error from 2
```


