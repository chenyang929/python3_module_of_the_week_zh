# pathlib_convenience.py

import pathlib

home = pathlib.Path.home()
print('home:', home)

cwd = pathlib.Path.cwd()
print('cwd :', cwd)
