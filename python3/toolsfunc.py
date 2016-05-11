# coding = utf8
import operator
import functools
from functools import partial
import contextlib

b = operator.itemgetter
# functools.cmp_to_key()
# s = sorted(student_objects, key=attrgetter('age'))
int2 = partial(int, base=2)
print (int2('1000'))


class test:
    def __enter__(self):
        print("enter")
        return 1

    def __exit__(self, *args):
        print("exit")


def function():
    print('function()')
    return 111


# with test() as t:
#      function()
#      print('t is', t)

import time


def foo():
    print('in foo()')


def timeit(func):
    start = time.clock()
    func()
    end = time.clock()
    print('used:', end - start)


timeit(foo)


def foo():
    print('in foo()')


# 定义一个计时器，传入一个，并返回另一个附加了计时功能的方法
def timeit(func):
    # 定义一个内嵌的包装函数，给传入的函数加上计时功能的包装
    def wrapper():
        start = time.clock()
        func()
        end = time.clock()
        print('used:', end - start)

    # 将包装后的函数返回
    return wrapper


foo = timeit(foo)
foo()
