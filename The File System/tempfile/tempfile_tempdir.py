# tempfile_tempdir.py

import tempfile

tempfile.tempdir = 'D:\Temp'
print('gettempdir():', tempfile.gettempdir())
