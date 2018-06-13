# shutil_copytree.py

import glob
import pprint
import shutil

print('BEFORE:')
pprint.pprint(glob.glob('../temp/*'))
pprint.pprint(glob.glob('../fnmatch/*'))

shutil.copytree('../fnmatch', '../temp')

print('\nAFTER:')
pprint.pprint(glob.glob('../temp/*'))