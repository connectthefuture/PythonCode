#!/home/afa/python/bin/python
# coding=gbk
import ConfigParser
import traceback
import logging
import _db2
import time
import datetime
import re
import os
import logging
import logging.handlers
import sys


def getlogger(filename, level=logging.DEBUG, hdlr=None, formatter=None):
    logging.setLoggerClass(logging.Logger)
    logger = logging.getLogger(filename)
    if not hdlr:
        hdlr = logging.handlers.RotatingFileHandler(filename, maxBytes=5 * 1024 * 1024,
                                                    backupCount=2)
    if not formatter:
        formatter = logging.Formatter('[%(asctime)s %(filename)15s %(lineno)4d %(levelname)8s]: [%(message)s]')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(level)
    return logger


logger = getlogger("/home/afa/log/backup2his.log")

MAXSELECTROW = 5000
SAVETBLPATH = os.path.join(os.getenv('HOME'), 'backupdb')
logger.debug(SAVETBLPATH)
if not os.path.exists(SAVETBLPATH):
    os.mkdir(SAVETBLPATH)

DBC = {'afa': {'db': 'afa', 'user': 'afa', 'password': 'afa', 'connection': None}
}

FAILED = []


def calcdate(offset, date=''):
    if date == '':
        date = time.strftime('%Y%m%d')
    if offset[0] == 'd':
        if offset[1] == '-':
            delta = datetime.timedelta(days=int(offset[2:]) * -1)
        else:
            delta = datetime.timedelta(days=int(offset[2:]))
        dt = datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:8])) + delta
        return "%04d%02d%02d" % (dt.year, dt.month, dt.day)
    elif offset[0] == 'm':
        year, month, day = int(date[:4]), int(date[4:6]), int(date[6:8])
        if offset[1] == '-':
            delta = int(offset[2:])
            m, n = divmod(delta, 12)
            return "%04d%02d%02d" % (year - m, month - n, day)
        else:
            delta = int(offset[2:])
            m, n = divmod(delta, 12)
            return "%04d%02d%02d" % (year + m, month + n, day)


def checkrun(mp):
    logger.info(mp['runtime'])
    day, month = re.split('\s+', mp['runtime'].strip())
    t = time.strftime('%Y%m%d')
    d = int(t[6:8])
    m = int(t[4:6])
    if day == '*':
        if month == '*' or m == int(month):
            return True
    else:
        if day == int(d):
            if month == '*' or m == int(month):
                return True
    return False


def gettblcols(db, table):
    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute("select * from %s fetch first 1 rows only" % table)
        return [i[0].lower() for i in cursor.description]
    finally:
        if cursor: cursor.close()


def execsql(db, sql):
    try:
        logger.info(sql)
        cursor = None
        cursor = db.cursor()
        cursor.execute(sql)
        logger.info("影响%d条数据" % cursor.rowcount)
        db.commit()
        return cursor.rowcount
    finally:
        cursor.close()


def select(db, sql):
    try:
        logger.info(sql)
        cursor = None
        cursor = db.cursor()
        cursor.execute(sql)
        result = []
        while 1:
            row = cursor.fetch()
            if not row:
                break
            result.append(row)
        return result
    finally:
        cursor.close()


def commit(db):
    db.commit()


def rollback(db):
    db.rollback()


def save2tbl(cfg, table):
    global DBC, FAILED
    try:
        logger.info("开始处理表%s" % table)
        d = dict(cfg.items(table))
        loc = locals()
        exec (d['pysrc'])
        var = [loc[i] for i in d['sqlvars'].split(',')]
        if not DBC[d['db']]['connection']:
            DBC[d['db']]['connection'] = _db2.connect(DBC[d['db']]['db'], DBC[d['db']]['user'],
                                                      DBC[d['db']]['password'])
        cols = ','.join(gettblcols(DBC[d['db']]['connection'], d['table']))
        var.insert(0, cols)
        d['sql'] = d['sql'].lower()
        r = re.search('\s*select\s+%s\s+', d['sql']).group()
        countsql = (r.replace('%s', 'count(*)') + d['sql'][len(r):]) % tuple(var[1:])
        selectsql = d['sql'] % tuple(var)
        if not checkrun(d):
            logger.info("表%s未到执行日期" % d['table'])
            return
        count = select(DBC[d['db']]['connection'], countsql)[0][0]
        deletesql = 'delete from %s ' % d['table'] + selectsql[selectsql.find(' where '):]
        if count == 0:
            logger.info("表%s查询无需清理记录" % (d['table']))
        elif count <= MAXSELECTROW:
            insertsql = 'insert into %s (%s) ' % (d['histable'], cols) + selectsql
            try:
                logger.info("插入历史表%s，共需插入%d条数据" % (d['table'], count))
                rc = execsql(DBC[d['db']]['connection'], insertsql)
                if rc == count:
                    logger.info("删除原始表%s" % (d['table'],))
                    rc = execsql(DBC[d['db']]['connection'], deletesql)
                    if rc == count:
                        logger.info("提交表%s" % (d['table'], ))
                        commit(DBC[d['db']]['connection'])
                        logger.info("执行成功表%s" % (d['table'], ))
                    else:
                        raise Exception("")
                else:
                    raise Exception("")
            except Exception as e1:
                logger.error("执行表%s失败" % (d['table'], ))
                rollback(DBC[d['db']]['connection'])
                FAILED.append(table)
                logger.error(traceback.format_exc())
            finally:
                # rollback(DBC[d['db']]['connection'])
                pass
        else:
            if 1:
                t = int(time.time())
                backupfile = '%s_%d.del' % (table, t)
                backuppathfile = os.path.join(SAVETBLPATH, backupfile)
                exportsql = "export to %s of del %s" % (backuppathfile, selectsql)
                importsql = "import from %s of del %s" % (backuppathfile, "insert into %s" % d['histable'])
                logger.debug(exportsql)
                os.system('/home/afa/tbin/sql "%s"' % exportsql)
                os.system('/home/afa/tbin/sql "%s"' % importsql)
                execsql(DBC[d['db']]['connection'], deletesql)
                commit(DBC[d['db']]['connection'])
    except Exception as e:
        logger.error(traceback.format_exc())
    finally:
        pass


def backup2his(table, typ, **kwargs):
    pass


if __name__ == '__main__':
    cp = ConfigParser.ConfigParser()
    cfgdir = os.path.join(os.getenv('HOME'), 'workspace/cfg')
    cp.read(os.path.join(cfgdir, 'backup2his.ini'))
    sections = cp.sections()
    if sys.argv[1] == 'run':
        for sec in sections:
            save2tbl(cp, sec)
        if FAILED:
            time.sleep(60)
            for sec in FAILED:
                save2tbl(cp, sec)
    elif sys.argv[1] == 'check':
        for table in sections:
            d = dict(cp.items(table))
            loc = locals()
            exec (d['pysrc'])
            var = [loc[i] for i in d['sqlvars'].split(',')]
            checkrun(d)