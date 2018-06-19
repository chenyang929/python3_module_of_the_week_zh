codecs -- String Encoding and Decoding
> 目的：编码器和解码器在不同表示之间转换文本。

codecs模块提供了用于传输数据的流和文件接口。它通常用于处理Unicode文本，但是其他的编码也可以用于其他目的。
## Unicode Primer
CPython3.x区分文本和字节字符串。字节实例使用8位字节值的序列。相反，str字符串是在内部管理的，作为Unicode代码点的序列。代码点值保存为每个2或4字节的序列，具体取决于编译Python时给出的选项。

当输出str值时，使用几种标准方案之一对它们进行编码，以便以后可以将字节序列重构为相同的文本字符串。编码值的字节不一定与代码点值相同，编码定义了在两组值之间进行转换的方法。读取Unicode数据还需要知道编码，以便可以将传入的字节转换为Unicode类使用的内部表示形式。

西方语言最常见的编码是UTF-8和UTF-16，它们分别使用一个字节值和两个字节值的序列来表示每个代码点。其他编码可以更有效地存储语言，在这些语言中，大多数字符由不适合两个字节的代码点表示。
### Encodings
理解编码的最佳方法是查看通过以不同的方式编码相同字符串产生的不同字节序列。下面的示例使用此函数格式化字节字符串，使其更易于读取。
```
# codecs_to_hex.py

import binascii


def to_hex(t, nbytes):
    """Format text t as a sequence of nbyte long values
    separated by spaces.
    """
    chars_per_item = nbytes * 2
    hex_version = binascii.hexlify(t)
    return b' '.join(
        hex_version[start:start + chars_per_item]
        for start in range(0, len(hex_version), chars_per_item)
    )


if __name__ == '__main__':
    print(to_hex(b'abcdef', 1))
    print(to_hex(b'abcdef', 2))
```
该函数使用binascii获取输入字节字符串的十六进制表示，然后在返回值之前在每个nbytes字节之间插入空格。
```
$ python codecs_to_hex.py

b'61 62 63 64 65 66'
b'6162 6364 6566'
```
第一个编码示例首先使用unicode类的原始表示形式打印文本“francais”，然后使用unicode数据库中的每个字符的名称。接下来的两行分别将字符串编码为UTF-8和UTF-16，并显示编码产生的十六进制值。
```
# codecs_encodings.py

import unicodedata
from codecs_to_hex import to_hex

text = 'français'

print('Raw   : {!r}'.format(text))
for c in text:
    print('  {!r}: {}'.format(c, unicodedata.name(c, c)))
print('UTF-8 : {!r}'.format(to_hex(text.encode('utf-8'), 1)))
print('UTF-16: {!r}'.format(to_hex(text.encode('utf-16'), 2)))
```
编码str的结果是一个字节对象。
```
$ python codecs_encodings.py

Raw   : 'français'
  'f': LATIN SMALL LETTER F
  'r': LATIN SMALL LETTER R
  'a': LATIN SMALL LETTER A
  'n': LATIN SMALL LETTER N
  'ç': LATIN SMALL LETTER C WITH CEDILLA
  'a': LATIN SMALL LETTER A
  'i': LATIN SMALL LETTER I
  's': LATIN SMALL LETTER S
UTF-8 : b'66 72 61 6e c3 a7 61 69 73'
UTF-16: b'fffe 6600 7200 6100 6e00 e700 6100 6900 7300'
```
如果将编码的字节序列作为字节实例，decode()方法将它们转换为代码点，并作为str实例返回序列。
```
# codecs_decode.py

from codecs_to_hex import to_hex

text = 'français'
encoded = text.encode('utf-8')
decoded = encoded.decode('utf-8')

print('Original :', repr(text))
print('Encoded  :', to_hex(encoded, 1), type(encoded))
print('Decoded  :', repr(decoded), type(decoded))
```
所使用的编码的选择不会改变输出类型。
```
$ python codecs_decode.py

Original : 'français'
Encoded  : b'66 72 61 6e c3 a7 61 69 73' <class 'bytes'>
Decoded  : 'français' <class 'str'>
```
## Working with Files
编码和解码字符串在处理I/O操作时尤为重要。无论是写入文件、套接字或其他流，数据都必须使用正确的编码。通常，所有文本数据都需要在读取时从字节表示中解码，并在写入时从内部值编码到特定的表示。程序可以显式地对数据进行编码和解码，但根据使用的编码，可以确定是否已经读取了足够的字节以充分解码数据。codecs提供了管理数据编码和解码的类，因此应用程序不必这样做。

codecs提供的最简单的接口是内置的open()函数的替代品。新版本的工作方式与内置的一样，但是添加了两个新的参数来指定编码和所需的错误处理技术。
```
# codecs_open_write.py

from codecs_to_hex import to_hex

import codecs
import sys

encoding = sys.argv[1]
filename = encoding + '.txt'

print('Writing to', filename)
with codecs.open(filename, mode='w', encoding=encoding) as f:
    f.write('français')

# Determine the byte grouping to use for to_hex()
nbytes = {
    'utf-8': 1,
    'utf-16': 2,
    'utf-32': 4,
}.get(encoding, 1)

# Show the raw bytes in the file
print('File contents:')
with open(filename, mode='rb') as f:
    print(to_hex(f.read(), nbytes))
```
这个示例以一个带有“ç”的unicode字符串开始，并使用命令行指定的编码将文本保存到文件中。
```
$ python codecs_open_write.py utf-8

Writing to utf-8.txt
File contents:
b'66 72 61 6e c3 a7 61 69 73'

$ python codecs_open_write.py utf-16

Writing to utf-16.txt
File contents:
b'fffe 6600 7200 6100 6e00 e700 6100 6900 7300'

$ python codecs_open_write.py utf-32

Writing to utf-32.txt
File contents:
b'fffe0000 66000000 72000000 61000000 6e000000 e7000000 61000000
69000000 73000000'
```
使用open()读取数据很简单，只需一个条件:必须事先知道编码，以便正确设置解码器。有些数据格式(如XML)将编码指定为文件的一部分，但通常由应用程序管理。codecs只是将编码作为参数，并假设它是正确的。
```
# codecs_open_read.py

import codecs
import sys

encoding = sys.argv[1]
filename = encoding + '.txt'

print('Reading from', filename)
with codecs.open(filename, mode='r', encoding=encoding) as f:
    print(repr(f.read()))
```
这个示例读取上一个程序创建的文件，并将结果unicode对象的表示形式打印到控制台。
```
$ python codecs_open_read.py utf-8

Reading from utf-8.txt
'français'

$ python codecs_open_read.py utf-16

Reading from utf-16.txt
'français'

$ python codecs_open_read.py utf-32

Reading from utf-32.txt
'français
```
## Byte Order
多字节编码如UTF-16和UTF-32在不同计算机系统之间传输数据时产生了问题，无论是直接复制文件还是通过网络通信。不同的系统使用不同的高阶和低阶字节排序。数据的这种特性(称为意外发现)取决于诸如硬件架构和操作系统和应用程序开发人员的选择等因素。对于给定的一组数据，并不总是能够预先知道使用哪个字节顺序，所以多字节编码包括字节顺序标记(BOM)作为编码输出的前几个字节。例如，UTF-16的定义方式是:0xFFFE和0xFEFF不是有效字符，可以用来表示字节顺序。codecs为UTF-16和UTF-32使用的字节顺序标记定义常量。
```
# codecs_bom.py

import codecs
from codecs_to_hex import to_hex

BOM_TYPES = [
    'BOM', 'BOM_BE', 'BOM_LE',
    'BOM_UTF8',
    'BOM_UTF16', 'BOM_UTF16_BE', 'BOM_UTF16_LE',
    'BOM_UTF32', 'BOM_UTF32_BE', 'BOM_UTF32_LE',
]

for name in BOM_TYPES:
    print('{:12} : {}'.format(
        name, to_hex(getattr(codecs, name), 2)))
```
BOM、BOM_UTF16和BOM_UTF32将根据当前系统的本地字节顺序自动设置为适当的大字节或小字节值。
```
$ python codecs_bom.py

BOM          : b'fffe'
BOM_BE       : b'feff'
BOM_LE       : b'fffe'
BOM_UTF8     : b'efbb bf'
BOM_UTF16    : b'fffe'
BOM_UTF16_BE : b'feff'
BOM_UTF16_LE : b'fffe'
BOM_UTF32    : b'fffe 0000'
BOM_UTF32_BE : b'0000 feff'
BOM_UTF32_LE : b'fffe 0000'
```
字节排序由编解码器自动检测和处理，但是在编码时可以指定显式排序。
```
# codecs_bom_create_file.py

import codecs
from codecs_to_hex import to_hex

# Pick the nonnative version of UTF-16 encoding
if codecs.BOM_UTF16 == codecs.BOM_UTF16_BE:
    bom = codecs.BOM_UTF16_LE
    encoding = 'utf_16_le'
else:
    bom = codecs.BOM_UTF16_BE
    encoding = 'utf_16_be'

print('Native order  :', to_hex(codecs.BOM_UTF16, 2))
print('Selected order:', to_hex(bom, 2))

# Encode the text.
encoded_text = 'français'.encode(encoding)
print('{:14}: {}'.format(encoding, to_hex(encoded_text, 2)))

with open('nonnative-encoded.txt', mode='wb') as f:
    # Write the selected byte-order marker.  It is not included
    # in the encoded text because the byte order was given
    # explicitly when selecting the encoding.
    f.write(bom)
    # Write the byte string for the encoded text.
    f.write(encoded_text)
```
codecs_bom_create_file.py计算出本机字节顺序，然后显式地使用替代表单，以便下一个示例在读取时显示自动检测。
```
$ python codecs_bom_create_file.py

Native order  : b'fffe'
Selected order: b'feff'
utf_16_be     : b'0066 0072 0061 006e 00e7 0061 0069 0073'
```
codecs_bom_detection.py在打开文件时没有指定字节顺序，因此解码器使用文件前两个字节中的BOM值来确定它。
```
# codecs_bom_detection.py

import codecs
from codecs_to_hex import to_hex

# Look at the raw data
with open('nonnative-encoded.txt', mode='rb') as f:
    raw_bytes = f.read()

print('Raw    :', to_hex(raw_bytes, 2))

# Re-open the file and let codecs detect the BOM
with codecs.open('nonnative-encoded.txt',
                 mode='r',
                 encoding='utf-16',
                 ) as f:
    decoded_text = f.read()

print('Decoded:', repr(decoded_text))
```
由于文件的前两个字节用于字节顺序检测，所以它们不包含在read()返回的数据中。
```
$ python codecs_bom_detection.py

Raw    : b'feff 0066 0072 0061 006e 00e7 0061 0069 0073'
Decoded: 'français'
```
## Error Handling
### Encoding Errors
最常见的错误条件是在将Unicode数据写入ASCII输出流(如常规文件或sys)时接收UnicodeEncodeError。没有更健壮的编码集的stdout。这个示例程序可以用来实验不同的错误处理模式。
```
# codecs_encode_error.py

import codecs
import sys

error_handling = sys.argv[1]

text = 'français'

try:
    # Save the data, encoded as ASCII, using the error
    # handling mode specified on the command line.
    with codecs.open('encode_error.txt', 'w',
                     encoding='ascii',
                     errors=error_handling) as f:
        f.write(text)

except UnicodeEncodeError as err:
    print('ERROR:', err)

else:
    # If there was no error writing to the file,
    # show what it contains.
    with open('encode_error.txt', 'rb') as f:
        print('File contents: {!r}'.format(f.read()))
```
虽然严格模式对于确保应用程序显式地为所有I/O操作设置正确的编码是最安全的，但是当出现异常时，它可能导致程序崩溃。
```
$ python codecs_encode_error.py strict

ERROR: 'ascii' codec can't encode character '\xe7' in position
4: ordinal not in range(128)
```
其他一些错误模式更加灵活。例如，replace确保不会增加错误，代价是可能丢失无法转换为所请求编码的数据。对于pi的Unicode字符仍然不能用ASCII编码，但是替换字符替换为?在输出。
```
$ python codecs_encode_error.py replace

File contents: b'fran?ais
```
要完全跳过问题数据，请使用ignore。不能编码的任何数据都将被丢弃。
```
$ python codecs_encode_error.py ignore

File contents: b'franais'
```
有两个无损错误处理选项，它们都用一个标准定义的替代表示替换字符，该标准与编码分离。xmlcharrestplace使用XML字符引用作为替代(字符引用的列表在W3C文档XML实体定义中指定)。
```
$ python codecs_encode_error.py xmlcharrefreplace

File contents: b'fran&#231;ais'
```
另一种无损错误处理方案是backslashreplace，它生成一种输出格式，如打印unicode对象的repr()时返回的值。Unicode字符被替换为\u，后面跟着代码点的十六进制值。
```
$ python codecs_encode_error.py backslashreplace

File contents: b'fran\\xe7ais'
```
### Decoding Errors
在解码数据时也可以看到错误，特别是如果使用了错误的编码。
```
# codecs_decode_error.py

import codecs
import sys

from codecs_to_hex import to_hex

error_handling = sys.argv[1]

text = 'français'
print('Original     :', repr(text))

# Save the data with one encoding
with codecs.open('decode_error.txt', 'w',
                 encoding='utf-16') as f:
    f.write(text)

# Dump the bytes from the file
with open('decode_error.txt', 'rb') as f:
    print('File contents:', to_hex(f.read(), 1))

# Try to read the data with the wrong encoding
with codecs.open('decode_error.txt', 'r',
                 encoding='utf-8',
                 errors=error_handling) as f:
    try:
        data = f.read()
    except UnicodeDecodeError as err:
        print('ERROR:', err)
    else:
        print('Read         :', repr(data))
```
与编码一样，如果不能正确解码字节流，严格的错误处理模式会引发异常。在这种情况下，UnicodeDecodeError会尝试使用UTF-8解码器将UTF-16 BOM的一部分转换为字符。
```
$ python codecs_decode_error.py strict

Original     : 'français'
File contents: b'ff fe 66 00 72 00 61 00 6e 00 e7 00 61 00 69 00
73 00'
ERROR: 'utf-8' codec can't decode byte 0xff in position 0:
invalid start byte
```
切换为忽略将导致解码器跳过无效字节。但是，结果仍然不完全是预期的，因为它包含了嵌入的空字节。
```
$ python codecs_decode_error.py ignore

Original     : 'français'
File contents: b'ff fe 66 00 72 00 61 00 6e 00 e7 00 61 00 69 00
73 00'
Read         : 'f\x00r\x00a\x00n\x00\x00a\x00i\x00s\x00'
```
在替换模式中，无效字节被替换为\uFFFD，这是一个官方的Unicode替换字符，它看起来像一个带有白色问号的黑色背景的钻石。
```
$ python codecs_decode_error.py replace

Original     : 'français'
File contents: b'ff fe 66 00 72 00 61 00 6e 00 e7 00 61 00 69 00
73 00'
Read         : '��f\x00r\x00a\x00n\x00�\x00a\x00i\x00s\x00'
```
## Encoding Translation
尽管大多数应用程序将在内部处理str数据，将其解码或编码为I/O操作的一部分，但有时更改文件的编码而不保留中间数据格式是有用的。EncodedFile()使用一个编码获取一个打开的文件句柄，并使用一个类将数据转换为另一个编码，当I/O发生时。
```
from codecs_to_hex import to_hex

import codecs
import io

# Raw version of the original data.
data = 'français'

# Manually encode it as UTF-8.
utf8 = data.encode('utf-8')
print('Start as UTF-8   :', to_hex(utf8, 1))

# Set up an output buffer, then wrap it as an EncodedFile.
output = io.BytesIO()
encoded_file = codecs.EncodedFile(output, data_encoding='utf-8',
                                  file_encoding='utf-16')
encoded_file.write(utf8)

# Fetch the buffer contents as a UTF-16 encoded byte string
utf16 = output.getvalue()
print('Encoded to UTF-16:', to_hex(utf16, 2))

# Set up another buffer with the UTF-16 data for reading,
# and wrap it with another EncodedFile.
buffer = io.BytesIO(utf16)
encoded_file = codecs.EncodedFile(buffer, data_encoding='utf-8',
                                  file_encoding='utf-16')

# Read the UTF-8 encoded version of the data.
recoded = encoded_file.read()
print('Back to UTF-8    :', to_hex(recoded, 1))
```
这个示例显示从EncodedFile()返回的句柄中读取和写入。无论句柄是用于读取还是写入，file_encoding总是指作为第一个参数传递的open file句柄所使用的编码，而data_encoding值是通过read()和write()调用传递的数据所使用的编码。
```
$ python codecs_encodefile.py

Start as UTF-8   : b'66 72 61 6e c3 a7 61 69 73'
Encoded to UTF-16: b'fffe 6600 7200 6100 6e00 e700 6100 6900 7300'
Back to UTF-8    : b'66 72 61 6e c3 a7 61 69 73'
```
## Non-Unicode Encodings
虽然前面的大多数示例都使用Unicode编码，但codecs可以用于许多其他数据转换。例如，Python包含用于处理base-64、bzip2、rt -13、ZIP和其他数据格式的codecs。
```
# codecs_rot13.py

import codecs
import io

buffer = io.StringIO()
stream = codecs.getwriter('rot_13')(buffer)

text = 'abcdefghijklmnopqrstuvwxyz'

stream.write(text)
stream.flush()

print('Original:', text)
print('ROT-13  :', buffer.getvalue())
```
任何可以表示为接受单个输入参数并返回字节或Unicode字符串的函数的转换都可以注册为编解码器。对于“rot_13”编解码器，输入应该是一个Unicode字符串，输出也应该是一个Unicode字符串。
```
$ python codecs_rot13.py

Original: abcdefghijklmnopqrstuvwxyz
ROT-13  : nopqrstuvwxyzabcdefghijklm
```
使用编解码器包装数据流比直接使用zlib提供更简单的接口。
```
# codecs_zlib.py

import codecs
import io

from codecs_to_hex import to_hex

buffer = io.BytesIO()
stream = codecs.getwriter('zlib')(buffer)

text = b'abcdefghijklmnopqrstuvwxyz\n' * 50

stream.write(text)
stream.flush()

print('Original length :', len(text))
compressed_data = buffer.getvalue()
print('ZIP compressed  :', len(compressed_data))

buffer = io.BytesIO(compressed_data)
stream = codecs.getreader('zlib')(buffer)

first_line = stream.readline()
print('Read first line :', repr(first_line))

uncompressed_data = first_line + stream.read()
print('Uncompressed    :', len(uncompressed_data))
print('Same            :', text == uncompressed_data)
```
并非所有的压缩或编码系统都支持使用readline()或read()通过流接口读取数据的一部分，因为它们需要找到压缩段的末端来展开数据。如果一个程序不能将整个未压缩的数据集保存在内存中，请使用压缩库的增量访问特性，而不是使用编解码。
```
$ python codecs_zlib.py

Original length : 1350
ZIP compressed  : 48
Read first line : b'abcdefghijklmnopqrstuvwxyz\n'
Uncompressed    : 1350
Same            : True
```
## Incremental Encoding
提供的一些编码，特别是bz2和zlib，在处理数据流时可能会极大地改变数据流的长度。对于大型数据集，这些编码以增量方式更好地操作，一次处理一小块数据。为此目的设计了IncrementalEncoder和IncrementalDecoder API。
```
# codecs_incremental_bz2.py

import codecs
import sys

from codecs_to_hex import to_hex

text = b'abcdefghijklmnopqrstuvwxyz\n'
repetitions = 50

print('Text length :', len(text))
print('Repetitions :', repetitions)
print('Expected len:', len(text) * repetitions)

# Encode the text several times to build up a
# large amount of data
encoder = codecs.getincrementalencoder('bz2')()
encoded = []

print()
print('Encoding:', end=' ')
last = repetitions - 1
for i in range(repetitions):
    en_c = encoder.encode(text, final=(i == last))
    if en_c:
        print('\nEncoded : {} bytes'.format(len(en_c)))
        encoded.append(en_c)
    else:
        sys.stdout.write('.')

all_encoded = b''.join(encoded)
print()
print('Total encoded length:', len(all_encoded))
print()

# Decode the byte string one byte at a time
decoder = codecs.getincrementaldecoder('bz2')()
decoded = []

print('Decoding:', end=' ')
for i, b in enumerate(all_encoded):
    final = (i + 1) == len(text)
    c = decoder.decode(bytes([b]), final)
    if c:
        print('\nDecoded : {} characters'.format(len(c)))
        print('Decoding:', end=' ')
        decoded.append(c)
    else:
        sys.stdout.write('.')
print()

restored = b''.join(decoded)

print()
print('Total uncompressed length:', len(restored))
```
每次将数据传递给编码器或解码器时，它的内部状态都会被更新。当状态是一致的(由codec定义)时，将返回数据并重新设置状态。在此之前，对encode()或decode()的调用将不会返回任何数据。当最后一个数据位传入时，参数final应该设置为True，以便编解码器知道要刷新任何剩余的缓冲数据。
```
$ python codecs_incremental_bz2.py

Text length : 27
Repetitions : 50
Expected len: 1350

Encoding: .................................................
Encoded : 99 bytes

Total encoded length: 99

Decoding: ......................................................
..................................
Decoded : 1350 characters
Decoding: ..........

Total uncompressed length: 1350
```
## Unicode Data and Network Communication
网络套接字是字节流，与标准的输入和输出流不同，它们默认不支持编码。这意味着希望通过网络发送或接收Unicode数据的程序必须在将其写入套接字之前将其编码为字节。此服务器将接收到的数据回传给发送方。
```
# codecs_socket_fail.py

import sys
import socketserver


class Echo(socketserver.BaseRequestHandler):

    def handle(self):
        # Get some bytes and echo them back to the client.
        data = self.request.recv(1024)
        self.request.send(data)
        return


if __name__ == '__main__':
    import codecs
    import socket
    import threading

    address = ('localhost', 0)  # let the kernel assign a port
    server = socketserver.TCPServer(address, Echo)
    ip, port = server.server_address  # what port was assigned?

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Send the data
    # WRONG: Not encoded first!
    text = 'français'
    len_sent = s.send(text)

    # Receive a response
    response = s.recv(len_sent)
    print(repr(response))

    # Clean up
    s.close()
    server.socket.close()
```
可以在每次调用send()之前显式地对数据进行编码，但是丢失一次调用send()将导致编码错误。
```
$ python codecs_socket_fail.py

Traceback (most recent call last):
  File "codecs_socket_fail.py", line 43, in <module>
    len_sent = s.send(text)
TypeError: a bytes-like object is required, not 'str'
```
使用makefile()获取套接字的类似文件的句柄，然后使用基于流的读写器或写入器对其进行包装，这意味着Unicode字符串将在进出套接字的过程中进行编码。
```
# codecs_socket.py

import sys
import socketserver


class Echo(socketserver.BaseRequestHandler):

    def handle(self):
        """Get some bytes and echo them back to the client.

        There is no need to decode them, since they are not used.

        """
        data = self.request.recv(1024)
        self.request.send(data)


class PassThrough:

    def __init__(self, other):
        self.other = other

    def write(self, data):
        print('Writing :', repr(data))
        return self.other.write(data)

    def read(self, size=-1):
        print('Reading :', end=' ')
        data = self.other.read(size)
        print(repr(data))
        return data

    def flush(self):
        return self.other.flush()

    def close(self):
        return self.other.close()


if __name__ == '__main__':
    import codecs
    import socket
    import threading

    address = ('localhost', 0)  # let the kernel assign a port
    server = socketserver.TCPServer(address, Echo)
    ip, port = server.server_address  # what port was assigned?

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Wrap the socket with a reader and writer.
    read_file = s.makefile('rb')
    incoming = codecs.getreader('utf-8')(PassThrough(read_file))
    write_file = s.makefile('wb')
    outgoing = codecs.getwriter('utf-8')(PassThrough(write_file))

    # Send the data
    text = 'français'
    print('Sending :', repr(text))
    outgoing.write(text)
    outgoing.flush()

    # Receive a response
    response = incoming.read()
    print('Received:', repr(response))

    # Clean up
    s.close()
    server.socket.close()
```
这个示例使用PassThrough来显示数据在发送之前被编码，响应在客户机中接收之后被解码。
```
$ python codecs_socket.py

Sending : 'français'
Writing : b'fran\xc3\xa7ais'
Reading : b'fran\xc3\xa7ais'
Reading : b''
Received: 'français'
```
## Defining a Custom Encoding
由于Python已经提供了大量的标准编解码，应用程序不太可能需要定义自定义编码器或解码器。但是，当需要时，codecs中有几个基类可以使过程更容易。

第一步是理解编码描述的转换的本质。这些示例将使用“反大写”编码，将大写字母转换为小写字母，小写字母转换为大写字母。下面是一个编码函数的简单定义，它在输入字符串上执行这个转换。
```
# codecs_invertcaps.py

import string


def invertcaps(text):
    """Return new string with the case of all letters switched.
    """
    return ''.join(
        c.upper() if c in string.ascii_lowercase
        else c.lower() if c in string.ascii_uppercase
        else c
        for c in text
    )


if __name__ == '__main__':
    print(invertcaps('ABCdef'))
    print(invertcaps('abcDEF'))
```
在这种情况下，编码器和解码器是相同的功能(rt -13也是如此)。
```
$ python codecs_invertcaps.py

abcDEF
ABCdef
```
虽然很容易理解，但是这种实现并不高效，特别是对于非常大的文本字符串。幸运的是，codecs包含了一些帮助函数，用于创建基于字符映射的codecs，比如invertcaps。字符映射编码由两个字典组成。编码映射将输入字符串中的字符值转换为输出中的字节值，解码映射则相反。首先创建解码映射，然后使用make_encoding_map()将其转换为编码映射。C函数charmap_encode()和charmap_decode()使用映射来有效地转换它们的输入数据。
```
# codecs_invertcaps_charmap.py

import codecs
import string

# Map every character to itself
decoding_map = codecs.make_identity_dict(range(256))

# Make a list of pairs of ordinal values for the lower
# and uppercase letters
pairs = list(zip(
    [ord(c) for c in string.ascii_lowercase],
    [ord(c) for c in string.ascii_uppercase],
))

# Modify the mapping to convert upper to lower and
# lower to upper.
decoding_map.update({
    upper: lower
    for (lower, upper)
    in pairs
})
decoding_map.update({
    lower: upper
    for (lower, upper)
    in pairs
})

# Create a separate encoding map.
encoding_map = codecs.make_encoding_map(decoding_map)

if __name__ == '__main__':
    print(codecs.charmap_encode('abcDEF', 'strict',
                                encoding_map))
    print(codecs.charmap_decode(b'abcDEF', 'strict',
                                decoding_map))
    print(encoding_map == decoding_map)
```
尽管逆变帽的编码和解码映射是相同的，但也不一定总是如此。make_encoding_map()检测将多个输入字符编码到相同输出字节并将编码值替换为None以将编码标记为未定义的情况。
```
$ python codecs_invertcaps_charmap.py

(b'ABCdef', 6)
('ABCdef', 6)
True
```
字符映射编码器和解码器支持前面描述的所有标准错误处理方法，因此不需要额外的工作来满足API的这一部分。
```
# codecs_invertcaps_error.py

import codecs
from codecs_invertcaps_charmap import encoding_map

text = 'pi: \u03c0'

for error in ['ignore', 'replace', 'strict']:
    try:
        encoded = codecs.charmap_encode(
            text, error, encoding_map)
    except UnicodeEncodeError as err:
        encoded = str(err)
    print('{:7}: {}'.format(error, encoded))
```
因为π的Unicode代码点编码映射,严格的错误处理方式提出了一个例外。
```
$ python3 codecs_invertcaps_error.py

ignore : (b'PI: ', 5)
replace: (b'PI: ?', 5)
strict : 'charmap' codec can't encode character '\u03c0' in position 4: character maps to <undefined>
```
在定义了编码和解码映射之后，需要设置一些额外的类，并注册编码。register()向注册表添加一个搜索函数，以便当用户希望使用编码编解码时可以找到它。搜索函数必须使用带有编码名称的单个字符串参数，如果知道编码，则返回CodecInfo对象，如果不知道编码，则返回None。
```
# codecs_register.py

import codecs
import encodings


def search1(encoding):
    print('search1: Searching for:', encoding)
    return None


def search2(encoding):
    print('search2: Searching for:', encoding)
    return None


codecs.register(search1)
codecs.register(search2)

utf8 = codecs.lookup('utf-8')
print('UTF-8:', utf8)

try:
    unknown = codecs.lookup('no-such-encoding')
except LookupError as err:
    print('ERROR:', err)
```
可以注册多个搜索函数，并依次调用每个函数，直到其中一个返回CodecInfo或列表耗尽。codecs注册的内部搜索函数知道如何从编码中加载UTF-8这样的标准编解码器，因此不会将这些名称传递给自定义搜索函数。
```
$ python codecs_register.py

UTF-8: <codecs.CodecInfo object for encoding utf-8 at 0x1007773a8>
search1: Searching for: no-such-encoding
search2: Searching for: no-such-encoding
ERROR: unknown encoding: no-such-encoding
```
搜索函数返回的CodecInfo实例告诉codecs如何使用支持的所有不同机制进行编码和解码:无状态、增量和流。codecs包含基类来帮助设置字符映射编码。这个示例将所有部分放在一起，以注册一个搜索函数，该函数返回为invertcaps编解码器配置的CodecInfo实例。
```
# codecs_invertcaps_register.py

import codecs

from codecs_invertcaps_charmap import encoding_map, decoding_map


class InvertCapsCodec(codecs.Codec):
    "Stateless encoder/decoder"

    def encode(self, input, errors='strict'):
        return codecs.charmap_encode(input, errors, encoding_map)

    def decode(self, input, errors='strict'):
        return codecs.charmap_decode(input, errors, decoding_map)


class InvertCapsIncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        data, nbytes = codecs.charmap_encode(input,
                                             self.errors,
                                             encoding_map)
        return data


class InvertCapsIncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        data, nbytes = codecs.charmap_decode(input,
                                             self.errors,
                                             decoding_map)
        return data


class InvertCapsStreamReader(InvertCapsCodec,
                             codecs.StreamReader):
    pass


class InvertCapsStreamWriter(InvertCapsCodec,
                             codecs.StreamWriter):
    pass


def find_invertcaps(encoding):
    """Return the codec for 'invertcaps'.
    """
    if encoding == 'invertcaps':
        return codecs.CodecInfo(
            name='invertcaps',
            encode=InvertCapsCodec().encode,
            decode=InvertCapsCodec().decode,
            incrementalencoder=InvertCapsIncrementalEncoder,
            incrementaldecoder=InvertCapsIncrementalDecoder,
            streamreader=InvertCapsStreamReader,
            streamwriter=InvertCapsStreamWriter,
        )
    return None


codecs.register(find_invertcaps)

if __name__ == '__main__':

    # Stateless encoder/decoder
    encoder = codecs.getencoder('invertcaps')
    text = 'abcDEF'
    encoded_text, consumed = encoder(text)
    print('Encoded "{}" to "{}", consuming {} characters'.format(
        text, encoded_text, consumed))

    # Stream writer
    import io
    buffer = io.BytesIO()
    writer = codecs.getwriter('invertcaps')(buffer)
    print('StreamWriter for io buffer: ')
    print('  writing "abcDEF"')
    writer.write('abcDEF')
    print('  buffer contents: ', buffer.getvalue())

    # Incremental decoder
    decoder_factory = codecs.getincrementaldecoder('invertcaps')
    decoder = decoder_factory()
    decoded_text_parts = []
    for c in encoded_text:
        decoded_text_parts.append(
            decoder.decode(bytes([c]), final=False)
        )
    decoded_text_parts.append(decoder.decode(b'', final=True))
    decoded_text = ''.join(decoded_text_parts)
    print('IncrementalDecoder converted {!r} to {!r}'.format(
        encoded_text, decoded_text))
```
无状态的编码器/解码器基类是编解码器。用新实现覆盖encode()和decode()(在本例中，分别调用charmap_encode()和charmap_decode())。每个方法必须返回一个元组，该元组包含转换后的数据和所使用的输入字节或字符的数量。很方便的是，charmap_encode()和charmap_decode()已经返回了该信息。

IncrementalEncoder和IncrementalDecoder作为增量接口的基类。增量类的encode()和decode()方法的定义方式是，它们只返回实际转换的数据。任何关于缓冲的信息都保持为内部状态。不需要对数据进行缓冲区编码(它使用一对一映射)。对于根据正在处理的数据(如压缩算法)生成不同数量输出的编码，BufferedIncrementalEncoder和BufferedIncrementalDecoder是更合适的基类，因为它们管理输入的未处理部分。

StreamReader和StreamWriter需要编码()和decode()方法，因为它们希望返回与Codec多继承版本相同的值，可以用于实现。
```
$ python codecs_invertcaps_register.py

Encoded "abcDEF" to "b'ABCdef'", consuming 6 characters
StreamWriter for io buffer:
  writing "abcDEF"
  buffer contents:  b'ABCdef'
IncrementalDecoder converted b'ABCdef' to 'abcDEF'
```













