# coding=utf-8

import SocketServer
import httplib
import socket
import traceback
import logging
import cStringIO as StringIO

from pubutils.parsemsgs.http import HttpMsg
from pubutils import toollib, socketlib, urlutils


formatter = logging.Formatter('[%(serialno)s %(filename)s %(lineno)d %(levelname)s]: %(message)s')
hdlrlogger = toollib.getlogger("tcphdlr", formatter=formatter)
errlogger = toollib.getlogger('errlog', formatter=formatter)


def httprequest(ip, port, url, method, head, body):
    httpClient = httplib.HTTPConnection(ip, port)
    httpClient.request(method, url, body, head)
    response = httpClient.getresponse()
    return response


def socketrequest(ip, port, msg):
    sock = socket.socket()
    sock.connect((ip, port))
    sock.sendall(msg)
    return socketlib.recvFull(sock)


def readchunk1(sock):
    return socketlib.recvFull(sock)


class HttpProxyHandler(SocketServer.BaseRequestHandler):
    def handle2(self):
        send = self.request.recv(1 * 1024 * 1024)
        hm = HttpMsg(send)
        option = hm.getoption()
        response = httprequest("192.168.254.10", 8080, '/ServerData.asmx', 'POST', option, hm.getbody())
        recv = response.read()
        self.request.sendall(recv)

    def handle(self):
        try:
            self._serialno = toollib.getserialno()
            extra = {'serialno': self._serialno}
            sendhead = socketlib.recvByStr(self.request, '\r\n\r\n')
            hdlrlogger.debug(sendhead, extra=extra)
            hm = HttpMsg(sendhead)
            option = hm.getoption()
            reqhttphead = hm.gethttphead()
            hdlrlogger.debug(reqhttphead, extra=extra)
            length = option.get('Content-Length', '0')
            if length != '0':
                sendbody = socketlib.recvNbit(self.request, int(length))
                send = sendhead + sendbody
            else:
                send = sendhead
            host, port = hm.gethost(option)
            hdlrlogger.debug('%s, %d' % (host, port), extra=extra)
            for url in urlutils.resolveurl(host):
                recv = self.socketrequest2(host, port, send)
                self.request.sendall(recv)
                break
        except Exception as e:
            hdlrlogger.error('%s' % traceback.format_exc(), extra=extra)
            toollib.printframe(hdlrlogger, extra)


    def socketrequest2(self, ip, port, msg):
        sock = socket.socket()
        sock.connect((ip, port))
        sock.sendall(msg)
        head = socketlib.recvByStr(sock, '\r\n\r\n')
        extra = {'serialno': self._serialno}
        hdlrlogger.debug(head, extra=extra)
        hm = HttpMsg(head)
        option = hm.getoption()
        hdlrlogger.debug(option, extra=extra)
        length = option.get('Content-Length', None)
        if length:
            body = socketlib.recvNbit(sock, int(length))
        else:
            body = self.readchunk(sock)
            toollib.writeonce('chunk.txt', body)
        hdlrlogger.debug(body, extra=extra)
        sock.close()
        return head + body

    def readchunk1(self, sock):
        extra = {'serialno': self._serialno}
        sio = StringIO.StringIO()
        while True:
            head = socketlib.recvByStr(sock, '\r\n')
            hdlrlogger.debug(head, extra=extra)
            length = int(head[:-2], 16) + 2
            if length == 2:
                socketlib.recvNbit(sock, 4)
                break
            else:
                hdlrlogger.debug('length=%d' % length, extra=extra)
                data = socketlib.recvNbit(sock, length)
                hdlrlogger.debug(data, extra=extra)
                sio.write(data)
        return sio.getvalues()


    def readchunk(self, sock):
        return socketlib.recvByStr(sock, '0\r\n\r\n')


