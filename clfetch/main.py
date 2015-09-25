import asyncio
from bs4 import BeautifulSoup
from urllib.request import Request
import urllib
import urllib.request
import os, sqlite3, sys
import aiohttp

RunTmp = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'RunTmp')
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'libs'))
import database
dbcon = sqlite3.connect(os.path.join(RunTmp, "sqlite3.db"))
database.setup('sqlite3', dbcon, False)
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
# req = urllib.request.Request(url='http://cc.ttum.pw/thread0806.php?fid=8&search=&page=2', headers=headers)

# with open('a.html', 'w') as fd:
# fd.write(urllib.request.urlopen(req).read().decode('gbk'))

@asyncio.coroutine
def fetchurl(url):
    headers = {'User-Agent': 'Opera/9.80 (Windows NT 6.1; WOW64; U; de) Presto/2.10.289 Version/12.01',
               'Accept-Language': 'zh-CN', 'Connection': 'Close',
               'Accept': 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1'}
    # response = yield from aiohttp.get('http://cc.ttum.pw/thread0806.php?fid=8&search=&page=2', headers=headers)
    response = yield from aiohttp.get(url, headers=headers)
    body = yield from response.read_and_close(decode=False)
    soup = BeautifulSoup(body.decode('gbk'), 'html.parser')
    tbody = soup.findAll('tbody')
    for t in tbody:
        for a in t.findAll('a'):
            print(a)

loop = asyncio.get_event_loop()
q.put()
loop.run_forever()