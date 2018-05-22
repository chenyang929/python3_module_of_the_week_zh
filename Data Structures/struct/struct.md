# struct -- Binary Data Structures
> 目的：在字符串和二进制数据之间进行转换。

struct模块包括用于在字节字符串和原生Python数据类型(如数字和字符串)之间转换的函数。
## Functions versus Struct Class
可以使用一组模块级别的函数来处理结构化值和Struct类。格式说明符由字符串格式转换为已编译的表示形式，类似于处理正则表达式的方式。
转换需要一些资源，因此在创建结构实例和实例调用方法(而不是使用模块级函数)时，通常会更高效。下面的所有示例都使用Struct类。
## Packing and Unpacking
Structs支持将数据打包成字符串，并使用由表示数据类型的字符和可选的count和endianness指示器组成的字符串来从字符串中提取数据。有关支持的格式说明符的完整列表，请参阅标准库文档。

在本例中，说明符需要一个整数或长整数值，一个双字节字符串和浮点数。格式说明符中的空格被包含在分隔类型指示器上，并且在编译格式时被忽略。
<pre><code># struct_pack.py

import struct
import binascii

values = (1, 'ab'.encode('utf-8'), 2.7)
s = struct.Struct('I 2s f')
packed_data = s.pack(*values)

print('Original values:', values)
print('Format string  :', s.format)
print('Uses           :', s.size, 'bytes')
print('Packed Value   :', binascii.hexlify(packed_data))</pre></code>
这个示例将填充的值转换为一个十六进制字节序列，以便与binascii.hexlify()一起打印，因为其中一些字符是空的。
<pre><code>$ python struct_pack.py
Original values: (1, b'ab', 2.7)
Format string  : b'I 2s f'
Uses           : 12 bytes
Packed Value   : b'0100000061620000cdcc2c40'</pre></code>
使用unpack()从填充的表示中提取数据。
<pre><code># struct_unpack.py

import struct
import binascii

packed_data = binascii.unhexlify(b'0100000061620000cdcc2c40')

s = struct.Struct('I 2s f')
unpacked_data = s.unpack(packed_data)
print('Unpacked Values:', unpacked_data)</pre></code>
将包装的值传递给unpack()时，会得到基本相同的值(注意浮点值的差异)。
<pre><code>$ python struct_unpack.py
Unpacked Values: (1, b'ab', 2.700000047683716)</pre></code>
## Endianness
默认情况下，值是使用本机C库的endianness概念进行编码的。通过在格式字符串中提供显式的endianness指令，很容易重写该选项。
<pre><code># struct_endianness.py

import struct
import binascii

values = (1, 'ab'.encode('utf-8'), 2.7)
print('Original values:', values)

endianness = [
    ('@', 'native, native'),
    ('=', 'native, standard'),
    ('<', 'little-endian'),
    ('>', 'big-endian'),
    ('!', 'network'),
]

for code, name in endianness:
    s = struct.Struct(code + ' I 2s f')
    packed_data = s.pack(*values)
    print()
    print('Format string  :', s.format, 'for', name)
    print('Uses           :', s.size, 'bytes')
    print('Packed Value   :', binascii.hexlify(packed_data))
    print('Unpacked Value :', s.unpack(packed_data))</pre></code>
endianness中元祖第二项是第一项的含义。
<pre><code>$ python struct_endianness.py
Original values: (1, b'ab', 2.7)

Format string  : b'@ I 2s f' for native, native
Uses           : 12 bytes
Packed Value   : b'0100000061620000cdcc2c40'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string  : b'= I 2s f' for native, standard
Uses           : 10 bytes
Packed Value   : b'010000006162cdcc2c40'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string  : b'< I 2s f' for little-endian
Uses           : 10 bytes
Packed Value   : b'010000006162cdcc2c40'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string  : b'> I 2s f' for big-endian
Uses           : 10 bytes
Packed Value   : b'000000016162402ccccd'
Unpacked Value : (1, b'ab', 2.700000047683716)

Format string  : b'! I 2s f' for network
Uses           : 10 bytes
Packed Value   : b'000000016162402ccccd'
Unpacked Value : (1, b'ab', 2.700000047683716)</pre></code>
## Buffers
使用二进制填充数据通常是为性能敏感的情况保留的，或者将数据输入和输出扩展模块。可以通过避免为每个填充结构分配一个新缓冲区的开销来优化这些情况。
pack_into()和unpack_from()方法直接支持写入预先分配的缓冲区。
<pre><code># struct_buffers.py

import array
import binascii
import ctypes
import struct

s = struct.Struct('I 2s f')
values = (1, 'ab'.encode('utf-8'), 2.7)
print('Original:', values)

print()
print('ctypes string buffer')

b = ctypes.create_string_buffer(s.size)
print('Before  :', binascii.hexlify(b.raw))
s.pack_into(b, 0, *values)
print('After   :', binascii.hexlify(b.raw))
print('Unpacked:', s.unpack_from(b, 0))

print()
print('array')

a = array.array('b', b'\0' * s.size)
print('Before  :', binascii.hexlify(a))
s.pack_into(a, 0, *values)
print('After   :', binascii.hexlify(a))
print('Unpacked:', s.unpack_from(a, 0))</pre></code>
结构的大小属性告诉我们缓冲区需要多大。
<pre><code>$ python struct_buffers.py
Original: (1, b'ab', 2.7)

ctypes string buffer
Before  : b'000000000000000000000000'
After   : b'0100000061620000cdcc2c40'
Unpacked: (1, b'ab', 2.700000047683716)

array
Before  : b'000000000000000000000000'
After   : b'0100000061620000cdcc2c40'
Unpacked: (1, b'ab', 2.700000047683716)</pre></code>
