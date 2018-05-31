# glob_question.py

import glob

for name in sorted(glob.glob('dir/file?.txt')):
    print(name)
