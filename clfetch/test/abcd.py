import urllib
from urllib import request
import asyncio


@asyncio.coroutine
def foo(n):
    while 1:
        n += 1
        print('foo begin')
        try:
            yield from goo(n)
        except Exception as e:
            print(e)
        # asyncio.ensure_future(goo(n))
        yield from asyncio.sleep(1)

        print('foo end')



@asyncio.coroutine
def goo(x):
    print('goo %d' % x)
    raise Exception('hello')
    yield from asyncio.sleep(1)


loop = asyncio.get_event_loop()
asyncio.ensure_future(foo(0))
loop.run_forever()
