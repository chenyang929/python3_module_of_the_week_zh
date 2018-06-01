# fnmatch_fnmatchcase.py

import fnmatch
import os

pattern = 'FNMATCH_*.py'
print('Pattern:', pattern)
print()

files = os.listdir('.')
for name in sorted(files):
    print('Filename: {:<25} {}'.format(name, fnmatch.fnmatchcase(name, pattern)))