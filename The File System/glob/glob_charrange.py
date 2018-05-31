# glob_charrange.py

import glob
for name in sorted(glob.glob('dir/*[0-9].*')):
    print(name)
