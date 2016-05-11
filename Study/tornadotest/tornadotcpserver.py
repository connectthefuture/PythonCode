# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import sys
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.tcpserver
import tornado.process
import os, time
import ctypes


if __name__ == "__main__":
    sockets = tornado.netutil.bind_sockets(9090)
    tornado.process.fork_processes(2)
    server = tornado.tcpserver.TCPServer()
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()