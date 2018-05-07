# datetime -- Date and Time Value Manipulation
> 目的：datetime模块包括用于执行日期和时间解析、格式化和算术的函数和类。

## Times
时间值用时间类表示。一个时间实例具有小时、分钟、秒和微秒的属性，还可以包含时区信息。
<pre><code># datetime_time.py

import datetime

t = datetime.time(1, 2, 3)
print(t)
print('hour       :', t.hour)
print('minute     :', t.minute)
print('second     :', t.second)
print('microsecond:', t.microsecond)
print('tzinfo     :', t.tzinfo)</pre></code>
初始化一个时间实例的参数是可选的，但是0的默认值不太可能是正确的。
<pre><code>$ python datetime_time.py
01:02:03
hour       : 1
minute     : 2
second     : 3
microsecond: 0
tzinfo     : None</pre></code>
时间实例只包含时间的值，而不是与时间相关的日期。
<pre><code># datetime_time_minmax.py

import datetime

print('Earliest  :', datetime.time.min)
print('Latest    :', datetime.time.max)
print('Resolution:', datetime.time.resolution)</pre></code>
min和max类属性反映了在一天内有效的时间范围。
<pre><code>$ python datetime_time_minmax.py
Earliest  : 00:00:00
Latest    : 23:59:59.999999
Resolution: 0:00:00.000001</pre></code>
时间的分辨率限制在整个微秒内。
<pre><code># datetime_time_resolution.py

import datetime

for m in [1, 0, 0.1, 0.6]:
    try:
        print('{:02.1f}:'.format(m), datetime.time(0, 0, 0, microsecond=m))
    except TypeError as err:
        print('ERROR:', err)</pre></code>
微秒的浮点值会导致一个类型错误。
<pre><code>$ python datetime_time_resolution.py
1.0: 00:00:00.000001
0.0: 00:00:00
ERROR: integer argument expected, got float
ERROR: integer argument expected, got float</pre></code>
## Dates
日历日期值用date类表示。实例具有年、月和日的属性。使用today()类方法创建表示当前日期的日期很容易。
<pre><code># datetime_date.py

import datetime

today = datetime.date.today()
print(today)
print('ctime:', today.ctime())
tt = today.timetuple()
print('tuple  : tm_year  =', tt.tm_year)
print('         tm_mon   =', tt.tm_mon)
print('         tm_mday  =', tt.tm_mday)
print('         tm_hour  =', tt.tm_hour)
print('         tm_min   =', tt.tm_min)
print('         tm_sec   =', tt.tm_sec)
print('         tm_wday  =', tt.tm_wday)
print('         tm_yday  =', tt.tm_yday)
print('         tm_isdst =', tt.tm_isdst)
print('ordinal:', today.toordinal())
print('Year   :', today.year)
print('Mon    :', today.month)
print('Day    :', today.day)</pre></code>
本例以几种格式打印当前日期:
<pre><code>$ python datetime_date.py
2018-05-07
ctime: Mon May  7 00:00:00 2018
tuple  : tm_year  = 2018
         tm_mon   = 5
         tm_mday  = 7
         tm_hour  = 0
         tm_min   = 0
         tm_sec   = 0
         tm_wday  = 0
         tm_yday  = 127
         tm_isdst = -1
ordinal: 736821
Year   : 2018
Mon    : 5
Day    : 7</pre></code>
还有一些类方法，用于从POSIX时间戳或从公历中表示日期值的整数来创建实例，其中1年1月1日为1，随后每一天递增1。
<pre><code># datetime_date_fromordinal.py

import datetime
import time

o = 736515
print('o              :', o)
print('fromoridinal(o):', datetime.date.fromordinal(o))

t = time.time()
print('t               :', t)
print('fromtimestamp(t):', datetime.date.fromtimestamp(t))</pre></code>
这个例子说明了fromordinal()和fromtimestamp()使用的不同值类型。
<pre><code>$ python datetime_date_fromordinal.py
o              : 736515
fromoridinal(o): 2017-07-05
t               : 1525658660.7558002
fromtimestamp(t): 2018-05-07</pre></code>
和时间一样，可以使用min和max属性确定支持的日期值的范围。
<pre><code># datetime_date_minmax.py

import datetime

print('Earliest  :', datetime.date.min)
print('Latest    :', datetime.datetime.max)
print('Resolution:', datetime.date.resolution)</pre></code>
关于日期的精度是一天。
<pre><code>$ python datetime_date_minmax.py
Earliest  : 0001-01-01
Latest    : 9999-12-31 23:59:59.999999
Resolution: 1 day, 0:00:00</pre></code>
创建新的日期实例的另一种方法是使用现有日期的replace()方法。
<pre><code># datetime_date_replace.py

import datetime

d1 = datetime.date(2008, 3, 29)
print('d1:', d1.ctime())

d2 = d1.replace(year=2009)
print('d2:', d2.ctime())</pre></code>
这个例子改变了年的值。
<pre><code>$ python datetime_date_replace.py
d1: Sat Mar 29 00:00:00 2008
d2: Sun Mar 29 00:00:00 2009</pre></code>
## timedeltas
未来和过去的某个日期可以通过对两个datetime对象进行基本加减运算得到。
即将一个datetime与一个timedelta结合起来，可加可减，timedelta的内部值存储的值可为天、秒和微秒。
<pre><code># datetime_timedelta.py

import datetime

print('microseconds:', datetime.timedelta(microseconds=1))
print('milliseconds:', datetime.timedelta(milliseconds=1))
print('seconds     :', datetime.timedelta(seconds=1))
print('minutes     :', datetime.timedelta(minutes=1))
print('hours       :', datetime.timedelta(hours=1))
print('days        :', datetime.timedelta(days=1))
print('weeks       :', datetime.timedelta(weeks=1))</pre></code>
传递给构造函数的中间层值被转换为天数、秒和微秒。
<pre><code>$ python datetime_timedelta.py
microseconds: 0:00:00.000001
milliseconds: 0:00:00.001000
seconds     : 0:00:01
minutes     : 0:01:00
hours       : 1:00:00
days        : 1 day, 0:00:00
weeks       : 7 days, 0:00:00</pre></code>
使用total_seconds()可以将一个timedelta的完整持续时间转化为秒钟。
<pre><code># datetime_timedelta_total_seconds.py

import datetime

for delta in [datetime.timedelta(microseconds=1),
              datetime.timedelta(milliseconds=1),
              datetime.timedelta(seconds=1),
              datetime.timedelta(minutes=1),
              datetime.timedelta(hours=1),
              datetime.timedelta(days=1),
              datetime.timedelta(weeks=1),
              ]:
    print('{:15} = {:8} seconds'.format(
        str(delta), delta.total_seconds())
    )</pre></code>
返回值是一个浮点数，以适应子秒的持续时间。
<pre><code>$ python datetime_timedelta_total_seconds.py
0:00:00.000001  =    1e-06 seconds
0:00:00.001000  =    0.001 seconds
0:00:01         =      1.0 seconds
0:01:00         =     60.0 seconds
1:00:00         =   3600.0 seconds
1 day, 0:00:00  =  86400.0 seconds
7 days, 0:00:00 = 604800.0 seconds</pre></code>
## Date Arithmetic
日期算数运算使用标准算术运算符。
<pre><code># datetime_date_math.py

import datetime

today = datetime.date.today()
print('Today   :', today)

one_day = datetime.timedelta(days=1)
print('One day  :', one_day)

yesterday = today - one_day
print('Yesterday:', yesterday)

tomorrow = today + one_day
print('Tomorrow :', tomorrow)

print()
print('tomorrow - yesterday:', tomorrow - yesterday)
print('yesterday - tomorrow:', yesterday - tomorrow)</pre></code>
这个带有日期对象的例子演示了使用timedelta对象来计算新的日期，并减去日期实例来产生timedelta(包括一个负的delta值)。
<pre><code>$ python datetime_date_math.py
Today   : 2018-05-07
One day  : 1 day, 0:00:00
Yesterday: 2018-05-06
Tomorrow : 2018-05-08

tomorrow - yesterday: 2 days, 0:00:00
yesterday - tomorrow: -2 days, 0:00:00</pre></code>
timedelta对象还支持整数、浮点数和其他时间增量实例的算术运算。
<pre><code># datetime_timedelta_math.py

import datetime

one_day = datetime.timedelta(days=1)
print('1 day    :', one_day)
print('5 days   :', one_day * 5)
print('1.5 days :', one_day * 1.5)
print('1/4 day  :', one_day / 4)

work_day = datetime.timedelta(hours=7)
meeting_length = datetime.timedelta(hours=1)
print('meetings per day :', work_day / meeting_length)</pre></code>
在本例中，计算了某一天的数倍，由此产生的时间增量保持了适当的天数或小时。
最后一个例子演示了如何通过两个timedelta对象来计算值。在这种情况下，结果是一个浮点数。
<pre><code>$ python datetime_timedelta_math.py
1 day    : 1 day, 0:00:00
5 days   : 5 days, 0:00:00
1.5 days : 1 day, 12:00:00
1/4 day  : 6:00:00
meetings per day : 7.0</pre></code>
## Comparing Values
可以使用标准比较运算符来比较日期和时间值，以确定哪个是更早或更晚。
<pre><code># datetime_comparing.py

import datetime

print('Times:')
t1 = datetime.time(12, 55, 0)
print('   t1:', t1)
t2 = datetime.time(13, 5, 0)
print('   t2:', t2)
print('   t1 < t2:', t1 < t2)

print()
print('Dates:')
d1 = datetime.date.today()
print('   d1:', d1)
d2 = datetime.date.today() + datetime.timedelta(days=1)
print('   d2:', d2)
print('   d1 > d2:', d1 > d2)</pre></code>
支持所有比较运算符。
<pre><code>$ python datetime_comparing.py
Times:
   t1: 12:55:00
   t2: 13:05:00
   t1 < t2: True

Dates:
   d1: 2018-05-07
   d2: 2018-05-08
   d1 > d2: False</pre></code>
## Combining Dates and Times
使用datetime类来保存包含日期和时间组件的值。与日期一样，有几种方便的类方法可以从其他公共值创建datetime实例。
<pre><code># datetime_datetime.py

import datetime

print('Now    :', datetime.datetime.now())
print('Today  :', datetime.datetime.today())
print('UTC Now:', datetime.datetime.utcnow())

FIELDS = [
    'year', 'month', 'day',
    'hour', 'minute', 'second',
    'microsecond',
]

d = datetime.datetime.now()
for attr in FIELDS:
    print('{:15} {}'.format(attr, getattr(d, attr)))</pre></code>
正如可以预期的那样，datetime实例具有日期和时间对象的所有属性。
<pre><code>$ python datetime_datetime.py
Now    : 2018-05-07 10:53:05.912575
Today  : 2018-05-07 10:53:05.912576
UTC Now: 2018-05-07 02:53:05.912575
year            2018
month           5
day             7
hour            10
minute          53
second          5
microsecond     912575</pre></code>
与日期一样，datetime为创建新实例提供了方便的类方法。它还包括fromordinal()和fromtimestamp()。
<pre><code># datetime_datetime_combine.py

import datetime

t = datetime.time(1, 2, 3)
print('t :', t)

d = datetime.date.today()
print('d :', d)

dt = datetime.datetime.combine(d, t)
print('dt:', dt)</pre></code>
combine()从一个日期和一个时间实例创建datetime实例。
<pre><code>$ python datetime_datetime_combine.py
t : 01:02:03
d : 2018-05-07
dt: 2018-05-07 01:02:03</pre></code>
## Formatting and Parsing
datetime对象的默认字符串表示使用ISO-8601格式(YYYY-MM-DDTHH:MM: ss.mmmmm)。
可以使用strftime()生成替代格式。
<pre><code># datetime_datetime_strptime.py

import datetime

ft = '%a %b %d %H:%M:%S %Y'

today = datetime.datetime.today()
print('ISO     :', today)

s = today.strftime(ft)
print('strftime:', s)

d = datetime.datetime.strptime(s, ft)
print(d)
print('strptime:', d.strftime(ft))</pre></code>
使用datetime.strptime()将格式化的字符串转换为datetime实例。
<pre><code>$ python datetime_datetime_strptime.py
ISO     : 2018-05-07 11:06:13.848991
strftime: Mon May 07 11:06:13 2018
2018-05-07 11:06:13
strptime: Mon May 07 11:06:13 2018</pre></code>
同样的格式化代码可以使用Python的字符串格式化迷你语言，将它们放在格式字符串的字段规范中。
<pre><code># datetime_format.py

import datetime

today = datetime.datetime.today()
print('ISO     :', today)
print('format(): {:%a %b %d %H:%M:%S %Y}'.format(today))</pre></code>
每个datetime格式代码都必须以%为前缀，然后将随后的冒号作为文本字符处理，以包含在输出中。
<pre><code>$ python datetime_format.py
ISO     : 2018-05-07 11:12:15.539830
format(): Mon May 07 11:12:15 2018</pre></code>
## Time Zones
在datetime中，时区由tzinfo的子类表示。由于tzinfo是一个抽象基类，因此应用程序需要定义一个子类，并为一些方法提供适当的实现以使其有用。

datetime在类时区中确实包含了一个稍微有点简单的实现，它使用UTC的固定偏移量，并且不支持在一年的不同时间内使用不同的偏移值，比如夏令时应用的地方，或者UTC的偏移量随时间的变化。
<pre><code># datetime_timezone.py

import datetime

min6 = datetime.timezone(datetime.timedelta(hours=-6))
plus6 = datetime.timezone(datetime.timedelta(hours=6))
d = datetime.datetime.now(min6)

print(min6, ':', d)
print(datetime.timezone.utc, ':',
      d.astimezone(datetime.timezone.utc))
print(plus6, ':', d.astimezone(plus6))

# convert to the current system timezone
d_system = d.astimezone()
print(d_system.tzinfo, '      :', d_system)</pre></code>
要将datetime值从一个时区转换为另一个时区，请使用astimezone()。在上面的例子中，在UTC的两边分别显示了两个独立的时区，以及来自datetime的UTC实例。
时区也用于参考。最后的输出行显示了系统时区中的值，该值通过调用astimezone()获得，没有参数。
<pre><code>$ python datetime_timezone.py
UTC-06:00 : 2018-05-06 21:18:02.766369-06:00
UTC : 2018-05-07 03:18:02.766369+00:00
UTC+06:00 : 2018-05-07 09:18:02.766369+06:00
CST       : 2018-05-07 11:18:02.766369+08:00</pre></code>
