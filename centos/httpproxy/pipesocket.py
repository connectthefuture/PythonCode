import socket, sys, select, errno, SocketServer


def forward_socket(local, remote, timeout, bufsize):
    """forward socket"""
    try:
        tick = 1
        timecount = timeout
        while 1:
            timecount -= tick
            if timecount <= 0:
                break
            (ins, _, errors) = select.select([local, remote], [], [local, remote], tick)
            if errors:
                break
            for sock in ins:
                data = sock.recv(bufsize)
                if not data:
                    break
                if sock is remote:
                    local.sendall(data)
                    timecount = timeout
                else:
                    remote.sendall(data)
                    timecount = timeout
    except socket.timeout:
        pass
    except (socket.error,) as e:
        if e.args[0] not in (errno.ECONNABORTED, errno.ECONNRESET, errno.ENOTCONN, errno.EPIPE):
            raise
        if e.args[0] in (errno.EBADF,):
            return
    finally:
        for sock in (remote, local):
            try:
                sock.close()
            except StandardError:
                pass


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class ProxyHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        sock = socket.socket()
        sock.connect(('192.168.183.128', 8087))
        forward_socket(self.request, sock, 60, 4096)

if __name__ == "__main__":
    HOST, PORT = "", 4000
    server = ThreadedTCPServer((HOST, PORT), ProxyHandler)
    server.serve_forever()
    server.shutdown()
