# shutil_rmtree.py

import glob
import pprint
import shutil

print('BEFORE:')
pprint.pprint(glob.glob('../tmp/*'))

shutil.rmtree('../tmp')

print('\nAFTER:')
pprint.pprint(glob.glob('../tmp/*'))
