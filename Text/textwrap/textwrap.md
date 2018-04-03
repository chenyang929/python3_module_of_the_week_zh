# textwrap -- Formatting Text Paragraphs
用途：通过调整段落中的换行符来格式化文本。

textwrap模块可用于在需要预打印的情况下为输出格式化文本。它提供类似于在许多文本编辑器和文字处理器中发现的段落包装或填充功能类似的编程功能

## Example Data
本节中的示例使用模块[textwrap_example.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/textwrap_src/textwrap_example.py)，其中包含一个字符串sample_text。
<pre><code># textwrap_example.py

sample_text = """
    The textwrap module can be used to format text for output in
    situations where pretty-printing is desired.  It offers
    programmatic functionality similar to the paragraph wrapping
    or filling features found in many text editors.
    """</code></pre>
## Filling Paragraphs
fill()函数的作用是：将文本作为输入，并生成格式化的文本作为输出。<br>
[textwrap_fill.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/textwrap_src/textwrap_fill.py)
<pre><code># textwrap_fill.py
import textwrap
from textwrap_example import sample_text

print(textwrap.fill(sample_text, width=50))</code></pre>
<pre><code>$ python textwrap_fill.py
     The textwrap module can be used to format
text for output in     situations where pretty-
printing is desired.  It offers     programmatic
functionality similar to the paragraph wrapping
or filling features found in many text editors.</code></pre>
输出结果并不理想。文本现在是左对齐，但第一行保留了缩进,并且在原始文本的每一行开头都嵌入了空格。
## Removing Existing Indentation
前面的例子输出中混有额外的空格，所以输出不太干净。用dedent()从示例文本中的所有行中删除公共的空白前缀，可以产生更好的结果，并允许使用docstring或从Python代码直接嵌入多行字符串，同时删除代码本身的格式。示例字符串有一个人工缩进级别，用于说明该特性。<br>
[textwrap_dedent.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/textwrap_src/textwrap_dedent.py)
<pre><code># textwrap_dedent.py
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text)
print("Dedented:")
print(dedented_text)</code></pre>
<pre><code>$ python textwrap_dedent.py
Dedented:

The textwrap module can be used to format text for output in
situations where pretty-printing is desired.  It offers
programmatic functionality similar to the paragraph wrapping
or filling features found in many text editors.</code></pre>
由于“dedent”是“缩进”的反义词，因此结果是一个文本块，从每一行删除了公共初始空格。如果一行的缩进比另一行多，一些空格将不会被删除。
## Combining Dedent and Fill
下面可以将去掉缩进的文本和不同的width值一起作为参数传递给fill()函数。<br>
[textwrap_fill_width.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/textwrap_src/textwrap_fill_width.py)
<pre><code># textwrap_fill_width.py
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text).strip()
for width in [45, 60]:
    print("{} Columns:\n".format(width))
    print(textwrap.fill(dedented_text, width=width))
    print()</code></pre>
<pre><code>$ python textwrap_fill_width.py
45 Columns:

The textwrap module can be used to format
text for output in situations where pretty-
printing is desired.  It offers programmatic
functionality similar to the paragraph
wrapping or filling features found in many
text editors.

60 Columns:

The textwrap module can be used to format text for output in
situations where pretty-printing is desired.  It offers
programmatic functionality similar to the paragraph wrapping
or filling features found in many text editors.</code></pre>
这就产生了指定宽度的输出。
## Indenting Blocks
使用indent()函数将一致的前缀文本添加到字符串中的所有行中。这个例子格式化了相同的示例文本，就像在回复中引用的电子邮件的一部分一样，使用>作为每一行的前缀。<br>
[textwrap_indent.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/textwrap_src/textwrap_indent.py)
<pre><code># textwrap_indent.py
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text)
wrapped = textwrap.fill(dedented_text, width=50)
wrapped += "\n\nSecond paragraph after a blank line."
final = textwrap.indent(wrapped, "> ")

print("Quoted block:\n")
print(final)</code></pre>
<pre><code>$ python textwrap_indent.py
Quoted block:

>  The textwrap module can be used to format text
> for output in situations where pretty-printing is
> desired.  It offers programmatic functionality
> similar to the paragraph wrapping or filling
> features found in many text editors.

> Second paragraph after a blank line.</code></pre>
要控制哪些行接收新前缀，可将一个回调作为谓词参数传递给indent()。该调用将依次调用每一行文本，并在返回值为true的行中添加前缀。<br>
[textwrap_indent_predicate.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/textwrap_src/textwrap_indent_predicate.py)
<pre><code># textwrap_indent_predicate.py
import textwrap
from textwrap_example import sample_text

def should_indent(line):
    print("Indent {!r}?".format(line))
    return len(line.strip()) % 2 == 0

dedented_text = textwrap.dedent(sample_text)
wrapped = textwrap.fill(dedented_text, width=50)
final = textwrap.indent(wrapped, "EVEN", predicate=should_indent)

print("\nQuoted block:\n")
print(final)</code></pre>
<pre><code>$ python textwrap_indent_predicate.py
Indent ' The textwrap module can be used to format text\n'?
Indent 'for output in situations where pretty-printing is\n'?
Indent 'desired.  It offers programmatic functionality\n'?
Indent 'similar to the paragraph wrapping or filling\n'?
Indent 'features found in many text editors.'?

Quoted block:

EVEN The textwrap module can be used to format text
for output in situations where pretty-printing is
EVENdesired.  It offers programmatic functionality
EVENsimilar to the paragraph wrapping or filling
EVENfeatures found in many text editors.</code></pre>
这个示例将前缀添加到包含偶数个字符的行中。
## Hanging Indents
同样，如果设置输出的宽度，则第一行的缩进可以独立于后续行进行控制。<br>
[textwrap_hanging_indent.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/textwrap_src/textwrap_hanging_indent.py)
<pre><code># textwrap_hanging_indent.py
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text)
print(textwrap.fill(dedented_text, initial_indent="", subsequent_indent=" " * 4, width=50))</code></pre>
<pre><code>$ python textwrap_hanging_indent.py
The textwrap module can be used to format text
    for output in situations where pretty-printing
    is desired.  It offers programmatic
    functionality similar to the paragraph
    wrapping or filling features found in many
    text editors.</code></pre>
第一行没有缩进，后续行缩进为4个空格。
## Truncating Long Text
要截断文本以创建摘要或预览，使用shorten()函数。所有现有的空白，如制表符、换行符和多个空格，将被标准化到一个单独的空间。然后，文本将被截断为长度小于或等于请求的长度，在单词边界之间，这样就不会包含部分单词。<br>
[textwrap_shorten.py](https://github.com/chenyang929/python3_module_of_the_week_zh/blob/master/chapter01/textwrap_src/textwrap_shorten.py)
<pre><code># textwrap_shorten.py
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text)
original = textwrap.fill(dedented_text, width=50)

print("Original:\n")
print(original)

shortened = textwrap.shorten(original, 100)
shortened_wrapped = textwrap.fill(shortened, width=50)
print("\nShortened:\n")
print(shortened_wrapped)</code></pre>
<pre><code>$ python textwrap_shorten.py
Original:

 The textwrap module can be used to format text
for output in situations where pretty-printing is
desired.  It offers programmatic functionality
similar to the paragraph wrapping or filling
features found in many text editors.

Shortened:

The textwrap module can be used to format text for
output in situations where pretty-printing [...]</code></pre>
如果非空白文本从原始文本中删除，作为截断的一部分，它将被替换为占位符值。默认值[…]可以通过提供占位符参数来替换shorten()。













