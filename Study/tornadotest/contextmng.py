import contextlib
import logging
import sys
from tornado import httpclient
from tornado.ioloop import IOLoop
from tornado import stack_context


@contextlib.contextmanager
def die_on_error():
    try:
        yield
    except Exception:
        logging.error("exception in asynchronous operation", exc_info=True)
        sys.exit(1)


def foo(data):
    print (
        'aa'
    )


# for i in xrange(10):
#     print ('begin %d' % i)  # Any exception thrown here *or in callback and its descendants*
#     http_client = httpclient.AsyncHTTPClient()
#     http_client.fetch("http://www.baidu.com", foo)
#     print('end %d' % i)

for i in xrange(1):
    with stack_context.StackContext(die_on_error):
        print ('begin %d' % i)
        # Any exception thrown here *or in callback and its descendants*
        # will cause the process to exit instead of spinning endlessly
        # in the ioloop.
        # http_client = httpclient.AsyncHTTPClient()
        # http_client.fetch("http://www1.baidu.com", foo)
        1 / 0
        print('end %d' % i)
IOLoop.current().start()
