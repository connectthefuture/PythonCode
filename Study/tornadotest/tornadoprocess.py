# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.process
import os, time
import ctypes
from tradeutil import AppHandler, E404Handler

loadlibrary = ctypes.cdll.LoadLibrary
# sys.path.append("/home/lotus/src/python_src/tornadoapp")
# print __file__
# print "add library path [%s]" % os.path.dirname(__file__)


if __name__ == "__main__":
    app = tornado.web.Application(([r'/(\w+)/(\w+)', AppHandler],
                                   [r'.*', E404Handler]))
    sockets = tornado.netutil.bind_sockets(8090)
    tornado.process.fork_processes(2)
    server = tornado.httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()
