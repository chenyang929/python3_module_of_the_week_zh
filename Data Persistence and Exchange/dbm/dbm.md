# dbm -- Unix Key-Value Databases
> 目的：dbm为dbm风格的字符串键控数据库提供了类似于字典的通用接口

dbm是dbm样式的数据库的前端，这些数据库使用简单的字符串值作为键来访问包含字符串的记录。它使用whichdb()来标识数据库，然后使用适当的模块打开它们。它被用作shelve的后端，它使用pickle存储DBM数据库中的对象。
## Database Types
Python附带了几个用于访问dbm风格的数据库的模块。所选择的默认实现取决于当前系统上可用的库和Python编译时使用的选项。与特定实现的单独接口允许Python程序与其他语言的程序交换数据，这些程序不自动地在可用格式之间切换，或者编写可移植的数据文件，这些文件将在多个平台上工作。
### dbm.gnu
dbm.gnu是一个从gnu项目到dbm库版本的接口。它的工作方式与本文描述的其他DBM实现相同，只是对open()支持的标志做了一些更改。

除了标准的“r”、“w”、“c”和“n”标志外，dbm.gnu.open()支持:

+ 'f'以快速模式打开数据库。在快速模式下，对数据库的写入是不同步的。
+ “s”以同步模式打开数据库。数据库的更改被写入到文件中，而不是被延迟到数据库关闭或显式地同步。
+ “u”打开数据库解锁。

### dbm.ndbm
dbm.ndbm模块为dbm格式的Unix ndbm实现提供了一个接口，具体取决于在编译期间如何配置该模块。模块属性库标识在编译扩展模块时配置的库的名称。
### dbm.dumb
dbm.dumb是DBM API在没有其他实现时的可移植回退实现。使用dbm不需要外部依赖，但是它比大多数其他实现都要慢。
## Creating a New Database
通过依次查找每个子模块的可用版本，选择新数据库的存储格式。
+ dbm.gnu
+ dbm.ndbm
+ dbm.dumb

open()函数使用标志来控制如何管理数据库文件。如需创建新数据库，请使用“c”。使用“n”总是创建一个新的数据库，覆盖现有的文件。
```
# dbm_new.py

import dbm

with dbm.open('example.db', 'n') as db:
    db['key'] = 'value'
    db['today'] = 'Sunday'
    db['author'] = 'Doug'
```
在本例中，文件总是被重新初始化。
```
$ python dbm_new.py
```
whichdb()报告所创建的数据库的类型。
```
# dbm_whichdb.py

import dbm

print(dbm.whichdb('example.db'))
```
示例程序的输出将根据系统上安装的模块而有所不同。
```
$ python dbm_whichdb.py

dbm.ndbm
```
## Opening an Existing Database
要打开现有数据库，可以使用“r”(只读)或“w”(用于读写)的标志。现有的数据库会自动地交给whichdb()来标识，因此只要可以标识文件，就会使用适当的模块来打开它。
```
# dbm_existing.py

import dbm

with dbm.open('example.db', 'r') as db:
    print('keys():', db.keys())
    for k in db.keys():
        print('iterating:', k, db[k])
    print('db["author"] =', db['author'])
```
一旦打开，db就是一个类字典的对象。当添加到数据库时，新键总是被转换为字节字符串，并作为字节字符串返回。
```
$ python dbm_existing.py

keys(): [b'key', b'today', b'author']
iterating: b'key' b'value'
iterating: b'today' b'Sunday'
iterating: b'author' b'Doug'
db["author"] = b'Doug'
```
## Error Cases
数据库的键必须是字符串。
```
# dbm_intkeys.py

import dbm

with dbm.open('example.db', 'w') as db:
    try:
        db[1] = 'one'
    except TypeError as err:
        print(err)
```
传递另一个类型会导致类型错误。
```
$ python dbm_intkeys.py

keys must be bytes or strings
```
值必须是字符串或None
```
# dbm_intvalue.py

import dbm

with dbm.open('example.db', 'w') as db:
    try:
        db['one'] = 1
    except TypeError as err:
        print(err)
```
如果值不是字符串，则会引发类似的类型错误。
```

values must be bytes or strings
```
