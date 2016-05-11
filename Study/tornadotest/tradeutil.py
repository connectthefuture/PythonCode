# coding=utf8
import traceback
import sys
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.process
import os, time
import ctypes
from ctypes import *
import json

loadlibrary = ctypes.cdll.LoadLibrary


class E404Handler(tornado.web.RequestHandler):
    def get(self):
        self.write("Url未定义")


class TradeHandler(tornado.web.RequestHandler):
    pass


class AppHandler(TradeHandler):
    def check_func_name(self, func):
        for i in func:
            if i.isdigit() or i.islower() or i.isupper() or i == "_":
                pass
            else:
                return False
        return True

    def post(self, libname, funcName):
        try:
            lib = None
            if not self.check_func_name(funcName):
                raise Exception("函数名[%s]不合法" % funcName)
            libfile = "%s.so" % libname
            # lib = loadlibrary(libfile)
            if libname in sys.modules:
                reload(sys.modules[libname])
                lib = sys.modules[libname]
            else:
                lib = __import__(libname)
            func = getattr(lib, funcName)
        except OSError as oe:
            self.write("模块[%s]未定义" % libfile)
        except AttributeError as ae:
            self.write("函数[%s]未定义" % funcName)
        except Exception as e:
            self.write(str(e))
        else:
            try:
                getArgsDefine = getattr(lib, "getArgsDefine")
                result = getArgsDefine(funcName)
                if result[0] == 1:
                    argsDefine = result[2][0]
                else:
                    raise Exception("未定义的函数")
                args = []
                for arg in argsDefine:
                    args.append(self.get_argument(arg, ""))
                # value = c_int.in_dll(lib, "FUNC_ARGS_DEFINE")
                # self.write(str(value))
                # self.write(str(func(1, 2)))
            except Exception:
                traceback.print_exc()
            else:
                result = apply(func, args, {})
                self.write(str(result))
        finally:
            lib = None
