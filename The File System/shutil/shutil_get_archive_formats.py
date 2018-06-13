# shutil_get_archive_formats.py

import shutil

for ft, desc in shutil.get_archive_formats():
    print('{:<5}: {}'.format(ft, desc))