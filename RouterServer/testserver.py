import socket
from pubutils import socketlib
sock = socket.socket()
sock.connect(("127.0.0.1", 8080))
sock.send("hello")
print(socketlib.recvByStr(sock, "0\r\n\r\n"))