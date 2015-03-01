import SocketServer  
from SocketServer import StreamRequestHandler as SRH

def InitServConfig():
    print 'init'


class SocketHandler(SRH):
    def handle(self):
        ENV = self.server.ENV
        pass
    def unpackin(self):
        pass
    def packout(self):
        pass
    def worker(self):
        pass

def CreateSocketServer(env,):
    server = SocketServer.ThreadingTCPServer(('', env['listenport']), SocketHandler)
    server.ENV = env
    return server

class C:
    pass

if __name__ == '__main__':
    C.initconfig = InitServConfig
    C.initconfig()