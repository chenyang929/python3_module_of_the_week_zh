# filecmp -- Compare Files
> 目的：比较文件系统上的文件和目录。

filecmp模块包含用于比较文件系统上的文件和目录的函数和类。
## Example Data
本讨论中的示例使用filecmp_mkexample.py创建的一组测试文件。
```
# filecmp_mkexamples.py

import os


def mkfile(filename, body=None):
    with open(filename, 'w') as f:
        f.write(body or filename)
    return


def make_example_dir(top):
    if not os.path.exists(top):
        os.mkdir(top)
    curdir = os.getcwd()
    os.chdir(top)

    os.mkdir('dir1')
    os.mkdir('dir2')

    mkfile('dir1/file_only_in_dir1')
    mkfile('dir2/file_only_in_dir2')

    os.mkdir('dir1/dir_only_in_dir1')
    os.mkdir('dir2/dir_only_in_dir2')

    os.mkdir('dir1/common_dir')
    os.mkdir('dir2/common_dir')

    mkfile('dir1/common_file', 'this file is the same')
    mkfile('dir2/common_file', 'this file is the same')

    mkfile('dir1/not_the_same')
    mkfile('dir2/not_the_same')

    mkfile('dir1/file_in_dir1', 'This is a file in dir1')
    os.mkdir('dir2/file_in_dir1')

    os.chdir(curdir)
    return


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__) or os.getcwd())
    make_example_dir('example')
    make_example_dir('example/dir1/common_dir')
    make_example_dir('example/dir2/common_dir')
```
## Comparing Files
cmp()比较文件系统中的两个文件。
```
# filecmp_cmp.py

import filecmp

print('common_file :', end=' ')
print(filecmp.cmp('example/dir1/common_file',
                  'example/dir2/common_file'),
      end=' ')
print(filecmp.cmp('example/dir1/common_file',
                  'example/dir2/common_file',
                  shallow=False))

print('not_the_same:', end=' ')
print(filecmp.cmp('example/dir1/not_the_same',
                  'example/dir2/not_the_same'),
      end=' ')
print(filecmp.cmp('example/dir1/not_the_same',
                  'example/dir2/not_the_same',
                  shallow=False))

print('identical   :', end=' ')
print(filecmp.cmp('example/dir1/file_only_in_dir1',
                  'example/dir1/file_only_in_dir1'),
      end=' ')
print(filecmp.cmp('example/dir1/file_only_in_dir1',
                  'example/dir1/file_only_in_dir1',
                  shallow=False))
```
shallow参数告诉cmp()是否除了查看文件的元数据之外还要查看文件的内容。默认情况是使用os.stat()提供的信息进行浅层次比较。如果统计结果相同，则认为文件是相同的，因此同时创建的大小相同的文件被报告为相同的文件，即使它们的内容不同。当shallow参数是False时，文件的内容总是被比较。
```
$ python filecmp_cmp.py
common_file : True True
not_the_same: False False # windows, linux为True False
identical   : True True
```
要比较两个目录中的一组文件而不使用递归，请使用cmpfiles()。参数是目录的名称和要在两个位置检查的文件的列表。传入的公共文件列表应该只包含文件名(目录总是导致不匹配)，并且文件必须出现在两个位置。下一个示例展示了构建公共列表的简单方法。与cmp()一样，比较也使用shallow标记。
```
# filecmp_cmpfiles.py

import filecmp
import os

# Determine the items that exist in both directories
d1_contents = set(os.listdir('example/dir1'))
d2_contents = set(os.listdir('example/dir2'))
common = list(d1_contents & d2_contents)
common_files = [
    f
    for f in common
    if os.path.isfile(os.path.join('example/dir1', f))
]
print('Common files:', common_files)

# Compare the directories
match, mismatch, errors = filecmp.cmpfiles(
    'example/dir1',
    'example/dir2',
    common_files,
)
print('Match       :', match)
print('Mismatch    :', mismatch)
print('Errors      :', errors)
```
cmpfiles()返回三个文件名列表，其中包含匹配的文件、不匹配的文件和不能进行比较的文件(由于权限问题或其他原因)。
```
$ python filecmp_cmpfiles.py
# windows
Common files: ['file_in_dir1', 'common_file', 'not_the_same']
Match       : ['common_file']
Mismatch    : ['file_in_dir1', 'not_the_same']
Errors      : []

# linux
Common files: ['not_the_same', 'file_in_dir1', 'common_file']
Match       : ['not_the_same', 'common_file']
Mismatch    : ['file_in_dir1']
Errors      : []
```
## Comparing Directories
前面描述的函数适用于相对简单的比较。对于大型目录树的递归比较或更完整的分析，dircmp类更有用。在最简单的用例中，report()打印比较两个目录的报表。
```
# filecmp_dircmp_report.py

import filecmp

dc = filecmp.dircmp('example/dir1', 'example/dir2')
dc.report()
```
输出是一个纯文本报告，只显示给定目录的内容的结果，不进行递归。在本例中，文件“not_the_same”被认为是相同的，因为没有对内容进行比较。没有办法让dircmp像cmp()那样比较文件的内容。
```
$ python filecmp_dircmp_report.py
# linux
diff example/dir1 example/dir2
Only in example/dir1 : ['dir_only_in_dir1', 'file_only_in_dir1']
Only in example/dir2 : ['dir_only_in_dir2', 'file_only_in_dir2']
Identical files : ['common_file', 'not_the_same']
Common subdirectories : ['common_dir']
Common funny cases : ['file_in_dir1']

# windows
diff example/dir1 example/dir2
Only in example/dir1 : ['dir_only_in_dir1', 'file_only_in_dir1']
Only in example/dir2 : ['dir_only_in_dir2', 'file_only_in_dir2']
Identical files : ['common_file']
Differing files : ['not_the_same']
Common subdirectories : ['common_dir']
Common funny cases : ['file_in_dir1']
```
要了解更多细节和递归比较，请使用report_full_closure():
```
# filecmp_dircmp_report_full_closure.py

import filecmp

dc = filecmp.dircmp('example/dir1', 'example/dir2')
dc.report_full_closure()
```
输出包括所有并行子目录的比较。
```
$ python filecmp_dircmp_report_full_closure.py
# linux
diff example/dir1 example/dir2
Only in example/dir1 : ['dir_only_in_dir1', 'file_only_in_dir1']
Only in example/dir2 : ['dir_only_in_dir2', 'file_only_in_dir2']
Identical files : ['common_file', 'not_the_same']
Common subdirectories : ['common_dir']
Common funny cases : ['file_in_dir1']

diff example/dir1/common_dir example/dir2/common_dir
Common subdirectories : ['dir1', 'dir2']

diff example/dir1/common_dir/dir1 example/dir2/common_dir/dir1
Identical files : ['common_file', 'file_in_dir1',
'file_only_in_dir1', 'not_the_same']
Common subdirectories : ['common_dir', 'dir_only_in_dir1']

diff example/dir1/common_dir/dir1/dir_only_in_dir1
example/dir2/common_dir/dir1/dir_only_in_dir1

diff example/dir1/common_dir/dir1/common_dir
example/dir2/common_dir/dir1/common_dir

diff example/dir1/common_dir/dir2 example/dir2/common_dir/dir2
Identical files : ['common_file', 'file_only_in_dir2',
'not_the_same']
Common subdirectories : ['common_dir', 'dir_only_in_dir2',
'file_in_dir1']

diff example/dir1/common_dir/dir2/common_dir
example/dir2/common_dir/dir2/common_dir

diff example/dir1/common_dir/dir2/file_in_dir1
example/dir2/common_dir/dir2/file_in_dir1

diff example/dir1/common_dir/dir2/dir_only_in_dir2
example/dir2/common_dir/dir2/dir_only_in_dir2

# windows
diff example/dir1 example/dir2
Only in example/dir1 : ['dir_only_in_dir1', 'file_only_in_dir1']
Only in example/dir2 : ['dir_only_in_dir2', 'file_only_in_dir2']
Identical files : ['common_file']
Differing files : ['not_the_same']
Common subdirectories : ['common_dir']
Common funny cases : ['file_in_dir1']

diff example/dir1\common_dir example/dir2\common_dir
Common subdirectories : ['dir1', 'dir2']

diff example/dir1\common_dir\dir1 example/dir2\common_dir\dir1
Identical files : ['common_file', 'file_in_dir1', 'file_only_in_dir1', 'not_the_same']
Common subdirectories : ['common_dir', 'dir_only_in_dir1']

diff example/dir1\common_dir\dir1\common_dir example/dir2\common_dir\dir1\common_dir

diff example/dir1\common_dir\dir1\dir_only_in_dir1 example/dir2\common_dir\dir1\dir_only_in_dir1

diff example/dir1\common_dir\dir2 example/dir2\common_dir\dir2
Identical files : ['common_file', 'file_only_in_dir2', 'not_the_same']
Common subdirectories : ['common_dir', 'dir_only_in_dir2', 'file_in_dir1']

diff example/dir1\common_dir\dir2\common_dir example/dir2\common_dir\dir2\common_dir

diff example/dir1\common_dir\dir2\dir_only_in_dir2 example/dir2\common_dir\dir2\dir_only_in_dir2

diff example/dir1\common_dir\dir2\file_in_dir1 example/dir2\common_dir\dir2\file_in_dir1
```
## Using Differences in a Program
除了生成打印的报告之外，dircmp还计算可以直接用于程序的文件列表。以下每个属性仅在请求时才计算，因此创建dircmp实例不会为未使用的数据带来开销。
```
# filecmp_dircmp_list.py

import filecmp
import pprint

dc = filecmp.dircmp('example/dir1', 'example/dir2')
print('Left:')
pprint.pprint(dc.left_list)

print('\nRight:')
pprint.pprint(dc.right_list)
```
被比较的目录中包含的文件和子目录在left_list和right_list中列出。
```
$ python filecmp_dircmp_list.py

Left:
['common_dir',
 'common_file',
 'dir_only_in_dir1',
 'file_in_dir1',
 'file_only_in_dir1',
 'not_the_same']

Right:
['common_dir',
 'common_file',
 'dir_only_in_dir2',
 'file_in_dir1',
 'file_only_in_dir2',
 'not_the_same']
```
可以通过向构造函数传递一个要忽略的名称列表来过滤输入。默认情况下，RCS、CVS和标记的名称将被忽略。
```
# filecmp_dircmp_list_filter.py

import filecmp
import pprint

dc = filecmp.dircmp('example/dir1', 'example/dir2', ignore=['common_file'])

print('Left:')
pprint.pprint(dc.left_list)

print('\nRight:')
pprint.pprint(dc.right_list)
```
在这种情况下，“common_file”被排除在要比较的文件列表之外。
```
$ python filecmp_dircmp_list_filter.py
Left:
['common_dir',
 'dir_only_in_dir1',
 'file_in_dir1',
 'file_only_in_dir1',
 'not_the_same']

Right:
['common_dir',
 'dir_only_in_dir2',
 'file_in_dir1',
 'file_only_in_dir2',
 'not_the_same']
```
两个输入目录中常见的文件的名称都是相同的，并且每个目录所特有的文件只在left_only和right_only中列出。
```
# filecmp_dircmp_membership.py

import filecmp
import pprint

dc = filecmp.dircmp('example/dir1', 'example/dir2')
print('Common:')
pprint.pprint(dc.common)

print('\nLeft:')
pprint.pprint(dc.left_only)

print('\nRight:')
pprint.pprint(dc.right_only)
```
“左”目录是dircmp()的第一个参数，而“右”目录是第二个。
```
$ python filecmp_dircmp_membership.py

Common:
['common_dir', 'common_file', 'file_in_dir1', 'not_the_same']

Left:
['dir_only_in_dir1', 'file_only_in_dir1']

Right:
['dir_only_in_dir2', 'file_only_in_dir2']
```
公共成员可以进一步细分为文件、目录和“funny”项(在两个目录中具有不同类型的任何东西，或者在os.stat()中出现错误的地方)。
```
# filecmp_dircmp_common.py

import filecmp
import pprint

dc = filecmp.dircmp('example/dir1', 'example/dir2')
print('Common:')
pprint.pprint(dc.common)

print('\nDirectories:')
pprint.pprint(dc.common_dirs)

print('\nFiles:')
pprint.pprint(dc.common_files)

print('\nFunny:')
pprint.pprint(dc.common_funny)
```
在示例数据中，名为“file_in_dir1”的项目是一个目录中的一个文件，另一个目录中有一个子目录，因此它显示在一个"funny"列表中。
```
$ python filecmp_dircmp_common.py

Common:
['common_dir', 'common_file', 'file_in_dir1', 'not_the_same']

Directories:
['common_dir']

Files:
['common_file', 'not_the_same']

Funny:
['file_in_dir1']
```
文件之间的差异被类似地分解。
```
# filecmp_dircmp_diff.py

import filecmp

dc = filecmp.dircmp('example/dir1', 'example/dir2')
print('Same      :', dc.same_files)
print('Different :', dc.diff_files)
print('Funny     :', dc.funny_files)
```
not_the_same文件仅通过os.stat()进行比较，并且不检查内容，因此它包含在same_files列表中。
```
$ python filecmp_dircmp_diff.py

# linux
Same      : ['common_file', 'not_the_same']
Different : []
Funny     : []

# windows
Same      : ['common_file']
Different : ['not_the_same']
Funny     : []
```
最后，还保存子目录，以便进行简单的递归比较。
```
# filecmp_dircmp_subdirs.py

import filecmp

dc = filecmp.dircmp('example/dir1', 'example/dir2')
print('Subdirectories:')
print(dc.subdirs)
```
属性subdirs是将目录名映射到新的dircmp对象的字典。
```
$ python filecmp_dircmp_subdirs.py

Subdirectories:
{'common_dir': <filecmp.dircmp object at 0x1019b2be0>}
```


