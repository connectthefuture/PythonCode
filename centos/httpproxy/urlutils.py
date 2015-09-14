import socket
import re

def resolveurl(domain):
    return socket.gethostbyname_ex(domain)[2]

def islegalurl(url):
    bool = re.search('\d+\.\d+\.\d+\.', url)
    return True if not bool is None else False
