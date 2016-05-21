import asyncio

#from queues import Queue

class Test:
    def __init__(self, loop=None):
        self._queue = asyncio.Queue(loop=loop)
        self._future = asyncio.Future(loop=loop)

    @asyncio.coroutine
    def run(self):
        asyncio.async(self._feed_queue(2))
        asyncio.async(self._recv())

    @asyncio.coroutine
    def _feed_queue(self, interval):
        v = 0
        while True:
            yield from asyncio.sleep(interval)
            print("feed")
            yield from self._queue.put(v)
            v = v+1
            # print("%s" % repr(self._queue))


    @asyncio.coroutine
    def _recv(self):

        while True:
            # print('wait')
            try:
                r = yield from asyncio.wait_for(self._queue.get(), timeout=1.0)
                print(">>>>>>>>>>>>>>>",r)
            except asyncio.TimeoutError:
                print("timeout")
                continue
            except:
                break

        print("quit")


loop = asyncio.get_event_loop()
t = Test(loop=loop)
asyncio.async(t.run())
loop.run_forever()