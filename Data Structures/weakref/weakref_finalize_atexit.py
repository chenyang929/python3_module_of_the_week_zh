# weakref_finalize_atexit.py

import sys
import weakref


class ExpensiveObject:

    def __del__(self):
        print('(Deleting) {}'.format(self))


def on_finalize(*args):
    print('on_finalize({!r})'.format(args))


obj = ExpensiveObject()
f = weakref.finalize(obj, on_finalize, 'extra argument')
f.atexit = bool(int(sys.argv[1]))
