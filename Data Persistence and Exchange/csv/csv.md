# csv -- Comma-separated Value Files
> 目的：读和写逗号分隔值文件。

csv模块可用于处理从电子表格和数据库导出的数据，并将其转换为带有字段和记录的文本文件，通常称为逗号分隔值(csv)格式，因为逗号通常用于分隔记录中的字段。
## Reading
使用reader()创建一个对象来从CSV文件中读取数据。读取器可以用作迭代器，按顺序处理文件的行。例如
```
# csv_reader.py

import csv
import sys

with open(sys.argv[1], 'rt', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```
reader()的第一个参数是文本行的来源。在本例中，它是一个文件，但是可以接受任何可迭代的内容(StringIO实例、列表等)。可以提供其他可选参数来控制如何解析输入数据。

当它被读取时，输入数据的每一行都被解析并转换为字符串列表。
```
$ python csv_reader.py testdata.csv

['Title 1', 'Title 2', 'Title 3', 'Title 4']
['1', 'a', '08/18/07', 'å']
['2', 'b', '08/19/07', '∫']
['3', 'c', '08/20/07', 'ç']
```
解析器处理嵌入在行中的字符串中的断行，这就是为什么“行”并不总是与来自文件的“行”输入相同。

输入中有换行符的字段在解析器返回时保留内部换行符。
```
$ python csv_reader.py testlinebreak.csv

['Title 1', 'Title 2', 'Title 3']
['1', 'first line\nsecond line', '08/18/07']
```
## Writing
编写CSV文件和读取它们一样简单。使用writer()创建要写入的对象，然后遍历行，使用writerow()写入行。
```
# csv_writer.py

import csv
import sys

unicode_chars = 'å∫ç'

with open(sys.argv[1], 'wt', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(('Title 1', 'Title 2', 'Title 3', 'Title 4'))
    for i in range(3):
        row = (
            i + 1,
            chr(ord('a') + i),
            '08/{:02d}/07'.format(i + 1),
            unicode_chars[i],
        )
        writer.writerow(row)

print(open(sys.argv[1], 'rt', encoding='utf-8').read())
```
输出与reader示例中使用的导出数据并不完全相同，因为它缺少引号。
```
$ python csv_writer.py testout.csv

Title 1,Title 2,Title 3,Title 4
1,a,08/01/07,å
2,b,08/02/07,∫
3,c,08/03/07,ç
```
### Quoting
对于writer来说，默认的引号行为是不同的，所以前面的例子中的第二和第三列没被引号。要添加引号，请将引用参数设置为其他引号模式之一。
```
writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
```
在本例中，QUOTE_NONNUMERIC在包含非数字值的列周围添加引号。
```
$ python csv_writer_quoted.py testout_quoted.csv

"Title 1","Title 2","Title 3","Title 4"
1,"a","08/01/07","å"
2,"b","08/02/07","∫"
3,"c","08/03/07","ç"
```
有四种不同的引号选项，在csv模块中定义为常量。
+ QUOTE_ALL: 无论什么类型，都加引号。
+ QUOTE_MINIMAL: 使用特殊字符的引号字段(使用相同的方言和选项配置的解析器可能会混淆的任何内容)。这是默认的。
+ QUOTE_NONNUMERIC: 所有非整数或浮点数的字段加引号。当与reader一起使用时，未加引号的输入字段将转换为浮点数。
+ QUOTE_NONE: 不在输出的任何内容上加引号。当与reader一起使用时，引号字符被包含在字段值中(通常，它们被视为分隔符并被删除)。

## Dialects
没有为逗号分隔的值文件定义良好的标准，因此解析器需要灵活。这种灵活性意味着有许多参数可以控制csv如何解析或写入数据。与其将这些参数分别传递给读写器，不如将它们组合成一个方言对象。

方言类可以按名称注册，因此csv模块的调用者不需要预先知道参数设置。可以使用list_dialect()检索已注册的方言的完整列表。
```
# csv_list_dialects.py

import csv

print(csv.list_dialects())
```
标准库包括三种方言:excel、excel-tabs和unix。excel方言是用于处理Microsoft excel默认导出格式的数据，也适用于LibreOffice。unix方言使用双引号引用所有字段，并使用\n作为记录分隔符。
```
$ python csv_list_dialects.py

['excel', 'excel-tab', 'unix']
```
### Creating a Dialect
如果不使用逗号分隔字段，则输入文件使用管道(|)，就像这样
```
"Title 1"|"Title 2"|"Title 3"
1|"first line
second line"|08/18/07
```
可以使用适当的分隔符注册新方言。
```
# csv_dialect.py

import csv

csv.register_dialect('pipes', delimiter='|')

with open('testdata.pipes', 'r') as f:
    reader = csv.reader(f, dialect='pipes')
    for row in reader:
        print(row)
```
使用“管道”方言，可以像读取逗号分隔的文件一样读取文件。
```
$ python csv_dialect.py

['Title 1', 'Title 2', 'Title 3']
['1', 'first line\nsecond line', '08/18/07']
```
### Dialect Parameters
```
# csv_dialect_variations.py

import csv
import sys

csv.register_dialect('escaped',
                     escapechar='\\',
                     doublequote=False,
                     quoting=csv.QUOTE_NONE,
                     )
csv.register_dialect('singlequote',
                     quotechar="'",
                     quoting=csv.QUOTE_ALL,
                     )

quoting_modes = {
    getattr(csv, n): n
    for n in dir(csv)
    if n.startswith('QUOTE_')
}

TEMPLATE = '''\
Dialect: "{name}"

  delimiter   = {dl!r:<6}    skipinitialspace = {si!r}
  doublequote = {dq!r:<6}    quoting          = {qu}
  quotechar   = {qc!r:<6}    lineterminator   = {lt!r}
  escapechar  = {ec!r:<6}
'''

for name in sorted(csv.list_dialects()):
    dialect = csv.get_dialect(name)

    print(TEMPLATE.format(
        name=name,
        dl=dialect.delimiter,
        si=dialect.skipinitialspace,
        dq=dialect.doublequote,
        qu=quoting_modes[dialect.quoting],
        qc=dialect.quotechar,
        lt=dialect.lineterminator,
        ec=dialect.escapechar,
    ))

    writer = csv.writer(sys.stdout, dialect=dialect)
    writer.writerow(
        ('col1', 1, '10/01/2010',
         'Special chars: " \' {} to parse'.format(
             dialect.delimiter))
    )
    print()
```
这个程序显示了在使用不同的方言进行格式化时如何显示相同的数据。
```
$ python csv_dialect_variations.py

Dialect: "escaped"

  delimiter   = ','       skipinitialspace = 0
  doublequote = 0         quoting          = QUOTE_NONE
  quotechar   = '"'       lineterminator   = '\r\n'
  escapechar  = '\\'

col1,1,10/01/2010,Special chars: \" ' \, to parse

Dialect: "excel"

  delimiter   = ','       skipinitialspace = 0
  doublequote = 1         quoting          = QUOTE_MINIMAL
  quotechar   = '"'       lineterminator   = '\r\n'
  escapechar  = None

col1,1,10/01/2010,"Special chars: "" ' , to parse"

Dialect: "excel-tab"

  delimiter   = '\t'      skipinitialspace = 0
  doublequote = 1         quoting          = QUOTE_MINIMAL
  quotechar   = '"'       lineterminator   = '\r\n'
  escapechar  = None

col1    1       10/01/2010      "Special chars: "" '     to parse"

Dialect: "singlequote"

  delimiter   = ','       skipinitialspace = 0
  doublequote = 1         quoting          = QUOTE_ALL
  quotechar   = "'"       lineterminator   = '\r\n'
  escapechar  = None

'col1','1','10/01/2010','Special chars: " '' , to parse'

Dialect: "unix"

  delimiter   = ','       skipinitialspace = 0
  doublequote = 1         quoting          = QUOTE_ALL
  quotechar   = '"'       lineterminator   = '\n'
  escapechar  = None

"col1","1","10/01/2010","Special chars: "" ' , to parse"
```
### Automatically Detecting Dialects
配置用于解析输入文件的方言的最佳方式是事先知道正确的设置。对于不知道方言参数的数据，可以使用Sniffer类进行有根据的猜测。sniff()方法获取输入数据的一个样本，以及一个可选参数，给出可能的分隔字符。
```
# csv_dialect_sniffer.py

import csv
from io import StringIO
import textwrap

csv.register_dialect('escaped',
                     escapechar='\\',
                     doublequote=False,
                     quoting=csv.QUOTE_NONE)
csv.register_dialect('singlequote',
                     quotechar="'",
                     quoting=csv.QUOTE_ALL)

# Generate sample data for all known dialects
samples = []
for name in sorted(csv.list_dialects()):
    buffer = StringIO()
    dialect = csv.get_dialect(name)
    writer = csv.writer(buffer, dialect=dialect)
    writer.writerow(
        ('col1', 1, '10/01/2010',
         'Special chars " \' {} to parse'.format(
             dialect.delimiter))
    )
    samples.append((name, dialect, buffer.getvalue()))

# Guess the dialect for a given sample, and then use the results
# to parse the data.
sniffer = csv.Sniffer()
for name, expected, sample in samples:
    print('Dialect: "{}"'.format(name))
    print('In: {}'.format(sample.rstrip()))
    dialect = sniffer.sniff(sample, delimiters=',\t')
    reader = csv.reader(StringIO(sample), dialect=dialect)
    print('Parsed:\n  {}\n'.format(
          '\n  '.join(repr(r) for r in next(reader))))
```
sniff()返回一个方言实例，其中包含用于解析数据的设置。结果并不总是完美的，如示例中的“转义”方言所示。
```
$ python csv_dialect_sniffer.py

Dialect: "escaped"
In: col1,1,10/01/2010,Special chars \" ' \, to parse
Parsed:
  'col1'
  '1'
  '10/01/2010'
  'Special chars \\" \' \\'
  ' to parse'

Dialect: "excel"
In: col1,1,10/01/2010,"Special chars "" ' , to parse"
Parsed:
  'col1'
  '1'
  '10/01/2010'
  'Special chars " \' , to parse'

Dialect: "excel-tab"
In: col1        1       10/01/2010      "Special chars "" '      to parse"
Parsed:
  'col1'
  '1'
  '10/01/2010'
  'Special chars " \' \t to parse'

Dialect: "singlequote"
In: 'col1','1','10/01/2010','Special chars " '' , to parse'
Parsed:
  'col1'
  '1'
  '10/01/2010'
  'Special chars " \' , to parse'

Dialect: "unix"
In: "col1","1","10/01/2010","Special chars "" ' , to parse"
Parsed:
  'col1'
  '1'
  '10/01/2010'
  'Special chars " \' , to parse'
```
## Using Field Names
除了处理数据序列之外，csv模块还包含用于将行作为字典使用的类，以便可以对字段进行命名。DictReader和DictWriter类将行转换为字典，而不是清单。可以传入字典的键，或者从输入的第一行推断(当行包含头时)。
```
# csv_dictreader.py

import csv
import sys

with open(sys.argv[1], 'rt', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```
基于字典的读取器和写入器作为基于序列的类的包装器实现，并使用相同的方法和参数。reader API的唯一不同之处在于，行作为OrderedDict实例返回，而不是作为列表或元组返回(在Python早期的verison之下，行作为常规的dict实例返回)。
```
$ python csv_dictreader.py testdata.csv

OrderedDict([('Title 1', '1'), ('Title 2', 'a'), ('Title 3', '08/18/07'), ('Title 4', 'å')])
OrderedDict([('Title 1', '2'), ('Title 2', 'b'), ('Title 3', '08/19/07'), ('Title 4', '∫')])
OrderedDict([('Title 1', '3'), ('Title 2', 'c'), ('Title 3', '08/20/07'), ('Title 4', 'ç')])
```
必须给DictWriter一个字段名列表，以便它知道如何对输出中的列进行排序。
```
# csv_dictwriter.py

import csv
import sys

fieldnames = ('Title 1', 'Title 2', 'Title 3', 'Title 4')
headers = {
    n: n
    for n in fieldnames
}
unicode_chars = 'å∫ç'

with open(sys.argv[1], 'wt', encoding='utf-8') as f:

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(3):
        writer.writerow({
            'Title 1': i + 1,
            'Title 2': chr(ord('a') + i),
            'Title 3': '08/{:02d}/07'.format(i + 1),
            'Title 4': unicode_chars[i],
        })

print(open(sys.argv[1], 'rt', encoding='utf-8').read())
```
字段名不是自动写入文件的，但是可以使用writeheader()方法显式地编写它们。
```
$ python csv_dictwriter.py testout.csv

Title 1,Title 2,Title 3,Title 4
1,a,08/01/07,å
2,b,08/02/07,∫
3,c,08/03/07,ç
```


