# pprint -- Pretty-Print Data Structures
> 漂亮的打印数据结构

pprint模块包含一个“漂亮的打印机”，用于产生美观的数据结构视图。格式化程序生成可以由解释器正确解析的数据结构的表示，这对于一个人来说也是很容易阅读的。
如果可能的话，输出将保持在单行上，并在跨多个行分割时缩进。

本节中的示例的数据都在pprint_data.py文件里
<pre><code># pprint_data.py

data = [
    (1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
    (2, {'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H',
         'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L'}),
    (3, ['m', 'n']),
    (4, ['o', 'p', 'q']),
    (5, ['r', 's', 't''u', 'v', 'x', 'y', 'z']),
]</pre></code>
## Printing
通过pprint()函数是使用该模块最简单的方式。
<pre><code># pprint_pprint.py

from pprint import pprint
from pprint_data import data

print('PRINT:')
print(data)
print('PPRINT:')
pprint(data)</pre></code>
pprint()格式化一个对象并将其作为参数传入数据流(或默认情况下sys.stdout)。
<pre><code>$ python pprint_pprint.py
PRINT:
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}), (2, {'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L'}), (3, ['m', 'n']), (4, ['o', 'p', 'q']), (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]
PPRINT:
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3, ['m', 'n']),
 (4, ['o', 'p', 'q']),
 (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]</pre></code>
## Formatting
若要格式化数据结构，而不直接将其写入流(例如，用于日志记录)，则使用pformat()来构建字符串表示。
<pre><code># pprint_pformat.py

import logging
from pprint import pformat
from pprint_data import data

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)-8s %(message)s'
)

logging.debug('Logging pformatted data')
formatted = pformat(data)
for line in formatted.splitlines():
    logging.debug(line.rstrip())</pre></code>
然后可以独立地打印或记录格式化的字符串。
<pre><code>$ python pprint_pformat.py
DEBUG    Logging pformatted data
DEBUG    [(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
DEBUG     (2,
DEBUG      {'e': 'E',
DEBUG       'f': 'F',
DEBUG       'g': 'G',
DEBUG       'h': 'H',
DEBUG       'i': 'I',
DEBUG       'j': 'J',
DEBUG       'k': 'K',
DEBUG       'l': 'L'}),
DEBUG     (3, ['m', 'n']),
DEBUG     (4, ['o', 'p', 'q']),
DEBUG     (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]</pre></code>
## Arbitrary Classes
如果定义了__repr__()方法，pprint()使用的PrettyPrinter类也可以使用自定义类。
<pre><code># pprint_arbitrary_object.py

from pprint import pprint


class Node:

    def __init__(self, name, contents=[]):
        self.name = name
        self.contents = contents[:]

    def __repr__(self):
        return (
                'node(' + repr(self.name) + ', ' +
                repr(self.contents) + ')'
        )


trees = [
    Node('node-1'),
    Node('node-2', [Node('node-2-1')]),
    Node('node-3', [Node('node-3-1')]),
]
pprint(trees)</pre></code>
嵌套对象的表示由PrettyPrinter组合，以返回全部字符串表示。
<pre><code>$ python pprint_arbitrary_object.py
[node('node-1', []),
 node('node-2', [node('node-2-1', [])]),
 node('node-3', [node('node-3-1', [])])]</pre></code>
## Recursion
递归数据结构以引用原始数据来源的方式表示，以格式<Recursion on typename with id=number>给出。
<pre><code># pprint_recursion.py

from pprint import pprint

local_data = ['a', 'b', 1, 2]
local_data.append(local_data)

print('id(local_data) =>', id(local_data))
pprint(local_data)
print(local_data)</pre></code>
在这个例子中，将列表local_data添加到它自己，创建一个递归引用。
<pre><code>$ python pprint_recursion.py
id(local_data) => 1874922808904
['a', 'b', 1, 2, <Recursion on list with id=1874922808904>]
['a', 'b', 1, 2, [...]]</pre></code>
## Limiting Nested Output
对于非常深的数据结构，输出可能不需要包含所有的细节。
数据可能无法正确格式化，格式化的文本可能太大无法管理，或者某些数据可能是无关的。
<pre><code># pprint_depth.py

from pprint import pprint
from pprint_data import data

pprint(data, depth=1)
pprint(data, depth=2)
pprint(data, depth=3)
pprint(data, depth=4)</pre></code>
使用深度参数来控制打印机递归的深度。输出中不包含的级别由省略号表示。
<pre><code>$ python pprint_depth.py
[(...), (...), (...), (...), (...)]
[(1, {...}), (2, {...}), (3, [...]), (4, [...]), (5, [...])]
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3, ['m', 'n']),
 (4, ['o', 'p', 'q']),
 (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3, ['m', 'n']),
 (4, ['o', 'p', 'q']),
 (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]</pre></code>
## Controlling Output Width
格式化文本的默认输出宽度为80列。要调整宽度，请使用宽度参数。
<pre><code># pprint_width.py

from pprint import pprint
from pprint_data import data

for width in [80, 5]:
    print('WIDTH = ', width)
    pprint(data, width=width)
    print()</pre></code>
当宽度太小，无法容纳格式化的数据结构时，如果这样做会引入无效的语法，那么这些行就不会被截断或封装。
<pre><code>$ python pprint_width.py
WIDTH =  80
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3, ['m', 'n']),
 (4, ['o', 'p', 'q']),
 (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]

WIDTH =  5
[(1,
  {'a': 'A',
   'b': 'B',
   'c': 'C',
   'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3,
  ['m',
   'n']),
 (4,
  ['o',
   'p',
   'q']),
 (5,
  ['r',
   's',
   'tu',
   'v',
   'x',
   'y',
   'z'])]</pre></code>
参数compact设置pprint()是否在每个单独的行上添加更多的数据，而不是跨行扩展复杂的数据结构。
<pre><code># pprint_compact.py

from pprint import pprint
from pprint_data import data

print('DEFAULT:')
pprint(data, compact=False)
print('\nCOMPACT:')
pprint(data, compact=True)</pre></code>
这个例子表明，当数据结构不适合一行时，它就会被拆分(就像数据列表中的第二项一样)。
当多个元素可以在一行上匹配时，就像第三个和第四个成员一样，它们是这样放置的。
<pre><code>$ python pprint_compact.py
DEFAULT:
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3, ['m', 'n']),
 (4, ['o', 'p', 'q']),
 (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]

COMPACT:
[(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
 (2,
  {'e': 'E',
   'f': 'F',
   'g': 'G',
   'h': 'H',
   'i': 'I',
   'j': 'J',
   'k': 'K',
   'l': 'L'}),
 (3, ['m', 'n']), (4, ['o', 'p', 'q']),
 (5, ['r', 's', 'tu', 'v', 'x', 'y', 'z'])]</pre></code>
 