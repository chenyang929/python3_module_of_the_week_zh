# pathlib_rmdir.py

import pathlib

p = pathlib.Path('example_dir')

print('Removing {}'.format(p))
p.rmdir()
