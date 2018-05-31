# glob_subdir.py

import glob

print('Named explicitly:')
for name in sorted(glob.glob('dir/subdir/*')):
    print(' {}'.format(name))

print('Named with wildcard:')
for name in sorted(glob.glob('dir/*/*')):
    print(' {}'.format(name))
