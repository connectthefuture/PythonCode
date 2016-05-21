import random
import urllib.request
import http.cookiejar as cookielib
import json
import time


def foo():
    while 1:
        # 声明一个CookieJar对象实例来保存cookie
        cookie = cookielib.CookieJar()
        # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        handler = urllib.request.HTTPCookieProcessor(cookie)
        # 通过handler来构建opener
        opener = urllib.request.build_opener(handler)
        req = urllib.request.Request(url='http://www.mgqr.com/control/checklogin.ashx',
                                     data=b'UserName=1392798578%40qq.com&UserPwd=111aaa&remember=1')
        # 此处的open方法同urllib2的urlopen方法，也可以传入request
        response = opener.open(req)
        text = response.read().decode('utf8')
        obj = json.loads(text, )
        print(obj["notice"])
        req1 = urllib.request.Request("http://www.mgqr.com/control/userres.ashx?q={}".format(random.random()), data=b"")
        response1 = opener.open(req1)
        print(response1.read())
        time.sleep(120)


# print(requests.post('http://www.mgqr.com/control/checklogin.ashx',
#                     b'UserName=1392798578%40qq.com&UserPwd=111aaa&remember=1'))

if __name__ == "__main__":
    foo()
