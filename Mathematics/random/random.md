# random -- Pseudorandom  Number Generators
> 目的：实现几种类型的伪随机数生成器。

随机模块提供了基于Mersenne Twister算法的快速伪随机数生成器。
Mersenne Twister最初是为模拟蒙特卡洛模拟而开发的，它产生的数字几乎是均匀分布的，而且是一个大的周期，这使得它适合于广泛的应用。
## Generating Random Numbers
random()函数的作用是:从生成的序列中返回下一个随机浮点值。所有返回值都在0 <= n < 1.0的范围内。
<pre><code># random_random.py

import random

for i in range(5):
    print('%04.3f' % random.random(), end=' ')
print()</pre></code>
重复运行这个程序会产生不同的数字序列。
<pre><code>$ python random_random.py
0.580 0.128 0.803 0.464 0.285 

$ python random_random.py
0.837 0.239 0.257 0.576 0.658</pre></code>
要在一个特定的数值范围内生成数字，请使用uniform()函数。
<pre><code># random_uniform.py

import random

for i in range(5):
    print('{:04.3f}'.format(random.uniform(1, 100)), end=' ')
print()</pre></code>
通过最小值和min最大值max，uniform()通过公式min + (max - min) * random()调整random()返回的值。
<pre><code>$ python random_uniform.py
17.554 26.603 81.956 14.709 70.008 </pre></code>
## Seeding
random()每次调用时产生不同的值，并且在重复任何数字之前有很长一段时间。这对于产生独特的值或变体非常有用，但是有时使用不同的方法处理相同的数据集是有用的。
一种技术是使用程序生成随机值，并将其保存为单独的步骤处理。但是，对于大量数据来说，这可能并不实用，因此，random包含了初始化pseudorandom生成器的seed()函数，以便它产生一组预期的值。
<pre><code># random_seed.py

import random

random.seed(1)

for i in range(5):
    print('{:04.3f}'.format(random.random()), end=' ')
print()</pre></code>
seed值控制了用于产生伪随机数的公式所产生的第一个值，由于该公式是确定的，它也会在种子发生变化后设置完整的序列。
seed()的参数可以是任何可哈希的对象。默认情况是使用特定于平台的随机性源，如果有的话。否则，将使用当前时间。
<pre><code>$ python random_seed.py
0.134 0.847 0.764 0.255 0.495 
$ python random_seed.py
0.134 0.847 0.764 0.255 0.495</pre></code>
## Saving State
random()使用的伪随机算法的内部状态可以被保存并用于控制后续运行中产生的数字。在继续减少重复值或之前输入的值序列的可能性之前，恢复先前的状态。
getstate函数的作用是:返回数据，然后被setstate()函数用来重新初始化随机数生成器。
<pre><code># random_state.py

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
print()</pre></code>
getstate()返回的数据是一个实现细节，因此这个示例使用pickle将数据保存到一个文件中，但将其视为一个黑盒子。
如果该文件存在于程序启动时，它将加载旧状态并继续。每次运行都会在保存状态之前和之后生成几个数字，以显示恢复状态会使生成器再次产生相同的值。
<pre><code>$ python random_state.py
No state.dat, seeding
0.134 0.847 0.764 

After saving state:
0.255 0.495 0.449 

$ python random_state.py
Found state.dat, initializing random module
0.255 0.495 0.449 

After saving state:
0.652 0.789 0.094</pre></code>
## Random Integers
random()函数生成浮点数。虽然可以将其转换成整数，但使用randint()函数来直接生成整数更方便。
<pre><code># random_randint.py

import random

print('[1, 100]:', end=' ')

for i in range(3):
    print(random.randint(1, 100), end=' ')

print('\n[-5, 5]:', end=' ')
for i in range(3):
    print(random.randint(-5, 5), end=' ')
print()</pre></code>
randint()的参数是值的包含范围的端点。数字可以是正的，也可以是负的，但是第一个值应该小于第二个。
<pre><code>$ python random_randint.py
[1, 100]: 86 78 60 
[-5, 5]: 3 -5 -5 </pre></code>
randrange()是从一个范围中选择值的更一般的形式。
<pre><code># random_randrange.py

import random

for i in range(3):
    print(random.randrange(0, 101, 5), end=' ')
print()</pre></code>
randrange()支持一个步骤参数，除了启动和停止值之外，它完全等同于从范围(开始、停止、步骤)中选择一个随机值。
它更有效，因为范围不是实际构造的。
<pre><code>$ python random_randrange.py
25 90 85</pre></code>
## Picking Random Items
随机数生成器的一个常见用途是从枚举值序列中选择一个随机项目，即使这些值不一定是数字。
random包含从序列中随机选择的choice()函数。这个例子模拟抛硬币1万次，计算出正面的次数和反面次数。
<pre><code># random_choice.py

import random

outcomes = {
    'heads': 0,
    'tails': 0,
}
sides = list(outcomes.keys())

for i in range(10000):
    outcomes[random.choice(sides)] += 1

print('Heads:', outcomes['heads'])
print('Tails:', outcomes['tails'])</pre></code>
结果显示如下:
<pre><code>$ python random_choice.py
Heads: 5029
Tails: 4971</pre></code>
## Permutations
一个纸牌游戏的模拟需要把牌堆混合起来，然后再把牌处理给玩家，而不需要多次使用相同的牌。
使用choice()可能会导致相同的卡片被处理两次，因此，可以将牌堆与shuffle()混合，然后在处理时删除已选出的卡片。
<pre><code># random_shuffle.py

import random
import itertools

FACE_CARDS = ('J', 'Q', 'K', 'A')
SUITS = ('H', 'D', 'C', 'S')


def new_deck():
    return [
        '{:>2}{}'.format(*c) for c in itertools.product(
            itertools.chain(range(2, 11), FACE_CARDS), SUITS)
    ]


def show_deck(deck):
    p_deck = deck[:]
    while p_deck:
        row = p_deck[:13]
        p_deck = p_deck[13:]
        for j in row:
            print(j, end=' ')
        print()


deck = new_deck()
print('Initial deck:')
show_deck(deck)

random.shuffle(deck)
print('\nShuffled deck:')
show_deck(deck)

hands = [[], [], [], []]

for i in range(5):
    for h in hands:
        h.append(deck.pop())

print('\nHands')
for n, h in enumerate(hands):
    print('{}:'.format(n + 1), end=' ')
    for c in h:
        print(c, end=' ')
    print()
    
print('\nRemaining deck:')
show_deck(deck)</pre></code>
这些卡片被表示为带有面值的字符串和表示花色的字母。每一次拿一张卡，并将它从牌堆中移除，这样它就不能再被选到了。
<pre><code>$ python random_shuffle.py
Initial deck:
 2H  2D  2C  2S  3H  3D  3C  3S  4H  4D  4C  4S  5H 
 5D  5C  5S  6H  6D  6C  6S  7H  7D  7C  7S  8H  8D 
 8C  8S  9H  9D  9C  9S 10H 10D 10C 10S  JH  JD  JC 
 JS  QH  QD  QC  QS  KH  KD  KC  KS  AH  AD  AC  AS 

Shuffled deck:
 2S  8S 10S  9S  7S  QH  3H  2C  6C  2H  6H  JH  5S 
 5H 10H  5D  7H  3D  3S  JD  QD  8C  7D  QC  6D  9C 
 AS  KD  AC  KH  9D  KC  6S  4C  4S  KS  AH  4D  9H 
 JS  7C  8D 10C  JC  AD  4H  8H  3C  2D 10D  5C  QS 

Hands
1:  QS  3C  JC  JS  KS 
2:  5C  8H 10C  9H  4S 
3: 10D  4H  8D  4D  4C 
4:  2D  AD  7C  AH  6S 

Remaining deck:
 2S  8S 10S  9S  7S  QH  3H  2C  6C  2H  6H  JH  5S 
 5H 10H  5D  7H  3D  3S  JD  QD  8C  7D  QC  6D  9C 
 AS  KD  AC  KH  9D  KC 
</pre></code>
## Sampling
许多模拟需要从输入值的总体中随机抽取样本。sample()函数生成的示例没有重复的值，并且不修改输入序列。
这个例子从系统字典中打印出一个随机的单词样本。
<pre><code># random_sample.py

import random

with open('/usr/share/dict/words', 'rt') as f:
    words = f.readlines()
words = [w.rstrip() for w in words]

for w in random.sample(words, 5):
    print(w)</pre></code>
生成结果集的算法考虑到输入的大小和请求的示例尽可能有效地生成结果。
<pre><code>$ python random_sample.py

streamlet
impestation
violaquercitrin
mycetoid
plethoretical

$ python random_sample.py

nonseditious
empyemic
ultrasonic
Kyurinish
amphide</pre></code>
## Multiple Simultaneous Generators
除了模块级函数之外，random包含一个随机的类来管理几个随机数生成器的内部状态。
前面描述的所有函数都可以作为随机实例的方法使用，并且每个实例都可以被初始化和单独使用，而不会影响其他实例返回的值。
<pre><code># random_random_class.py

import random
import time

print('Default initialization:\n')

r1 = random.Random()
r2 = random.Random()

for i in range(3):
    print('{:04.3f} {:04.3f}'.format(r1.random(), r2.random()))

print('\nSame seed:\n')

seed = time.time()
r1 = random.Random(seed)
r2 = random.Random(seed)

for i in range(3):
    print('{:04.3f} {:04.3f}'.format(r1.random(), r2.random()))</pre></code>
在具有良好本地随机值种子的系统中，实例从独特的状态开始。
然而，如果没有好的平台随机值生成器，实例很可能是与当前时间一起被播种的，因此产生相同的值。
<pre><code>$ python random_random_class.py
Default initialization:

0.773 0.990
0.791 0.867
0.271 0.673

Same seed:

0.254 0.254
0.099 0.099
0.067 0.067</pre></code>
## SystemRandom
一些操作系统提供了一个随机数生成器，它可以访问更多的熵源，这些信息可以被引入到生成器中。
random通过SystemRandom类公开该特性，该类具有与random相同的API，但使用os.urandom()来生成构成所有其他算法基础的值。
<pre><code># random_system_random.py

import random
import time

print('Default initializiation:\n')

r1 = random.SystemRandom()
r2 = random.SystemRandom()

for i in range(3):
    print('{:04.3f}  {:04.3f}'.format(r1.random(), r2.random()))

print('\nSame seed:\n')

seed = time.time()
r1 = random.SystemRandom(seed)
r2 = random.SystemRandom(seed)

for i in range(3):
    print('{:04.3f}  {:04.3f}'.format(r1.random(), r2.random()))</pre></code>
由SystemRandom产生的序列不是可复制的，因为随机性来自于系统，而不是软件状态(实际上，seed()和setstate()没有任何效果)。
<pre><code>$ python random_system_random.py
Default initializiation:

0.125  0.888
0.452  0.724
0.639  0.867

Same seed:

0.022  0.203
0.193  0.576
0.982  0.641</pre></code>

