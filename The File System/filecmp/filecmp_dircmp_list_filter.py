# filecmp_dircmp_list_filter.py

import filecmp
import pprint

dc = filecmp.dircmp('example/dir1', 'example/dir2', ignore=['common_file'])

print('Left:')
pprint.pprint(dc.left_list)

print('\nRight:')
pprint.pprint(dc.right_list)
