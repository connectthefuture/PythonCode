#coding=utf-8
import imp
import sys
imp.reload(sys)
# sys.setfilesystemencoding('utf8')
import urllib
import aiohttp
import asyncio
import json

@asyncio.coroutine
def foo():
    s = yield from aiohttp.post("https://getpocket.com/a/queue/",)
    print(s)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [foo()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.run_forever()

