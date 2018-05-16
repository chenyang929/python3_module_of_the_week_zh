# statistics_median.py

from statistics import *

data = [1, 2, 2, 5, 10, 12]
data1 = [1, 2, 2, 8, 5, 10, 12]
print(data)
print('median   : {:0.2f}'.format(median(data)))
print('low      : {:0.2f}'.format(median_low(data)))
print('high     : {:0.2f}'.format(median_high(data)))
print(data1)
print('median   : {:0.2f}'.format(median(data1)))
print('low      : {:0.2f}'.format(median_low(data1)))
print('high     : {:0.2f}'.format(median_high(data1)))
