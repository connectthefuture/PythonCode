import ssl, time, SocketServer


class HTTPSHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        sc = ssl.wrap_socket(self.request,
                             server_side=True,
                             certfile='cert.pem',
                             keyfile='cert.key',
                             )
        self.data = sc.recv(1024)
        print(self.data)
        buf = 'test HTTPS Server Handler<br>%f' % time.time()
        buf = buf.encode()
        sc.send(buf)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "", 4430
    server = ThreadedTCPServer((HOST, PORT), HTTPSHandler)
    server.serve_forever()
    server.shutdown()
