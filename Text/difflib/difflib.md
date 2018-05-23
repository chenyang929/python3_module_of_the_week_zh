# difflib -- Compare Sequences
> 目的：比较序列，特别是文本行。

difflib模块包含用于计算和处理序列之间差异的工具。它对于比较文本非常有用，并且包括使用几种常见的差异格式生成报告的函数。
本节中的示例中的测试数据将来源difflib_data.py:
<pre><code># difflib_data.py

text1 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
pharetra tortor.  In nec mauris eget magna consequat
convalis. Nam sed sem vitae odio pellentesque interdum. Sed
consequat viverra nisl. Suspendisse arcu metus, blandit quis,
rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
tristique enim. Donec quis lectus a justo imperdiet tempus."""

text1_lines = text1.splitlines()

text2 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
pharetra tortor. In nec mauris eget magna consequat
convalis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
consequat viverra nisl. Suspendisse arcu metus, blandit quis,
rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Duis vulputate tristique enim. Donec quis lectus a
justo imperdiet tempus.  Suspendisse eu lectus. In nunc."""

text2_lines = text2.splitlines()</pre></code>
## Comparing Bodies of Text
Differ类在文本行序列上工作，生成人类可读的增量，或更改指令，包括在单个行内的差异。不同的默认输出类似于Unix下的diff命令行工具。它包括来自两个列表的原始输入值，包括公共值和标记数据，以指示所做的更改。

- 前缀为-的行在第一个序列中，但不是第二个序列。
- 前缀为+的行是在第二个序列中，而不是第一个序列。
- 如果一行在不同的版本之间有一个增量的差别，那么一个额外的行前缀?用于突出新版本中的更改。
- 如果一行没有更改，则在左列上打印一个额外的空白空间，以便与可能存在差异的其他输出保持一致。

将文本分割成一个单独的行序列，然后将其传递给compare()，从而产生比传递大字符串更容易读取的输出。
<pre><code># difflib_differ.py
import difflib
from difflib_data import *

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
print('\n'.join(diff))</pre></code>
输出结果：
<pre><code>
# 示例数据中的两个文本段的开头都是相同的，所以第一行是不带任何额外注释的。
  Lorem ipsum dolor sit amet, consectetuer adipiscing
  elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
  
# 数据的第三行已经更改为在修改后的文本中包含一个逗号。这两个版本的行都是打印出来的，在第5行的额外信息显示了文本被修改的列，包括添加了字符的事实。
- pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
+ pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
?         +

# 下一行行输出显示额外的空间被删除了。
- pharetra tortor.  In nec mauris eget magna consequat
?                 -

+ pharetra tortor. In nec mauris eget magna consequat

# 接下来，一个更复杂的变化发生了，用一个短语替换了几个单词。
- convalis. Nam sed sem vitae odio pellentesque interdum. Sed
?                 - --

+ convalis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
?               +++ +++++   +

# 段落的最后一个句子发生了很大的变化，所以区别在于删除旧版本和添加新版本。
  consequat viverra nisl. Suspendisse arcu metus, blandit quis,
  rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
  molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
  tristique vel, mauris. Curabitur vel lorem id nisl porta
- adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
- tristique enim. Donec quis lectus a justo imperdiet tempus.
+ adipiscing. Duis vulputate tristique enim. Donec quis lectus a
+ justo imperdiet tempus.  Suspendisse eu lectus. In nunc.</pre></code>
ndiff()函数的作用是:产生基本相同的输出。这种处理是专门为处理文本数据和消除输入中的“噪音”而量身定做的。
## Other Output Formats
Differ类显示了所有的输入行，unified_diff()函数产生只包含修改后的行和一些上下文这种输出。
<pre><code># difflib_unified.py

import difflib
from difflib_data import *

diff = difflib.unified_diff(
    text1_lines,
    text2_lines,
    lineterm='',
)
print('\n'.join(diff))</pre></code>
lineterm参数用于告诉unified_diff()，跳过将新行添加到它返回的控制行中，因为输入行不包含它们。
当所有行被打印时，都会添加新行。对于许多流行的版本控制工具的用户来说，输出应该是熟悉的。

<pre><code>$ python difflib_unified.py
\---
+++ 
@@ -1,11 +1,11 @@
 Lorem ipsum dolor sit amet, consectetuer adipiscing
 elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
-pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
-pharetra tortor.  In nec mauris eget magna consequat
-convalis. Nam sed sem vitae odio pellentesque interdum. Sed
+pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
+pharetra tortor. In nec mauris eget magna consequat
+convalis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
 consequat viverra nisl. Suspendisse arcu metus, blandit quis,
 rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
 molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
 tristique vel, mauris. Curabitur vel lorem id nisl porta
-adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
-tristique enim. Donec quis lectus a justo imperdiet tempus.
+adipiscing. Duis vulputate tristique enim. Donec quis lectus a
+justo imperdiet tempus.  Suspendisse eu lectus. In nunc.</pre></code>
使用context_diff()产生类似可读的输出。
## Junk Data
产生差异序列的所有函数都接受参数，以指示哪些行应该被忽略，哪些字符应该被忽略。例如，可以使用这些参数跳过文件的两个版本中的标记或空白更改。
<pre><code># difflib_junk.py

from difflib import SequenceMatcher


def show_results(match):
    print('  a    = {}'.format(match.a))
    print('  b    = {}'.format(match.b))
    print('  size = {}'.format(match.size))
    i, j, k = match
    print('  A[a:a+size] = {!r}'.format(A[i:i + k]))
    print('  B[b:b+size] = {!r}'.format(B[j:j + k]))


A = " abcd"
B = "abcd abcd"

print('A = {!r}'.format(A))
print('B = {!r}'.format(B))

print('\nWithout junk detection:')
s1 = SequenceMatcher(None, A, B)
match1 = s1.find_longest_match(0, len(A), 0, len(B))
show_results(match1)

print('\nTreat spaces as junk:')
s2 = SequenceMatcher(lambda x: x == " ", A, B)
match2 = s2.find_longest_match(0, len(A), 0, len(B))
show_results(match2)</pre></code>
不同的默认值是不显式地忽略任何行或字符，而是依赖于SequenceMatcher检测噪声的能力。ndiff()的默认值是忽略空格和制表符。
<pre><code>$ python difflib_junk.py
A = ' abcd'
B = 'abcd abcd'

Without junk detection:
  a    = 0
  b    = 4
  size = 5
  A[a:a+size] = ' abcd'
  B[b:b+size] = ' abcd'

Treat spaces as junk:
  a    = 1
  b    = 0
  size = 4
  A[a:a+size] = 'abcd'
  B[b:b+size] = 'abcd'</pre></code>
## Comparing Arbitrary Types
SequenceMatcher类比较任何类型的两个序列，只要这些值是可洗的。它使用一种算法来识别序列中最长的连续匹配块，消除对真实数据没有贡献的“垃圾”值。

函数get_opcodes()返回修改第一个序列的指令列表，使其与第二个序列匹配。指令被编码为五元组元组，包括字符串指令(“操作码”，见下表)和两对启动和停止索引到序列中(表示为i1、i2、j1和j2)。
<pre><code># difflib_seq.py

import difflib

s1 = [1, 2, 3, 5, 6, 4]
s2 = [2, 3, 5, 4, 6, 1]

print('Initial data:')
print('s1 =', s1)
print('s2 =', s2)
print('s1 == s2:', s1 == s2)
print()

matcher = difflib.SequenceMatcher(None, s1, s2)
for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):

    if tag == 'delete':
        print('Remove {} from positions [{}:{}]'.format(
            s1[i1:i2], i1, i2))
        print('  before =', s1)
        del s1[i1:i2]

    elif tag == 'equal':
        print('s1[{}:{}] and s2[{}:{}] are the same'.format(
            i1, i2, j1, j2))

    elif tag == 'insert':
        print('Insert {} from s2[{}:{}] into s1 at {}'.format(
            s2[j1:j2], j1, j2, i1))
        print('  before =', s1)
        s1[i1:i2] = s2[j1:j2]

    elif tag == 'replace':
        print(('Replace {} from s1[{}:{}] '
               'with {} from s2[{}:{}]').format(
                   s1[i1:i2], i1, i2, s2[j1:j2], j1, j2))
        print('  before =', s1)
        s1[i1:i2] = s2[j1:j2]

    print('   after =', s1, '\n')

print('s1 == s2:', s1 == s2)</pre></code>
这个示例比较两个整数列表，并使用get_opcodes()来派生将原始列表转换为新版本的指令。这些修改以相反的顺序应用，以便在添加和删除项目后，列表索引保持准确。
<pre><code>$ python difflib_seq.py
Initial data:
s1 = [1, 2, 3, 5, 6, 4]
s2 = [2, 3, 5, 4, 6, 1]
s1 == s2: False

Replace [4] from s1[5:6] with [1] from s2[5:6]
  before = [1, 2, 3, 5, 6, 4]
   after = [1, 2, 3, 5, 6, 1] 

s1[4:5] and s2[4:5] are the same
   after = [1, 2, 3, 5, 6, 1] 

Insert [4] from s2[3:4] into s1 at 4
  before = [1, 2, 3, 5, 6, 1]
   after = [1, 2, 3, 5, 4, 6, 1] 

s1[1:4] and s2[0:3] are the same
   after = [1, 2, 3, 5, 4, 6, 1] 

Remove [1] from positions [0:1]
  before = [1, 2, 3, 5, 4, 6, 1]
   after = [2, 3, 5, 4, 6, 1] 

s1 == s2: True</pre></code>
SequenceMatcher与自定义类以及内置类型一起工作，只要它们是可哈希的。
