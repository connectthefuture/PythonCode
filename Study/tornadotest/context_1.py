from contextlib import contextmanager
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado import ioloop
# import gevent

@gen.coroutine
def gethttp():
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch("http://example.com")


# io_loop = ioloop.IOLoop.current()
#
# io_loop.start()


@contextmanager
def make_context():
    print 'enter'
    try:
        yield {}
    except RuntimeError, err:
        print 'error', err
    finally:
        print 'exit'


with make_context() as value:
    print value

# with open('a') as fa, open('b') as fb:
#     pass

def foo():
    yield 1

# f = foo()
# print f.next()
# print f.next()
