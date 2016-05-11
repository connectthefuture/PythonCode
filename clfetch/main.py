import asyncio
import traceback
from bs4 import BeautifulSoup
import os, sqlite3, sys
import aiohttp
import re
from copy import deepcopy

RunTmp = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'RunTmp')
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'libs'))
import database
import logutils

logger = logutils.getlogger("clfetch", "S")
database.setlog(logger)

dbcon = sqlite3.connect(os.path.join(RunTmp, "sqlite3.db"))
database.setup('sqlite3', dbcon, False)
CLURL = 'http://cc.ttum.pw/'
SAVEPATH = 'E:\\HenTai\\CaoLiu'
# database.execute("drop table t_caoliu")
# database.execute("create table t_caoliu (url varchar(256) primary key, title varchar(256), status char(6))", True)
# result = database.select(["*"], [], "t_caoliu", 0)
# print(result)
asyncq = asyncio.Queue()
asyncq.qsize()
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

def geturltyp(url):
    pass


@asyncio.coroutine
def fetchcontent(url):
    logger.info(url)
    headers = {'User-Agent': 'Opera/9.80 (Windows NT 6.1; WOW64; U; de) Presto/2.10.289 Version/12.01',
               'Accept-Language': 'zh-CN', 'Connection': 'Close',
               'Accept': 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1'}
    # response = yield from aiohttp.get('http://cc.ttum.pw/thread0806.php?fid=8&search=&page=2', headers=headers)
    response = yield from aiohttp.get(url, headers=headers)
    body = yield from response.read_and_close(decode=False)
    soup = BeautifulSoup(body.decode('gbk'), 'html.parser')
    return soup


@asyncio.coroutine
def fetchurl(url):
    baseurl = 'http://cc.ttum.pw/'
    # if not url.startswith('http:') and not url.startswith('https:'):
    #     url = 'http://' + url
    url = baseurl + url
    soup = fetchcontent(url)
    tbody = soup.findAll('tbody')
    for t in tbody:
        for a in t.findAll('a', {'target': '_blank', 'id': ''}):
            try:
                href = a.attrs['href']
                title = str(a.contents[0])
                if title[:3] == '.::':
                    continue
                if href.startswith('htm_data/8/1509/'):
                    i = href[16:-5]
                    result = database.insert([['url', href], ['status', '099999'], ['title', title]], 't_caoliu')
                    logger.debug(result)
                    task = {'tasktype': '1', 'url': href, 'title': title}
            except:
                logger.error(traceback.format_exc())


@asyncio.coroutine
def dispatchjob():
    result = database.select(['*'], ['substr(status, 1, 1)', '=', '0'], 't_caoliu', 0, 'order by url')
    caoliu = result[3]
    for i in range(1, 101):
        print(caoliu['url'][i - 1])
        asyncio.ensure_future(fetchimg(caoliu['url'][i - 1]))
        if i % 10 == 0:
            yield from asyncio.sleep(30)

@asyncio.coroutine
def downimg(url, savepath):
    try:
        headers = {'User-Agent': 'Opera/9.80 (Windows NT 6.1; WOW64; U; de) Presto/2.10.289 Version/12.01',
                   'Accept-Language': 'zh-CN', 'Connection': 'Close',
                   'Accept': 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1'}
        # response = yield from aiohttp.get('http://cc.ttum.pw/thread0806.php?fid=8&search=&page=2', headers=headers)
        response = yield from aiohttp.get(url, headers=headers)
        body = yield from response.read_and_close(decode=False)
        filename = os.path.basename(url)
        with open(os.path.join(savepath, filename), 'wb') as fd:
            fd.write(body)
    except Exception as e:
        logger.info(url)
        logger.error(traceback.format_exc())
        raise e

@asyncio.coroutine
def fetchimg(url):
    global CLURL
    try:
        imgid = re.search('\/(\d+).html$', url).group(1)
        result = database.select(['*'], [['url', '=', url]], 't_caoliu')
        urlinfo = result[3]
        status = urlinfo['status'][0]
        if status[0] == '1' or status[1] == 'P':
            return
        database.execute("update t_caoliu set status = '%s' where url='%s'" % ('0P' + status[2:], url))
        requesturl = CLURL + url
        asoup = yield from fetchcontent(requesturl)
        div = asoup.find('div', {'class': 'tpc_content do_not_catch'})
        for i in div.findAll('input', {'type': 'image'}):
            savepath = os.path.join(SAVEPATH, imgid)
            logger.info("save %s to %s" %(i.attrs['src'], savepath))
            try:
                os.mkdir(savepath)
            except FileExistsError:
                pass
            except Exception as e:
                raise e
            yield from asyncio.sleep(2)
            # asyncio.ensure_future(downimg(i.attrs['src'], savepath))
            yield from downimg(i.attrs['src'], savepath)
        database.execute("update t_caoliu set status = '%s' where url='%s'" % ('1F' + status[2:], url))
    except:
        logger.error(traceback.format_exc())
        database.execute("update t_caoliu set status = '%s' where url = '%s'" % ('0F' + status[2:], url))
    finally:
        pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if 0:
        tasks = [fetchurl('thread0806.php?fid=8&search=&page=%d' % i) for i in range(10)]
        loop.run_until_complete(asyncio.wait(tasks))
    else:
        tasks = [dispatchjob()]
        # tasks = [downimg('http://img02.cweb-pix.com/images/2015/09/25/cef18d2e343bdf061629e93122afb290.jpg', 'D:/')]
        loop.run_until_complete(asyncio.wait(tasks))
    loop.run_forever()
