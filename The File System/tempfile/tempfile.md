# tempfile -- Temporary File System Objects
> 目的：创建临时文件系统对象。

安全地创建具有惟一名称的临时文件，这样就不会被希望破坏应用程序或窃取数据的人猜到。tempfile模块为安全地创建临时文件系统资源提供了几个函数。TemporaryFile()打开并返回一个未命名文件，NamedTemporaryFile()打开并返回一个命名文件，SpooledTemporaryFile在写入磁盘之前将其内容保存在内存中，而TemporaryDirectory是一个上下文管理器，在上下文关闭时删除该目录。
## Temporary Files
需要临时文件来存储数据而不需要与其他程序共享该文件的应用程序应该使用TemporaryFile()函数来创建文件。该函数创建一个文件，在可能的平台上，立即断开它。这使得另一个程序无法找到或打开文件，因为在文件系统表中没有对它的引用。TemporaryFile()创建的文件在关闭时自动删除，可以调用close()或使用上下文管理器API和with语句。
<pre><code># tempfile_TemporaryFile.py

import os
import tempfile

print('Building a filename with PID:')
filename = '{}.txt'.format(os.getpid())
with open(filename, 'w+b') as temp:
    print('temp:')
    print('  {!r}'.format(temp))
    print('temp.name:')
    print('  {!r}'.format(temp.name))

# Clean up the temporary file yourself.
os.remove(filename)

print()
print('TemporaryFile:')
with tempfile.TemporaryFile() as temp:
    print('temp:')
    print('  {!r}'.format(temp))
    print('temp.name:')
    print('  {!r}'.format(temp.name))

# Automatically cleans up the file.
</pre></code>
这个示例演示了使用创建名称的通用模式创建临时文件与使用TemporaryFile()函数的区别。TemporaryFile()返回的文件没有名称。
<pre><code>$ python tempfile_TemporaryFile.py
Building a filename with PID:
temp:
  <_io.BufferedRandom name='3320.txt'>
temp.name:
  '3320.txt'

TemporaryFile:
temp:
  <tempfile._TemporaryFileWrapper object at 0x0000017C77921D68>
temp.name:
  'C:\\Users\\coder\\AppData\\Local\\Temp\\tmpqpany_1m'
</pre></code>
默认情况下，文件句柄是用“w+b”模式创建的，所以它在所有平台上都是一致的，调用者可以编写并从中读取。
<pre><code># tempfile_TemporaryFile_binary.py

import os
import tempfile

with tempfile.TemporaryFile() as temp:
    temp.write(b'Some data')

    temp.seek(0)
    print(temp.read())
</pre></code>
写入之后，必须使用seek()对文件句柄进行重新定位，以便从它读取数据。
<pre><code>$ python tempfile_TemporaryFile_binary.py
b'Some data'
</pre></code>
要在文本模式下打开文件，请在创建文件时将模式设置为“w+t”。
<pre><code># tempfile_TemporaryFile_text.py

import tempfile

with tempfile.TemporaryFile(mode='w+t') as f:
    f.writelines(['first\n', 'second\n'])

    f.seek(0)
    for line in f:
        print(line.rstrip())
</pre></code>
文件句柄将数据视为文本。
<pre><code>$ python tempfile_TemporaryFile_text.py
first
second
</pre></code>
## Named Files
有些情况下，有一个命名的临时文件很重要。对于跨越多个进程甚至主机的应用程序，命名文件是在应用程序的各个部分之间传递文件的最简单方式。NamedTemporaryFile()函数创建一个文件而不断开它的链接，因此它保留其名称(使用name属性访问)
<pre><code># tempfile_NamedTemporaryFile.py

import os
import pathlib
import tempfile

with tempfile.NamedTemporaryFile() as temp:
    print('temp:')
    print(' {!r}'.format(temp))
    print('temp.name:')
    print(' {!r}'.format(temp.name))

    f = pathlib.Path(temp.name)

print('Exists after close:', f.exists())
</pre></code>
句柄关闭文件就删除了。
<pre><code>$ python tempfile_NamedTemporaryFile.py
temp:
 <tempfile._TemporaryFileWrapper object at 0x000001A38E211CF8>
temp.name:
 'C:\\Users\\coder\\AppData\\Local\\Temp\\tmpot0vwedg'
Exists after close: False
</pre></code>
## Spooled Files
对于包含相对较少数据的临时文件，使用SpooledTemporaryFile可能更有效，因为它使用io.BytesIO或io.StringIO缓冲将文件内容保存在内存中直到它们达到阈值大小。当数据量超过阈值时，它将被“滚动”并写入磁盘，然后用一个普通的TemporaryFile()替换缓冲区。
<pre><code># tempfile_SpooledTemporaryFile.py

import tempfile

with tempfile.SpooledTemporaryFile(max_size=100, mode='w+t', encoding='utf-8') as temp:
    print('temp: {!r}'.format(temp))

    for i in range(3):
        temp.write('This line is repeated over and over.\n')
        print(temp._rolled, temp._file)
</pre></code>
本例使用SpooledTemporaryFile的私有属性来确定何时发生磁盘翻转。通常不需要检查这个状态，除非在调整缓冲区大小时。
<pre><code>$ python tempfile_SpooledTemporaryFile.py
temp: <tempfile.SpooledTemporaryFile object at 0x0000020F6C8D1128>
False <_io.StringIO object at 0x0000020F6C8363A8>
False <_io.StringIO object at 0x0000020F6C8363A8>
True <tempfile._TemporaryFileWrapper object at 0x0000020F6C8D1390>
</pre></code>
要显式地将缓冲区写入磁盘，请调用rollover()或fileno()方法。
<pre><code># tempfile_SpooledTemporaryFile_explicit.py

import tempfile

with tempfile.SpooledTemporaryFile(max_size=1000, mode='w+t', encoding='utf-8') as temp:
    print('temp: {!r}'.format(temp))

    for i in range(3):
        temp.write('This line is repeated over and over.\n')
        print(temp._rolled, temp._file)
    print('rolling over')
    temp.rollover()
    print(temp._rolled, temp._file)
</pre></code>
在本例中，由于缓冲区大小比数据量大得多，因此不会在磁盘上创建文件，除非调用rollover()。
<pre><code>$ python tempfile_SpooledTemporaryFile_explicit.py
temp: <tempfile.SpooledTemporaryFile object at 0x0000021524B41128>
False <_io.StringIO object at 0x0000021522FA1288>
False <_io.StringIO object at 0x0000021522FA1288>
False <_io.StringIO object at 0x0000021522FA1288>
rolling over
True <tempfile._TemporaryFileWrapper object at 0x0000021524B41390>
</pre></code>
## Temporary Directories
当需要几个临时文件时，可以更方便地使用TemporaryDirectory创建一个临时目录，并打开该目录中的所有文件。
<pre><code># tempfile_TemporaryDirectory.py

import pathlib
import tempfile

with tempfile.TemporaryDirectory() as directory_name:
    the_dir = pathlib.Path(directory_name)
    print(the_dir)
    a_file = the_dir / 'a_file.txt'
    a_file.write_text('This file is deleted.')

print('Directory exists after?', the_dir.exists())
print('Contents after:', list(the_dir.glob('*')))
</pre></code>
上下文管理器生成目录的名称，然后可以在上下文块中使用该名称来构建其他文件名。
<pre><code>$ python tempfile_TemporaryDirectory.py
C:\Users\coder\AppData\Local\Temp\tmpk12h2ojw
Directory exists after? False
Contents after: []
</pre></code>
## Predicting Names
虽然与严格匿名的临时文件(包括名称中可预测的部分)相比不那么安全，但为了调试目的，可以找到该文件并对其进行检查。到目前为止描述的所有函数都使用三个参数在一定程度上控制文件名。使用公式生成名称:
```
dir + prefix + random + suffix
```
除了random之外的所有值都可以作为参数传递给用于创建临时文件或目录的函数。
<pre><code># tempfile_NamedTemporaryFile_args.py

import tempfile

with tempfile.NamedTemporaryFile(suffix='_suffix', prefix='prefix_', dir='') as temp:
    print('temp:')
    print(' ', temp)
    print('temp.name:')
    print(' ', temp.name)
</pre></code>
前缀和后缀参数与构建文件名的随机字符串相结合，并且使用dir参数作为新文件的位置。
<pre><code>$ python tempfile_NamedTemporaryFile_args.py
temp:
  <tempfile._TemporaryFileWrapper object at 0x0000022308731128>
temp.name:
  D:\python3_module_of_the_week_zh\The File System\tempfile\prefix_tvtzclb7_suffix
</pre></code>
## Temporary File Location
如果没有使用dir参数指定一个明确的目的地，那么临时文件所使用的路径将根据当前的平台和设置而变化。tempfile模块包含两个函数，用于查询运行时使用的设置。
<pre><code># tempfile_settings.py

import tempfile

print('gettempdir():', tempfile.gettempdir())
print('gettempprefix():', tempfile.gettempprefix())
</pre></code>
gettempdir()返回包含所有临时文件的默认目录，而gettempprefix()返回用于新文件和目录名的字符串前缀。
<pre><code>$ python tempfile_settings.py
gettempdir(): C:\Users\coder\AppData\Local\Temp
gettempprefix(): tmp
</pre></code>
gettempdir()返回的值是基于一种简单的算法来设置的，该算法查看当前进程可以创建文件的位置列表。搜索列表:
+ 1、环境变量TMPDIR
+ 2、环境变量临时
+ 3、环境变量TMP
+ 4、基于平台的退路。(Windows使用第一个可用的C:\temp, C:\tmp， \temp，或\tmp。其他平台使用/tmp、/var/tmp或/usr/tmp。
+ 5、如果找不到其他目录，则使用当前工作目录。
<pre><code># tempfile_tempdir.py

import tempfile

tempfile.tempdir = 'D:\Temp'
print('gettempdir():', tempfile.gettempdir())
</pre></code>
需要为所有临时文件使用全局位置而不使用这些环境变量的程序应该设置tempfile。通过为变量赋值，直接使用tempdir。
<pre><code>$ python tempfile_tempdir.py
gettempdir(): D:\Temp
</pre></code>

