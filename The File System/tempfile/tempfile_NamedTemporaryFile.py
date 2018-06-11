# tempfile_NamedTemporaryFile.py

import os
import pathlib
import tempfile

with tempfile.NamedTemporaryFile() as temp:
    print('temp:')
    print(' {!r}'.format(temp))
    print('temp.name:')
    print(' {!r}'.format(temp.name))

    f = pathlib.Path(temp.name)

print('Exists after close:', f.exists())