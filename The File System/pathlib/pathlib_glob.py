# pathlib_glob.py

import pathlib

p = pathlib.Path('.')

for f in p.glob('*.md'):
    print(f)
