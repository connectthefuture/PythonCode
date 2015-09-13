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

def recvByStr(sock, s):
    # sio = StringIO.StringIO()
    try:
        buf = ""
        N = len(s)
        lastN = ""
        sio = StringIO.StringIO()
        while 1:
            ch = sock.recv(1)
            if ch == "":
                buf = sio.getvalue()
                break
            else:
                sio.write(ch)
                if N != 1:
                    lastN = lastN[-1 * (N - 1):] + ch
                else:
                    lastN = ch
                if lastN == s:
                    buf = sio.getvalue()
                    break
        return buf
    finally:
        sio.close()


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