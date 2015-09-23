# coding=utf-8

import SocketServer
import httplib
import socket
import traceback
import logging
import cStringIO as StringIO
import logutils
import sys
import os
import ssl
from urlparse import urlparse

from HttpMsg import HttpMsg
import toollib, socketlib, urlutils


class HttpProxyHandler(SocketServer.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        self.logger = logutils.getlogger("httpproxy", formatter=logging.Formatter(
            '[%(levelname)-8s][%(_filename)-20s%(_lineno)06d][%(serialno)s][%(message)s]'))
        SocketServer.BaseRequestHandler.__init__(self, *args, **kwargs)

    def socketrequest2(self, ip, port, msg, schema='http'):
        try:
            port = int(port)
            self.info("%s %d %s" % (ip, port, schema))
            sock = socket.socket()
            if schema.lower() == 'https' or port == 443:
                sock = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_NONE, ca_certs=None)
            sock.connect((ip, port))
            sock.sendall(msg)
            head = socketlib.recvByStr(sock, '\r\n\r\n')
            self.info(str(head))
            hm = HttpMsg(head)
            option = hm.getoption()
            length = option.get('Content-Length', 0)
            if length:
                body = socketlib.recvNbit(sock, int(length))
            else:
                body = self.readchunk(sock)
            self.info(body)
            return head + body
        except Exception as e:
            self.error(traceback.format_exc())
        finally:
            sock.close()

    def info(self, *args, **kwargs):
        frame = sys._getframe(1)
        self.logger.error(*args,
                          extra={'serialno': self.serialno, '_filename': os.path.basename(frame.f_code.co_filename, ),
                                 '_lineno': frame.f_lineno})

    def error(self, *args, **kwargs):
        frame = sys._getframe(1)
        self.logger.error(*args,
                          extra={'serialno': self.serialno, '_filename': os.path.basename(frame.f_code.co_filename),
                                 '_lineno': frame.f_lineno})

    def handle(self):
        try:
            self.serialno = toollib.getserialno()
            sendhead = socketlib.recvByStr(self.request, '\r\n\r\n').replace("Connection: keep-alive",
                                                                             "Connection: close").replace(
                "Connection: Keep-Alive", "Connection: Close")
            hm = HttpMsg(sendhead)
            option = hm.getoption()
            self.info(sendhead)
            method, requesturl, _ = hm.gethttphead()
            length = option.get('Content-Length', '0')
            if length != '0':
                sendbody = socketlib.recvNbit(self.request, int(length))
                if method == 'POST':
                    self.info(sendbody)
                send = sendhead + sendbody
            else:
                send = sendhead
            host, port = hm.gethost(option)
            self.info("host=%s, port=%s" % (str(host), str(port)))
            parseResult = urlparse(requesturl)
            # for url in urlutils.resolveurl(host):
            recv = self.socketrequest2(host, port, send, 'http' if parseResult.scheme == '' else parseResult.scheme)
            self.request.sendall(recv)
            # break
        except KeyboardInterrupt as kie:
            sys.exit(0)
        except Exception as e:
            self.error(traceback.format_exc(), )

    def readchunk1(self, sock):
        sio = StringIO.StringIO()
        while True:
            head = socketlib.recvByStr(sock, '\r\n')
            length = int(head[:-2], 16) + 2
            if length == 2:
                socketlib.recvNbit(sock, 4)
                break
            else:
                data = socketlib.recvNbit(sock, length)
                sio.write(data)
        return sio.getvalues()

    def readchunk(self, sock):
        response = socketlib.recvByStr(sock, '0\r\n\r\n')
        try:
            if response:
                toollib.writeonce(os.path.join(os.path.join(os.getenv("HOME"), "log"), "chunk.txt"), response)
        except:
            self.error(traceback.format_exc())
        return response
