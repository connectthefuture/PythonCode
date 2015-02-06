import logging
import datetime
import thread
import sys

# formatter = logging.Formatter('[%(serialno)s %(filename)s %(lineno)d %(levelname)s]: %(message)s')

try:
    import cStringIO as StringIO
except:
    import StringIO

READMAX = 4096


def recvNbit(sock, N):
    buf = StringIO.StringIO()
    nRead = 0
    while nRead < N:
        left = N - nRead
        tmp = sock.recv(min(left, READMAX))
        if tmp == '':
            break
        buf.write(tmp)
        nRead += len(tmp)
    rs = buf.getvalue()
    buf.close()
    return rs


def readNbit(fd, N):
    buf = StringIO.StringIO()
    nRead = 0
    while nRead < N:
        left = N - nRead
        tmp = fd.read(min(left, READMAX))
        if tmp == '':
            break
        buf.write(tmp)
        nRead += len(tmp)
    rs = buf.getvalue()
    buf.close()
    return rs

def readByStr(fd, s):
    # sio = StringIO.StringIO()
    buf = ""
    N = len(s)
    while True:
        ch = fd.read(1)
        if ch == "":
            return buf
        else:
            buf += ch
            if buf[-N:] == s:
                return buf

def recvByStr(sock, s):
    # sio = StringIO.StringIO()
    buf = ""
    N = len(s)
    while True:
        ch = sock.recv(1)
        if ch == "":
            return buf
        else:
            buf += ch
            if buf[-N:] == s:
                return buf


def recvFull(sock):
    data = ''
    while True:
        try:
            tmp = ''
            tmp = sock.recv(READMAX)
            if tmp:
                data += tmp
            else:
                return data
            if len(tmp) < READMAX:
                return data
        except Exception as e:
            return data