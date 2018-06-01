# fnmatch_fnmatch.py

import fnmatch
import os

pattern = 'fnmatch_*.py'
print('Pattern:', pattern)
print()

files = os.listdir('.')
for name in sorted(files):
    print('Filename: {:<25} {}'.format(name, fnmatch.fnmatch(name, pattern)))