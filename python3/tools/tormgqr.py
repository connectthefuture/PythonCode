import asyncio, aiohttp, logging, traceback
from http.cookiejar import LWPCookieJar
import sqlalchemy
import tornado
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
from tornado import httpclient
import tornado.ioloop


@tornado.gen.coroutine
def foo():
    ahc = AsyncHTTPClient()
    request = httpclient.HTTPRequest(
        url='http://www.mgqr.com/control/checklogin.ashx',  # 这里的url想要有东西就需要带着cookie
        method='POST',
        body=b""
    )
    response = yield tornado.gen.Task(ahc.fetch, request)
    print(response.body.decode('utf8'))


if __name__ == '__main__':
    s = tornado.ioloop.IOLoop.current().run_sync(foo)
    tornado.ioloop.IOLoop.current().start()
