# itertools -- Iterator Functions
> 目的：itertools模块包含一组用于处理序列数据集的函数。

itertools提供的功能受到类似功能编程语言特性的启发，比如Clojure、Haskell、APL和SML。它们的目的是快速和有效地使用内存，并且被连接在一起以表示更复杂的基于迭代的算法。

与使用列表的代码相比，基于迭代器的代码提供了更好的内存消耗特性。由于数据不是由迭代器产生的，直到需要时，所有的数据都不需要同时存储在内存中。这种“惰性”处理模型可以减少大数据集的交换和其他副作用，提高性能。

除了在itertools中定义的函数之外，本节中的示例还依赖于迭代的一些内置函数。
## Merging and Splitting Iterators
chain()函数的作用是:获取多个迭代器作为参数，返回一个迭代器，该迭代器生成所有输入的内容，就像它们来自一个迭代器一样。
```
# itertools_chain.py

from itertools import chain

for i in chain([1, 2, 3], ['a', 'b', 'c']):
    print(i, end=' ')
print()
```
chain()使处理多个序列而不构建一个大列表变得很容易。
```
$ python itertools_chain.py

1 2 3 a b c
```
如果要组合的iterables不是预先知道的，或者需要被延迟生成，chain.from_iterable()可以用来构建chain。
```
# itertools_chain_from_iterable.py

from itertools import chain


def make_iterables_to_chain():
    yield [1, 2, 3]
    yield ['a', 'b', 'c']


for i in chain.from_iterable(make_iterables_to_chain()):
    print(i, end=' ')
print()
```
```
$ python itertools_chain_from_iterable.py

1 2 3 a b c
```
内置函数zip()返回一个迭代器，该迭代器将多个迭代器的元素组合成元组。
```
# itertools_zip.py

for i in zip([1, 2, 3], ['a', 'b', 'c']):
    print(i)
```
与此模块中的其他函数一样，返回值是一个可迭代的对象，每次生成一个值。
```
$ python itertools_zip.py

(1, 'a')
(2, 'b')
(3, 'c')
```
当第一个输入迭代器耗尽时，zip()将停止。要处理所有输入，即使迭代器产生不同数量的值，要使用zip_longest()。
```
# itertools_zip_longest.py

from itertools import zip_longest

r1 = range(3)
r2 = range(2)

print('zip stops early:')
print(list(zip(r1, r2)))

r1 = range(3)
r2 = range(2)

print('\nzip_longest processes all of the values:')
print(list(zip_longest(r1, r2)))
```
默认情况下，zip_long()将任何丢失的值替换为None。使用fillvalue参数使用不同的替代值。
```
$ python itertools_zip_longest.py

zip stops early:
[(0, 0), (1, 1)]

zip_longest processes all of the values:
[(0, 0), (1, 1), (2, None)]
```
islice()函数的作用是:返回一个迭代器，该迭代器通过索引从输入迭代器中返回选定的项。
```
# itertools_islice.py

from itertools import islice

print('Stop at 5:')
for i in islice(range(100), 5):
    print(i, end=' ')
print('\n')

print('Start at 5, Stop at 10:')
for i in islice(range(100), 5, 10):
    print(i, end=' ')
print('\n')

print('By tens to 100:')
for i in islice(range(100), 0, 100, 10):
    print(i, end=' ')
print('\n')
```
islice()与列表的切片操作具有相同的参数:start、stop和step。start和step参数是可选的。
```
$ python itertools_islice.py

Stop at 5:
0 1 2 3 4

Start at 5, Stop at 10:
5 6 7 8 9

By tens to 100:
0 10 20 30 40 50 60 70 80 90
```
tee()函数的作用是:根据一个原始输入返回几个(默认为2)独立的迭代器。
```
# itertools_tee.py

from itertools import islice, tee, count

r = islice(count(), 5)
i1, i2 = tee(r)

print('i1:', list(i1))
print('i2:', list(i2))
```
tee()的语义类似于Unix tee实用程序，该实用程序重复从输入中读取的值，并将其写入一个命名文件和标准输出。tee()返回的迭代器可用于将相同的数据集提供给多个并行处理的算法。
```
$ python itertools_tee.py

i1: [0, 1, 2, 3, 4]
i2: [0, 1, 2, 3, 4]
```
tee()创建的新迭代器共享其输入，因此在创建新迭代器之后不应该使用原始迭代器。
```
# itertools_tee_error.py

from itertools import islice, count, tee

r = islice(count(), 5)
i1, i2 = tee(r)

print('r:', end=' ')
for i in r:
    print(i, end=' ')
    if i > 1:
        break
print()

print('i1:', list(i1))
print('i2:', list(i2))
```
如果从原始输入中使用值，新的迭代器将不会产生这些值:
```
$ python itertools_tee_error.py

r: 0 1 2
i1: [3, 4]
i2: [3, 4]
```
## Converting Inputs
内置函数map()函数的作用是:返回一个迭代器，该迭代器在输入迭代器的值上调用一个函数，并返回结果。当耗尽任何输入迭代器时，它将停止。
```
# itertools_map.py

def times_two(x):
    return 2 * x


def multiply(x, y):
    return (x, y, x * y)


print('Doubles:')
for i in map(times_two, range(5)):
    print(i)

print('\nMultiples:')
r1 = range(5)
r2 = range(5, 10)
for i in map(multiply, r1, r2):
    print('{:d} * {:d} = {:d}'.format(*i))

print('\nStopping:')
r1 = range(5)
r2 = range(2)
for i in map(multiply, r1, r2):
    print(i)
```
在第一个例子中，lambda函数将输入值乘以2。在第二个示例中，lambda函数将两个参数相乘，从不同的迭代器中获取，并返回一个带有原始参数和计算值的元组。第三个示例在生成两个元组之后停止，因为第二个范围已经耗尽。
```
$ python itertools_map.py

Doubles:
0
2
4
6
8

Multiples:
0 * 5 = 0
1 * 6 = 6
2 * 7 = 14
3 * 8 = 24
4 * 9 = 36

Stopping:
(0, 0, 0)
(1, 1, 1)
```
starmap()函数类似于map()，但它不是使用多个迭代器构造一个tuple，而是使用*语法将单个迭代器中的项作为映射函数的参数进行分割。
```
# itertools_starmap.py

from itertools import starmap

values = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]

for i in starmap(lambda x, y: (x, y, x * y), values):
    print('{} * {} = {}'.format(*i))
```
映射到map()的映射函数称为f(i1, i2)，传递给starmap()的映射函数称为f(*i)。
```
$ python itertools_starmap.py

0 * 5 = 0
1 * 6 = 6
2 * 7 = 14
3 * 8 = 24
4 * 9 = 36
```
## Producing New Values
count()函数的作用是:返回一个迭代器，它可以无限地生成连续的整数。第一个数字可以作为参数传递(默认值为0)。没有上限参数(请参阅内置的range()以获得对结果集的更多控制)。
```
# itertools_count.py

from itertools import count

for i in zip(count(1), ['a', 'b', 'c']):
    print(i)
```
这个示例之所以停止，是因为使用了list参数。
```
$ python itertools_count.py

(1, 'a')
(2, 'b')
(3, 'c')
```
count()的start和step参数可以是任何可以相加的数值。
```
# itertools_count_step.py

import fractions
from itertools import count

start = fractions.Fraction(1, 3)
step = fractions.Fraction(1, 3)

for i in zip(count(start, step), ['a', 'b', 'c']):
    print('{}: {}'.format(*i))
```
在本例中，起始点和步骤是来自分数模块的分数对象。
```
$ python itertools_count_step.py

1/3: a
2/3: b
1: c
```
cycle()函数的作用是:返回一个迭代器，该迭代器重复无限给定的参数的内容。因为它必须记住输入迭代器的全部内容，所以如果迭代器很长，它可能会消耗相当多的内存。
```
# itertools_cycle.py

from itertools import cycle

for i in zip(range(7), cycle(['a', 'b', 'c'])):
    print(i)
```
在本例中，计数器变量用于在几个循环之后跳出循环。
```
$ python itertools_cycle.py

(0, 'a')
(1, 'b')
(2, 'c')
(3, 'a')
(4, 'b')
(5, 'c')
(6, 'a')
```
repeat()函数的作用是:返回一个迭代器，每次访问该迭代器时都会产生相同的值。
```
# itertools_repeat.py

from itertools import repeat

for i in repeat('over-and-over', 5):
    print(i)
```
repeat()返回的迭代器始终返回数据，除非提供了可选的times参数来限制数据。
```
$ python itertools_repeat.py

over-and-over
over-and-over
over-and-over
over-and-over
over-and-over
```
当需要将不变量值与其他迭代器的值一起包含时，将repeat()与zip()或map()组合在一起是很有用的。
```
# itertools_repeat_zip.py

from itertools import count, repeat

for i, s in zip(count(), repeat('over-and-over', 5)):
    print(i, s)
```
在本例中，计数器值与repeat()返回的常量相结合。
```
$ python itertools_repeat_zip.py

0 over-and-over
1 over-and-over
2 over-and-over
3 over-and-over
4 over-and-over
```
这个示例使用map()将范围为0到4的数字乘以2。
```
# itertools_repeat_map.py

from itertools import repeat

for i in map(lambda x, y: (x, y, x * y), repeat(2), range(5)):
    print('{:d} * {:d} = {:d}'.format(*i))
```
repeat()迭代器不需要显式地限制，因为map()在任何输入结束时停止处理，range()只返回5个元素。
```
$ python itertools_repeat_map.py

2 * 0 = 0
2 * 1 = 2
2 * 2 = 4
2 * 3 = 6
2 * 4 = 8
```
## Filtering
dropwhile()函数的作用是:返回一个迭代器，当条件第一次为false时，该迭代器产生输入迭代器的元素。
```
# itertools_dropwhile.py

from itertools import dropwhile


def should_drop(x):
    print('Testing:', x)
    return x < 1


for i in dropwhile(should_drop, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)
```
dropwhile()不会过滤输入的每一项;第一次条件为false后，返回输入中的所有剩余项。
```
$ python itertools_dropwhile.py

Testing: -1
Testing: 0
Testing: 1
Yielding: 1
Yielding: 2
Yielding: -2
```
dropwhile()的反面是takewhile()。它返回一个迭代器，该迭代器返回输入迭代器中的项目，只要测试函数返回true。
```
# itertools_takewhile.py

from itertools import takewhile


def should_take(x):
    print('Testing:', x)
    return x < 2


for i in takewhile(should_take, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)
```
当should_take()返回False时，takewhile()停止处理输入。
```
$ python itertools_takewhile.py

Testing: -1
Yielding: -1
Testing: 0
Yielding: 0
Testing: 1
Yielding: 1
Testing: 2
```
内置函数filter()返回一个迭代器，它只包含测试函数返回true的项。
```
# itertools_filter.py


def check_item(x):
    print('Testing:', x)
    return x < 1


for i in filter(check_item, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)
```
filter()与dropwhile()和takewhile()不同，因为每个条目在返回之前都要进行测试。
```
$ python itertools_filter.py

Testing: -1
Yielding: -1
Testing: 0
Yielding: 0
Testing: 1
Testing: 2
Testing: -2
Yielding: -2
```
filterfalse()返回一个迭代器，该迭代器只包含测试函数返回false的项。
```
# itertools_filterfalse.py

from itertools import filterfalse


def check_item(x):
    print('Testing:', x)
    return x < 1


for i in filterfalse(check_item, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)
```
check_item()中的测试表达式是相同的，因此这个带有filterfalse()的示例中的结果与前面示例中的结果相反。
```
$ python itertools_filterfalse.py

Testing: -1
Testing: 0
Testing: 1
Yielding: 1
Testing: 2
Yielding: 2
Testing: -2
```
compress()提供了另一种筛选可迭代内容的方法。它不调用函数，而是使用另一个可迭代的值来指示何时接受一个值以及何时忽略它。
```
# itertools_compress.py

from itertools import compress, cycle

every_third = cycle([False, False, True])
data = range(1, 10)

for i in compress(data, every_third):
    print(i, end=' ')
print()
```
第一个参数是可迭代处理的数据，第二个参数是可迭代生成布尔值的选择器，该布尔值指示从数据输入中获取哪些元素(true值导致生成值，false值导致忽略值)。
```
$ python itertools_compress.py

3 6 9
```
## Grouping Data
groupby()函数返回一个迭代器，该迭代器生成由公共键组织的值集。这个例子说明了基于属性对相关值进行分组。
```
# itertools_groupby_seq.py

import functools
from itertools import groupby, cycle, islice, count
import operator
import pprint


@functools.total_ordering
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)


# Create a dataset of Point instances
data = list(map(Point,
                cycle(islice(count(), 3)),
                islice(count(), 7)))
print('Data:')
pprint.pprint(data, width=35)
print()

# Try to group the unsorted data based on X values
print('Grouped, unsorted:')
for k, g in groupby(data, operator.attrgetter('x')):
    print(k, list(g))
print()

# Sort the data
data.sort()
print('Sorted:')
pprint.pprint(data, width=35)
print()

# Group the sorted data based on X values
print('Grouped, sorted:')
for k, g in groupby(data, operator.attrgetter('x')):
    print(k, list(g))
print()
```
输入序列需要对键值进行排序，以便按照预期进行分组。
```
$ python itertools_groupby_seq.py

Data:
[(0, 0),
 (1, 1),
 (2, 2),
 (0, 3),
 (1, 4),
 (2, 5),
 (0, 6)]

Grouped, unsorted:
0 [(0, 0)]
1 [(1, 1)]
2 [(2, 2)]
0 [(0, 3)]
1 [(1, 4)]
2 [(2, 5)]
0 [(0, 6)]

Sorted:
[(0, 0),
 (0, 3),
 (0, 6),
 (1, 1),
 (1, 4),
 (2, 2),
 (2, 5)]

Grouped, sorted:
0 [(0, 0), (0, 3), (0, 6)]
1 [(1, 1), (1, 4)]
2 [(2, 2), (2, 5)]
```
## Combining Inputs
accumulate()函数的作用是:处理可迭代的输入，将第n和n+1项传递给函数，生成返回值，而不是任何一个输入。用于合并两个值的默认函数添加了它们，因此accumulate()可以用于生成一系列数值输入的累积和。
```
# itertools_accumulate.py

from itertools import accumulate

print(list(accumulate(range(5))))
print(list(accumulate('abcde')))
```
当与非数值序列一起使用时，结果取决于将两个项“相加”在一起的含义。该脚本中的第二个示例显示，当accumulate()接收一个字符串输入时，每个响应都是该字符串的一个逐渐长的前缀。
```
$ python itertools_accumulate.py

[0, 1, 3, 6, 10]
['a', 'ab', 'abc', 'abcd', 'abcde']
```
可以将accumul()与其他任何需要两个输入值以实现不同结果的函数结合在一起。
```
# itertools_accumulate_custom.py

from itertools import accumulate


def f(a, b):
    print(a, b)
    return b + a + b


print(list(accumulate('abcde', f)))
```
这个示例以一种使一系列(荒谬的)回文的方式组合字符串值。调用f()时的每一步，它都打印出accumulate()传递给它的输入值。
```
$ python itertools_accumulate_custom.py

a b
bab c
cbabc d
dcbabcd e
['a', 'bab', 'cbabc', 'dcbabcd', 'edcbabcde']
```
迭代多个序列的嵌套for循环通常可以用product()替换，product()生成一个可迭代的值，该值是输入值集合的笛卡尔积。
```
# itertools_product.py

from itertools import product, chain
import pprint

FACE_CARDS = ('J', 'Q', 'K', 'A')
SUITS = ('H', 'D', 'C', 'S')

DECK = list(
    product(
        chain(range(2, 11), FACE_CARDS),
        SUITS,
    )
)

for card in DECK:
    print('{:>2}{}'.format(*card), end=' ')
    if card[1] == SUITS[-1]:
        print()
```
product()生成的值是元组，其中每个迭代的成员作为参数以其传递的顺序传入。返回的第一个元组包含每个可迭代的第一个值。传递给product()的最后一个可迭代对象首先被处理，然后是下一个，最后一个，依此类推。结果是返回值是基于第一个可迭代的，然后是下一个可迭代的，等等。

在本例中，卡片按值排序，然后按suit排序。
```
$ python itertools_product.py

 2H  2D  2C  2S
 3H  3D  3C  3S
 4H  4D  4C  4S
 5H  5D  5C  5S
 6H  6D  6C  6S
 7H  7D  7C  7S
 8H  8D  8C  8S
 9H  9D  9C  9S
10H 10D 10C 10S
 JH  JD  JC  JS
 QH  QD  QC  QS
 KH  KD  KC  KS
 AH  AD  AC  AS
 ```
 要更改卡片的顺序，请更改product()参数的顺序。
 ```
 # itertools_product_ordering.py

from itertools import product, chain
import pprint

FACE_CARDS = ('J', 'Q', 'K', 'A')
SUITS = ('H', 'D', 'C', 'S')

DECK = list(
    product(
        SUITS,
        chain(range(2, 11), FACE_CARDS),
    )
)

for card in DECK:
    print('{:>2}{}'.format(card[1], card[0]), end=' ')
    if card[1] == FACE_CARDS[-1]:
        print()
```
本例中的打印循环查找Ace卡片，而不是spade suit，然后添加一个换行符来分解输出。
```
$ python itertools_product_ordering.py

 2H  3H  4H  5H  6H  7H  8H  9H 10H  JH  QH  KH  AH
 2D  3D  4D  5D  6D  7D  8D  9D 10D  JD  QD  KD  AD
 2C  3C  4C  5C  6C  7C  8C  9C 10C  JC  QC  KC  AC
 2S  3S  4S  5S  6S  7S  8S  9S 10S  JS  QS  KS  AS
```
要计算序列本身的乘积，请指定输入应该重复多少次。
```
# itertools_product_repeat.py

from itertools import product


def show(iterable):
    for i, item in enumerate(iterable, 1):
        print(item, end=' ')
        if (i % 3) == 0:
            print()
    print()


print('Repeat 2:\n')
show(list(product(range(3), repeat=2)))

print('Repeat 3:\n')
show(list(product(range(3), repeat=3)))
```
因为重复一个迭代就像传递相同的迭代次数，每个由product()产生的元组将包含多个与repeat计数器相等的项。
```
$ python itertools_product_repeat.py

Repeat 2:

(0, 0) (0, 1) (0, 2)
(1, 0) (1, 1) (1, 2)
(2, 0) (2, 1) (2, 2)

Repeat 3:

(0, 0, 0) (0, 0, 1) (0, 0, 2)
(0, 1, 0) (0, 1, 1) (0, 1, 2)
(0, 2, 0) (0, 2, 1) (0, 2, 2)
(1, 0, 0) (1, 0, 1) (1, 0, 2)
(1, 1, 0) (1, 1, 1) (1, 1, 2)
(1, 2, 0) (1, 2, 1) (1, 2, 2)
(2, 0, 0) (2, 0, 1) (2, 0, 2)
(2, 1, 0) (2, 1, 1) (2, 1, 2)
(2, 2, 0) (2, 2, 1) (2, 2, 2)
```
permutation()函数从输入可迭代的组合中生成给定长度的可能排列。它默认生成所有排列的完整集合。
```
# itertools_permutations.py

from itertools import permutations


def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print(''.join(item), end=' ')
    print()


print('All permutations:\n')
show(permutations('abcd'))

print('\nPairs:\n')
show(permutations('abcd', r=2))
```
使用r参数来限制返回的单个排列的长度和数量。
```
$ python itertools_permutations.py

All permutations:

abcd abdc acbd acdb adbc adcb
bacd badc bcad bcda bdac bdca
cabd cadb cbad cbda cdab cdba
dabc dacb dbac dbca dcab dcba

Pairs:

ab ac ad
ba bc bd
ca cb cd
da db dc
```
要将值限制为唯一的组合而不是排列，请使用combination()。只要输入的成员是唯一的，输出就不会包含任何重复的值。
```
# itertools_combinations.py

from itertools import combinations


def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print(''.join(item), end=' ')
    print()


print('Unique pairs:\n')
show(combinations('abcd', r=2))
```
与排列不同，需要对combinations()进行r参数。
```
$ python itertools_combinations.py

Unique pairs:

ab ac ad
bc bd
cd
```
虽然combination()不重复单个输入元素，但有时考虑包含重复元素的组合是有用的。对于这些情况，使用combinations_with_replacement()。
```
# itertools_combinations_with_replacement.py

from itertools import combinations_with_replacement


def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print(''.join(item), end=' ')
    print()


print('Unique pairs:\n')
show(combinations_with_replacement('abcd', r=2))
```
在这个输出中，每个输入项都与自己以及输入序列的所有其他成员配对。
```
$ python itertools_combinations_with_replacement.py

Unique pairs:

aa ab ac ad
bb bc bd
cc cd
dd
```

