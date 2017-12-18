# re -- Regular Expressions
用途：使用正式模式搜索并更改文本。

正则表达式是使用正式语法描述的文本匹配模式。模式被解释为一组指令，然后用一个字符串作为输入执行，以产生匹配的子集或修改的原始版本。“正则表达式”在会话中经常被缩短为“regex”或“regexp”。表达式可以包括文本匹配、重复、模式组合、分支和其他复杂的规则。使用正则表达式来解决大量的解析问题比创建专用的lexer和解析器更容易。<br>
正则表达式通常用于涉及大量文本处理的应用程序。例如，它们通常被用作开发人员使用的文本编辑程序中的搜索模式，包括vi、emacs和现代ide。它们也是Unix命令行实用程序的组成部分，如sed、grep和awk。许多编程语言包括对语言语法中的正则表达式的支持(Perl、Ruby、Awk和Tcl)。其他语言，如C、c++和Python，通过扩展库支持正则表达式。<br>
正则表达式的多个开源实现存在，每个都共享一个共同的核心语法，但是对于它们的高级特性有不同的扩展或修改。Python的re模块中使用的语法基于Perl中用于正则表达式的语法，有一些Python特有的增强。<br>
Note: 虽然“正则表达式”的正式定义仅限于描述常规语言的表达式，但有些扩展支持的扩展超出了常规语言的描述。“正则表达式”这个术语在这里使用更一般的含义，表示可以用Python的re模块来评估的任何表达式。

## Finding Patterns in Text
re的最常用的用法是在文本中搜索模式。search()函数使用模式和文本进行扫描，并在找到模式时返回一个Match对象。如果没有找到该模式，search()将返回None。

每个Match对象都包含关于匹配的性质的信息，包括原始的输入字符串，使用的正则表达式，以及模式发生的原始字符串中的位置。<br>
re_simple_match.py
<pre><code># re_simple_match.py
import re

pattern = "this"
text = "Does this text match the pattern?"

match = re.search(pattern, text)

s = match.start()
e = match.end()

print("match object:", match)
print("Found '{}'\nin '{}'\nfrom {} to {} ('{}')".format(
    match.re.pattern, match.string, s, e, text[s:e]
))</code></pre>
<pre><code>$ python re_simple_match.py
match object: <_sre.SRE_Match object; span=(5, 9), match='this'>
Found 'this'
in 'Does this text match the pattern?'
from 5 to 9 ('this')</code></pre>
start()和end()方法得到字符串中所匹配的文本的位置索引。
## Compiling Expressions
尽管re包含了用于使用正则表达式作为文本字符串工作的模块级函数，但是程序使用编译后的表达式的效率更高。compile()函数的作用是:将表达式字符串转换为RegexObject。<br>
re_simple_compiled.py
<pre><code># re_simple_compiled.py
import re

# 预编译模式
regexes = [re.compile(p) for p in ["this", "that"]]
text = "Does this text match the pattern?"

print("Text: {!r}\n".format(text))

for regex in regexes:
    print("Seeking '{}' ->".format(regex.pattern), end=" ")
    if regex.search(text):
        print("match!")
    else:
        print("no match")</code></pre>
<pre><code>$ python re_simple_compiled.py
Text: 'Does this text match the pattern?'

Seeking 'this' -> match!
Seeking 'that' -> no match</code></pre>
模块级函数保留编译表达式的缓存，但是缓存的大小是有限的，使用编译的表达式可以直接避免与缓存查找相关的开销。使用编译表达式的另一个好处是，通过在加载模块时预编译所有的表达式，编译工作被转移到应用程序启动时间，而不是在程序可能响应用户操作的某个点上发生。
## Multiple Matches
到目前为止，示例模式都使用search()来查找文本字符串的单个实例。findall()函数返回与输入模式匹配相匹配的所有无重复子字符串。<br>
re_findall.py
<pre><code># re_findall.py
import re

text = "abbaaabbbbaaaaa"
pattern = "ab"

for match in re.findall(pattern, text):
    print("Found {!r}".format(match))</code></pre>
<pre><code>$ python re_findall.py
Found 'ab'
Found 'ab'</code></pre>
finditer()函数的作用是：返回一个迭代器，该迭代器生成匹配实例，而不是findall()返回的字符串。
re_finditer.py
<pre><code># re_finditer.py
import re

text = "abbaaabbbbaaaaa"
pattern = "ab"

for match in re.finditer(pattern, text):
    print("match:", match)
    s = match.start()
    e = match.end()
    print("Found {!r} at {:d}:{:d}".format(text[s:e], s, e))</code></pre>
<pre><code>$ python re_finditer.py
match: <_sre.SRE_Match object; span=(0, 2), match='ab'>
Found 'ab' at 0:2
match: <_sre.SRE_Match object; span=(5, 7), match='ab'>
Found 'ab' at 5:7</code></pre>
## Pattern Syntax
正则表达式比简单的文本字符串支持更强大的模式。模式可以重复，可以锚定在输入的不同逻辑位置，并且可以用紧凑的形式表示，不需要每个文字字符都出现在模式中。所有这些特性都是通过将文字文本值与元字符结合使用的，这些元字符是re所实现的正则表达式模式语法的一部分。
re_test_patterns.py
<pre><code># re_test_patterns.py
import re

def test_patterns(text, patterns):
    """
    给定源文本和模式列表，在文本中查找每个模式的匹配，
    并将它们打印到stdout
    """
    for pattern, desc in patterns:
        print("'{}' ({})\n".format(pattern, desc))
        print("'{}'".format(text))
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            substr = text[s:e]
            n_backslashes = text[:s].count("\\")
            prefix = "." * (s + n_backslashes)
            print("{}'{}'".format(prefix, substr))
        print()
    return

if __name__ == "__main__":
    test_patterns("abbaaabbbbaaaaa", [("ab", "'a' followed by 'b'")])</code></pre>
<pre><code>$ python re_test_patterns.py
'ab' ('a' followed by 'b')

'abbaaabbbbaaaaa'
'ab'
.....'ab'</code></pre>
## Repetition
有五种方法可以在模式中表达重复。元字符“\*”后面的模式重复0次或多次(允许模式重复0次意味着它不需要出现在所有匹配上)。如果“\*”被“+”替换，模式必须至少出现一次。使用“?”表示模式为零或一次。对于特定数量的事件，在模式之后使用{m}，其中m是模式应该重复的次数。最后，允许一个变量，但重复次数有限，使用{m,n}，其中m是最小重复次数，n是最大值。去掉n({m，})意味着值必须至少出现m次，没有最大值。
re_repetition.py
<pre><code># re_repetition.py
from re_test_patterns import test_patterns

test_patterns(
    "abbaabbba",
    [("ab*", "a followed by zero or more b"),
     ("ab+", "a followed by one or more b"),
     ("ab?", "a followed by zero or one b"),
     ("ab{3}", "a follows by three b"),
     ("ab{2,3}", "a followed by two to three b")]
)</code></pre>
<pre><code>$ python re_repetition.py
'ab*' (a followed by zero or more b)

'abbaabbba'
'abb'
...'a'
....'abbb'
........'a'

'ab+' (a followed by one or more b)

'abbaabbba'
'abb'
....'abbb'

'ab?' (a followed by zero or one b)

'abbaabbba'
'ab'
...'a'
....'ab'
........'a'

'ab{3}' (a follows by three b)

'abbaabbba'
....'abbb'

'ab{2,3}' (a followed by two to three b)

'abbaabbba'
'abb'
....'abbb'</code></pre>
当处理重复指令时，re通常会在匹配模式时消耗尽可能多的输入。这种所谓的贪婪行为可能导致更少的个人匹配，或者匹配可能包括更多的输入文本。通过在模式后加“？”，可以关闭贪婪行为。<br>
re_repetition_non_greedy.py
<pre><code># re_repetition_non_greedy.py
from re_test_patterns import test_patterns

test_patterns(
    "abbaabbba",
    [("ab*?", "a followed by zero or more b"),
     ("ab+?", "a followed by one or more b"),
     ("ab??", "a followed by zero or one b"),
     ("ab{3}?", "a follows by three b"),
     ("ab{2,3}?", "a followed by two to three b")]
)</code></pre>
<pre><code>$ python re_repetition_non_greedy.py
'ab*?' (a followed by zero or more b)

'abbaabbba'
'a'
...'a'
....'a'
........'a'

'ab+?' (a followed by one or more b)

'abbaabbba'
'ab'
....'ab'

'ab??' (a followed by zero or one b)

'abbaabbba'
'a'
...'a'
....'a'
........'a'

'ab{3}?' (a follows by three b)

'abbaabbba'
....'abbb'

'ab{2,3}?' (a followed by two to three b)

'abbaabbba'
'abb'
....'abb'</code></pre>
允许对任何模式的输入禁用贪婪行为，这意味着匹配的子字符串不包括任何b字符。
## Character Sets
字符集是一组字符，任何一个字符都可以在该模式中被匹配。例如，[ab]可以匹配a或b。<br>
re_charset.py
<pre><code># re_charset.py
from re_test_patterns import test_patterns

test_patterns(
    "abbaabbba",
    [("[ab]", "either a or b"),
     ("a[ab]+", "a followed by 1 or more a or b"),
     ("a[ab]+?", "a followed by 1 or more a or b, not greedy")]
)</code></pre>
<pre><code>$ python re_charset.py
'[ab]' (either a or b)

'abbaabbba'
'a'
.'b'
..'b'
...'a'
....'a'
.....'b'
......'b'
.......'b'
........'a'

'a[ab]+' (a followed by 1 or more a or b)

'abbaabbba'
'abbaabbba'

'a[ab]+?' (a followed by 1 or more a or b, not greedy)

'abbaabbba'
'ab'
...'aa'</code></pre>
表达式的贪婪形式(a[ab]+)使用整个字符串，因为第一个字母是a，每个后续字符不是a就是b。

字符集也可以用来排除特定字符。“^”意味着不匹配跟在后面的字符。<br>
re_charset_exclude.py
<pre><code># re_charset_exclude.py
from re_test_patterns import test_patterns

test_patterns(
    "This is some text -- with punctuation",
    [("[^-. ]+", "sequences without -, ., or space")]
)</code></pre>
<pre><code>$ python re_charset_exclude.py
'[^-. ]+' (sequences without -, ., or space)

'This is some text -- with punctuation'
'This'
.....'is'
........'some'
.............'text'
.....................'with'
..........................'punctuation'</code></pre>
此模式查找不包含字符“-”、“.”或空格的所有子字符串。

随着字符集的增大，键入所有应该(或不应该)匹配的字符变得单调乏味。使用字符范围的更紧凑的格式可以用来定义一个字符集，该字符集包含在指定的起始点和停止点之间的所有连续字符。<br>
re_charset_ranges.py
<pre><code># re_charset_ranges.py
from re_test_patterns import test_patterns

test_patterns(
    "This is some text -- with punctuation.",
    [("[a-z]+", "sequences of lowercase letters"),
     ("[A-Z]+", "sequences of uppercase letters"),
     ("[a-zA-Z]+", "sequences of letters of either case"),
     ("[A-Z][a-z]+", "one uppercase followed by lowercase")]
)</code></pre>
<pre><code>$ python re_charset_ranges.py
'[a-z]+' (sequences of lowercase letters)

'This is some text -- with punctuation.'
.'his'
.....'is'
........'some'
.............'text'
.....................'with'
..........................'punctuation'

'[A-Z]+' (sequences of uppercase letters)

'This is some text -- with punctuation.'
'T'

'[a-zA-Z]+' (sequences of letters of either case)

'This is some text -- with punctuation.'
'This'
.....'is'
........'some'
.............'text'
.....................'with'
..........................'punctuation'

'[A-Z][a-z]+' (one uppercase followed by lowercase)

'This is some text -- with punctuation.'
'This'</code></pre>
在这里，范围a - z包括小写的ASCII字母，范围A - Z包括大写的ASCII字母。范围也可以组合成一个字符集。

作为字符集的特殊情况，元字符点(.)表示该模式应该匹配该位置中的任何单个字符。<br>
re_charset_dot.py
<pre><code># re_charset_dot.py
from re_test_patterns import test_patterns

test_patterns(
    "abbaabbba",
    [("a.", "a followed by any one character"),
     ("b.", "b followed by any one character"),
     ("a.*b", "a followed by anything, ending in b"),
     ("a.*?b", "a followed by anything, ending in b")]
)</code></pre>
<pre><code>$ python re_charset_dot.py
'a.' (a followed by any one character)

'abbaabbba'
'ab'
...'aa'

'b.' (b followed by any one character)

'abbaabbba'
.'bb'
.....'bb'
.......'ba'

'a.*b' (a followed by anything, ending in b)

'abbaabbba'
'abbaabbb'

'a.*?b' (a followed by anything, ending in b)

'abbaabbba'
'ab'
...'aab'</code></pre>
如果不使用非贪婪形式，将“.”与“*”相结合会导致很长的匹配。
## Escape Codes
一个更紧凑的表示使用一些预定义字符集的转义码。re所识别的转义代码如下表所示。
Code | Meaning   
---- |--------
\d   |一个数字 
\D   |一个非数字
\s   |空格(tab，空格，换行等)
\S   |非空格
\w   |字母数字
\W   |非字母数字

Note：通过以反斜杠(\\)来前缀字符来表示转义。不幸的是，在正常的Python字符串中，反斜杠本身必须被转义，这会导致难以读懂的表达式。使用原始字符串，通过用r前缀创建预固定文本值，消除了这个问题并保持可读性。<br>
re_escape_codes.py
<pre><code># re_escape_codes.py
from re_test_patterns import test_patterns

test_patterns(
    "A prime #1 example!",
    [(r"\d+", "sequence of digits"),
     (r"\D+", "sequence of non-digits"),
     (r"\s+", "sequence of whitespace"),
     (r"\S+", "sequence of non-whitespace"),
     (r"\w+", "alphanumeric characters"),
     (r"\W", "non-alphanumeric")]
)</code></pre>
<pre><code>$ python re_escape_codes.py
'\d+' (sequence of digits)

'A prime #1 example!'
.........'1'

'\D+' (sequence of non-digits)

'A prime #1 example!'
'A prime #'
..........' example!'

'\s+' (sequence of whitespace)

'A prime #1 example!'
.' '
.......' '
..........' '

'\S+' (sequence of non-whitespace)

'A prime #1 example!'
'A'
..'prime'
........'#1'
...........'example!'

'\w+' (alphanumeric characters)

'A prime #1 example!'
'A'
..'prime'
.........'1'
...........'example'

'\W' (non-alphanumeric)

'A prime #1 example!'
.' '
.......' '
........'#'
..........' '
..................'!'</code></pre>
这些示例表达式将转义码与“+”相结合，以查找输入字符串中类似字符的序列。

要匹配正则表达式语法的一部分字符，可以从搜索模式中转义字符。<br>
re_escape_escapes.py
<pre><code># re_escape_escapes.py
from re_test_patterns import test_patterns

test_patterns(
    r"\d+ \D+ \s+",
    [(r"\\.\+", "escape code")]
)</code></pre>
<pre><code>$ python re_escape_escapes.py
'\\.\+' (escape code)

'\d+ \D+ \s+'
'\d+'
.....'\D+'
..........'\s+'</code></pre>
这个例子中的模式转义反斜杠和“+”字符，因为它们都是元字符，并且在正则表达式中具有特殊的含义。
## Anchoring
除了描述匹配的模式的内容外，可以在输入文本中指定相对位置，使用锚定指令来显示模式。下表列出有效的锚定码。

正则表达式锚定码

Code | Meaning
-|-
^|字符串或行的开头
$|字符串或行的结尾
\A|字符串的开头
\Z|字符串的结尾
\b|单词的开头或结尾为空字符串
\B|单词的开头或结尾为非空字符串

re_anchoring.py
<pre><code># re_anchoring.py
from re_test_patterns import test_patterns

test_patterns(
    "This is some text -- with punctuation",
    [(r"^\w+", "word at start of string"),
     (r"\A\w+", "word at start of string"),
     (r"\w+\S*$", "word near end of string"),
     (r"\w+\S*\Z", "word near end of string"),
     (r"\w*t\w*", "word containing t"),
     (r"\bt\w+", "t at start of word"),
     (r"\w+t\b", "t at end of word"),
     (r"\Bt\B", "t, not start or end of word")]
)</code></pre>
<pre><code>$ python re_anchoring.py
'^\w+' (word at start of string)

'This is some text -- with punctuation'
'This'

'\A\w+' (word at start of string)

'This is some text -- with punctuation'
'This'

'\w+\S*$' (word near end of string)

'This is some text -- with punctuation'
..........................'punctuation'

'\w+\S*\Z' (word near end of string)

'This is some text -- with punctuation'
..........................'punctuation'

'\w*t\w*' (word containing t)

'This is some text -- with punctuation'
.............'text'
.....................'with'
..........................'punctuation'

'\bt\w+' (t at start of word)

'This is some text -- with punctuation'
.............'text'

'\w+t\b' (t at end of word)

'This is some text -- with punctuation'
.............'text'

'\Bt\B' (t, not start or end of word)

'This is some text -- with punctuation'
.......................'t'
..............................'t'
.................................'t'</code></pre>
# Constraning the Search
在已知的情况下，只需要搜索全部输入的一个子集，就可以进一步限制正则表达式匹配，以限制搜索范围。例如，如果模式必须出现在输入的前面，那么使用match()而不是search()将锚定搜索，而不必显式地在搜索模式中包含一个锚。<br>
re_match.py
<pre><code># re_match.py
import re

text = "This is some text -- with punctuation."
pattern = "is"

print("Text   :", text)
print("Pattern:", pattern)

m = re.match(pattern, text)
print("Match  :", m)
s = re.search(pattern, text)
print("Search :", s)</code></pre>
<pre><code>$ python re_match.py
Text   : This is some text -- with punctuation.
Pattern: is
Match  : None
Search : <_sre.SRE_Match object; span=(2, 4), match='is'></code></pre>
由于匹配序列没有出现在输入文本的开头，所以使用match()没有找到它。不过，这个序列在文本中出现了另外两次，所以search()找到了它。

fullmatch()方法要求匹配整个输入字符。<br>
re_fullmatch.py
<pre><code># re_fullmatch.py
import re

text = "This is some text -- with punctuation."
pattern = "is"

text1 = "python"
pattern1 = "python"
print("Text       :", text)
print("Pattern    :", pattern)

m = re.search(pattern, text)
print("Search     :", m)
s = re.fullmatch(pattern, text)
print("Full match :", s)
s1 = re.fullmatch(pattern1, text1)
print("Full match1:", s1)</code></pre>
<pre><code>$ python re_fullmatch.py
Text       : This is some text -- with punctuation.
Pattern    : is
Search     : <_sre.SRE_Match object; span=(2, 4), match='is'>
Full match : None
Full match1: <_sre.SRE_Match object; span=(0, 6), match='python'></code></pre>

已编译正则表达式的search()方法接受可选的开始和结束位置参数，以限制对输入的子字符串的搜索。<br>
re_search_substring.py
<pre><code>
# re_search_substring.py
import re

text = "This is some text -- with punctuation."
pattern = re.compile(r"\b\w*is\w*\b")

print("Text:", text)
print()

pos = 0
while True:
    match = pattern.search(text, pos)
    if not match:
        break
    s = match.start()
    e = match.end()
    print("  {:>2d} : {:>2d} = '{}'".format(s, e-1, text[s:e]))
    pos = e
</code></pre>
<pre><code>
$ python re_search_substring.py
# re_search_substring.py
import re

text = "This is some text -- with punctuation."
pattern = re.compile(r"\b\w*is\w*\b")

print("Text:", text)
print()

pos = 0
while True:
    match = pattern.search(text, pos)
    if not match:
        break
    s = match.start()
    e = match.end()
    print("  {:>2d} : {:>2d} = '{}'".format(s, e-1, text[s:e]))
    pos = e
</code></pre>
这个例子实现了一个不那么有效的iterall()形式。每次找到匹配时，该匹配的结束位置将用于下一个搜索。
## Dissecting Matches with Groups
搜索模式匹配是正则表达式提供的强大功能的基础。在模式中添加组将隔离匹配文本的部分，扩展这些功能来创建解析器。分组是用括号中的模式来定义的。<br>
re_groups.py
<pre><code>
# re_groups.py
from re_test_patterns import test_patterns

test_patterns(
    "abbaaabbbbaaaaa",
    [("a(ab)", "a followed by literal ab"),
     ("a(a*b*)", "a followed by 0-n a and 0-n b"),
     ("a(ab)*", "a followed by 0-n ab"),
     ("a(ab)+", "a followed by 1-n ab")]
)
</code></pre>
<pre><code>
$ python re_groups.py
'a(ab)' (a followed by literal ab)

'abbaaabbbbaaaaa'
....'aab'

'a(a*b*)' (a followed by 0-n a and 0-n b)

'abbaaabbbbaaaaa'
'abb'
...'aaabbbb'
..........'aaaaa'

'a(ab)*' (a followed by 0-n ab)

'abbaaabbbbaaaaa'
'a'
...'a'
....'aab'
..........'a'
...........'a'
............'a'
.............'a'
..............'a'

'a(ab)+' (a followed by 1-n ab)

'abbaaabbbbaaaaa'
....'aab'
</code></pre>
任何完整的正则表达式都可以转换为一个组，并嵌套在一个更大的表达式中。所有的重复修改器都可以应用于一个整体，要求整个组模式重复。

要访问一个模式中单个组匹配的子字符串，请使用Match对象的groups()方法<br>
re_groups_match.py
<pre><code>
# re_groups_match.py
import re

text = "This is some text -- with punctuation."

print(text)
print()

patterns = [
    (r"^(\w+)", "word at start of string"),
    (r"(\w+)\S*$", "word at end, with optional punctuation"),
    (r"(\bt\w+)\W+(\w+)", "word starting with t, another word"),
    (r"(\w+t)\b", "word ending with it"),
]

for pattern, desc in patterns:
    regex = re.compile(pattern)
    match = regex.search(text)
    print("'{}'({})\n".format(pattern, desc))
    print(" ", match.groups())
    print()
</code></pre>
<pre><code>
$ python re_groups_match.py
This is some text -- with punctuation.

'^(\w+)'(word at start of string)

  ('This',)

'(\w+)\S*$'(word at end, with optional punctuation)

  ('punctuation',)

'(\bt\w+)\W+(\w+)'(word starting with t, another word)

  ('text', 'with')

'(\w+t)\b'(word ending with it)

  ('text',)
</code></pre>
match.groups()以与字符串匹配的表达式中的组的顺序返回字符串序列。

要请求单个组的匹配，使用group()方法。这在只需要匹配结果的部分字符串时很有用。<br>
re_groups_individual.py
<pre><code>
# re_groups_individual.py
import re

text = "This is some text -- with punctuation."

print("Input text            :", text)

regex = re.compile(r"(\bt\w+)\W+(\w+)")
print("Pattern               :", regex.pattern)

match = regex.search(text)
print(match.groups())
print("Entire match          :", match.group(0))
print("Word starting with 't':", match.group(1))
print("Word after 't' word   :", match.group(2))
</code></pre>
<pre><code>
$ python re_groups_individual.py
Input text            : This is some text -- with punctuation.
Pattern               : (\bt\w+)\W+(\w+)
('text', 'with')
Entire match          : text -- with
Word starting with 't': text
Word after 't' word   : with
</code></pre>
组0表示与整个表达式匹配的字符串，子组以1开始顺序编号。

Python扩展了基本的分组语法以添加命名组。使用名称来引用组使得随着时间的推移更容易修改模式，而不必使用匹配结果修改代码。要设置一个组的名称，使用语法(? P <名>模式)。<br>
re_groups_named.py
<pre><code>
# re_groups_named.py
import re

text = "This is some text -- with punctuation."

print(text)
print()

patterns = [
    r"^(?P<first_word>\w+)",
    r"(?P<last_word>\w+\S*$)",
    r"(?P<t_word>\bt\w+)(?P<other_word>\w+)",
    r"(?P<ends_with_t>\w+t)\b"
]

for pattern in patterns:
    regex = re.compile(pattern)
    match = regex.search(text)
    print("'{}'".format(pattern))
    print(" ", match.groups())
    print(" ", match.groupdict())
    print()
</code></pre>
<pre><code>
$ python re_groups_named.py
This is some text -- with punctuation.

'^(?P<first_word>\w+)'
  ('This',)
  {'first_word': 'This'}

'(?P<last_word>\w+\S*$)'
  ('punctuation.',)
  {'last_word': 'punctuation.'}

'(?P<t_word>\bt\w+)(?P<other_word>\w+)'
  ('tex', 't')
  {'t_word': 'tex', 'other_word': 't'}

'(?P<ends_with_t>\w+t)\b'
  ('text',)
  {'ends_with_t': 'text'}
</code></pre>
使用groupdict()从匹配中检索字典映射组名称到子字符串。命名模式也包括在groups()返回的有序序列中。

test_patterns()的更新版本显示了被编号和命名的组匹配的模式，这将使下面的示例更容易遵循。<br>
re_test_patterns_groups.py
<pre><code>
# re_test_patterns_groups.py
import re

def test_patterns(text, patterns):
    """
    给定源文本和模式列表，在文本中查找每个模式的匹配，
    并将它们打印到stdout
    """
    # 在文本中查找每个模式并打印结果
    for pattern, desc in patterns:
        print("{!r}({})\n".format(pattern, desc))
        print("{!r}".format(text))
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            prefix = " " * (s)
            print("{}{!r}{}".format(prefix, text[s:e], " " * (len(text) - e)), end=" ",)
            print(match.groups())
            if match.groupdict():
                print("{}{}".format(" " * (len(text) - s), match.groupdict()))
        print()
    return
</code></pre>
由于组本身是一个完整的正则表达式，因此可以在其他组内嵌套组来构建更复杂的表达式。<br>
re_groups_nested.py
<pre><code>
# re_groups_nested.py
from re_test_patterns_groups import test_patterns

test_patterns("abbaabbba", [(r"a((a*)(b*))", "a folloewd by 0-n a and 0-n b")])
</code></pre>
<pre><code>
$ python re_groups_nested.py
'a((a*)(b*))'(a folloewd by 0-n a and 0-n b)

'abbaabbba'
'abb'       ('bb', '', 'bb')
   'aabbb'  ('abbb', 'a', 'bbb')
        'a' ('', '', '')
</code></pre>
在这种情况下，group(a *)匹配一个空字符串，因此group()的返回值包含空字符串作为匹配的值。

re_groups_alternative.py
<pre><code>
# re_groups_alternative.py

from re_test_patterns_groups import test_patterns

test_patterns("abbaabbba", [(r"a((a+)|(b+))", "a then seq. of a or ser. of b"),
(r"a((a|b)+)", "a then seq. of [ab]")])
</code></pre>
<pre><code>
$ python re_groups_alternative.py
'a((a+)|(b+))'(a then seq. of a or ser. of b)

'abbaabbba'
'abb'       ('bb', None, 'bb')
   'aa'     ('a', 'a', None)

'a((a|b)+)'(a then seq. of [ab])

'abbaabbba'
'abbaabbba' ('bbaabbba', 'a')
</code></pre>

在字符串匹配子模式的情况下，定义包含子模式的组也很有用，因为该子模式不属于应该从全文中提取的内容。这些类型的群体被称为非捕捉。非捕获组可用于描述重复模式或替代方案，而不需要隔离返回值中字符串的匹配部分。要创建一个非捕获组，请使用语法(?:模式)。<br>
re_groups_noncapturing.py
<pre><code>
# re_groups_noncapturing.py

from re_test_patterns_groups import test_patterns

test_patterns("abbaabbba",
              [(r"a((a+)|(b+))", "capturing form"),
               (r"a((?:a+)|(?:b+))", "noncapturing")])
</code></pre>
<pre><code>
$ python re_groups_noncapturing.py
'a((a+)|(b+))'(capturing form)

'abbaabbba'
'abb'       ('bb', None, 'bb')
   'aa'     ('a', 'a', None)

'a((?:a+)|(?:b+))'(noncapturing)

'abbaabbba'
'abb'       ('bb',)
   'aa'     ('a',)
</code></pre>
## Search Options
选项标志用于改变匹配引擎处理表达式的方式。可以使用位或操作组合标志，然后传递给compile()、search()、match()和其他接受模式进行搜索的函数。
### Case-insensitive Matching
IGNORECASE使文字字符和字符范围在模式中匹配大写和小写字符。<br>
re_flags_ignorecase.py
<pre><code>
# re_flags_ignorecase.py
import re

text = "This is some text -- with punctuation."
pattern = r"\bT\w+"
with_case = re.compile(pattern)
without_case = re.compile(pattern, re.IGNORECASE)

print("Text:\n {!r}".format(text))
print("Pattern:\n {}".format(pattern))
print("Case-sensitive:")
for match in with_case.findall(text):
    print(" {!r}".format(match))
print("Case-insensitive:")
for match in without_case.findall(text):
    print(" {!r}".format(match))
</code></pre>
<pre><code>
$ python re_flags_ignorecase.py
Text:
 'This is some text -- with punctuation.'
Pattern:
 \bT\w+
Case-sensitive:
 'This'
Case-insensitive:
 'This'
 'text'
</code></pre>
### Input with Multiple Lines
两种标志影响了多行输入工作中的搜索:MULTILINE和DOTALL。<br>
MULTILINE标志控制模式匹配代码如何处理包含换行符的文本的指令。多行模式打开时,锚^和$规则适用于每一行的开始和结束,除了整个字符串。<br>
re_flags_multiline.py
<pre><code>
# re_flags_multiline.py
import re

text = "This is some text -- with punctuation.\nA second line."
pattern = r"(^\w+)|(\w+\S*$)"
single_line = re.compile(pattern)
multiline = re.compile(pattern, re.MULTILINE)

print("Text:\n {!r}".format(text))
print("Pattern:\n {}".format(pattern))
print("Single Line :")
for match in single_line.findall(text):
    print(" {!r}".format(match))
print("Multiline   :")
for match in multiline.findall(text):
    print(" {!r}".format(match))
</code></pre>
<pre><code>
$ python re_flags_multiline.py
Text:
 'This is some text -- with punctuation.\nA second line.'
Pattern:
 (^\w+)|(\w+\S*$)
Single Line :
 ('This', '')
 ('', 'line.')
Multiline   :
 ('This', '')
 ('', 'punctuation.')
 ('A', '')
 ('', 'line.')
</code></pre>

DOTALL是与多行文本相关的另一个标志。通常，点字符(.)匹配输入文本中的所有内容，除了换行符。该标志允许圆点同时匹配换行。<br>
re_flags_dotall.py
<pre><code>
# re_flags_dotall.py
import re

text = "This is some text -- with punctuation.\nA second line."
pattern = r".+"
no_newlines = re.compile(pattern)
dotall = re.compile(pattern, re.DOTALL)

print("Text:\n {!r}".format(text))
print("Pattern:\n {}".format(pattern))
print("No newline :")
for match in no_newlines.findall(text):
    print(" {!r}".format(match))
print("Dotall     :")
for match in dotall.findall(text):
    print(" {!r}".format(match))
</code></pre>
<pre><code>
$ python re_flags_dotall.py
Text:
 'This is some text -- with punctuation.\nA second line.'
Pattern:
 .+
No newline :
 'This is some text -- with punctuation.'
 'A second line.'
Dotall     :
 'This is some text -- with punctuation.\nA second line.'
</code></pre>
### Unicode
在python3下，str对象使用完整的Unicode字符集，str上的正则表达式处理假设模式和输入文本都是Unicode的。前面描述的转义代码在默认情况下定义为Unicode。这些假设意味着模式\w+将匹配“French”和“Français”两个词。要只匹配ASCII字符集，就像在Python 2中默认的那样，在编译模式或调用模块级别函数search()和match()时使用ASCII标记。<br>
re_flags_ascii.py
<pre><code>
# re_flags_ascii.py
import re

text = u"Français złoty Österreich"
pattern = r"\w+"
ascii_pattern = re.compile(pattern, re.ASCII)
unicode_pattern = re.compile(pattern)

print("Text    :", text)
print("Pattern :", pattern)
print("ASCII   :", list(ascii_pattern.findall(text)))
print("Unicode :", list(unicode_pattern.findall(text)))
</code></pre>
<pre><code>
$ python re_flags_ascii.py
Text    : Français złoty Österreich
Pattern : \w+
ASCII   : ['Fran', 'ais', 'z', 'oty', 'sterreich']
Unicode : ['Français', 'złoty', 'Österreich']
</code></pre>
### Verbose Expression Syntax
当表达式变得更加复杂时，正则表达式语法的紧凑格式会成为阻碍。当一个表达式中的组数增加时，将会有更多的工作来跟踪为什么需要每个元素，以及表达式的各个部分是如何交互的。使用命名组有助于缓解这些问题，但是更好的解决方案是使用verbose模式表达式，允许注释和额外的空白嵌入到模式中。

一个验证电子邮件地址的模式将说明详细模式如何使使用正则表达式更容易。第一个版本识别了在三个顶级域中的一个:.com, .org, 或者.edu结尾的地址。<br>
re_email_compact.py
<pre><code>
# re_email_compact.py
import re

address = re.compile("[\w\d.+-]+@([\w\d.]+\.)+(com|org|edu)")

candidates = [
    u"first.last@example.com",
    u"first.last+category@gmail.com",
    u"valid-address@mail.example.com",
    u"not-valid@example.foo",
]

for candidate in candidates:
    match = address.search(candidate)
    print("{:<30} {}".format(candidate, "Matches" if match else "No match"))
</code></pre>
<pre><code>
$ python re_email_compact.py
first.last@example.com         Matches
first.last+category@gmail.com  Matches
valid-address@mail.example.com Matches
not-valid@example.foo          No match
</code></pre>
上例表达式已经很复杂了。有几个字符类、组和重复表达式。

将表达式转换为verbose的格式将使扩展更容易。<br>
re_email_verbose.py
<pre><code>
# re_email_verbose.py
import re

address = re.compile(
    '''
    [\w\d.+-]      # username
    @
    ([\w\d.+\.])+  # domain name prefix
    (com|org|edu)  # TODO: support more top-level domains
    ''',
    re.VERBOSE

)

candidates = [
    u"first.last@example.com",
    u"first.last+category@gmail.com",
    u"valid-address@mail.example.com",
    u"not-valid@example.foo",
]

for candidate in candidates:
    match = address.search(candidate)
    print("{:<30} {}".format(candidate, "Matches" if match else "No match"),)
</code></pre>
<pre><code>
$ python re_email_verbose.py
first.last@example.com         Matches
first.last+category@gmail.com  Matches
valid-address@mail.example.com Matches
not-valid@example.foo          No match
</code></pre>
表达式匹配相同的输入，但在这种扩展格式中，它更容易阅读。这些注释还有助于识别模式的不同部分，以便可以扩展以匹配更多的输入。

下面这个扩展的版本解析输入包括一个人的姓名和电子邮件地址，可能出现在电子邮件标题中。该名称首先出现，并独立地站在它自己的位置上，然后是通过尖括号(<和>)包围的电子邮件地址。<br>
re_email_with_name.py
<pre><code>
# re_email_with_name.py
import re

address = re.compile(
    '''

    # A name is made up of letters, and may include "."
    # for title abbreviations and middle initials.
    ((?P<name>
       ([\w.,]+\s+)*[\w.,]+)
       \s*
       # Email addresses are wrapped in angle
       # brackets < >, but only if a name is
       # found, so keep the start bracket in this
       # group.
       <
    )? # the entire name is optional

    # The address itself: username@domain.tld
    (?P<email>
      [\w\d.+-]+       # username
      @
      ([\w\d.]+\.)+    # domain name prefix
      (com|org|edu)    # limit the allowed top-level domains
    )

    >? # optional closing angle bracket
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'first.last+category@gmail.com',
    u'valid-address@mail.example.com',
    u'not-valid@example.foo',
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'First Last',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
    u'<first.last@example.com>',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Name :', match.groupdict()['name'])
        print('  Email:', match.groupdict()['email'])
    else:
        print('  No match')
</code></pre>
<pre><code>
$ python re_email_with_name.py
Candidate: first.last@example.com
  Name : None
  Email: first.last@example.com
Candidate: first.last+category@gmail.com
  Name : None
  Email: first.last+category@gmail.com
Candidate: valid-address@mail.example.com
  Name : None
  Email: valid-address@mail.example.com
Candidate: not-valid@example.foo
  No match
Candidate: First Last <first.last@example.com>
  Name : First Last
  Email: first.last@example.com
Candidate: No Brackets first.last@example.com
  Name : None
  Email: first.last@example.com
Candidate: First Last
  No match
Candidate: First Middle Last <first.last@example.com>
  Name : First Middle Last
  Email: first.last@example.com
Candidate: First M. Last <first.last@example.com>
  Name : First M. Last
  Email: first.last@example.com
Candidate: <first.last@example.com>
  Name : None
  Email: first.last@example.com
</code></pre>
### Embedding Flags in Patterns
在编译表达式时不能添加标志的情况，例如，当一个模式作为一个参数传递给一个库函数时，该函数将稍后进行编译，因此可以将标志嵌入到表达式字符串本身中。例如，要将不区分大小写的匹配打开，添加(?i)到表达式的开头。
re_flags_embedded.py
<pre><code>
# re_flags_embedded.py
import re

text = "This is some text -- with punctuation."
pattern = r"(?i)\bT\w+"
regex = re.compile(pattern)

print("Text    :", text)
print("Pattern :", pattern)
print("Matches :", regex.findall(text))
</code></pre>
<pre><code>
$ python re_flags_embedded.py
Text    : This is some text -- with punctuation.
Pattern : (?i)\bT\w+
Matches : ['This', 'text']
</code></pre>
因为选项控制整个表达式的计算或解析方式，所以它们应该始终出现在表达式的开头。

所有标记的缩写都列在下表中
Flag       | Abbreviation
-----      | -------
ASCII      | a
IGNORECASE | i
MULTILINE  | m
DOTALL     | s
VERBOSE    | x
嵌入的标志可以组合在同一组内。例如，(?im)对多行字符串进行不区分大小写的匹配。
## Looking Ahead or Behind
在许多情况下，只有在其他部分匹配的情况下，匹配模式的一部分是有用的。例如，在邮件解析表达式中，尖括号被标记为可选。现实地说，括号应该是成对的，并且表达式应该只有在成对出现时才匹配，或者两者都不匹配。该表达式的修改版本使用了一个积极的先行断言来匹配这一对。前面的断言语法是(?=模式)。<br>
re_look_ahead.py
<pre><code>
import re

address = re.compile(
    '''
    # A name is made up of letters, and may include "."
    # for title abbreviations and middle initials.
    ((?P<name>
       ([\w.,]+\s+)*[\w.,]+
     )
     \s+
    ) # name is no longer optional

    # LOOKAHEAD
    # Email addresses are wrapped in angle brackets, but only
    # if both are present or neither is.
    (?= (<.*>$)       # remainder wrapped in angle brackets
        |
        ([^<].*[^>]$) # remainder *not* wrapped in angle brackets
      )

    <? # optional opening angle bracket

    # The address itself: username@domain.tld
    (?P<email>
      [\w\d.+-]+       # username
      @
      ([\w\d.]+\.)+    # domain name prefix
      (com|org|edu)    # limit the allowed top-level domains
    )

    >? # optional closing angle bracket
    ''',
    re.VERBOSE)

candidates = [
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'Open Bracket <first.last@example.com',
    u'Close Bracket first.last@example.com>',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Name :', match.groupdict()['name'])
        print('  Email:', match.groupdict()['email'])
    else:
        print('  No match')
</code></pre>
<pre><code>
$ python re_look_ahead.py
Candidate: First Last <first.last@example.com>
  Name : First Last
  Email: first.last@example.com
Candidate: No Brackets first.last@example.com
  Name : No Brackets
  Email: first.last@example.com
Candidate: Open Bracket <first.last@example.com
  No match
Candidate: Close Bracket first.last@example.com>
  No match
</code></pre>

一个消极的先行断言((?!模式))申明模式与当前点后面的文本不匹配。例如，可以修改电子邮件识别模式，以忽略自动化系统常用的noreply邮件地址。<br>
re_negative_look_ahead.py
<pre><code>
# re_negative_look_ahead.py
import re

address = re.compile(
    '''
    ^

    # An address: username@domain.tld

    # Ignore noreply addresses
    (?!noreply@.*$)

    [\w\d.+-]+       # username
    @
    ([\w\d.]+\.)+    # domain name prefix
    (com|org|edu)    # limit the allowed top-level domains

    $
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'noreply@example.com',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Match:', candidate[match.start():match.end()])
    else:
        print('  No match')
</code></pre>
<pre><code>
$ python re_negative_look_behind.py
Candidate: first.last@example.com
  Match: first.last@example.com
Candidate: noreply@example.com
  No match
</code></pre>
以noreply开始的地址与模式不匹配，因为前面的断言失败了。

除了在电子邮件地址的用户名部分查找noreply之外，在使用语法(?<!pattern)匹配用户名之后，模式还可以使用消极的外观来编写。<br>
re_negative_look_behind.py
<pre><code>
import re

address = re.compile(
    '''
    ^

    # An address: username@domain.tld

    [\w\d.+-]+       # username

    # Ignore noreply addresses
    (?&lt!noreply)

    @
    ([\w\d.]+\.)+    # domain name prefix
    (com|org|edu)    # limit the allowed top-level domains

    $
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'noreply@example.com',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Match:', candidate[match.start():match.end()])
    else:
        print('  No match')
</code></pre>
<pre><code>
$ python re_negative_look_behind.py
Candidate: first.last@example.com
  Match: first.last@example.com
Candidate: noreply@example.com
  No match
</code></pre>

在使用语法(?<= pattern)的模式之后，可以使用断言的积极查找。在下面的示例中，表达式找到了Twitter句柄。<br>
re_look_behind.py
<pre><code>
# re_look_behind.py
import re

twitter = re.compile(
    '''
    # A twitter handle: @username
    (?<=@)
    ([\w\d_]+)       # username
    ''',
    re.VERBOSE)

text = '''This text includes two Twitter handles.
One for @ThePSF, and one for the author, @doughellmann.
'''

print(text)
for match in twitter.findall(text):
    print('Handle:', match)
</code></pre>
<pre><code>
$ python re_look_behind.py
This text includes two Twitter handles.
One for @ThePSF, and one for the author, @doughellmann.

Handle: ThePSF
Handle: doughellmann
</code></pre>
该模式匹配可以组成Twitter句柄的字符序列，只要它们之前有@。
## Self-referencing Expressions
匹配的值可以用于表达式的后面部分。例如，可以更新电子邮件示例，以匹配包含某人的第一个和最后一个名称的地址，包括对这些组的反向引用。要实现这一点，最简单的方法是通过使用\num引用先前匹配的组。<br>
re_refer_to_group.py
<pre><code>
# re_refer_to_group.py
import re

address = re.compile(
    r'''

    # The regular name
    (\w+)               # first name
    \s+
    (([\w.]+)\s+)?      # optional middle name or initial
    (\w+)               # last name

    \s+

    <

    # The address: first_name.last_name@domain.tld
    (?P<email>
      \1               # first name
      \.
      \4               # last name
      @
      ([\w\d.]+\.)+    # domain name prefix
      (com|org|edu)    # limit the allowed top-level domains
    )

    >
    ''',
    re.VERBOSE | re.IGNORECASE)

candidates = [
    u'First Last <first.last@example.com>',
    u'Different Name <first.last@example.com>',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Match name :', match.group(1), match.group(4))
        print('  Match email:', match.group(5))
    else:
        print('  No match')
</code></pre>
<pre><code>
$ python re_refer_to_group.py
Candidate: First Last <first.last@example.com>
  Match name : First Last
  Match email: first.last@example.com
Candidate: Different Name <first.last@example.com>
  No match
Candidate: First Middle Last <first.last@example.com>
  Match name : First Last
  Match email: first.last@example.com
Candidate: First M. Last <first.last@example.com>
  Match name : First Last
  Match email: first.last@example.com
</code></pre>
尽管语法很简单，但通过数值ID创建反向引用也有一些缺点。从实际的角度来看，当表达式发生变化时，必须重新计算组，并且需要更新所有引用。另一个缺点是，只有99个引用可以使用标准的反向引用语法\ n，因为如果ID号是3位长，那么它将被解释为八进制字符值，而不是一个组引用。当然，如果在一个表达式中有超过99个组，那么将会有更严重的维护挑战，而不是简单地无法引用它们。

Python的表达式解析器包括一个使用(?P=name)的扩展，以引用在表达式前面匹配的命名组的值。
re_refer_to_named_group.py
<pre><code>
# re_refer_to_named_group.py
import re

address = re.compile(
    '''

    # The regular name
    (?P<first_name>\w+)
    \s+
    (([\w.]+)\s+)?      # optional middle name or initial
    (?P<last_name>\w+)

    \s+

    <

    # The address: first_name.last_name@domain.tld
    (?P<email>
      (?P=first_name)
      \.
      (?P=last_name)
      @
      ([\w\d.]+\.)+    # domain name prefix
      (com|org|edu)    # limit the allowed top-level domains
    )

    >
    ''',
    re.VERBOSE | re.IGNORECASE)

candidates = [
    u'First Last <first.last@example.com>',
    u'Different Name <first.last@example.com>',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Match name :', match.groupdict()['first_name'],
              end=' ')
        print(match.groupdict()['last_name'])
        print('  Match email:', match.groupdict()['email'])
    else:
        print('  No match')
</code></pre>
<pre><code>
Candidate: First Last <first.last@example.com>
  Match name : First Last
  Match email: first.last@example.com
Candidate: Different Name <first.last@example.com>
  No match
Candidate: First Middle Last <first.last@example.com>
  Match name : First Last
  Match email: first.last@example.com
Candidate: First M. Last <first.last@example.com>
  Match name : First Last
  Match email: first.last@example.com
</code></pre>
地址表达式是用IGNORECASE标志编译的，因为专有名称通常大写，但电子邮件地址不是。

在表达式中使用反向引用的另一种机制根据之前的组是否匹配选择了不同的模式。电子邮件模式可以被纠正，这样，如果有一个名字，就需要尖括号，如果邮件地址本身是不需要的。测试一组是否匹配的语法是(?(id)yes -expression |无表达式)，其中id为组名或编号，yes - expression是在组有值时使用的模式，而无表达式则是使用其他方式使用的模式。<br>
re_id.py
<pre><code>
$ python re_id.py
Candidate: First Last <first.last@example.com>
  Match name : First Last
  Match email: first.last@example.com
Candidate: No Brackets first.last@example.com
  No match
Candidate: Open Bracket <first.last@example.com
  No match
Candidate: Close Bracket first.last@example.com>
  No match
Candidate: no.brackets@example.com
  Match name : None
  Match email: no.brackets@example.com
</code></pre>
这个版本的电子邮件地址解析器使用了两个测试。如果名称组匹配，那么前面的断言需要两个尖括号，并设置括号组。如果名称不匹配，则断言需要文本的其余部分没有相应的尖括号。稍后，如果设置了括号组，那么实际的模式匹配代码使用文本模式在输入中使用括号;否则，它将消耗任何空白空间。
## Modifying String with Patterns
除了通过文本搜索，re还支持使用正则表达式作为搜索机制修改文本，而替换可以引用在模式中匹配的组作为替换文本的一部分。使用sub()来用另一个字符串替换所有出现的模式。<br>
re_sub.py
<pre><code>
# re_sub.py
import re

bold = re.compile(r'\*{2}(.*?)\*{2}')

text = 'Make this **bold**.  This **too**.'

print('Text:', text)
print('Bold:', bold.sub(r'<b>\1</b>', text))
</code></pre>
<pre><code>
$ python re_sub.py
Text: Make this **bold**.  This **too**.
Bold: Make this <b>bold</b>.  This <b>too</b>.
</code></pre>

要在替换中使用命名组，使用语法\g<name >。<br>
re_sub_named_groups.py
<pre><code>
# re_sub_named_groups.py
import re

bold = re.compile(r'\*{2}(?P<bold_text>.*?)\*{2}')

text = 'Make this **bold**.  This **too**.'

print('Text:', text)
print('Bold:', bold.sub(r'<b>\g<bold_text></b>', text))
</code></pre>
<pre><code>
$ python re_sub_named_groups.py
Text: Make this **bold**.  This **too**.
Bold: Make this <b>bold</b>.  This <b>too</b>.
</code></pre>
\g<name >语法也适用于编号的引用，并且使用它消除了组号和周围文字数字之间的歧义。

传递一个值来计数，以限制执行的替换数量。<br>
re_sub_count.py
<pre><code>
# re_sub_count.py
import re

bold = re.compile(r'\*{2}(.*?)\*{2}')

text = 'Make this **bold**.  This **too**.'

print('Text:', text)
print('Bold:', bold.sub(r'<b>\1</b>', text, count=1))
</code></pre>
<pre><code>
$ python re_sub_count.py
Text: Make this **bold**.  This **too**.
Bold: Make this <b>bold</b>.  This **too**.
</code></pre>
只有第一个变量替换，因为count是1。

subn()函数类似sub()函数，它还会返回修改后的字符串和替换计数。<br>
re_subn.py
<pre><code>
# re_subn.py
import re

bold = re.compile(r'\*{2}(.*?)\*{2}')

text = 'Make this **bold**.  This **too**.'

print('Text:', text)
print('Bold:', bold.subn(r'<b>\1</b>', text))
</code></pre>
<pre><code>
$ python re_subn.py
Text: Make this **bold**.  This **too**.
Bold: ('Make this <b>bold</b>.  This <b>too</b>.', 2)
</code></pre>
## Splitting with Patterns
split()是分解字符串来解析它们的最常用方法之一。它只支持将文字值作为分隔符使用，但如果输入的格式不一致，则有时需要使用正则表达式。例如，许多纯文本标记语言将段落分隔符定义为两个或更多的newline(\n)字符。在本例中，由于定义的“或更多”部分不能使用str.split()。

使用findall()识别段落的策略将使用like(.+?)\n {2,}的模式。<br>
re_paragraphs_findall.py
<pre><code>
# re_paragraphs_findall.py
import re

text = '''Paragraph one
on two lines.

Paragraph two.


Paragraph three.'''

for num, para in enumerate(re.findall(r'(.+?)\n{2,}',
                                      text,
                                      flags=re.DOTALL)
                           ):
    print(num, repr(para))
    print()
</code></pre>

扩展这个模式，说一个段落以两个或更多的新行结尾，或者是输入的结尾解决问题，但使模式更加复杂。转换为re. split()而不是re.findall()会自动处理边界条件，并使模式更简单。<br>
re_split.py
<pre><code>
# re_split.py
import re

text = '''Paragraph one
on two lines.

Paragraph two.


Paragraph three.'''

print('With findall:')
for num, para in enumerate(re.findall(r'(.+?)(\n{2,}|$)',
                                      text,
                                      flags=re.DOTALL)):
    print(num, repr(para))
    print()

print()
print('With split:')
for num, para in enumerate(re.split(r'\n{2,}', text)):
    print(num, repr(para))
    print()
</code></pre>
<pre><code>
$ python re_split.py
With findall:
0 ('Paragraph one\non two lines.', '\n\n')

1 ('Paragraph two.', '\n\n\n')

2 ('Paragraph three.', '')


With split:
0 'Paragraph one\non two lines.'

1 'Paragraph two.'

2 'Paragraph three.'
</code></pre>
split()模式参数更精确地表示标记规范。两个或多个换行符在输入字符串的段落之间标记分隔点。

在括号中封装表达式以定义一个组，使split()更像str.partition()，因此它返回分隔符值和字符串的其他部分。<br>
re_split_groups.py
<pre><code>
# re_split_groups.py
import re

text = '''Paragraph one
on two lines.

Paragraph two.


Paragraph three.'''

print('With split:')
for num, para in enumerate(re.split(r'(\n{2,})', text)):
    print(num, repr(para))
    print()
</code></pre>
<pre><code>
With split:
0 'Paragraph one\non two lines.'

1 '\n\n'

2 'Paragraph two.'

3 '\n\n\n'

4 'Paragraph three.'
</code></pre>
输出现在包括每个段落，以及分隔它们的新行序列。
























































