# array_file.py

import array
import binascii
import tempfile

a = array.array('i', range(5))
print('A1:', a)

# 把数组写进临时文件
output = tempfile.NamedTemporaryFile(dir='d:\\')
a.tofile(output.file)
output.flush()

# 读原始数据
with open(output.name, 'rb') as input:
    raw_data = input.read()
    print('Raw Contents:', binascii.hexlify(raw_data))

    # 把数据读入数组
    input.seek(0)
    a2 = array.array('i')
    a2.fromfile(input, len(a))
    print('A2:', a2)
