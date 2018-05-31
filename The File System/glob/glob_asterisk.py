# glob_asterisk.py

import glob
for name in sorted(glob.glob('dir/*')):
    print(name)