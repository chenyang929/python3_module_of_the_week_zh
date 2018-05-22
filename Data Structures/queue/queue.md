# queue -- Thread-Safe FIFO Implementation
> 目的：实现一个先进先出队列

队列模块提供了适合多线程编程的先进先出(FIFO)数据结构。它可以用于在生产者和消费者线程之间安全地传递消息或其他数据。锁定是为调用方处理的，因此许多线程可以安全地和轻松地处理相同的队列实例。
队列的大小(包含它所包含的元素的数量)可能被限制为限制内存使用或处理。
## Basic FIFO Queue
队列类实现了基本的先入、先出容器。使用put()将元素添加到序列的一个“end”端，并使用get()从另一端删除元素。
<pre><code># queue_fifo.py

import queue

q = queue.Queue()

for i in range(5):
    q.put(i)

while not q.empty():
    print(q.get(), end=' ')
print()</pre></code>
这个示例使用一个线程来说明从队列中删除元素的顺序与插入它们的顺序是相同的。
<pre><code>$ python queue_fifo.py
0 1 2 3 4 </pre></code>
## LIFO Queue
与队列的标准FIFO实现形成对比的是，LifoQueue实现LIFO，后进先出(通常与堆栈数据结构相关联)。
<pre><code># queue_lifo.py

import queue

q = queue.LifoQueue()

for i in range(5):
    q.put(i)

while not q.empty():
    print(q.get(), end=' ')
print()</pre></code>
最近放入队列中的项目被先get出来。
<pre><code>$ python queue_lifo.py
4 3 2 1 0 </pre></code>
## Priority Queue
有时候，队列中项目的处理顺序需要基于这些项的特征，而不仅仅是它们创建或添加到队列中的顺序。
例如，来自payroll部门的打印作业可能优先于开发人员想要打印的代码清单。PriorityQueue使用队列内容的排序顺序来决定要检索的项。
<pre><code># queue_priority.py

import functools
import queue
import threading


@functools.total_ordering
class Job:

    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print('New job:', description)
        return

    def __eq__(self, other):
        try:
            return self.priority == other.priority
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.priority < other.priority
        except AttributeError:
            return NotImplemented


q = queue.PriorityQueue()

q.put(Job(3, 'Mid-level job'))
q.put(Job(10, 'Low-level job'))
q.put(Job(1, 'Important job'))


def process_job(q):
    while True:
        next_job = q.get()
        print('Processing job:', next_job.description)
        q.task_done()


workers = [
    threading.Thread(target=process_job, args=(q,)),
    threading.Thread(target=process_job, args=(q,)),
]
for w in workers:
    w.setDaemon(True)
    w.start()

q.join()</pre></code>
这个例子有多个线程消耗作业，这些线程在调用get()时是根据队列中的项目的优先级来的。
在消费者线程运行时，对添加到队列的项的处理顺序取决于线程上下文切换。
<pre><code>$ python queue_priority.py
New job: Mid-level job
New job: Low-level job
New job: Important job
Processing job: Important job
Processing job: Mid-level job
Processing job: Low-level job</pre></code>
## Building a Threaded Podcast Client
本节中的podcasting客户机的源代码演示了如何使用多线程的队列类。该程序读取一个或多个RSS提要，为每个提要中的5个最近的片段排队等待下载，并使用线程并行处理多个下载。它对于生产使用没有足够的错误处理，但是框架的实现说明了队列模块的使用。

首先，建立了一些操作参数。通常，这些数据来自于用户输入(例如，首选项或数据库)。该示例使用硬编码的值来获取线程数和url列表。
<pre><code># fetch_podcasts.py

from queue import Queue
import threading
import time
import urllib.request
from urllib.parse import urlparse
import feedparser   # 第三方库

num_fetch_threads = 2
enclosure_queue = Queue()

feed_urls = [
    'http://talkpython.fm/episodes/rss'
]


def message(s):
    print('{}: {}'.format(threading.current_thread().name, s))


def download_enclosures(q):
    while True:
        message('looking for the next enclosure')
        url = q.get()
        filename = url.rpartition('/')[-1]
        message('downloading {}'.format(filename))
        response = urllib.request.urlopen(url)
        data = response.read()
        message('writing to {}'.format(filename))
        with open(filename, 'wb') as outfile:
            outfile.write(data)
        q.task_done()


for i in range(num_fetch_threads):
    worker = threading.Thread(
        target=download_enclosures,
        args=(enclosure_queue,),
        name='worker-{}'.format(i),
    )
    worker.setDaemon(True)
    worker.start()

for url in feed_urls:
    response = feedparser.parse(url, agent='fetch_podcasts.py')
    for entry in response['entries'][:5]:
        for enclosure in entry.get('enclosures', []):
            parsed_url = urlparse(enclosure['url'])
            message('queuing {}'.format(parsed_url.path.rpartition('/')[-1]))
            enclosure_queue.put(enclosure['url'])

message('*** main thread waiting')
enclosure_queue.join()
message('*** done')</pre></code>
运行样例脚本会产生类似以下的输出。
<pre><code>$ python fetch_podcasts.py
worker-0: looking for the next enclosure
worker-1: looking for the next enclosure
MainThread: queuing turbogears-and-the-future-of-python-web-frameworks.mp3
MainThread: queuing continuum-scientific-python-and-the-business-of-open-source.mp3
MainThread: queuing openstack-cloud-computing-built-on-python.mp3
MainThread: queuing pypy.js-pypy-python-in-your-browser.mp3
MainThread: queuing machine-learning-with-python-and-scikit-learn.mp3
MainThread: *** main thread waiting
worker-0: downloading turbogears-and-the-future-of-python-web-frameworks.mp3
worker-1: downloading continuum-scientific-python-and-the-business-of-open-source.mp3
worker-0: looking for the next enclosure
worker-0: downloading openstack-cloud-computing-built-on-python.mp3
worker-1: looking for the next enclosure
worker-1: downloading pypy.js-pypy-python-in-your-browser.mp3
worker-0: looking for the next enclosure
worker-0: downloading machine-learning-with-python-and-scikit-learn.mp3
worker-1: looking for the next enclosure
worker-0: looking for the next enclosure
MainThread: *** done</pre></code>


