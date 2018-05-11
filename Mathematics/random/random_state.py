# random_state.py

import random
import os
import pickle

if os.path.exists('state.dat'):
    # 恢复之前保存的状态
    print('Found state.dat, initializing random module')
    with open('state.dat', 'rb') as f:
        state = pickle.load(f)
    random.setstate(state)
else:
    # 使用一个已知的开始状态
    print('No state.dat, seeding')
    random.seed(1)

# 产生随机值
for i in range(3):
    print('{:04.3f}'.format(random.random()), end=' ')
print()

# 为下一次保存状态
with open('state.dat', 'wb') as f:
    pickle.dump(random.getstate(), f)

# 产生更多的随机值
print('\nAfter saving state:')
for i in range(3):
    print('{:04.3f}'.format(random.random()), end=' ')
print()
