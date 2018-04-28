# weakref_valuedict.py

import gc
from pprint import pprint
import weakref

gc.set_debug(gc.DEBUG_UNCOLLECTABLE)


class ExpensiveObject:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'ExpensiveObject({})'.format(self.name)

    def __del__(self):
        print('   (Deleting {})'.format(self))


def demo(cache_factory):
    #  保存对象防止任何弱引用被立即移除
    all_refs = {}
    #  使用工厂创建缓存
    print('CACHE TYPE:', cache_factory)
    cache = cache_factory()
    for name in ['one', 'two', 'three']:
        o = ExpensiveObject(name)
        cache[name] = o
        all_refs[name] = o
        del o

    print('  all_refs =', end=' ')
    pprint(all_refs)
    print('\n  Before, cache contains:', list(cache.keys()))
    for name, value in cache.items():
        print('   {} = {}'.format(name, value))
        del value

    # 除了缓存外删除所有对象的引用
    print('\n  Cleanup')
    del all_refs
    gc.collect()

    print('\n  After, cache contains:', list(cache.keys()))
    for name, value in cache.items():
        print('   {} = {}'.format(name, value))
    print('   demo returning')
    return


demo(dict)
print()
demo(weakref.WeakValueDictionary)

