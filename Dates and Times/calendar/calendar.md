# calendar -- Work with Dates
> 目的：calendar模块实现了用于处理日期的类，以管理年/月/周的值。

calendar模块定义了calendar类，它封装了一些值的计算，比如给定月份或年份中的日期。
另外，TextCalendar和HTMLCalendar类可以生成预格式化的输出。
## Formatting Examples
prmonth()方法是一个简单的函数，它可以生成一个月的格式化文本输出。
<pre><code># calendar_textcalendar.py

import calendar

c = calendar.TextCalendar(calendar.SUNDAY)   # 星期天作为一周的第一天
c.prmonth(2018, 5)</pre></code>
输出如下:
<pre><code>$ python calendar_textcalendar.py
      May 2018
Su Mo Tu We Th Fr Sa
       1  2  3  4  5
 6  7  8  9 10 11 12
13 14 15 16 17 18 19
20 21 22 23 24 25 26
27 28 29 30 31</pre></code>
可以使用HTMLCalendar和formatmonth()生成类似的HTML表。呈现的输出看起来与纯文本版本大致相同，但是用HTML标记包装。每个表单元格都有一个对应于一周的类属性，因此HTML可以通过CSS样式化。

要以除可用缺省值之一之外的格式生成输出，使用calendar计算日期，并将值组织为周和月范围，然后对结果进行迭代。日历的weekheader()、monthcalendar()和yeardays2calendar()方法对它特别有用。

调用yeardays2calendar()生成一个“月行”列表的序列。每个列表包括几个月的另一个列表。周数是由日数(1-31)和工作日号(0-6)组成的元组列表。在这个月之外的日子有一天的数字是0。
<pre><code># calendar_yearday2calendar

import calendar
import pprint

cal = calendar.Calendar(calendar.SUNDAY)

cal_data = cal.yeardays2calendar(2018, 3)
print('len(cal_data)  :', len(cal_data))

top_months = cal_data[0]
print('len(top_months):', len(top_months))

first_month = top_months[0]
print('len(first_month):', len(first_month))

print('first_month:')
pprint.pprint(first_month, width=65)</pre></code>
调用yeardays2calendar(2017,3)将返回2017年的全部日期数据，每行3个月。
<pre><code>$ python calendar_yearday2calendar
len(cal_data)  : 4
len(top_months): 3
len(first_month): 5
first_month:
[[(0, 6), (1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)],
 [(7, 6), (8, 0), (9, 1), (10, 2), (11, 3), (12, 4), (13, 5)],
 [(14, 6), (15, 0), (16, 1), (17, 2), (18, 3), (19, 4), (20, 5)],
 [(21, 6), (22, 0), (23, 1), (24, 2), (25, 3), (26, 4), (27, 5)],
 [(28, 6), (29, 0), (30, 1), (31, 2), (0, 3), (0, 4), (0, 5)]]</pre></code>
这相当于formatyear()所使用的数据。
<pre><code># calendar_formatyear.py

import calendar

cal = calendar.TextCalendar(calendar.SUNDAY)
print(cal.formatyear(2018, 2, 1, 1, 3))</pre></code>
对于相同的参数，formatyear()产生如下输出:
<pre><code>$ python calendar_formatyear.py
                              2018

      January               February               March
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
    1  2  3  4  5  6               1  2  3               1  2  3
 7  8  9 10 11 12 13   4  5  6  7  8  9 10   4  5  6  7  8  9 10
14 15 16 17 18 19 20  11 12 13 14 15 16 17  11 12 13 14 15 16 17
21 22 23 24 25 26 27  18 19 20 21 22 23 24  18 19 20 21 22 23 24
28 29 30 31           25 26 27 28           25 26 27 28 29 30 31

       April                  May                   June
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
 1  2  3  4  5  6  7         1  2  3  4  5                  1  2
 8  9 10 11 12 13 14   6  7  8  9 10 11 12   3  4  5  6  7  8  9
15 16 17 18 19 20 21  13 14 15 16 17 18 19  10 11 12 13 14 15 16
22 23 24 25 26 27 28  20 21 22 23 24 25 26  17 18 19 20 21 22 23
29 30                 27 28 29 30 31        24 25 26 27 28 29 30

        July                 August              September
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
 1  2  3  4  5  6  7            1  2  3  4                     1
 8  9 10 11 12 13 14   5  6  7  8  9 10 11   2  3  4  5  6  7  8
15 16 17 18 19 20 21  12 13 14 15 16 17 18   9 10 11 12 13 14 15
22 23 24 25 26 27 28  19 20 21 22 23 24 25  16 17 18 19 20 21 22
29 30 31              26 27 28 29 30 31     23 24 25 26 27 28 29
                                            30

      October               November              December
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
    1  2  3  4  5  6               1  2  3                     1
 7  8  9 10 11 12 13   4  5  6  7  8  9 10   2  3  4  5  6  7  8
14 15 16 17 18 19 20  11 12 13 14 15 16 17   9 10 11 12 13 14 15
21 22 23 24 25 26 27  18 19 20 21 22 23 24  16 17 18 19 20 21 22
28 29 30 31           25 26 27 28 29 30     23 24 25 26 27 28 29
                                            30 31
</pre></code>
day_name、day_abbr、month_name和month_abbr模块属性用于生成自定义格式化输出(比如:，在HTML输出中包含链接）
它们自动为当前区域设置正确配置。
## Locales
要生成一个为本地语言环境而不是当前默认设置的日历，请使用LocaleTextCalendar或LocaleHTMLCalendar。
## Calculating Dates
虽然日历模块主要侧重于以各种格式打印完整的日历，但它也提供了一些有用的功能，可以以其他方式处理日期，比如计算重复事件的日期。
例如，Python亚特兰大用户的小组在每个月的第二个星期四开会。要计算一年的会议日期，可使用monthcalendar()。
<pre><code># calendar_monthcalendar.py

import calendar
import pprint

pprint.pprint(calendar.monthcalendar(2018, 5))</pre></code>
有些天是0值。这些是与给定月份没有的天数，但这是前后月的一部分。
<pre><code>$ python calendar_monthcalendar.py
[[0, 1, 2, 3, 4, 5, 6],
 [7, 8, 9, 10, 11, 12, 13],
 [14, 15, 16, 17, 18, 19, 20],
 [21, 22, 23, 24, 25, 26, 27],
 [28, 29, 30, 31, 0, 0, 0]]</pre></code>
一周的第一天默认为星期一。可以通过调用setfirstweekday()来改变这一点，但是由于calendar模块包含了用于索引到monthcalendar()返回的日期范围的常量，因此在这种情况下跳过这一步就更方便了。

要计算一年的小组会议日期，假设他们总是在每个月的第二个星期四，查看monthcalendar()的输出，以找到周四日期。月的第一个和最后一个星期里日期是在前一个月或下个月的天数中时用0值作为占位符。例如，如果一个月从周五开始，那么在周四的第一个星期的值将是0。
<pre><code># calendar_secondthursday.py

import calendar
import sys

year = int(sys.argv[1])

for month in range(1, 13):
    c = calendar.monthcalendar(year, month)
    first_week = c[0]
    second_week = c[1]
    third_week = c[2]
    if first_week[calendar.THURSDAY]:
        meeting_date = second_week[calendar.THURSDAY]
    else:
        meeting_date = third_week[calendar.THURSDAY]

    print('{:>3}: {:>2}'.format(calendar.month_abbr[month], meeting_date))</pre></code>
2018年的会议日期如下:
<pre><code>$ python calendar_secondthursday.py 2018
Jan: 11
Feb:  8
Mar:  8
Apr: 12
May: 10
Jun: 14
Jul: 12
Aug:  9
Sep: 13
Oct: 11
Nov:  8
Dec: 13</pre></code>

