import asyncio
from bs4 import BeautifulSoup
from urllib.request import Request
import urllib
import urllib.request
import os, sqlite3, sys

RunTmp = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'RunTmp')
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'libs'))
import database
# dbcon = sqlite3.connect(os.path.join(RunTmp, "db.sqlite3"))

a = [[1,2,], [3,4]]
zipped = zip(a)
for i in zipped:
    print(i)

q = asyncio.Queue()
q.put_nowait(1)
q.put_nowait(2)
# while 1:
#     try:
#         i = q.get()
#     except asyncio.queues.QueueEmpty:
#         break

# response = urllib.request.urlopen('http://python.org/')
# req = Request('http://cc.ttum.pw/thread0806.php?fid=8')
# response = urllib.request.urlopen('http://cc.ttum.pw/thread0806.php?fid=8')
# soup = BeautifulSoup(response.read(), 'html.parser')
# print()