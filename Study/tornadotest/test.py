#coding=utf8
import tornado.ioloop
from tornado import stack_context

IL = tornado.ioloop.IOLoop.instance()


def callback():
    raise Exception, 'in callback'


def foo():
    pass


with stack_context.ExceptionStackContext(foo):
    def func():
        IL.add_callback(callback)


def out():
    try:
        func()
    except:
        print 'ok'

from collections import defaultdict

def tree():
    return defaultdict(tree)
# out()
# IL.start()

# import module

# print module.addPerson("中国", "", "", "")[2][0]
xml = tree()
xml['a'] = '100'
print xml['a']

d = defaultdict(float)
print d['a']
