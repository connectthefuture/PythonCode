# coding=utf-8
from urlparse import urlparse

import logutils

logger = logutils.getlogger("httpmsg")


class HttpMsg:
    def __init__(self, msg="", response=None):
        self._msg = msg
        self._response = response

    def gethttphead(self):
        return self._msg[:self._msg.find("\r\n")].split(' ')

    def gethost(self, option=None):
        try:
            if not option:
                option = self.getoption()
            # if not "Host" in option:
            if 0:
                url = self.gethttphead()[1]
                up = urlparse(url)
                if up.find(':'):
                    tmp = up.split(':')
                    return (tmp[0], int(tmp[1]))
                else:
                    return (up, 80)
            else:
                host = option['Host']
                if host.find(':') >= 0:
                    tmp = host.split(":")
                    return (tmp[0], int(tmp[1]))
                else:
                    return (host, 80)
        except Exception as e:
            logger.info(option)



    def getoption(self):
        kv = {}
        options = self._msg.split('\r\n')[:-2]
        for i, opt in enumerate(options):
            if i == 0:
                continue
            try:
                key, value = opt.split(': ')
            except:
                pass
            kv[key] = value
        return kv

    def getbody(self):
        pos = self._msg.find('\r\n\r\n')
        return self._msg[pos + 4:]

    def http2plain(self):
        head = "HTTP/1.1 %d %s" % (self._response.status, self._response.reason)
        header = self._response.msg
        body = self._response.read()
        return head + "\r\n" + header + "\r\n" * 2 + body

    @staticmethod
    def genhttpResponse():
        pass
