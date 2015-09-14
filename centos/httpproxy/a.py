import sys

def foo():
    frame = sys._getframe(1)
    print frame.f_code.co_filename, frame.f_lineno

if __name__ == '__main__':
    foo()