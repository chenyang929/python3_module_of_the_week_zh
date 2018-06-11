# tempfile_SpooledTemporaryFile.py

import tempfile

with tempfile.SpooledTemporaryFile(max_size=100, mode='w+t', encoding='utf-8') as temp:
    print('temp: {!r}'.format(temp))

    for i in range(3):
        temp.write('This line is repeated over and over.\n')
        print(temp._rolled, temp._file)
