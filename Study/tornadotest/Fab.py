import sys


class Fab(object):
    def __init__(self, max):
        self.max = max
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def next(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration()


# for i in Fab(10):
#     sys.stdout.write("%d " % i)
# print


def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        # print b
        a, b = b, a + b
        n = n + 1


# for i in fab(10):
#     sys.stdout.write("%d " % i)
# print
#
# f = fab(10)
# while 1:
#     try:
#         sys.stdout.write("%d " % f.next())
#     except:
#         break
# print

def null(N):
    i = 0
    print 'N=%d' % N
    while i < N:
        i += 1
        print '%d aa' % (i-1)
        b = (yield)
        print '%d bb' % (i-1)
        # print b


f = null(1)
# f.send(None)
print 'ffff'
n = 0
while 1:
    n += 1
    print 'yyyy'
    try:
        f.next()
    except:
        break
    print 'xxxx'
