## mmap -- Memory-map Files
> 目的：内存映射文件而不是直接读取内容。

内存映射文件使用操作系统虚拟内存系统直接访问文件系统上的数据，而不是使用普通的I/O函数。内存映射通常改进I/O性能，因为它不涉及对每个访问的单独系统调用，也不需要在缓冲区之间复制数据——内核和用户应用程序都直接访问内存。

根据需要，内存映射文件可以被视为可变字符串或类文件对象。映射文件支持预期的文件API方法，如close()、flush()、read()、readline()、seek()、tell()和write()。它还支持string API，具有切片等特性和find()等方法。

所有示例都使用文本文件lorem.txt，包含一点Lorem Ipsum。作为参考，文件的文本是
```
# lorem.txt

Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
Donec egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo,
a elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
facilisi. Sed tristique eros eu libero. Pellentesque vel
arcu. Vivamus purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
dui. Pellentesque habitant morbi tristique senectus et netus et
malesuada fames ac turpis egestas. Aliquam viverra fringilla
leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
mauris in nibh placerat egestas. Suspendisse potenti. Mauris
massa. Ut eget velit auctor tortor blandit sollicitudin. Suspendisse
imperdiet justo
```
注意：Unix和Windows之间的mmap()的参数和行为存在差异，这里没有详细讨论。有关更多细节，请参考标准库文档。

## Reading
使用mmap()函数创建一个内存映射文件。第一个参数是一个文件描述符，要么来自file对象的fileno()方法，要么来自os.open()。调用者负责在调用mmap()之前打开文件，在不再需要它之后关闭它。

mmap()的第二个参数是用于映射文件的部分的字节大小。如果值为0，则映射整个文件。如果文件的大小大于当前文件的大小，则扩展文件。

注意：Windows不支持创建零长度映射。

两个平台都支持可选的关键字参数access。为只读访问使用ACCESS_READ，读写器的读写方法(分配给内存的任务直接指向文件)，或者用于复制-on-write的ACCESS_COPY(分配到内存的任务没有写到文件中)。
```
# mmap_read.py

import mmap

with open('lorem.txt', 'r') as f:
    with mmap.mmap(f.fileno(), 0,
                   access=mmap.ACCESS_READ) as m:
        print('First 10 bytes via read :', m.read(10))
        print('First 10 bytes via slice:', m[:10])
        print('2nd   10 bytes via read :', m.read(10))
```
文件指针跟踪通过切片操作访问的最后一个字节。在本例中，指针在第一次读取后向前移动了10个字节。然后通过切片操作将其重置到文件的开头，然后再由切片向前移动10字节。在切片操作之后，再次调用read()将在文件中返回11-20个字节。
```
$ python mmap_read.py
First 10 bytes via read : b'Lorem ipsu'
First 10 bytes via slice: b'Lorem ipsu'
2nd   10 bytes via read : b'm dolor si'
```
## Writing
要设置内存映射文件来接收更新，首先打开它，在映射之前将它添加到mode 'r+'(不是'w')中。然后使用任何改变数据的API方法(write()、分配给切片等)。

下一个示例使用ACCESS_WRITE的默认访问模式并将其分配给一个切片，以修改适当的行。
```
# mmap_write_slice.py

import mmap
import shutil

# Copy the example file
shutil.copyfile('lorem.txt', 'lorem_copy.txt')

word = b'consectetuer'
reversed = word[::-1]
print('Looking for    :', word)
print('Replacing with :', reversed)

with open('lorem_copy.txt', 'r+') as f:
    with mmap.mmap(f.fileno(), 0) as m:
        print('Before:\n{}'.format(m.readline().rstrip()))
        m.seek(0)  # rewind

        loc = m.find(word)
        m[loc:loc + len(word)] = reversed
        m.flush()

        m.seek(0)  # rewind
        print('After :\n{}'.format(m.readline().rstrip()))

        f.seek(0)  # rewind
        print('File  :\n{}'.format(f.readline().rstrip()))
```
在内存和文件的第一行中间替换了单词“consectetuer”。
```
$ python mmap_write_slice.py

Looking for    : b'consectetuer'
Replacing with : b'reutetcesnoc'
Before:
b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.'
After :
b'Lorem ipsum dolor sit amet, reutetcesnoc adipiscing elit.'
File  :
Lorem ipsum dolor sit amet, reutetcesnoc adipiscing elit.
```
### Copy Mode
使用访问设置ACCESS_COPY不会将更改写入磁盘上的文件。
```
# mmap_write_copy.py

import mmap
import shutil

# Copy the example file
shutil.copyfile('lorem.txt', 'lorem_copy.txt')

word = b'consectetuer'
reversed = word[::-1]

with open('lorem_copy.txt', 'r+') as f:
    with mmap.mmap(f.fileno(), 0,
                   access=mmap.ACCESS_COPY) as m:
        print('Memory Before:\n{}'.format(
            m.readline().rstrip()))
        print('File Before  :\n{}\n'.format(
            f.readline().rstrip()))

        m.seek(0)  # rewind
        loc = m.find(word)
        m[loc:loc + len(word)] = reversed

        m.seek(0)  # rewind
        print('Memory After :\n{}'.format(
            m.readline().rstrip()))

        f.seek(0)
        print('File After   :\n{}'.format(
            f.readline().rstrip()))
```
需要将本例中的文件句柄与mmap句柄分开回绕，因为这两个对象的内部状态是分开维护的。
```
$ python mmap_write_copy.py

Memory Before:
b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit.'
File Before  :
Lorem ipsum dolor sit amet, consectetuer adipiscing elit.

Memory After :
b'Lorem ipsum dolor sit amet, reutetcesnoc adipiscing elit.'
File After   :
Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
```
### Regular Expressions
由于内存映射文件可以充当字符串，因此可以将它与其他操作字符串的模块一起使用，例如正则表达式。这个示例查找所有包含“nulla”的句子。
```
# mmap_regex.py

import mmap
import re

pattern = re.compile(rb'(\.\W+)?([^.]?nulla[^.]*?\.)',
                     re.DOTALL | re.IGNORECASE | re.MULTILINE)

with open('lorem.txt', 'r') as f:
    with mmap.mmap(f.fileno(), 0,
                   access=mmap.ACCESS_READ) as m:
        for match in pattern.findall(m):
            print(match[1].replace(b'\n', b' '))
```
因为该模式包含两个组，所以findall()的返回值是一个元组序列。print语句取出匹配的句子，并用空格替换换行，以便每个结果都在一行上打印。
```
$ python mmap_regex.py

b'Nulla\r facilisi.'
b'Nulla feugiat augue eleifend nulla.'
```
