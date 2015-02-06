#coding=gbk
import httplib


def needlogin(func):
    def _deco(*args, **kwargs):
        if args[0]:
            ret = 100
        else:
            ret = func(*args, **kwargs)
        return ret
    return _deco

@needlogin
def foo(a):
    print 'foo', a
    return a

def httppost():
    httpclient = httplib.HTTPConnection('127.0.0.1', 8000)
    httpclient.connect()
    header = {

    }
    httpclient.request("POST", "/xmlservice/dsdf/", '<?xml version="1.0" encoding="gbk"?><root><transcode>3333</transcode><serno>中国</serno></root>', header)
    resp = httpclient.getresponse()
    html = resp.read()
    if resp.status == 500:
        with open('test.html', 'w') as fd:
            fd.write(html)
    else:
        print resp.status
        print html.decode('gbk')


def httppost1():
    httpclient = httplib.HTTPConnection('127.0.0.1', 8000)
    httpclient.connect()
    header = {

    }
    httpclient.request("POST", "/ajaxservice/1000/", '', header)
    resp = httpclient.getresponse()
    html = resp.read()
    if resp.status == 500:
        with open('test.html', 'w') as fd:
            fd.write(html)
    else:
        print resp.status
        print html

if __name__ == '__main__':
    httppost()