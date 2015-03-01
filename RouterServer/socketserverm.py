import tcphandlerdefine
import SocketServer


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "", 8081
    httpproxy = tcphandlerdefine.HttpProxyHandler
    server = ThreadedTCPServer((HOST, PORT), tcphandlerdefine.HttpProxyHandler)
    server.serve_forever()
    server.shutdown()