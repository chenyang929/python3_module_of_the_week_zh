# string -- Text Constans and Templates
用途：包含用于处理文本的常量和类

字符串模块可以追溯到最早的Python版本。以前在这个模块中实现的许多函数已经被移动到str对象的方法中了。字符串模块保留几个有用的常量和类，用于与str对象一起工作。这次讨论将集中在他们身上。

## Functions
函数capwords()将字符串中的所有英文单词首字母转换成大写。</br>
[string_capwords.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/string_src/string_capwords.py)
<pre><code>import string

s = "人生苦短, we use pytHon."
print(s)
print(string.capwords(s))</code></pre>
<pre><code>$ python string_capwords.py
人生苦短, we use python.
人生苦短, We Use Python.</code></pre>
查看string.capwords()函数源码可知，其将字符串分开成单词列表，然后将每个单词变成只有首字母大写形式，最后把列表拼接成字符串。
<pre><code>def capwords(s, sep=None):
    return (sep or ' ').join(x.capitalize() for x in s.split(sep))</code></pre>
## Templates
在[PEP 292](https://www.python.org/dev/peps/pep-0292/)中添加了字符串模板，作为内置插值语法的替代品。使用字符串模板插值，变量用$(例如$ var)前缀来标识。或置于大括号内(例如 ${var})。</br>
[string_template.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/string_src/string_template.py)
<pre><code>import string

values = {"var": "foo"}

t = string.Template("""
Variable         : $var
Escape           : $$
Variable in text : ${var}iable
""")
print("TEMPLATE:", t.substitute(values))

s = """
Variable         : %(var)s
Escape           : %%
Variable in text : %(var)siable
"""
print("INTERPOLATION:", s % values)

p = """
Variable         : {var}
Escape           : {{}}
Variable in text : {var}iable
"""
print("FORMAT:", p.format(**values))</code></pre>
<pre><code>$ python string_templates.py
TEMPLATE:
Variable         : foo
Escape           : $
Variable in text : fooiable

INTERPOLATION:
Variable         : foo
Escape           : %
Variable in text : fooiable

FORMAT:
Variable         : foo
Escape           : {}
Variable in text : fooiable</code></pre>
在前两种情况下，触发器字符($ or %)可以通过重复两次来避免格式化。对于format语法，"{"和"}"都需要通过重复它们来避免格式化。
字符串模板插值和format格式字符串之间的一个关键区别是，前者没有格式化选项可用。例如，无法控制表示浮点值的位数。
不过，好处是使用safe_substitute()方法可以避免模板所需要的所有值作为参数提供的异常。</br>
[string_template_missing.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/string_src/string_template_missing.py)
<pre><code>import string

values = {"var": "foo"}

t = string.Template("$var is here but $missing is not provided")
try:
    print("substitute():", t.substitute(values))
except KeyError as err:
    print("ERROR:", str(err))
print("safe_substitute():", t.safe_substitute(values))</code></pre>
<pre><code>ERROR: 'missing'
safe_substitute(): foo is here but $missing is not provided</code></pre>
由于在vlaues字典中没有"missing"的对应值，因此substitute()引发异常KeyError。safe_substitute()没有引发错误，而是捕获它并将变量表达式单独留在文本中。
## Advanced Templates
通过调整用于在模板主体中查找变量名的正则表达式模式，可以更改字符串模板的默认语法。一种简单的方法是改变分隔符和idpattern类的属性。</br>
[string_template_advanced.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/string_src/string_template_advanced.py)
<pre><code>import string

class MyTemplate(string.Template):
    delimiter = "%"
    idpattern = "[a-z]+_[a-z]+"

template_text = """
Delimiter : %%
Replaced  : %with_underscore
Ignored   : %notunderscored
"""
d = {
    "with_underscore": "replaced",
    "notunderscored": "not replaced"
}
t = MyTemplate(template_text)
print("Modified ID pattern:")
print(t.safe_substitute(d))</code></pre>
<pre><code>$ python string_template_advanced.py
Modified ID pattern:

Delimiter : %
Replaced  : replaced
Ignored   : %notunderscored</code></pre>
在本例中，替换规则发生了更改，分隔符是%而不是$，变量名必须在中间的某处包含一个下划线。%notunderscored没有被替换，因为它不包括下划线。
对于更复杂的更改，可以重写pattern属性并定义一个全新的正则表达式。所提供的模式必须包含4个命名组，用于捕获转义分隔符、命名变量、变量名称的支撑版本和无效的分隔符模式。</br>
[string_template_defaultpattern.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/string_src/string_template_defaultpattern.py)
<pre><code>import string

t = string.Template("$var")
print(t.pattern.pattern)</code></pre>
<pre><code>$ python string_template_defaultpattern.py
\$(?:
  (?P<escaped>\$) |                # 两个分隔符的转义序列
  (?P<named>[_a-z][_a-z0-9]*)    | # 分隔符和Python标识符
  {(?P<braced>[_a-z][_a-z0-9]*)} | # 分隔符和加固标识符
  (?P<invalid>)                    # 其他不规范的分隔符
)</code></pre>
下面这个例子定义了一个新模式，以创建一个新的模板类型，使用{{var}}作为变量语法。</br>
[string_template_newsyntax.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/string_src/string_template_newsyntax.py)
<pre><code>import re
import string

class MyTemplate(string.Template):
    delimiter = "{{"
    pattern = r"""
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    """
t = MyTemplate("""
{{{{
{{var}}
""")
print("MATCHES:", t.pattern.findall(t.template))
print("SUBSTITUTED:", t.safe_substitute(var="replacement"))</code></pre>
<pre><code>$ python string_template_newsyntax.py
MATCHES: [('{{', '', '', ''), ('', 'var', '', '')]
SUBSTITUTED:
{{
replacement</code></pre>
命名和支撑模式必须单独提供，即使它们是相同的。
## Formatter
Formatter类实现了与str的format()方法相同的布局规范语言，其特性包括类型强制、对齐、属性和字段引用、命名和位置模板参数，以及类型特定的格式选项。大多数时候，format()方法是这些特性的一个更方便的接口，但是对于需要变化的情况，Formatter作为一种构建子类的方法。
## Constants
字符串模块包含了一些与ASCII和数值字符集相关的常量。</br>
[string_constances.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/string_src/string_constances.py)
<pre><code>import inspect
import string

def is_str(value):
    return isinstance(value, str)

for name, value in inspect.getmembers(string, is_str):
    if name.startswith("_"):
        continue
    print("%s=%r\n" % (name, value))</code></pre>
<pre><code>$ python string_constances.py
ascii_letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

ascii_lowercase='abcdefghijklmnopqrstuvwxyz'

ascii_uppercase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

digits='0123456789'

hexdigits='0123456789abcdefABCDEF'

octdigits='01234567'

printable='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

whitespace=' \t\n\r\x0b\x0c'</code></pre>
这些常量在处理ASCII数据时很有用，但由于在某种形式的Unicode中遇到非ASCII文本越来越常见，因此它们的应用程序非常有限。


