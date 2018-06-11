# tempfile_NamedTemporaryFile_args.py

import tempfile

with tempfile.NamedTemporaryFile(suffix='_suffix', prefix='prefix_', dir='') as temp:
    print('temp:')
    print(' ', temp)
    print('temp.name:')
    print(' ', temp.name)
