# io -- Text, Binary, and Raw Stream I/O Tools
> 目的：实现文件I/O并提供使用类文件API处理缓冲区的类。

io模块为基于文件的输入和输出操作实现解释器内置open()后面的类。这些类的分解方式是这样的:它们可以被重新组合，以实现其他目的，例如允许将Unicode数据写入网络套接字。
## In-memory Streams
StringIO提供了使用file API (read()、write()等)处理内存中的文本的方便方法。在某些情况下，使用StringIO构建大型字符串可以比其他一些字符串连接技术节省性能。内存流缓冲区对于测试也很有用，在测试中向磁盘上的真实文件写入可能会减慢测试套件的速度。

下面是一些使用StringIO缓冲区的标准示例:
```
# io_stringio.py

import io

# Writing to a buffer
output = io.StringIO()
output.write('This goes into the buffer. ')
print('And so does this.', file=output)

# Retrieve the value written
print(output.getvalue())

output.close()  # discard buffer memory

# Initialize a read buffer
input = io.StringIO('Inital value for read buffer')

# Read from the buffer
print(input.read())
```
这个示例使用read()，但是readline()和readlines()方法也是可用的。StringIO类还提供了一个seek()方法，用于在读取时在缓冲区中进行跳转，如果正在使用查找前面的解析算法，那么该方法对于重卷很有用。
```
$ python io_stringio.py

This goes into the buffer. And so does this.

Inital value for read buffer
```
要使用原始字节而不是Unicode文本，请使用BytesIO。
```
# io_bytesio.py

import io

# Writing to a buffer
output = io.BytesIO()
output.write('This goes into the buffer. '.encode('utf-8'))
output.write('ÁÇÊ'.encode('utf-8'))

# Retrieve the value written
print(output.getvalue())

output.close()  # discard buffer memory

# Initialize a read buffer
input = io.BytesIO(b'Inital value for read buffer')

# Read from the buffer
print(input.read())
```
写入BytesIO的值必须是字节，而不是str。
```
$ python io_bytesio.py

b'This goes into the buffer. \xc3\x81\xc3\x87\xc3\x8a'
b'Inital value for read buffer'
```
# Wrapping Byte Streams for Text Data
原始字节流(如套接字)可以用一个层包装起来，以处理字符串编码和解码，使它们更容易与文本数据一起使用。TextIOWrapper类支持写作和阅读。write_through参数禁用缓冲，并立即将写入包装器的所有数据刷新到底层缓冲区。
```
# io_textiowrapper.py

import io

# Writing to a buffer
output = io.BytesIO()
wrapper = io.TextIOWrapper(
    output,
    encoding='utf-8',
    write_through=True,
)
wrapper.write('This goes into the buffer. ')
wrapper.write('ÁÇÊ')

# Retrieve the value written
print(output.getvalue())

output.close()  # discard buffer memory

# Initialize a read buffer
input = io.BytesIO(
    b'Inital value for read buffer with unicode characters ' +
    'ÁÇÊ'.encode('utf-8')
)
wrapper = io.TextIOWrapper(input, encoding='utf-8')

# Read from the buffer
print(wrapper.read())
```
这个示例使用BytesIO实例作为流。使用TextIOWrapper与其他类型的类文件对象演示示例bz2, http.server和子进程。
```
$ python io_textiowrapper.py

b'This goes into the buffer. \xc3\x81\xc3\x87\xc3\x8a'
Inital value for read buffer with unicode characters ÁÇÊ
```


