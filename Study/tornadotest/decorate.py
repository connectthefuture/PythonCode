import functools
import time


def deco(func):
    # func()
    try:
        return func
    finally:
        print 'ended'

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print 'call %s():' % func.__name__
        return func(*args, **kw)
    return wrapper

@log
def now():
    print time.strftime("%Y%m%d")

def log_1(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print '%s %s():' % (text, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator

@log_1("execute")
def now_1():
    print time.strftime("%Y%m%d")


def myfunc():
    return 1

@deco
def myfunc1():
    return 1

# myfunc_d = deco(myfunc)

# print myfunc_d()
# print myfunc1()

now()
now_1()

