import xml.dom.minidom as minidom
from django.http import HttpResponseRedirect
import models
import os
import logging
import xpath

logger = logging.getLogger("djangoweb.app")

def log2db():
    pass


class BaseObject:
    def getmap(self):
        return self.__dict__

    def getkeys(self):
        return self.__dict__.keys()

class XmlUtil:
    @staticmethod
    def getencoding(xml):
        tmp = xml[:xml.find('>')]
        # tmp = tmp.lower()
        if tmp.find('utf-8') > 0:
            return 'utf-8'
        elif tmp.find('UTF-8') > 0:
            return 'UTF-8'
        elif tmp.find('gbk') > 0:
            return 'gbk'
        elif tmp.find('GBK') > 0:
            return 'GBK'
        elif tmp.find('gb18030') > 0:
            return 'gb18030'
        elif tmp.find('GB18030') > 0:
            return 'GB18030'

    @staticmethod
    def gbk2utf8(xml):
        encoding = XmlUtil.getencoding(xml)
        if encoding != 'utf-8' and encoding != 'UTF-8':
            xml = xml.replace(encoding, 'utf-8', 1)
            return xml.decode('gb18030').encode('utf-8')
        else:
            return xml


class MsgHandler:
    def __init__(self, input, config):
        self._input = input
        self._config = config

    def parse(self):
        raise Exception("UnImplementExcetion")


class XmlHandler(MsgHandler):
    def parse(self):
        self.dom = minidom.parseString(self._input)
        o = BaseObject()
        parsexml(self.dom, o)
        return o

    def gettranscode(self):
        context = xpath.XPathContext()
        return context.find(self._config.trancodexpath, self.dom)[0].childNodes[0].nodeValue

    def getserialno(self):
        context = xpath.XPathContext()
        return context.find(self._config.serialnoxpath, self.dom)[0].childNodes[0].nodeValue


def parsexml(node, mp):
    for child in node.childNodes:
        if child.nodeType == 3:
            setattr(mp, node.nodeName, child.nodeValue)
        parsexml(child, mp)


class TradeContext:
    def __init__(self, project, request):
        self.project = project
        self.request = request

    def getconfig(self):
        self.config = models.ProjectDef.objects.get(project=self.project)

    def execute(self):
        global logger
        self.request = XmlUtil.gbk2utf8(self.request)
        self.getconfig()
        if self.config.msgtype == '1':
            msghdr = XmlHandler(self.request, self.config)
        input = msghdr.parse()
        self.transcode = msghdr.gettranscode()
        self.getpysource()
        export = {}
        if self.pysource:
            execfile(self.pysource)
        self.trantmplmap()
        export['input'] = input
        self.map2tmplate = export

    def trantmplmap(self):
        tranmap = models.TranMsgMap.objects.get(project=self.project, transcode=self.transcode, active='1')
        self.template = "%s_%s_%s.html" % (self.project, self.transcode, tranmap.template)


    def getpysource(self):
        pysource = "%s_%s.py" % (self.project, self.transcode)
        sourcedir = os.path.join(os.path.dirname(__file__), 'transconfig')
        fname = os.path.join(sourcedir, pysource)
        if os.path.exists(fname):
            self.pysource = fname
        else:
            self.pysource = ""


def needlogin(func):
    def _deco(*args, **kwargs):
        if args[0].session.get('UserId') is None:
            ret = HttpResponseRedirect('/login/')
        else:
            ret = func(*args, **kwargs)
        return ret
    return _deco