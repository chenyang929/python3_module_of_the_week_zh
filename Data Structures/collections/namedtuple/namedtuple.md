# namedtuple -- Tuple Subclass with Named Field
标准元组使用数字索引访问其成员。
<pre><code># collections_tuple.py

bob = ('Bob', 30, 'male')
print('Representation:', bob)

jane = ('Jane', 29, 'female')
print('\nField by index:', jane[0])

print('\nFields by index:')
for p in [bob, jane]:
    print('{} is a {} year old {}'.format(*p))</pre></code>
对于简单的使用，tuple是方便的。
<pre><code>$ python collections_tuple.py
Representation: ('Bob', 30, 'male')

Field by index: Jane

Fields by index:
Bob is a 30 year old male
Jane is a 29 year old female</pre></code>
相反，要记住每个值应该使用哪个索引可能会导致错误，特别是如果tuple有很多字段，并且在使用它的地方还很远。一个namedtuple分配给每个成员的名称，以及数值索引。
## Defining
namedtuple实例与常规元组一样具有内存效率，因为它们没有每个实例的字典。每一种名称都由它自己的类表示，它是通过使用namedtuple()工厂函数创建的。参数是新类的名称和包含元素名称的字符串。
<pre><code># collections_namedtuple_person.py

import collections

Person = collections.namedtuple('Person', 'name age')

bob = Person(name='Bob', age=30)
print('\nRepresentation:', bob)

jane = Person(name='Jane', age=29)
print('\nField by name:', jane.name)

print('\nFields by index:')
for p in [bob, jane]:
    print('{} is {} years old'.format(*p))</pre></code>
如示例所示，通过使用点符号(object .attr)以及使用标准元组的位置索引来访问namedtuple的字段都是可能的。
<pre><code>$ python collections_namedtuple_person.py

Representation: Person(name='Bob', age=30)

Field by name: Jane

Fields by index:
Bob is 30 years old
Jane is 29 years old</pre></code>
就像普通的tuple一样，一个namedtuple是不可变的。这个限制允许tuple实例具有一致的散列值，这使得可以将它们作为字典中的键并包含在集合中。
<pre><code># collections_namedtuple_immutable.py

import collections

Person = collections.namedtuple('Person', 'name age')

pat = Person(name='Pat', age=12)
print('\nRepresentation:', pat)

pat.age = 21</pre></code>
试图通过其命名属性更改一个值会导致一个AttributeError。
<pre><code>$ python collections_namedtuple_immutable.py
Representation: Person(name='Pat', age=12)
Traceback (most recent call last):
  File "collections_namedtuple_immutable.py", line 10, in <module>
    pat.age = 21
AttributeError: can't set attribute</pre></code>
## Invalid Field Names
如果字段名称重复或与Python关键字冲突，则是无效的。
<pre><code># collections_namedtuple_bad_fields.py

import collections

try:
    collections.namedtuple('Person', 'name class age')
except ValueError as err:
    print(err)

try:
    collections.namedtuple('Person', 'name age age')
except ValueError as err:
    print(err)</pre></code>
当字段名被解析时，无效的值会导致ValueError异常。
<pre><code>$ python collections_namedtuple_bad_fields.py
Type names and field names cannot be a keyword: 'class'
Encountered duplicate field name: 'age'</pre></code>
在基于程序控制之外的值创建namedtuple的情况(例如，为了表示数据库查询返回的行，而在前面不知道模式)，应该将重命名选项设置为True，以便重命名无效字段。
<pre><code># collections_namedtuple_rename.py

import collections

with_class = collections.namedtuple('Person', 'name class age', rename=True)
print(with_class._fields)

two_ages = collections.namedtuple('Person', 'name age age', rename=True)
print(two_ages._fields)</pre></code>
重命名字段的新名称依赖于tuple中的索引。
<pre><code>$ python collections_namedtuple_rename.py
('name', '_1', 'age')
('name', 'age', '_2')</pre></code>
## Special Attributes
namedtuple提供了用于处理子类和实例的几个有用的属性和方法。所有这些内置属性都有一个带有下划线(_)前缀的名称，在大多数Python程序中，这都表示一个私有属性。然而，对于namedtuple，前缀的目的是解决名称与用户提供的属性名称的冲突。
传递给namedtuple的字段的名称将在_fields属性中保存。
可以使用_asdict()将namedtuple实例转换为OrderedDict实例。
<pre><code># collections_namedtuple_asdict.py

import collections

Person = collections.namedtuple('Person', 'name age')

bob = Person(name='Bob', age=30)
print('Representation:', bob)
print('As Dictionary:', bob._asdict())</pre></code>
OrderedDict的键与namedtuple的字段相同。
<pre><code>$ python collections_namedtuple_asdict.py
Representation: Person(name='Bob', age=30)
As Dictionary: OrderedDict([('name', 'Bob'), ('age', 30)])</pre></code>
_replace()方法构建一个新的实例，替换某些字段的值。
<pre><code># collections_namedtuple_replace.py

import collections

Person = collections.namedtuple('Person', 'name age')

bob = Person(name='Bob', age=30)
print('\nBefore:', bob)
bob2 = bob._replace(name='Robert')
print('After:', bob2)
print('Same?:', bob is bob2)</pre></code>
因为namedtuple实例是不可变的，该方法实际上返回一个新对象。
<pre><code>$ python collections_namedtuple_replace.py

Before: Person(name='Bob', age=30)
After: Person(name='Robert', age=30)
Same?: False</pre></code>

