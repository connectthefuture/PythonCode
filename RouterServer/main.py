import cStringIO as StringIO

from pubutils import toollib


def foo(end):
    R = len(end)
    sio = StringIO.StringIO()
    fd = open('a.txt', 'rb')
    while True:
        head = toollib.readByStr(fd, end)
        print "tell %d" % fd.tell()
        print '[%s], %d' %(head, len(head))
        length = int(head[:-1 * R], 16) + R
        print('len=%d' % length)
        if length == R:
            toollib.readNbit(fd, R)
            break
        else:
            data = toollib.readNbit(fd, length)
            print "tell %d %d" % (fd.tell(), len(data))
            sio.write(data)

if __name__ == '__main__':
    foo('\r\n\n')
    import urllib2
    import urllib