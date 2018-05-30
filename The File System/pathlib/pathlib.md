# pathlib -- Filesystem Paths as Objects
> 目的：使用面向对象的API(而不是低级字符串操作)来解析、构建、测试和处理文件名和路径。

## Path Representations
pathlib包括使用POSIX标准或Microsoft Windows语法管理格式化的文件系统路径的类。它包括所谓的“纯”类，它们在字符串上操作，但不与实际的文件系统交互，并且“具体”类，它扩展了API，以包括反映或修改本地文件系统上的数据的操作。

纯类PurePosixPath和PureWindowsPath可以在任何操作系统上实例化和使用，因为它们只处理名称。要实例化使用真实文件系统的正确类，可以使用路径获得PosixPath或WindowsPath，这取决于平台。
## Building Paths
要实例化一条新路径，请将字符串作为第一个参数。路径对象的字符串表示是这个名称值。要创建指向与现有路径相关的值的新路径，请使用/操作符来扩展路径。操作符的参数可以是字符串或其他路径对象。
<pre><code># pathlib_operator.py

import pathlib

usr = pathlib.PurePosixPath('/usr')
print(usr)

usr_local = usr / 'local'
print(usr_local)

usr_share = usr / pathlib.PurePosixPath('share')
print(usr_share)

root = usr / '..'
print(root)

etc = root / '/etc/'
print(etc)
</pre></code>
在示例输出显示的root值中，操作符将路径值与给定的值相结合，并且在包含父目录引用“..”时不会使结果规范化。但是，如果一个段以路径分隔符开始，它被解释为一个新的“根”引用，就像os.path.join()一样。额外的路径分隔符从路径值的中间移除，就像这里的例子一样。
<pre><code>$ python pathlib_operator.py
/usr
/usr/local
/usr/share
/usr/..
/etc
</pre></code>
具体的路径类包括一个resolve()方法，它通过查看目录和符号链接的文件系统，并生成一个名称所引用的绝对路径来实现路径的规范化。
<pre><code># pathlib_resolve.py

import pathlib

usr_local = pathlib.Path('/usr/local')
share = usr_local / '..' / 'share'
print(share)
print(share.resolve())
</pre></code>
在这里，相对路径被转换为/usr/share的绝对路径。如果输入路径包含符号链接，那么这些符号也会被扩展，从而允许解析路径直接指向目标。
<pre><code>$ python pathlib_resolve.py
# windows
\usr\local\..\share
D:\usr\share

# linux
/usr/local/../share
/usr/share
</pre></code>
要在未预先知道片段的情况下构建路径，请使用joinpath()，将每个路径段作为单独的参数传递。
<pre><code># pathlib_joinpath.py

import pathlib

root = pathlib.PurePosixPath('/')
subdirs = ['usr', 'local']
usr_local = root.joinpath(*subdirs)
print(usr_local)
</pre></code>
与/操作符一样，调用joinpath()创建一个新实例。
<pre><code>$ python pathlib_joinpath.py
/usr/local
</pre></code>
给定一个现有的路径对象，很容易构建一个具有较小差异的新对象，例如在同一个目录中引用不同的文件。使用with_name()创建一个新路径，该路径用不同的文件名替换路径的名称部分。使用with_suffix()创建一个新路径，该路径以不同的值替换文件名称的扩展名。
<pre><code># pathlib_from_existing.py

import pathlib

ind = pathlib.PurePosixPath('source/pathlib/index.rst')
print(ind)

py = ind.with_name('pathlib_from_existing.py')
print(py)

pyc = py.with_suffix('.pyc')
print(pyc)
</pre></code>
这两种方法都返回新的对象，而原始的则保持不变。
<pre><code>$ python pathlib_from_existing.py
source/pathlib/index.rst
source/pathlib/pathlib_from_existing.py
source/pathlib/pathlib_from_existing.pyc
</pre></code>
## Parsing Paths
Path对象具有从名称中提取部分值的方法和属性。例如，部件属性生成基于路径分隔符值的路径段序列。
<pre><code># pathlib_parts.py

import pathlib

p = pathlib.PurePosixPath('/usr/local')
print(p.parts)
</pre></code>
序列是一个元组，反映了路径实例的不可变性。
<pre><code>$ python pathlib_parts.py
('/', 'usr', 'local')
</pre></code>
有两种方法可以从给定的路径对象中向上导航文件系统层次结构。父属性指向包含路径的目录的新路径实例，该路径的值由os.path.dirname()返回。父母属性是一个可迭代的，它生成父目录引用，不断地“向上”的路径层次结构直到到达根。
<pre><code># pathlib_parents.py

import pathlib

p = pathlib.PurePosixPath('/usr/local/lib')

print('parent: {}'.format(p.parent))

print('\nhierarchy:')
for up in p.parents:
    print(up)
</pre></code>
该示例遍历双亲属性并打印成员值。
<pre><code>$ python pathlib_parents.py
parent: /usr/local

hierarchy:
/usr/local
/usr
/
</pre></code>
路径的其他部分可以通过path对象的属性访问。name属性保存路径的最后一部分，在最后的路径分隔符之后(与os.path.basename()相同的值)。后缀属性保存了扩展分隔符之后的值，而阀杆属性在后缀之前保留了名称的部分。
<pre><code># pathlib_name.py

import pathlib

p = pathlib.PurePosixPath('./source/pathlib/pathlib_name.py')
print('path  : {}'.format(p))
print('name  : {}'.format(p.name))
print('suffix: {}'.format(p.suffix))
print('stem  : {}'.format(p.stem))
</pre></code>
虽然后缀和stem值类似于os.path.splitext()所产生的值，但是这些值只基于名称的值，而不是完整的路径。
<pre><code>$ python pathlib_name.py
path  : source/pathlib/pathlib_name.py
name  : pathlib_name.py
suffix: .py
stem  : pathlib_name
</pre></code>
## Creating Concrete Paths
具体路径类的实例可以用字符串参数创建，引用文件系统中的文件、目录或符号链接的名称(或潜在名称)。这个类还提供了几种方便的方法来构建实例，这些方法使用通常使用的位置进行更改，比如当前工作目录和用户的主目录。
<pre><code># pathlib_convenience.py

import pathlib

home = pathlib.Path.home()
print('home:', home)

cwd = pathlib.Path.cwd()
print('cwd :', cwd)
</pre></code>
这两种方法都创建了具有绝对文件系统引用的路径实例。
<pre><code>$ python pathlib_convenience.py
# windows
home: C:\Users\coder
cwd : D:\python3_module_of_the_week_zh\The File System\pathlib

# linux(root用户)
home: /root
cwd : /data/crawler_system/projects/di
</pre></code>
## Directory Contents
有三种方法可以访问目录清单，以发现文件系统上可用的文件的名称。iterdir()是一个生成器，它为包含目录中的每个项目提供一个新的路径实例。
<pre><code># pathlib_iterdir.py

import pathlib

p = pathlib.Path('.')

for f in p.iterdir():
    print(f)
</pre></code>
如果路径没有关联一个目录，iterdir()会引发NotADirectoryError。
<pre><code>$ python pathlib_iterdir.py
pathlib.md
pathlib_convenience.py
pathlib_from_existing.py
pathlib_iterdir.py
pathlib_joinpath.py
pathlib_name.py
pathlib_operator.py
pathlib_parents.py
pathlib_parts.py
pathlib_resolve.py
</pre></code>
使用glob()查找与模式匹配的文件。
<pre><code># pathlib_glob.py

import pathlib

p = pathlib.Path('.')

for f in p.glob('*.md'):
    print(f)
</pre></code>
<pre><code>$ python pathlib_glob.py
pathlib.md
</pre></code>
glob支持使用模式前缀**或调用rglob()而不是glob()来进行递归扫描。
<pre><code># pathlib_rglob.py

import pathlib

p = pathlib.Path('..')
for f in p.rglob('pathlib_*.py'):
    print(f)
</pre></code>
因为这个示例是从父目录开始的，因此需要进行递归搜索，以找到匹配pathlib_*.py的示例文件。
<pre><code>$ python pathlib_rglob.py
..\pathlib\pathlib_convenience.py
..\pathlib\pathlib_from_existing.py
..\pathlib\pathlib_glob.py
..\pathlib\pathlib_iterdir.py
..\pathlib\pathlib_joinpath.py
..\pathlib\pathlib_name.py
..\pathlib\pathlib_operator.py
..\pathlib\pathlib_parents.py
..\pathlib\pathlib_parts.py
..\pathlib\pathlib_resolve.py
..\pathlib\pathlib_rglob.py
</pre></code>
## Reading and Writing Files
每个路径实例都包含用于处理其引用的文件内容的方法。为了立即检索内容，请使用read_bytes()或read_text()。要写入文件，请使用write_bytes()或write_text()。使用open()方法打开文件并保留文件句柄，而不是将名称传递给内置的open()函数。
<pre><code># pathlib_read_write.py

import pathlib

f = pathlib.Path('example.txt')

f.write_bytes('This is the content'.encode('utf-8'))

with f.open('r', encoding='utf-8') as handle:
    print('read from open(): {!r}'.format(handle.read()))

print('read_text(): {!r}'.format(f.read_text('utf-8')))
</pre></code>
便利方法在打开文件和写入文件之前进行一些类型检查，但是它们与直接执行操作是等价的。
<pre><code>$ python pathlib_read_write.py
read from open(): 'This is the content'
read_text(): 'This is the content'
</pre></code>
## Manipulating Directories and Symbolic Links
表示不存在的目录或符号链接的路径可以用来创建关联的文件系统条目。
<pre><code># pathlib_mkdir.py
import pathlib

p = pathlib.Path('example_dir')

print('Creating {}'.format(p))
p.mkdir()
</pre></code>
如果目录已存在，mkdir()抛出FileExistsError异常。
<pre><code>$ python pathlib_mkdir.py
Creating example_dir
</pre></code>
使用symlink_to()创建一个符号链接。该链接将根据路径的值命名，并将引用作为参数给symlink_to()。
<pre><code># pathlib_symlink_to.py

import pathlib

p = pathlib.Path('example_link')
p.symlink_to('index.rst')

print(p)
print(p.resolve().name)
</pre></code>
此示例创建一个符号链接，然后使用resolve()来读取链接，以找到它指向的内容并打印名称。
<pre><code>$ python pathlib_symlink_to.py
example_link
index.rst
</pre></code>
## File Types
路径实例包括几种用于测试路径引用的文件类型的方法。这个示例创建了几个不同类型的文件，并测试了这些文件以及本地操作系统上其他一些特定于设备的文件。
<pre><code># pathlib_types.py

import itertools
import os
import pathlib

root = pathlib.Path('test_files')

# Clean up from previous runs.
if root.exists():
    for f in root.iterdir():
        f.unlink()
else:
    root.mkdir()

# Create test files
(root / 'file').write_text(
    'This is a regular file', encoding='utf-8')
(root / 'symlink').symlink_to('file')
os.mkfifo(str(root / 'fifo'))

# Check the file types
to_scan = itertools.chain(
    root.iterdir(),
    [pathlib.Path('/dev/disk0'),
     pathlib.Path('/dev/console')],
)
hfmt = '{:18s}' + ('  {:>5}' * 6)
print(hfmt.format('Name', 'File', 'Dir', 'Link', 'FIFO', 'Block',
                  'Character'))
print()

fmt = '{:20s}  ' + ('{!r:>5}  ' * 6)
for f in to_scan:
    print(fmt.format(
        str(f),
        f.is_file(),
        f.is_dir(),
        f.is_symlink(),
        f.is_fifo(),
        f.is_block_device(),
        f.is_char_device(),
    ))
</pre></code>
<pre><code>$ python pathlib_types.py
Name                 File    Dir   Link   FIFO  Block  Character

test_files/fifo       False  False  False   True  False  False
test_files/file        True  False  False  False  False  False
test_files/symlink     True  False   True  False  False  False
/dev/disk0            False  False  False  False   True  False
/dev/console          False  False  False  False  False   True
</pre></code>
## File Properties
可以使用方法stat()或lstat()来访问文件的详细信息(用于检查可能是符号链接的内容的状态)。这些方法产生与os.stat()和os.lstat()相同的结果。
<pre><code># pathlib_stat.py

import pathlib
import sys
import time

if len(sys.argv) == 1:
    filename = __file__
else:
    filename = sys.argv[1]

p = pathlib.Path(filename)
stat_info = p.stat()

print('{}:'.format(filename))
print('  Size:', stat_info.st_size)
print('  Permissions:', oct(stat_info.st_mode))
print('  Owner:', stat_info.st_uid)
print('  Device:', stat_info.st_dev)
print('  Created      :', time.ctime(stat_info.st_ctime))
print('  Last modified:', time.ctime(stat_info.st_mtime))
print('  Last accessed:', time.ctime(stat_info.st_atime))
</pre></code>
输出将取决于如何安装示例代码。尝试在命令行上传递不同的文件名到pathlib_stat.py。
<pre><code>$ python pathlib_stat.py

pathlib_stat.py:
  Size: 607
  Permissions: 0o100644
  Owner: 527
  Device: 16777220
  Created      : Thu Dec 29 12:38:23 2016
  Last modified: Thu Dec 29 12:38:23 2016
  Last accessed: Sun Mar 18 16:21:41 2018

$ python pathlib_stat.py index.rst

index.rst:
  Size: 19569
  Permissions: 0o100644
  Owner: 527
  Device: 16777220
  Created      : Sun Mar 18 16:11:31 2018
  Last modified: Sun Mar 18 16:11:31 2018
  Last accessed: Sun Mar 18 16:21:40 2018
</pre></code>
为了更简单地访问关于文件所有者的信息，请使用owner()和group()。
<pre><code># pathlib_ownership.py

import pathlib

p = pathlib.Path(__file__)

print('{} is owned by {}/{}'.format(p, p.owner(), p.group()))
</pre></code>
当stat()返回数值系统ID值时，这些方法会查找与IDs关联的名称。
<pre><code>$ python pathlib_ownership.py
# linux(root用户)
pathlib_ownership.py is owned by root/root
</pre></code>
touch()方法类似于Unix命令触摸来创建文件或更新现有文件的修改时间和权限。
<pre><code># pathlib_touch.py

import pathlib
import time

p = pathlib.Path('touched')
if p.exists():
    print('already exists')
else:
    print('creating new')

p.touch()
start = p.stat()

time.sleep(1)

p.touch()
end = p.stat()

print('Start:', time.ctime(start.st_mtime))
print('End  :', time.ctime(end.st_mtime))
</pre></code>
运行这个示例两次结果如下。
<pre><code>$ python pathlib_touch.py
creating new
Start: Wed May 30 10:20:37 2018
End  : Wed May 30 10:20:38 2018

$ python pathlib_touch.py
already exists
Start: Wed May 30 10:20:59 2018
End  : Wed May 30 10:21:00 2018
</pre></code>
## Permissions
在类unix系统中，可以使用chmod()来更改文件权限，将模式作为整数传递。模式值可以使用stat模块中定义的常量来构造。这个示例切换用户的执行权限位。
<pre><code># pathlib_chmod.py

import os
import pathlib
import stat
# Create a fresh test file.
f = pathlib.Path('pathlib_chmod_example.txt')
if f.exists():
    f.unlink()
f.write_text('contents')

# Determine what permissions are already set using stat.
existing_permissions = stat.S_IMODE(f.stat().st_mode)
print('Before: {:o}'.format(existing_permissions))

# Decide which way to toggle them.
if not (existing_permissions & os.X_OK):
    print('Adding execute permission')
    new_permissions = existing_permissions | stat.S_IXUSR
else:
    print('Removing execute permission')
    # use xor to remove the user execute permission
    new_permissions = existing_permissions ^ stat.S_IXUSR

# Make the change and show the new value.
f.chmod(new_permissions)
after_permissions = stat.S_IMODE(f.stat().st_mode)
print('After: {:o}'.format(after_permissions))
</pre></code>
该脚本假定它具有在运行时修改文件模式所需的权限。
<pre><code>$ python pathlib_chmod.py
# linux
Before: 644
Adding execute permission
After: 744
</pre></code>
## Deleting
有两种方法可以从文件系统中删除东西，这取决于类型。要删除空目录，请使用rmdir()。
<pre><code># pathlib_rmdir.py

import pathlib

p = pathlib.Path('example_dir')

print('Removing {}'.format(p))
p.rmdir()
</pre></code>
运行两次结果如下
<pre><code>$ python pathlib_rmdir.py
Removing example_dir

$ python pathlib_rmdir.py
Removing example_dir
Traceback (most recent call last):
  File "pathlib_rmdir.py", line 8, in <module>
    p.rmdir()
  File "C:\python3\lib\pathlib.py", line 1270, in rmdir
    self._accessor.rmdir(self)
  File "C:\python3\lib\pathlib.py", line 387, in wrapped
    return strfunc(str(pathobj), *args)
FileNotFoundError: [WinError 2] 系统找不到指定的文件。: 'example_dir'
</pre></code>
对于文件、符号链接，以及大多数其他路径类型使用unlink()。
<pre><code># pathlib_unlink.py

import pathlib

p = pathlib.Path('touched')

p.touch()

print('exists before removing:', p.exists())

p.unlink()

print('exists after removing:', p.exists())
</pre></code>
用户必须具有删除文件、符号链接、套接字或其他文件系统对象的权限。
<pre><code>$ python pathlib_unlink.py
exists before removing: True
exists after removing: False
</pre></code>

