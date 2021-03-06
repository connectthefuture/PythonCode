import socket, ssl, pprint
import time

crtf = "cert.pem"
keyf = "cert.key"
cacrtf = "cert.pem"

if 1:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ssl_socket = ssl.wrap_socket(socket, cert_reqs=ssl.CERT_REQUIRED, ca_certs=None)
    ssl_socket = ssl.wrap_socket(socket, cert_reqs=ssl.CERT_NONE, ca_certs=None)
    ssl_socket.connect(('127.0.0.1', 4430))
    print(repr(ssl_socket.getpeername()))
    print(ssl_socket.cipher())
    print(pprint.pformat(ssl_socket.getpeercert()))
    ssl_socket.write("Time: %s\r\n" % time.time())
    data = ssl_socket.read()
    print(data)
    ssl_socket.close()
else:
    context = ssl._create_default_https_context()
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = context.wrap_socket(sc, server_hostname='www.baidu.com')
