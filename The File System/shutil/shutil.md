# shutil -- High-level File Operations
> 目的：高级文件操作

shutil模块包含高级文件操作，如复制和归档。
## Copying Files
copyfile()将源文件的内容复制到目标文件，如果没有对目标文件进行写入权限，则引发IOError。
```
# shutil_copyfile.py

import glob
import shutil

print('BEFORE:', glob.glob('shutil_copyfile.*'))

shutil.copyfile('shutil_copyfile.py', 'shutil_copyfile.py.copy')

print('AFTER:', glob.glob('shutil_copyfile.*'))
```
由于该函数打开输入文件进行读取，因此无论输入文件的类型如何，都不能将特殊文件(例如Unix设备节点)复制为带有copyfile()的新特殊文件。
```
$ python shutil_copyfile.py
BEFORE: ['shutil_copyfile.py']
AFTER: ['shutil_copyfile.py', 'shutil_copyfile.py.copy']
```
copyfile()的实现使用了低级函数copyfileobj()。虽然copyfile()的参数是文件名，但是copyfileobj()的参数是打开的文件句柄。可选的第三个参数是用于在块中读取的缓冲区长度。
```
# shutil_copyfileobj.py

import io
import os
import shutil
import sys

class VerboseStringIO(io.StringIO):

    def read(self, n=-1):
        next = io.StringIO.read(self, n)
        print('read({}) got {} bytes'.format(n, len(next)))
        return next


lorem_ipsum = '''Lorem ipsum dolor sit amet, consectetuer
adipiscing elit.  Vestibulum aliquam mollis dolor. Donec
vulputate nunc ut diam. Ut rutrum mi vel sem. Vestibulum
ante ipsum.'''

print('Default:')
input = VerboseStringIO(lorem_ipsum)
output = io.StringIO()
shutil.copyfileobj(input, output)

print()

print('All at once:')
input = VerboseStringIO(lorem_ipsum)
output = io.StringIO()
shutil.copyfileobj(input, output, -1)

print()

print('Blocks of 256:')
input = VerboseStringIO(lorem_ipsum)
output = io.StringIO()
shutil.copyfileobj(input, output, 256)
```
默认的行为是使用大块读取数据。使用-1来一次读取所有输入，或另一个正整数来设置一个特定的块大小。这个示例使用几个不同的块大小来显示效果。
```
$ python shutil_copyfileobj.py
Default:
read(16384) got 166 bytes
read(16384) got 0 bytes

All at once:
read(-1) got 166 bytes
read(-1) got 0 bytes

Blocks of 256:
read(256) got 166 bytes
read(256) got 0 bytes
```
copy()函数的作用是:像Unix命令行工具cp一样解释输出名。
如果指定的目标指向一个目录而不是一个文件，则使用源的基本名称在目录中创建一个新文件。
```
# shutil_copy.py

import glob
import os
import shutil

os.mkdir('example')
print('BEFORE:', glob.glob('example/*'))

shutil.copy('shutil_copy.py', 'example')

print('AFTER:', glob.glob('example/*'))
```
文件的权限与内容一起被复制。
```
$ python shutil_copy.py
BEFORE: []
AFTER: ['example\\shutil_copy.py']
```
copy2()的工作方式类似于copy()，但是包含了复制到新文件的元数据中的访问和修改时间。
```
# shutil_copy2.py

import os
import shutil
import time

def show_file_info(filename):
    stat_info = os.stat(filename)
    print('  Mode    :', oct(stat_info.st_mode))
    print('  Created :', time.ctime(stat_info.st_ctime))
    print('  Accessed:', time.ctime(stat_info.st_atime))
    print('  Modified:', time.ctime(stat_info.st_mtime))


os.mkdir('example')
print('SOURCE:')
show_file_info('shutil_copy2.py')

shutil.copy2('shutil_copy2.py', 'example')

print('DEST:')
show_file_info('example/shutil_copy2.py')
```
新文件具有与旧版本相同的所有特征。
```
$ python shutil_copy2.py
SOURCE:
  Mode    : 0o100666
  Created : Tue Jun 12 09:52:41 2018
  Accessed: Tue Jun 12 09:52:41 2018
  Modified: Tue Jun 12 09:56:52 2018
DEST:
  Mode    : 0o100666
  Created : Tue Jun 12 09:57:05 2018
  Accessed: Tue Jun 12 09:52:41 2018
  Modified: Tue Jun 12 09:56:52 2018
```
## Copying File Metadata
默认情况下，当在Unix下创建新文件时，它将根据当前用户的umask接收权限。要将权限从一个文件复制到另一个文件，请使用copymode()。
```
# shutil_copymode.py

import os
import shutil
import subprocess

with open('file_to_change.txt', 'wt') as f:
    f.write('content')
os.chmod('file_to_change.txt', 0o444)

print('BEFORE:', oct(os.stat('file_to_change.txt').st_mode))

shutil.copymode('shutil_copymode.py', 'file_to_change.txt')

print('AFTER :', oct(os.stat('file_to_change.txt').st_mode))
```
这个示例脚本创建要修改的文件，然后使用copymode()将脚本的权限复制到示例文件。
```
$ python shutil_copymode.py
BEFORE: 0o100444
AFTER : 0o100644
```
要复制关于文件的其他元数据，请使用copystat()。
```
# shutil_copystat.py

import os
import shutil
import time


def show_file_info(filename):
    stat_info = os.stat(filename)
    print('  Mode    :', oct(stat_info.st_mode))
    print('  Created :', time.ctime(stat_info.st_ctime))
    print('  Accessed:', time.ctime(stat_info.st_atime))
    print('  Modified:', time.ctime(stat_info.st_mtime))


with open('file_to_change.txt', 'wt') as f:
    f.write('content')
os.chmod('file_to_change.txt', 0o444)

print('BEFORE:')
show_file_info('file_to_change.txt')

shutil.copystat('shutil_copystat.py', 'file_to_change.txt')

print('AFTER:')
show_file_info('file_to_change.txt')
```
只有与该文件关联的权限和日期与copystat()重复。
```
$ python shutil_copystat.py
BEFORE:
  Mode    : 0o100444
  Created : Tue Jun 12 10:08:29 2018
  Accessed: Tue Jun 12 10:08:18 2018
  Modified: Tue Jun 12 10:08:29 2018
AFTER:
  Mode    : 0o100644
  Created : Tue Jun 12 10:08:29 2018
  Accessed: Tue Jun 12 10:08:18 2018
  Modified: Tue Jun 12 10:07:52 2018
```
## Working With Directory Trees
shutil包含三个用于处理目录树的函数。要将目录从一个地方复制到另一个地方，请使用copytree()。它通过源目录树递归，将文件复制到目的地。目标目录不能预先存在。
```
# shutil_copytree.py

import glob
import pprint
import shutil

print('BEFORE:')
pprint.pprint(glob.glob('../temp/*'))
pprint.pprint(glob.glob('../fnmatch/*'))

shutil.copytree('../fnmatch', '../temp')

print('\nAFTER:')
pprint.pprint(glob.glob('../temp/*'))
```
symlinks参数控制符号链接是作为链接复制还是作为文件复制。默认情况是将内容复制到新文件中。如果选项为真，则在目标树中创建新的符号链接。
```
$ python shutil_copytree.py
BEFORE:
[]
['../fnmatch\\fnmatch.md',
 '../fnmatch\\fnmatch_filter.py',
 '../fnmatch\\fnmatch_fnmatch.py',
 '../fnmatch\\fnmatch_fnmatchcase.py',
 '../fnmatch\\fnmatch_translate.py']

AFTER:
['../temp\\fnmatch.md',
 '../temp\\fnmatch_filter.py',
 '../temp\\fnmatch_fnmatch.py',
 '../temp\\fnmatch_fnmatchcase.py',
 '../temp\\fnmatch_translate.py']
```
copytree()接受两个可调用的参数来控制其行为。忽略参数被调用时，每个目录或子目录的名称与目录的内容列表一起被复制。它应该返回应该复制的项目列表。调用copy_function参数来实际复制文件。
```
# shutil_copytree_verbose.py

import glob
import pprint
import shutil


def verbose_copy(src, dst):
    print('copying\n {!r}\n to {!r}'.format(src, dst))
    return shutil.copy2(src, dst)


print('BEFORE:')
pprint.pprint(glob.glob('../tmp/*'))
print()

shutil.copytree(
    '../fnmatch', '../tmp',
    copy_function=verbose_copy,
    ignore=shutil.ignore_patterns('*.py'),
)

print('\nAFTER:')
pprint.pprint(glob.glob('../tmp/*'))
```
在本例中，ignore_patterns()用于创建忽略函数，以跳过复制Python源文件的过程。verbose_copy()在复制文件时打印它们的名称，然后使用默认的copy函数copy2()进行复制。
```
$ python shutil_copytree_verbose.py
BEFORE:
[]

copying
 '../fnmatch\\fnmatch.md'
 to '../tmp\\fnmatch.md'

AFTER:
['../tmp\\fnmatch.md']
```
要删除目录及其内容，请使用rmtree()。
```
# shutil_rmtree.py

import glob
import pprint
import shutil

print('BEFORE:')
pprint.pprint(glob.glob('../tmp/*'))

shutil.rmtree('../tmp')

print('\nAFTER:')
pprint.pprint(glob.glob('../tmp/*'))
```
默认情况下，错误作为异常被提出，但是如果第二个参数为true，可以忽略错误，并且可以在第三个参数中提供一个特殊的错误处理函数。
```
$ python shutil_rmtree.py
BEFORE:
['../tmp\\fnmatch.md']

AFTER:
[]
```
要将文件或目录从一个位置移动到另一个位置，请使用move()。
```
# shutil_move.py

import glob
import shutil

with open('example.txt', 'wt') as f:
    f.write('contents')

print('BEFORE: ', glob.glob('example*'))

shutil.move('example.txt', 'example.out')

print('AFTER : ', glob.glob('example*'))
```
语义类似于Unix命令mv。如果源文件和目标文件在同一个文件系统中，源文件将被重命名。否则，源被复制到目标，然后源被删除。
```
$ python shutil_move.py
BEFORE:  ['example.txt']
AFTER :  ['example.out']
```
## Finding Files
which()函数的作用是:扫描寻找指定文件的搜索路径。典型的用例是在环境变量路径中定义的shell搜索路径上查找可执行程序。
```
# shutil_which.py

import shutil

print(shutil.which('virtualenv'))
print(shutil.which('requests'))
print(shutil.which('no-such-program'))
```
如果找不到匹配搜索参数的文件，则返回None()。
```
$ python shutil_which.py
C:\Users\coder\AppData\Roaming\Python\Python36\Scripts\virtualenv.EXE
None
None
```
which()根据文件的权限和要检查的搜索路径进行参数筛选。路径参数默认为os.environmental('PATH')，但可以是任何包含由os.pathsep分隔的目录名的字符串。模式参数应该是匹配文件权限的位掩码。默认情况下，屏蔽查找可执行文件，但是下面的示例使用可读的位掩码和替代搜索路径来查找配置文件。
```
# shutil_which_regular_file.py

import os
import shutil

path = os.pathsep.join([
    '.',
    os.path.expanduser('~/pymotw'),
])

mode = os.F_OK | os.R_OK

filename = shutil.which(
    'config.ini',
    mode=mode,
    path=path,
)

print(filename)
```
以这种方式搜索可读文件仍然存在竞争条件，因为在找到文件和实际尝试使用文件之间，可以删除文件或修改其权限。
```
$ touch config.ini
$ python shutil_which_regular_file.py

./config.ini
```
## Archives
Python的标准库包含许多管理归档文件(如tarfile和zipfile)的模块。在shutil中还有几个用于创建和提取归档的高级函数。get_archive_formats()返回当前系统支持的格式的名称和描述序列。
```
# shutil_get_archive_formats.py

import shutil

for ft, desc in shutil.get_archive_formats():
    print('{:<5}: {}'.format(ft, desc))
```
支持的格式依赖于哪些模块和底层库可用，因此这个例子的输出可能会根据运行的位置而变化。
```
$ python shutil_get_archive_formats.py
bztar: bzip2'ed tar-file
gztar: gzip'ed tar-file
tar  : uncompressed tar file
xztar: xz'ed tar-file
zip  : ZIP file
```
使用make_archive()创建一个新的存档文件。它的输入被设计成最好地支持对整个目录及其所有内容进行递归归档。默认情况下，它使用当前工作目录，以便所有文件和子目录都显示在归档的顶层。要更改此行为，请使用root_dir参数移动到文件系统上的一个新的相对位置，并使用base_dir参数指定要添加到归档的目录。
```
# shutil_make_archive.py

import logging
import shutil
import sys
import tarfile

logging.basicConfig(
    format='%(message)s',
    stream=sys.stdout,
    level=logging.DEBUG,
)
logger = logging.getLogger('pymotw')

print('Creating archive:')
shutil.make_archive(
    'example', 'gztar',
    root_dir='..',
    base_dir='shutil',
    logger=logger,
)

print('\nArchive contents:')
with tarfile.open('example.tar.gz', 'r') as t:
    for n in t.getnames():
        print(n)
```
这个示例从shutil示例的源目录开始，向上移动文件系统中的一个级别，然后将shutil目录添加到使用gzip压缩的tar归档文件中。日志模块被配置为显示来自make_archive()的关于它正在做什么的消息。
```
$ python shutil_make_archive.py
Creating archive:
changing into '..'
Creating tar archive
changing back to 'D:\python3_module_of_the_week_zh\The File System\shutil'

Archive contents:
shutil
shutil/shutil.md
shutil/shutil_copy.py
shutil/shutil_copy2.py
shutil/shutil_copyfile.py
shutil/shutil_copyfileobj.py
shutil/shutil_copymode.py
shutil/shutil_copystat.py
shutil/shutil_copytree.py
shutil/shutil_copytree_verbose.py
shutil/shutil_get_archive_formats.py
shutil/shutil_make_archive.py
shutil/shutil_move.py
shutil/shutil_rmtree.py
shutil/shutil_which.py
shutil/shutil_which_regular_file.py
```
shutil维护一个可以在当前系统上解压缩的格式注册表，可以通过get_unpack_formats()访问该注册表。
```
# shutil_get_unpack_formats.py

import shutil

for ft, exts, desc in shutil.get_unpack_formats():
    print('{:<5}: {}, names ending in {}'.format(ft, desc, exts))
```
这个注册表与创建存档的注册表不同，因为它还包含用于每种格式的公共文件扩展名，以便提取存档的函数可以根据文件扩展名猜测使用哪种格式。
```
$ python shutil_get_unpack_formats.py
bztar: bzip2'ed tar-file, names ending in ['.tar.bz2', '.tbz2']
gztar: gzip'ed tar-file, names ending in ['.tar.gz', '.tgz']
tar  : uncompressed tar file, names ending in ['.tar']
xztar: xz'ed tar-file, names ending in ['.tar.xz', '.txz']
zip  : ZIP file, names ending in ['.zip']
```
使用unpack_archive()提取归档文件，传递存档文件名称和应该提取的目录。如果没有给定目录，则使用当前目录。
```
# shutil_unpack_archive.py

import pathlib
import shutil
import sys
import tempfile

with tempfile.TemporaryDirectory() as d:
    print('Unpacking archive:')
    shutil.unpack_archive(
        'example.tar.gz',
        extract_dir=d,
    )

    print('\nCreated:')
    prefix_len = len(d) + 1
    for extracted in pathlib.Path(d).rglob('*'):
        print(str(extracted)[prefix_len:])
```
在这个示例中，unpack_archive()能够确定归档的格式，因为文件名以tar结尾。这个值与unpack格式注册表中的gztar格式相关联。
```
$ python shutil_unpack_archive.py
Unpacking archive:

Created:
shutil
shutil\shutil.md
shutil\shutil_copy.py
shutil\shutil_copy2.py
shutil\shutil_copyfile.py
shutil\shutil_copyfileobj.py
shutil\shutil_copymode.py
shutil\shutil_copystat.py
shutil\shutil_copytree.py
shutil\shutil_copytree_verbose.py
shutil\shutil_get_archive_formats.py
shutil\shutil_get_unpack_formats.py
shutil\shutil_make_archive.py
shutil\shutil_move.py
shutil\shutil_rmtree.py
shutil\shutil_unpack_archive.py
shutil\shutil_which.py
shutil\shutil_which_regular_file.py
```
## File System Space
在执行可能耗尽该空间的长时间运行操作之前，检查本地文件系统看看有多少可用空间是有用的。disk_usage()返回一个元组，该元组包含总空间、当前使用的数量和剩余的空闲数量。
```
# shutil_disk_usage.py

import shutil

total_b, used_b, free_b = shutil.disk_usage('.')

gib = 2 ** 30  # GiB == gibibyte
gb = 10 ** 9   # GB == gigabyte

print('Total: {:6.2f} GB  {:6.2f} GiB'.format(
    total_b / gb, total_b / gib))
print('Used : {:6.2f} GB  {:6.2f} GiB'.format(
    used_b / gb, used_b / gib))
print('Free : {:6.2f} GB  {:6.2f} GiB'.format(
    free_b / gb, free_b / gib))
```
disk_usage()返回的值是字节数，因此示例程序在打印它们之前将它们转换为可读性更好的单元。
```
$ python shutil_disk_usage.py
Total: 154.15 GB  143.56 GiB
Used :  20.25 GB   18.86 GiB
Free : 133.90 GB  124.71 GiB
```
