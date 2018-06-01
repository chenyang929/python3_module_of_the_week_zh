# fnmatch -- Unix-style Glob Pattern Matching
> 目的：处理unix形式文件名的比较。

fnmatch模块用于比较文件名与全局样式的模式(如Unix shell所使用的模式)。
## Simple Matching
fnmatch()将单个文件名与模式进行比较，并返回一个布尔值，指示它们是否匹配。当操作系统使用区分大小写的文件系统时，比较是区分大小写的。
<pre><code># fnmatch_fnmatch.py

import fnmatch
import os

pattern = 'fnmatch_*.py'
print('Pattern:', pattern)
print()

files = os.listdir('.')
for name in sorted(files):
    print('Filename: {:<25} {}'.format(name, fnmatch.fnmatch(name, pattern)))
</pre></code>
在本例中，模式匹配以'fnmatch_'开头、以'.py'结尾的所有文件。
<pre><code>$ python fnmatch_fnmatch.py
Pattern: fnmatch_*.py

Filename: fnmatch.md                False
Filename: fnmatch_fnmatch.py        True
</pre></code>
要强制区分大小写的比较，无论文件系统和操作系统设置是什么，请使用fnmatchcase()。
<pre><code># fnmatch_fnmatchcase.py

import fnmatch
import os

pattern = 'FNMATCH_*.py'
print('Pattern:', pattern)
print()

files = os.listdir('.')
for name in sorted(files):
    print('Filename: {:<25} {}'.format(name, fnmatch.fnmatchcase(name, pattern)))
</pre></code>
<pre><code>$ python fnmatch_fnmatchcase.py
Pattern: FNMATCH_*.py

Filename: fnmatch.md                False
Filename: fnmatch_fnmatch.py        False
Filename: fnmatch_fnmatchcase.py    False
</pre></code>
## Filtering
要测试一个文件名序列，请使用filter()，它返回匹配模式参数的名称的列表。
<pre><code># fnmatch_filter.py

import fnmatch
import os
import pprint

pattern = 'fnmatch_*.py'
print('Pattern:', pattern)

files = list(sorted(os.listdir('.')))

print('\nFiles:')
pprint.pprint(files)

print('\nMatches:')
pprint.pprint(fnmatch.filter(files, pattern))
</pre></code>
在本例中，filter()返回与本节相关的示例源文件的名称列表。
<pre><code>$ python fnmatch_filter.py
Pattern: fnmatch_*.py

Files:
['fnmatch.md',
 'fnmatch_filter.py',
 'fnmatch_fnmatch.py',
 'fnmatch_fnmatchcase.py']

Matches:
['fnmatch_filter.py', 'fnmatch_fnmatch.py', 'fnmatch_fnmatchcase.py']
</pre></code>
## Translating Patterns
在内部，fnmatch将glob模式转换为正则表达式，并使用re模块来比较名称和模式。函数的作用是:将glob模式转换为正则表达式的公共API。
<pre><code># fnmatch_translate.py

import fnmatch

pattern = 'fnmatch_*.py'
print('Pattern:', pattern)
print('Regex:', fnmatch.translate(pattern))
</pre></code>
一些字符被转义以形成一个有效的表达式。
<pre><code>$ python fnmatch_translate.py
Pattern: fnmatch_*.py
Regex: (?s:fnmatch_.*\.py)\Z
</pre></code>
