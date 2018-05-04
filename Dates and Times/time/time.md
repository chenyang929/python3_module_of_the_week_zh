# time -- Clock Time
> 目的：操作时钟时间的函数。

时间模块提供了对几种不同类型的时钟的访问，每个时钟对不同的目的都有用。
标准的系统调用像time()报告系统“挂钟”时间。
monotonic()时钟可以用来度量长时间运行的流程中的运行时间，因为它保证不会向后移动，即使系统时间发生了变化。
对于性能测试，perf_counter()提供了对时钟的访问，它具有最高的可用分辨率，以使短时间测量更加准确。
通过clock()可以获得CPU时间，process_time()返回组合处理器时间和系统时间。
## Comparing Clocks
时钟的实现细节因平台而异。使用get_clock_info()访问关于当前实现的基本信息，包括时钟的解析。
<pre><code># time_get_clock_info.py

import textwrap
import time

available_clocks = [
    ('clock', time.clock),
    ('monotonic', time.monotonic),
    ('perf_counter', time.perf_counter),
    ('process_time', time.process_time),
    ('time', time.time),
]

for clock_name, func in available_clocks:
    print(textwrap.dedent('''\
    {name}:
        adjustable    : {info.adjustable}
        implementation: {info.implementation}
        monotonic     : {info.monotonic}
        resolution    : {info.resolution}
        current       : {current}
    ''').format(
        name=clock_name,
        info=time.get_clock_info(clock_name),
        current=func())
    )</pre></code>
下面是window10系统输出情况。
<pre><code>$ python time_get_clock_info.py
clock:
    adjustable    : False
    implementation: QueryPerformanceCounter()
    monotonic     : True
    resolution    : 3.208016448141933e-07
    current       : 2.8872148033277396e-06

monotonic:
    adjustable    : False
    implementation: GetTickCount64()
    monotonic     : True
    resolution    : 0.015625
    current       : 169570.375

perf_counter:
    adjustable    : False
    implementation: QueryPerformanceCounter()
    monotonic     : True
    resolution    : 3.208016448141933e-07
    current       : 0.0001148469888434812

process_time:
    adjustable    : False
    implementation: GetProcessTimes()
    monotonic     : True
    resolution    : 1e-07
    current       : 0.046875

time:
    adjustable    : True
    implementation: GetSystemTimeAsFileTime()
    monotonic     : False
    resolution    : 0.015625
    current       : 1525399055.6742718</pre></code>
## Wall Clock Time
时间模块的核心功能之一是time(),它返回自起始时间以来的秒数，以浮点值形式。
<pre><code># time.time.py

import time

print('The time is:', time.time())</pre></code>
对于Unix系统来说，起始时间1970年1月1日的0:00。
尽管值始终是一个浮点数，但实际的精度是平台依赖的。
<pre><code>$ python time.time.py
The time is: 1525399544.8118806</pre></code>
在存储或比较日期时，浮点表示是有用的，但对于生成人类可读的表示没有多大用处。
对于日志记录或打印时，ctime()可能更有用。
<pre><code># time_ctime.py

import time

print('The time is     :', time.ctime())
later = time.time() + 15
print('15 secs from now:', time.ctime(later))</pre></code>
在这个示例中，第二个print()调用显示了如何使用ctime()来格式化除当前时间以外的时间值。
<pre><code>$ python time_ctime.py
The time is     : Fri May  4 10:12:02 2018
15 secs from now: Fri May  4 10:12:17 2018</pre></code>
## Monotonic Clocks
由于time()查看系统时钟，系统时钟可以由用户或系统服务更改，以便在多台计算机上同步时钟，因此多次调用time()可能产生向前和向后的值。
这可能会导致在尝试度量持续时间或使用那些时间进行计算时出现意外的行为。使用monotonic()来避免这些情况，它总是返回前进的值。
<pre><code># time_monotonic.py

import time

start = time.monotonic()
time.sleep(0.2)
end = time.monotonic()
print('start: {:>9.2f}'.format(start))
print('end  : {:>9.2f}'.format(end))
print('span : {:>9.2f}'.format(end - start))</pre></code>
monotonic时钟的起始点没有定义，因此返回值只适用于与其他时钟值进行计算。
在这个例子中，睡眠的持续时间是用monotonic()来测量的。
<pre><code>$ python time_monotonic.py
start: 171134.14
end  : 171134.34
span :      0.20</pre></code>
## Processor Clock Time
当time()返回一个挂钟时间时，clock()返回处理器时钟时间。clock()返回的值反映程序运行时所使用的实际时间。
<pre><code># time_clock.py

import hashlib
import time

# 用于计算md5校验和的数据
data = open(__file__, 'rb').read()

for i in range(5):
    h = hashlib.sha1()
    print(time.ctime(), ': {:0.3f} {:0.3f}'.format(time.time(), time.clock()))
    for i in range(300000):
        h.update(data)
    cksum = h.digest()</pre></code>
在本例中，每次循环打印出格式化的ctime()与time()和clock()的值。
<pre><code>$ python time_clock.py
Fri May  4 10:37:36 2018 : 1525401456.709 0.000
Fri May  4 10:37:36 2018 : 1525401456.879 0.170
Fri May  4 10:37:37 2018 : 1525401457.052 0.344
Fri May  4 10:37:37 2018 : 1525401457.221 0.512
Fri May  4 10:37:37 2018 : 1525401457.388 0.679</pre></code>
通常，如果程序没有做任何事情，处理器时钟就不会滴答作响(linux系统)。
<pre><code># time_clock_sleep.py

import time

template = '{} - {:0.2f} - {:0.2f}'

print(template.format(time.ctime(), time.time(), time.clock()))

for i in range(3, 0, -1):
    print('Sleeping', i)
    time.sleep(i)
    print(template.format(time.ctime(), time.time(), time.clock()))</pre></code>
在这个例子中，循环在每次迭代之后都要sleep，做的工作很少。
当应用程序处于休眠状态时，time()值会增加，但是clock()值不增加(linux)。
<pre><code>$ python time_clock_sleep.py
Fri May  4 11:11:11 2018 - 1525403471.32 - 0.02
Sleeping 3
Fri May  4 11:11:14 2018 - 1525403474.32 - 0.02
Sleeping 2
Fri May  4 11:11:16 2018 - 1525403476.33 - 0.02
Sleeping 1
Fri May  4 11:11:17 2018 - 1525403477.33 - 0.02</pre></code>
window10系统执行输出如下
<pre><code>$ python time_clock_sleep.py
Fri May  4 11:13:35 2018 - 1525403615.24 - 0.00
Sleeping 3
Fri May  4 11:13:38 2018 - 1525403618.24 - 3.00
Sleeping 2
Fri May  4 11:13:40 2018 - 1525403620.24 - 5.00
Sleeping 1
Fri May  4 11:13:41 2018 - 1525403621.24 - 6.00</pre></code>
## Performance Counter
有一个高分辨率的单调时钟来测量性能是很重要的。
确定最佳时钟数据源需要特定于平台的知识，Python在perf_counter()中提供。
<pre><code># time_perf_counter.py

import hashlib
import time

data = open(__file__, 'rb').read()

loop_start = time.perf_counter()

for i in range(5):
    iter_start = time.perf_counter()
    h = hashlib.sha1()
    for i in range(300000):
        h.update(data)
    cksum = h.digest()
    now = time.perf_counter()
    loop_elapsed = now - loop_start
    iter_elapsed = now - iter_start
    print(time.ctime(), ': {:0.3f} {:0.3f}'.format(iter_elapsed, loop_elapsed))</pre></code>
与monotonic()一样，perf_counter()的时间是未定义的，而且值是用来比较和计算值的，而不是绝对时间。
<pre><code>$ python time_perf_counter.py
Fri May  4 11:25:11 2018 : 0.237 0.237
Fri May  4 11:25:11 2018 : 0.248 0.485
Fri May  4 11:25:11 2018 : 0.237 0.722
Fri May  4 11:25:12 2018 : 0.237 0.959
Fri May  4 11:25:12 2018 : 0.240 1.199</pre></code>
## Time Components
在某些情况下，存储时间是有用的，但有时程序需要访问日期(年、月等)的各个字段。
time模块定义了用于保存日期和时间值的struct_time，这些组件被分离出来，因此它们很容易访问。
有几个函数使用struct_time值来代替浮点数。
<pre><code># time_struct.py

import time


def show_struct(s):
    print('  tm_year :', s.tm_year)
    print('  tm_mon  :', s.tm_mon)
    print('  tm_mday :', s.tm_mday)
    print('  tm_hour :', s.tm_hour)
    print('  tm_min  :', s.tm_min)
    print('  tm_sec  :', s.tm_sec)
    print('  tm_wday :', s.tm_wday)
    print('  tm_yday :', s.tm_yday)
    print('  tm_isdst:', s.tm_isdst)


print('gmtime')
show_struct(time.gmtime())
print('\nlocaltime:')
show_struct(time.localtime())
print('\nmktime:', time.mktime(time.localtime()))</pre></code>
gmtime()返回UTC中的当前时间。
localtime()返回当前时区应用的当前时间。
mktime()使用struct_time并将其转换为浮点表示法。
<pre><code>$ python time_struct.py
gmtime
  tm_year : 2018
  tm_mon  : 5
  tm_mday : 4
  tm_hour : 3
  tm_min  : 31
  tm_sec  : 44
  tm_wday : 4
  tm_yday : 124
  tm_isdst: 0

localtime:
  tm_year : 2018
  tm_mon  : 5
  tm_mday : 4
  tm_hour : 11
  tm_min  : 31
  tm_sec  : 44
  tm_wday : 4
  tm_yday : 124
  tm_isdst: 0

mktime: 1525404704.0</pre></code>
## Working with Time Zones
确定当前时间的函数依赖于时区设置，要么是通过程序，要么是使用系统的默认时区设置。改变时区并不会改变实际的时间，就像它所代表的那样。

要更改时区，设置环境变量TZ，然后调用tzset()。时区可以用很多细节来指定，就在夏令时的开始和停止时间。通常，使用时区名称并让底层库获得其他信息通常比较容易。

这个示例程序将时区更改为几个不同的值，并显示更改如何影响时间模块中的其他设置(linux下运行)。
<pre><code># time_timezone.py

import time
import os


def show_zone_info():
    print('  ZT    :', os.environ.get('TZ', '(not set)'))
    print('  tzname:', time.tzname)
    print('  Zone  : {} ({})'.format(time.timezone, (time.timezone/3600)))
    print('  DST   :', time.daylight)
    print('  Time  :', time.ctime())
    print()


print('Default')
show_zone_info()

ZONES = [
    'GMT',
    'Europe/Amsterdam'
]

for zone in ZONES:
    os.environ['TZ'] = zone
    time.tzset()
    print(zone, ':')
    show_zone_info()</pre></code>
用于准备示例的系统的默认时区是US/Eastern。示例中的其他区域更改了tzname、日光标记和时区偏移值。
<pre><code>$ python time_timezone.py
Default
  ZT    : (not set)
  tzname: ('CST', 'CST')
  Zone  : -28800 (-8.0)
  DST   : 0
  Time  : Fri May  4 11:47:27 2018

GMT :
  ZT    : GMT
  tzname: ('GMT', 'GMT')
  Zone  : 0 (0.0)
  DST   : 0
  Time  : Fri May  4 03:47:27 2018

Europe/Amsterdam :
  ZT    : Europe/Amsterdam
  tzname: ('CET', 'CEST')
  Zone  : -3600 (-1.0)
  DST   : 1
  Time  : Fri May  4 05:47:27 2018</pre></code>
## Parsing and Formatting Times
两个函数strptime()和strftime()在时间值的struct_time和string表示之间进行转换。
有一长串格式说明可用来支持不同风格的输入和输出。完整的列表记录在时间模块的库文档中。

此示例将当前时间从字符串转换为struct_time实例并返回到字符串。
<pre><code># time_strptime.py

import time


def show_struct(s):
    print('  tm_year :', s.tm_year)
    print('  tm_mon  :', s.tm_mon)
    print('  tm_mday :', s.tm_mday)
    print('  tm_hour :', s.tm_hour)
    print('  tm_min  :', s.tm_min)
    print('  tm_sec  :', s.tm_sec)
    print('  tm_wday :', s.tm_wday)
    print('  tm_yday :', s.tm_yday)
    print('  tm_isdst:', s.tm_isdst)


now = time.ctime(1483391847.433716)
print('Now:', now)

parsed = time.strptime(now)
print('\nParsed:')
show_struct(parsed)

print('\nFormatted:',
      time.strftime("%a %b %d %H:%M:%S %Y", parsed))</pre></code>
输出字符串不完全匹配输入，因为日期是前缀有0。
<pre><code>$ python time_strptime.py
Now: Tue Jan  3 05:17:27 2017

Parsed:
  tm_year : 2017
  tm_mon  : 1
  tm_mday : 3
  tm_hour : 5
  tm_min  : 17
  tm_sec  : 27
  tm_wday : 1
  tm_yday : 3
  tm_isdst: -1

Formatted: Tue Jan 03 05:17:27 2017</pre></code>
