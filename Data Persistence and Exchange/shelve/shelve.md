# shelve -- Persistent Storage of Objects
> 目的：shelve模块实现了对任意Python对象的持久性存储，可以使用类似于字典的API对这些对象进行pickle。

当不需要关系数据库时，可以将shelve模块用作Python对象的简单持久存储选项。可以通过键访问shelf，就像使用字典一样。将这些值进行pickle并写入dbm创建和管理的数据库中。
## Creating a new Shelf
使用shelve最简单的方法是通过DbfilenameShelf类。它使用dbm存储数据。可以直接使用该类，或者调用shelve.open()。
```
# shelve_create.py

import shelve

with shelve.open('test_shelf.db') as s:
    s['key1'] = {
        'int': 10,
        'float': 9.5,
        'string': 'Sample data',
    }
```
要再次访问数据，请打开shelf，像使用字典一样使用它。
```
# shelve_existing.py

import shelve

with shelve.open('test_shelf.db') as s:
    existing = s['key1']

print(existing)
```
运行这两个示例脚本将产生以下输出。
```
$ python shelve_create.py
$ python shelve_existing.py

{'int': 10, 'float': 9.5, 'string': 'Sample data'}
```
dbm模块不支持同时向同一数据库写入多个应用程序，但它支持并发只读客户机。如果客户端不修改shelf，通过传递flag='r'告诉shelve以只读方式打开数据库。
```
# shelve_readonly.py

import dbm
import shelve

with shelve.open('test_shelf.db', flag='r') as s:
    print('Existing:', s['key1'])
    try:
        s['key1'] = 'new value'
    except dbm.error as err:
        print('ERROR: {}'.format(err))
```
如果程序试图在数据库以只读方式打开时修改它，则会生成一个访问错误异常。异常类型取决于数据库创建时dbm选择的数据库模块。
```
$ python shelve_readonly.py

Existing: {'int': 10, 'float': 9.5, 'string': 'Sample data'}
ERROR: cannot add item to database
```
## Write-back
默认情况下，shelve不会跟踪对易失性对象的修改。这意味着，如果存储在shelf的内容发生了更改，那么必须通过再次存储整个内容来显式地更新shelf。
```
# shelve_withoutwriteback.py

import shelve

with shelve.open('test_shelf.db') as s:
    print(s['key1'])
    s['key1']['new_value'] = 'this was not here before'

with shelve.open('test_shelf.db', writeback=True) as s:
    print(s['key1'])
```
在本例中，“key1”的字典不会再次存储，所以当重新打开这个书架时，这些更改不会被保存。
```
$ python shelve_create.py
$ python shelve_withoutwriteback.py

{'int': 10, 'float': 9.5, 'string': 'Sample data'}
{'int': 10, 'float': 9.5, 'string': 'Sample data'}
```
要自动捕获存储在shelf中的易失性对象的更改，请打开它并启用回写。回写标记使shelf记住使用内存缓存从数据库检索到的所有对象。当shelf关闭时，每个缓存对象也被写回数据库。
```
# shelve_writeback.py

import shelve
import pprint

with shelve.open('test_shelf.db', writeback=True) as s:
    print('Initial data:')
    pprint.pprint(s['key1'])

    s['key1']['new_value'] = 'this was not here before'
    print('\nModified:')
    pprint.pprint(s['key1'])

with shelve.open('test_shelf.db', writeback=True) as s:
    print('\nPreserved:')
    pprint.pprint(s['key1'])
```
虽然它减少了程序员出错的机会，并且可以使对象持久性更透明，但是使用回写模式可能不是所有情况下都需要的。缓存打开时将消耗额外的内存，关闭时暂停将每个缓存对象写回数据库会减慢应用程序的速度。所有缓存的对象都被写回数据库，因为无法判断它们是否已被修改。如果应用程序读取的数据多于写入的数据，那么回写将不必要地影响性能。
```
$ python shelve_create.py
$ python shelve_writeback.py

Initial data:
{'float': 9.5, 'int': 10, 'string': 'Sample data'}

Modified:
{'float': 9.5,
 'int': 10,
 'new_value': 'this was not here before',
 'string': 'Sample data'}

Preserved:
{'float': 9.5,
 'int': 10,
 'new_value': 'this was not here before',
 'string': 'Sample data'}
```
## Specific Shelf Types
前面的示例都使用了默认的shelf实现。使用shelve.open()而不是直接使用一个shelf实现是一种常见的使用模式，特别是如果使用哪种类型的数据库来存储数据并不重要的话。但是，有时数据库格式很重要。在这些情况下，可以直接使用 DbfilenameShelf或BsdDbShelf，甚至是定制解决方案的子类shelf。


