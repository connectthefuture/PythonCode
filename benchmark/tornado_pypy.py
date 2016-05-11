import tornado.ioloop
import tornado.web
import tornado.httpserver

import pymysql
import database

conn = pymysql.connect(host='192.168.31.241', user='root', passwd='root', db='test', charset='utf8')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    if 0:
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.bind(9999)
        http_server.start(num_processes=0)
    else:
        application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
