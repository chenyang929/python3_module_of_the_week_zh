# enum -- Enumeration Type
enum模块定义了具有迭代和比较功能的枚举类型。它可以用来为值创建定义良好的符号，而不是使用文字整数或字符串。
## Creating Enumerations
一个新的枚举是通过创建一个继承自enum的子类并添加属性来定义的。
<pre><code># enum_create.py

import enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


print('\nMember name: {}'.format(BugStatus.wont_fix.name))
print('Member value: {}'.format(BugStatus.wont_fix.value))</pre></code>
当类被解析时，枚举的成员被转换为实例。每个实例都有对应于成员名称的名称属性，以及对应于类定义中分配给名称的值的值属性。
<pre><code>$ python enum_create.py

Member name: wont_fix
Member value: 4</pre></code>
## Iteration
在enum类上迭代生成枚举的单个成员。
<pre><code># enum_iterate.py

import enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))</pre></code>
成员的生成顺序是在类定义中声明的顺序。
<pre><code>$ python enum_iterate.py
new             = 7
incomplete      = 6
invalid         = 5
wont_fix        = 4
in_progress     = 3
fix_committed   = 2
fix_released    = 1</pre></code>
## Comparing Enums
因为枚举成员不是有序的，所以它们只支持身份(is)和等式(==)的比较。
<pre><code># enum_comparison.py

import enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


actual_state = BugStatus.wont_fix
desired_state = BugStatus.fix_released

print('Equality:',
      actual_state == desired_state,
      actual_state == BugStatus.wont_fix)
print('Identity:',
      actual_state is desired_state,
      actual_state is BugStatus.wont_fix)
print('Ordered by value:')
try:
    print('\n'.join('  ' + s.name for s in sorted(BugStatus)))
except TypeError as err:
    print('  Cannot sort: {}'.format(err))</pre></code>
大于和小于比较运算符会引发类型错误异常。
<pre><code>$ python enum_comparison.py
Equality: False True
Identity: False True
Ordered by value:
  Cannot sort: '<' not supported between instances of 'BugStatus' and 'BugStatus'</pre></code>
使用IntEnum类创建枚举可以使用排序操作。
<pre><code># enum_intenum.py

import enum


class BugStatus(enum.IntEnum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


print('Ordered by value:')
print('\n'.join(' ' + s.name for s in sorted(BugStatus)))</pre></code>
<pre><code>$ python enum_intenum.py
Ordered by value:
 fix_released
 fix_committed
 in_progress
 wont_fix
 invalid
 incomplete
 new</pre></code>
## Unique Enumeration Values
具有相同值的枚举成员被跟踪为同一成员对象的别名引用。别名不会在Enum的迭代器中引起重复的值。
<pre><code># enum_aliases.py

import enum


class BugStatus(enum.IntEnum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1

    by_design = 4
    closed = 1


for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))

print('\nSame: by_design is won_fix:', BugStatus.by_design is BugStatus.wont_fix)
print('Same: closed is fix_released:', BugStatus.closed is BugStatus.fix_released)</pre></code>
因为by_design和closed是其他成员的别名，所以在枚举中迭代时，它们不会单独出现在输出中。成员的规范名称是附加到该值上的第一个名称。
<pre><code>$ python enum_aliases.py
new             = 7
incomplete      = 6
invalid         = 5
wont_fix        = 4
in_progress     = 3
fix_committed   = 2
fix_released    = 1

Same: by_design is won_fix: True
Same: closed is fix_released: True</pre></code>
要要求所有成员都具有唯一的值，请使用@unique装饰器
<pre><code># enum_unique_enforce.py

import enum


@enum.unique
class BugStatus(enum.IntEnum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1

    by_design = 4
    closed = 1</pre></code>
在解释枚举类时，具有重复值的成员会触发ValueError异常。
<pre><code>$ python enum_unique_enforce.py
Traceback (most recent call last):
  File "enum_unique_enforce.py", line 7, in <module>
    class BugStatus(enum.IntEnum):
  File "C:\python3\lib\enum.py", line 834, in unique
    (enumeration, alias_details))
ValueError: duplicate values found in <enum 'BugStatus'>: by_design -> wont_fix, closed -> fix_released</pre></code>
## Creating Enumerations Programmatically
在某些情况下，用编程方式创建枚举更方便，而不是在类定义中硬编码它们。对于这些情况，Enum还支持将成员名称和值传递给类构造函数。
<pre><code># enum_programmatic_create.py


import enum

BugStatus = enum.Enum(
    value='BugStatus',
    names=('fix_released fix_committed in_progress '
           'wont_fix invalid incomplete new'),
)

print('Member: {}'.format(BugStatus.new))

print('\nAll members:')
for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))</pre></code>
值参数是枚举的名称，它用于构建成员的表示。名称参数列出枚举的成员。
当一个字符串被传递给名称参数时，它在空格和逗号上进行拆分，并将拆分后的字符串用作成员的名称，这些成员会自动分配以1开头递增的值。
<pre><code>$ python enum_programmatic_create.py
Member: BugStatus.new

All members:
fix_released    = 1
fix_committed   = 2
in_progress     = 3
wont_fix        = 4
invalid         = 5
incomplete      = 6
new             = 7</pre></code>
为了更好地控制与成员关联的值，可以用一个由两部分组成的元组序列或一个字典映射名称来替换名称字符串。
<pre><code># enum_programmatic_mapping.py


import enum


BugStatus = enum.Enum(
    value='BugStatus',
    names=[
        ('new', 7),
        ('incomplete', 6),
        ('invalid', 5),
        ('wont_fix', 4),
        ('in_progress', 3),
        ('fix_committed', 2),
        ('fix_released', 1),
    ],
)

print('All members:')
for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))</pre></code>
在本例中，给出了两部分元组的列表，而不是只包含成员名称的单个字符串。
这使得可以用与在enum_create.py中定义的版本相同的顺序来重新构造BugStatus枚举。
<pre><code>$ enum_programmatic_mapping.py
All members:
new             = 7
incomplete      = 6
invalid         = 5
wont_fix        = 4
in_progress     = 3
fix_committed   = 2
fix_released    = 1</pre></code>
## Non-integer Member Values
枚举成员值不限于整数。事实上，任何类型的对象都可以与成员关联。如果值是tuple，则将成员作为单个参数传递给__init__()。
<pre><code># enum_tuple_values.py

import enum


class BugStatus(enum.Enum):

    new = (7, ['incomplete',
               'invalid',
               'wont_fix',
               'in_progress'])
    incomplete = (6, ['new', 'wont_fix'])
    invalid = (5, ['new'])
    wont_fix = (4, ['new'])
    in_progress = (3, ['new', 'fix_committed'])
    fix_committed = (2, ['in_progress', 'fix_released'])
    fix_released = (1, ['new'])

    def __init__(self, num, transitions):
        self.num = num
        self.transitions = transitions

    def can_transition(self, new_state):
        return new_state.name in self.transitions


print('Name:', BugStatus.in_progress)
print('Value:', BugStatus.in_progress.value)
print('Custom attribute:', BugStatus.in_progress.transitions)
print('Using attribute:',
      BugStatus.in_progress.can_transition(BugStatus.new))</pre></code>
在本例中，每个成员值都是一个包含数字ID的元组(例如，可能存储在数据库中)和从当前状态转移的有效转换列表。
<pre><code>$ python enum_tuple_values.py
Name: BugStatus.in_progress
Value: (3, ['new', 'fix_committed'])
Custom attribute: ['new', 'fix_committed']
Using attribute: True</pre></code>
对于更复杂的情况，元组可能变得难以处理。由于成员值可以是任何类型的对象，因此可以使用字典，在这些情况下，有许多单独的属性来跟踪每个枚举值。
复杂的值被直接传递给__init__()作为除self之外的唯一参数。
<pre><code># enum_complex_values.py


import enum


class BugStatus(enum.Enum):

    new = {
        'num': 7,
        'transitions': [
            'incomplete',
            'invalid',
            'wont_fix',
            'in_progress',
        ],
    }
    incomplete = {
        'num': 6,
        'transitions': ['new', 'wont_fix'],
    }
    invalid = {
        'num': 5,
        'transitions': ['new'],
    }
    wont_fix = {
        'num': 4,
        'transitions': ['new'],
    }
    in_progress = {
        'num': 3,
        'transitions': ['new', 'fix_committed'],
    }
    fix_committed = {
        'num': 2,
        'transitions': ['in_progress', 'fix_released'],
    }
    fix_released = {
        'num': 1,
        'transitions': ['new'],
    }

    def __init__(self, vals):
        self.num = vals['num']
        self.transitions = vals['transitions']

    def can_transition(self, new_state):
        return new_state.name in self.transitions


print('Name:', BugStatus.in_progress)
print('Value:', BugStatus.in_progress.value)
print('Custom attribute:', BugStatus.in_progress.transitions)
print('Using attribute:',
      BugStatus.in_progress.can_transition(BugStatus.new))</pre></code>
此示例使用字典而不是元组表示与前面示例相同的数据。
<pre><code>$ python enum_complex_values.py
Name: BugStatus.in_progress
Value: {'num': 3, 'transitions': ['new', 'fix_committed']}
Custom attribute: ['new', 'fix_committed']
Using attribute: True</pre></code>

