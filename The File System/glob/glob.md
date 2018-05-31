# glob -- Filename Pattern Matching
> 目的：使用Unix shell规则查找匹配模式的文件名。

尽管glob API很小，但模块却具有很大的威力。在任何情况下，程序都需要在文件系统上查找与模式匹配的文件名列表。要创建所有具有一定扩展名、前缀或中间的任何普通字符串的文件名列表，请使用glob而不是编写自定义代码来扫描目录内容。

glob的模式规则与re模块使用的正则表达式不一样。相反，它们遵循标准的Unix路径扩展规则。只有少数特殊字符用于实现两种不同的通配符和字符范围。模式规则应用于文件名的段(在路径分隔符/处停止)。模式中的路径可以是相对的，也可以是绝对的。不扩展Shell变量名和波浪号(~)。
## Example Data
假设当前目录有一下目录和文件
<pre><code>
dir
dir/file.txt
dir/file1.txt
dir/file2.txt
dir/filea.txt
dir/fileb.txt
dir/file[.txt
dir/subdir
dir/subdir/subfile.txt
</pre></code>
## Wildcards
星号(*)在一个名称的部分中匹配零个或多个字符。例如,dir/*。
<pre><code># glob_asterisk.py

import glob
for name in sorted(glob.glob('dir/*')):
    print(name)
</pre></code>
该模式匹配目录dir中的每个路径名(文件或目录)，而不将其递归到子目录中。glob()返回的数据没有排序。
<pre><code>$ python glob_asterisk.py
# windows(linux结果'\'换成'/')
dir\file.txt
dir\file1.txt
dir\file2.txt
dir\file[.txt
dir\filea.txt
dir\fileb.txt
dir\subdir
</pre></code>
要在子目录中列出文件，子目录必须包含在模式中。
<pre><code># glob_subdir.py

import glob

print('Named explicitly:')
for name in sorted(glob.glob('dir/subdir/*')):
    print(' {}'.format(name))

print('Named with wildcard:')
for name in sorted(glob.glob('dir/*/*')):
    print(' {}'.format(name))
</pre></code>
前面显示的第一个例子明确地列出了子目录名，而第二种情况则依赖于通配符来查找目录。
<pre><code>$ python glob_subdir.py
Named explicitly:
 dir/subdir\subfile.txt
Named with wildcard:
 dir\subdir\subfile.txt
 </pre></code>
 在这种情况下，结果是一样的。如果有另一个子目录，则通配符将匹配两个子目录，并从两个子目录中包含文件名。
 ## Single Character Wildcard
 问号(?)是另一个通配符。它在名称中与该位置中的任何单个字符匹配。
 <pre><code># glob_question.py

import glob

for name in sorted(glob.glob('dir/file?.txt')):
    print(name)
</pre></code>
前面的示例匹配以'file'开头，以.txt结束，中间具有任何类型的一个字符的文件名。
<pre><code>$ python glob_question.py
dir\file1.txt
dir\file2.txt
dir\file[.txt
dir\filea.txt
dir\fileb.txt
</pre></code>
## Character Ranges
使用一个字符范围([a-z])而不是一个问号来匹配多个字符中的一个。此示例在扩展名之前找到所有带有数字的文件。
<pre><code># glob_charrange.py

import glob
for name in sorted(glob.glob('dir/*[0-9].*')):
    print(name)
</pre></code>
字符范围[0-9]匹配任何单个数字。这个范围是根据每个字母/数字的字符代码来排序的，而连字符'-'则显示了连续字符的一个完整的范围。同样的范围值可以写[0123456789]。
<pre><code>$ python glob_charrange.py
dir\file1.txt
dir\file2.txt
</pre></code>
## Escaping Meta-characters
有时，有必要搜索包含特殊元字符的文件，其中包含其模式的特殊元字符。escape()函数用特殊字符“转义”构建了一个合适的模式，这样它们就不会被glob扩展或解释为特殊字符。
<pre><code># glob_escape.py

import glob

specials = '['

for char in specials:
    pattern = 'dir/*' + glob.escape(char) + '.txt'
    print('Searching for: {!r}'.format(pattern))
    for name in sorted(glob.glob(pattern)):
        print(name)
</pre></code>
每个特殊字符都通过构建一个包含单个条目的字符范围来逃脱。
<pre><code>$ python glob_escape.py
Searching for: 'dir/*[[].txt'
dir\file[.txt
</pre></code>

