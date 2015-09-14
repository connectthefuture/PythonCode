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


def getlogger(filename, level=logging.DEBUG, hdlr=None, formatter=None):
    logger = logging.getLogger(filename)
    hdlr = logging.FileHandler(filename + ".log")
    if not formatter:
        formatter = logging.Formatter('[%(asctime)s %(filename)s %(lineno)d %(levelname)s]: %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(level)
    return logger


def printframe(logger, extra):
    frame = sys._getframe(1)
    vars = frame.f_locals
    logger.info('%s, %d' %(frame.f_code.co_filename, frame.f_lineno), extra=extra)
    for key in vars:
        logger.info('%s=%s' %(key, str(vars[key])), extra=extra)

def hexdump(s):
    m,n = divmod(len(s), 16)
    if n > 0: m += 1


def getserialno():
    now = datetime.datetime.now()
    tid = thread.get_ident()
    s = '%04d%02d%02d%02d%02d%02d%06d'%(now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)
    return s[:-3] + '%04d' % tid

def writeonce(fname, content):
    with open(fname, 'wb') as fd:
        fd.write(content)

