# linecache -- Read Text Files Efficiently
> 目的：从文件或导入的Python模块中检索文本行，保存结果的缓存，使从同一文件中读取许多行更有效。

在处理Python源文件时，linecache模块在Python标准库的其他部分中使用。缓存的实现在内存中保存文件的内容，并将其解析为单独的行。API通过将所请求的行索引到列表中来返回，并通过反复读取文件和解析行来查找所需的行来节省时间。这在查找来自同一文件的多行代码时特别有用，例如在生成错误报告的回溯时。
## Test Data
本文用一个Lorem Ipsum生成器生成的文本作为样本输入。
<pre><code># linecache_data.py

import os
import tempfile

lorem = '''Lorem ipsum dolor sit amet, consectetuer
adipiscing elit.  Vivamus eget elit. In posuere mi non
risus. Mauris id quam posuere lectus sollicitudin
varius. Praesent at mi. Nunc eu velit. Sed augue massa,
fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur
eros pede, egestas at, ultricies ac, apellentesque eu,
tellus.

Sed sed odio sed mi luctus mollis. Integer et nulla ac augue
convallis accumsan. Ut felis. Donec lectus sapien, elementum
nec, condimentum ac, interdum non, tellus. Aenean viverra,
mauris vehicula semper porttitor, ipsum odio consectetuer
lorem, ac imperdiet eros odio a sapien. Nulla mauris tellus,
aliquam non, egestas a, nonummy et, erat. Vivamus sagittis
porttitor eros.'''


def make_tempfile():
    fd, temp_file_name = tempfile.mkstemp()
    os.close(fd)
    with open(temp_file_name, 'wt') as f:
        f.write(lorem)
    return temp_file_name


def cleanup(filename):
    os.unlink(filename)
</pre></code>
## Reading Specific Lines
linecache模块读取的文件的行号以1开头，但是通常列出从0开始索引数组的行号。
<pre><code># linecache_getline.py

import linecache
from linecache_data import lorem, make_tempfile, cleanup

filename = make_tempfile()

print('SOURCE:')
print('{!r}'.format(lorem.split('\n')[4]))
print()
print('CACHE:')
print('{!r}'.format(linecache.getline(filename, 5)))

cleanup(filename)
</pre></code>
返回的每一行都包含一个尾换行。
<pre><code>$ python linecache_getline.py
SOURCE:
'fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur'

CACHE:
'fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur\n'
</pre></code>
## Handling Blank Lines
返回值总是包含行尾的换行符，所以如果行是空的，返回值就是换行符。
<pre><code># linecache_empty_line.py
import linecache
from linecache_data import make_tempfile, cleanup

filename = make_tempfile()

print('BLANK : {!r}'.format(linecache.getline(filename, 8)))

cleanup(filename)
</pre></code>
输入文件的第8行不包含文本。
<pre><code>$ python linecache_empty_line.py
BLANK : '\n'
</pre></code>
## Error Handling
如果请求的行号超出文件中有效行的范围，getline()将返回一个空字符串。
<pre><code># linecache_out_of_range.py

import linecache
from linecache_data import make_tempfile, cleanup

filename = make_tempfile()

not_there = linecache.getline(filename, 500)
print('NOT THERE: {!r} include {} characters'.format(not_there, len(not_there)))

cleanup(filename)
</pre></code>
输入文件只有15行，所以请求第500行就超出文本范围。
<pre><code>$ python linecache_out_of_range.py
NOT THERE: '' include 0 characters
</pre></code>
从不存在的文件中读取数据的处理方式和上面是相同的。
<pre><code># linecache_missing_file.py

import linecache

no_such_file = linecache.getline('this_file_does_not_exist.txt', 1)

print('NO FILE: {!r}'.format(no_such_file))
</pre></code>
当调用者试图读取数据时，模块不会引发异常。
<pre><code>$ python linecache_missing_file.py
NO FILE: ''
</pre></code>
## Reading Python Source Files
由于linecache在生成回溯时大量使用，所以它的一个关键特性是能够通过指定模块的基本名称在导入路径中找到Python源模块。
<pre><code># linecache_path_search.py

import linecache
import os

module_line = linecache.getline('linecache.py', 3)
print('MODULE:')
print(repr(module_line))

file_src = linecache.__file__
if file_src.endswith('.pyc'):
    file_src = file_src[:-1]
print('\nFILE:')
with open(file_src, 'r') as f:
    file_line = f.readlines()[2]
print(repr(file_line))
</pre></code>
如果在当前目录中找不到具有该名称的文件，linecache在sys.path中的搜索命名模块。命名模块的路径，。本例查找linecache.py。由于当前目录中没有副本，因此只能找到来自标准库的文件。
<pre><code>$ python linecache_path_search.py
MODULE:
'This is intended to read lines from modules imported -- hence if a filename\n'

FILE:
'This is intended to read lines from modules imported -- hence if a filename\n'
</pre></code>
