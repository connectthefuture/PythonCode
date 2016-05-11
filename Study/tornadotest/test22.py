import os, time
import ctypes
import sys

loadlibrary = ctypes.cdll.LoadLibrary

# lib = loadlibrary("foo.so")
# func = getattr(lib, "add")
# print func(1, 2)

class A():
    pass

a = 1
print sys.getrefcount(a)
a = A()
print sys.getrefcount(a)
b = a
print sys.getrefcount(a)
del b
print sys.getrefcount(a)