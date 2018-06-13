# shutil_get_unpack_formats.py

import shutil

for ft, exts, desc in shutil.get_unpack_formats():
    print('{:<5}: {}, names ending in {}'.format(ft, desc, exts))
