import socket, select, os, sys, re
from tornado import gen

queue = list()


def grep(pattern):
    print "Looking for %s" % pattern
    while True:
        print '3'
        line = (yield)
        print '4'
        if pattern in line:
            print line,


def product():
    g = grep("python")
    g1 = grep("python")
    print '1'
    g.next()
    print '2'
    g.send("Yeah, but no, but yeah, but no")
    g.send("A series of tubes")
    g.send("python generators rock!")


def fd_accept():
    while 1:
        fd = (yield)
        sock, address = fd.accept()
        print address


if __name__ == '__main__':
    server = socket.socket()
    server.bind(("", 8000))
    server.listen(5)
    rfd, wfd, efd = [server], [], []
    g = fd_accept()
    g.next()
    while 1:
        r, w, e = select.select(rfd, wfd, efd)
        for fd in r:
            g.send(fd)

