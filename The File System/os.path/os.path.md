# os.path -- Platform-independent Manipulation of Filenames
> 目的：解析、构建、测试和其他方法处理文件名和路径。

使用包含在os.path模块中的函数来编写在多个平台上使用文件的代码是很容易的。即使不打算在平台之间移植的程序也应该使用os.path来可靠的解析文档名。
## Parsing Paths
os.path中的第一组函数可以用来解析表示文件名的字符串。重要的是要认识到这些函数并不依赖于实际存在的路径;它们只是解析字符串。
路径的解析依赖于一些定义在os中的一些变量：
+ os.sep - 路径之间的分隔符（如“/”或“\”）
+ os.extsep - 文件名和文件“扩展”之间的分隔符（如“.”）
+ os.pardir - 路径组件意味着将目录树向上遍历一个级别（如“..”）
+ os.curdir - 路径组件关联到当前目录（如“.”）

split()函数把路径分割成两部分，并已元祖的形式返回结果。元组的第二个元素是路径的最后一个元素，第一个元素是之前的所有元素。
<pre><code># ospath_split.py
import os.path

PATHS = [
    '/one/two/three',
    '/one/two/three/',
    '/',
    '.',
    '',
]

for path in PATHS:
    print('{!r:>17} : {}'.format(path, os.path.split(path)))
</pre></code>
当路径字符串以os.sep结尾，路径的最后一个元素是空字符串。
<pre><code>$ python ospath_split.py
 '/one/two/three' : ('/one/two', 'three')
'/one/two/three/' : ('/one/two/three', '')
              '/' : ('/', '')
              '.' : ('', '.')
               '' : ('', '')
</pre></code>
basename()函数的作用是:返回一个等价于split()返回值的第二部分的值。
<pre><code># ospath_basename.py

import os.path

PATHS = [
    '/one/two/three',
    '/one/two/three/',
    '/',
    '.',
    '',
]

for path in PATHS:
    print('{!r:>17} : {!r}'.format(path, os.path.basename(path)))
</pre></code>
<pre><code>$ python ospath_basename.py
 '/one/two/three' : 'three'
'/one/two/three/' : ''
              '/' : ''
              '.' : '.'
               '' : ''
</pre></code>
dirname()函数返回split()返回的第一部分元素。
<pre><code># ospath_dirname.py

import os.path

PATHS = [
    '/one/two/three',
    '/one/two/three/',
    '/',
    '.',
    '',
]

for path in PATHS:
    print('{!r:>17} : {!r}'.format(path, os.path.dirname(path)))
</pre></code>
<pre><code>$ python ospath_dirname.py
 '/one/two/three' : '/one/two'
'/one/two/three/' : '/one/two/three'
              '/' : '/'
              '.' : ''
               '' : ''
</pre></code>
splitext()类似于split()，但是它将路径以扩展分隔符分隔开，而不是目录分隔符。
<pre></code># ospath_splitext.py

import os.path

PATHS = [
    'filename.txt',
    'filename',
    '/path/to/filename.txt',
    '/',
    '',
    'my-archive.tar.gz',
    'no-extension',
]

for path in PATHS:
    print('{!r:>21} : {!r}'.format(path, os.path.splitext(path)))
</pre></code>
只有最后出现的os.extsep在查找扩展时使用，因此如果一个文件名有多个扩展，那么将其拆分的结果就会在前缀上留下部分扩展。
<pre><code>$ python ospath_splitext.py
       'filename.txt' : ('filename', '.txt')
           'filename' : ('filename', '')
'/path/to/filename.txt' : ('/path/to/filename', '.txt')
                  '/' : ('/', '')
                   '' : ('', '')
  'my-archive.tar.gz' : ('my-archive.tar', '.gz')
       'no-extension' : ('no-extension', '')
</pre></code>
commonprefix()将路径列表作为参数，并返回表示所有路径中常见前缀的单个字符串。该值可能表示不存在的路径，并且路径分隔符不包含在考虑中，因此前缀可能不会在分隔符边界上停止。
<pre><code># ospath_commonprefix.py

import os.path

paths = [
    '/one/two/three/four',
    '/one/two/threefold',
    '/one/two/three/',
]
for path in paths:
    print('PATH:', path)

print()
print('PREFIX:', os.path.commonprefix(paths))
</pre></code>
在本例中，常见的前缀字符串为'/one/two/three'，即使其中一条路径不包含名为three的目录中。
<pre><code>$ python ospath_commonprefix.py
PATH: /one/two/three/four
PATH: /one/two/threefold
PATH: /one/two/three/

PREFIX: /one/two/three
</pre></code>
commonpath()执行荣誉路径分隔符，并返回一个不包含部分路径值的前缀。
<pre><code># ospath_commonpath.py

import os.path

paths = [
    '/one/two/three/four',
    '/one/two/threefold',
    '/one/two/three/',
]
for path in paths:
    print('PATH:', path)

print()
print('PREFIX:', os.path.commonpath(paths))
</pre></code>
<pre><code>$ python ospath_commonpath.py
PATH: /one/two/three/four
PATH: /one/two/threefold
PATH: /one/two/three/

PREFIX: \one\two
</pre></code>
## Building Paths
除了将现有路径分开之外，通常还需要从其他字符串构建路径。要将多个路径组件组合为一个值，请使用join():
<pre><code># ospath_join.py

import os.path

PATHS = [
    ('one', 'two', 'three'),
    ('/', 'one', 'two', 'three'),
    ('/one', '/two', '/three'),
]

for parts in PATHS:
    print('{} : {!r}'.format(parts, os.path.join(*parts)))
</pre></code>
如果join的任何参数以os.sep开头，则先前的参数都被丢弃，从该参数开始join之后的参数。
<pre><code>$ python ospath_join.py
# windows
('one', 'two', 'three') : 'one\\two\\three'
('/', 'one', 'two', 'three') : '/one\\two\\three'
('/one', '/two', '/three') : '/three'

# linux
('one', 'two', 'three') : 'one/two/three'
('/', 'one', 'two', 'three') : '/one/two/three'
('/one', '/two', '/three') : '/three'
</pre></code>
还可以使用包含可自动扩展的“变量”组件的路径。例如，expanduser()将tilde(~)字符转换为用户主目录的名称。
<pre><code># ospath_expanduser.py

import os.path

for user in ['', 'dhellmann', 'nosuchuser']:
    lookup = '~' + user
    print('{!r:>15} : {!r}'.format(lookup, os.path.expanduser(lookup)))
</pre></code>
如果无法找到用户的主目录，则返回的字符串不变。
<pre><code>$ python ospath_expanduser.py
# windows
            '~' : 'C:\\Users\\coder'
   '~dhellmann' : 'C:\\Users\\dhellmann'
  '~nosuchuser' : 'C:\\Users\\nosuchuser'

# linux root用户
            '~' : '/root'
   '~dhellmann' : '~dhellmann'
  '~nosuchuser' : '~nosuchuser'
</pre></code>
expandvars()更一般化，并扩展路径中存在的任何shell环境变量。
<pre><code># ospath_expandvars.py

import os.path
import os

os.environ['MYVAR'] = 'VALUE'

print(os.path.expandvars('/path/to/$MYVAR'))
</pre></code>
expandvars()确保变量值会导致已经存在的文件的名称。
<pre><code>$ python ospath_expandvars.py
/path/to/VALUE
</pre></code>
## Normalizing Paths
使用join()或嵌入变量的独立字符串组合的路径可能会以额外的分隔符或相对路径组件结束。使用normpath()来清除它们:
<pre><code># ospath_normpath.py

import os.path

PATHS = [
    'one//two//three',
    'one/./two/./three',
    'one/../alt/two/three',
]

for path in PATHS:
    print('{!r:>22} : {!r}'.format(path, os.path.normpath(path)))
</pre></code>
<pre><code>$ python ospath_normpath.py
# windows
     'one//two//three' : 'one\\two\\three'
   'one/./two/./three' : 'one\\two\\three'
'one/../alt/two/three' : 'alt\\two\\three'

# linux
     'one//two//three' : 'one/two/three'
   'one/./two/./three' : 'one/two/three'
'one/../alt/two/three' : 'alt/two/three'
</pre></code>
要将相对路径转换为绝对文件名，请使用abspath()。
<pre><code># ospath_abspath.py

import os
import os.path

os.chdir('/usr')

PATHS = [
    '.',
    '..',
    './one/two/three',
    '../one/two/three'
]

for path in PATHS:
    print('{!r:>21} : {!r}'.format(path, os.path.abspath(path)))
</pre></code>
<pre><code>$ python ospath_abspath.py
# linux
                  '.' : '/usr'
                 '..' : '/'
    './one/two/three' : '/usr/one/two/three'
   '../one/two/three' : '/one/two/three'
</pre></code>
## File Times
除了操作路径，os.path包含用于检索文件属性的函数，类似于os.stat()所返回的函数。
<pre><code># ospath_properties.py

import os.path
import time

print('File         :', __file__)
print('Access time  :', time.ctime(os.path.getatime(__file__)))
print('Modified time:', time.ctime(os.path.getmtime(__file__)))
print('Change time  :', time.ctime(os.path.getctime(__file__)))
print('Size         :', os.path.getsize(__file__))
</pre></code>
getatime()返回访问时间，os.path.getmtime()返回修改时间，而os.path.getctime()返回创建时间。getsize()返回文件中的数据量，以字节表示。
<pre><code>$ python ospath_properties.py
File         : d:/python3_module_of_the_week_zh/The File System/os.path/ospath_properties.py
Access time  : Mon May 28 17:00:18 2018
Modified time: Mon May 28 17:00:14 2018
Change time  : Mon May 28 16:57:10 2018
Size         : 339
</pre></code>
## Testing Files
当一个程序遇到路径名时，它通常需要知道路径是否指向一个文件、目录或符号链接，以及它是否存在。os.path包含用于测试所有这些条件的函数。
<pre><code># ospath_tests.py

import os.path

FILENAMES = [
    __file__,
    os.path.dirname(__file__),
    '/',
    './broken_link',
]

for file in FILENAMES:
    print('File        : {!r}'.format(file))
    print('Absolute    :', os.path.isabs(file))
    print('Is File?    :', os.path.isfile(file))
    print('Is Dir?     :', os.path.isdir(file))
    print('Is Link?    :', os.path.islink(file))
    print('Mountpoint? :', os.path.ismount(file))
    print('Exists?     :', os.path.exists(file))
    print('Link Exists?:', os.path.lexists(file))
    print()
</pre></code>
所有函数返回布尔值
<pre><code>$ python ospath_tests.py
# windows
File        : 'd:/python3_module_of_the_week_zh/The File System/os.path/ospath_tests.py'
Absolute    : True
Is File?    : True
Is Dir?     : False
Is Link?    : False
Mountpoint? : False
Exists?     : True
Link Exists?: True

File        : 'd:/python3_module_of_the_week_zh/The File System/os.path'
Absolute    : True
Is File?    : False
Is Dir?     : True
Is Link?    : False
Mountpoint? : False
Exists?     : True
Link Exists?: True

File        : '/'
Absolute    : True
Is File?    : False
Is Dir?     : True
Is Link?    : False
Mountpoint? : True
Exists?     : True
Link Exists?: True

File        : './broken_link'
Absolute    : False
Is File?    : False
Is Dir?     : False
Is Link?    : False
Mountpoint? : False
Exists?     : False
Link Exists?: False

# linux
File        : 'ospath_tests.py'
Absolute    : False
Is File?    : True
Is Dir?     : False
Is Link?    : False
Mountpoint? : False
Exists?     : True
Link Exists?: True

File        : ''
Absolute    : False
Is File?    : False
Is Dir?     : False
Is Link?    : False
Mountpoint? : False
Exists?     : False
Link Exists?: False

File        : '/'
Absolute    : True
Is File?    : False
Is Dir?     : True
Is Link?    : False
Mountpoint? : True
Exists?     : True
Link Exists?: True

File        : './broken_link'
Absolute    : False
Is File?    : False
Is Dir?     : False
Is Link?    : False
Mountpoint? : False
Exists?     : False
Link Exists?: False
</pre></code>

