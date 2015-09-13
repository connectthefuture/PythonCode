import tcphandlerdefine
import SocketServer


class ThreadedTCPServer(SocketServer.TCPServer):
    pass


class HttpProxyHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print(self.client_address)
        print(self.request.recv(100))
        self.request.sendall("xx0\r\n\r\n")
        self.request.close()


if __name__ == "__main__":
    HOST, PORT = "", 8080
    httpproxy = tcphandlerdefine.HttpProxyHandler
    server = ThreadedTCPServer((HOST, PORT), HttpProxyHandler)
    server.serve_forever()