import httphandler
import SocketServer


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "", 8087
    server = ThreadedTCPServer((HOST, PORT), httphandler.HttpProxyHandler)
    server.serve_forever()
    server.shutdown()
