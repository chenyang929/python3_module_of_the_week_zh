# defaultdict -- Missing Keys Return a Default Value
标准字典包括用于检索值的方法setdefault()，如果值不存在，则建立默认值。相反，defaultdict让调用方在初始化容器时指定默认值
<pre><code># collections_defaultdict.py

import collections


def default_factory():
    return 'default value'


d = collections.defaultdict(default_factory, foo='bar')
print('d:', d)
print('foo =>', d['foo'])
print('bar =>', d['bar'])</pre></code>
只要适用于所有键都具有相同的缺省值，此方法就能正常工作。如果默认值是用于聚合或累积值的类型，比如list、set、甚至int，那么它可能特别有用。
<pre><code>$ python collections_defaultdict.py
d: defaultdict(<function default_factory at 0x00000230C8FBB8C8>, {'foo': 'bar'})
foo => bar
bar => default value</pre></code>
### See also
+ [defaultdict_example](https://docs.python.org/3.6/library/collections.html#defaultdict-examples) -- Examples of using defaultdict from the standard library documentation.
+ [Evolution of Default Dictionaries in Python](http://jtauber.com/blog/2008/02/27/evolution_of_default_dictionaries_in_python/) -- James Tauber’s discussion of how defaultdict relates to other means of initializing dictionaries.