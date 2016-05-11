# coding=gbk
# 这是py3程序，注意与py2的兼容
import os

try:
    import cStringIO.StringIO as StringIO
except:
    from io import StringIO
import traceback
import sqlite3
import time, sys
import logutils

_conn = None
_isUnicode = True
_dbType = ""
_logger = None


def connect2Db():
    # db = MySQLdb.connect()
    setup('mysql', db, False)


def setconn(c):
    global _conn
    _conn = c


def setlog(log):
    global _logger
    _logger = log


def getlog():
    global _logger
    return _logger


def setUnicode(u):
    global _isUnicode
    _isUnicode = u


def setup(typ, c, u):
    global _conn, _isUnicode, _dbType
    _conn = c
    _isUnicode = u
    _dbType = typ


def save2db(s):
    return s


def retrivedb(s):
    return s


def getcursor():
    global _conn
    if _dbType == 'mysql':
        try:
            _conn.ping()
        except:
            connect2Db()
        finally:
            return _conn.cursor()
    else:
        return _conn.cursor()


def travelquery(lst, cols):
    '''
            作用： 处理复杂查询函数
            作者：  ZH
    '''
    if len(lst) == 0:
        yield u""
    elif type(lst[0]) is list or type(lst[0]) is tuple:
        yield u'('
        for x in lst:
            for y in travelquery(x, cols):
                yield y
        yield u')'
    else:
        if type(lst) is list or type(lst) is tuple:
            if len(lst) == 4:
                field = lst[3]
            else:
                field = lst[0]
            if lst[2]:
                if type(lst[2]) is str:
                    if lst[1].find('is') >= 0 or lst[1].find('in') >= 0:
                        # yield "(%s %s %s)" % (lst[0], lst[1], lst[2])
                        cols.append(lst[2])
                        if _dbType != 'mysql':
                            yield u"(%s %s ?)" % (lst[0], lst[1],)
                        else:
                            yield u"(%s %s %%s)" % (lst[0], lst[1],)
                    else:
                        cols.append(lst[2])
                        if _dbType != 'mysql':
                            yield u"(%s %s ?)" % (lst[0], lst[1],)
                        else:
                            yield u"(%s %s %%s)" % (lst[0], lst[1],)
                else:
                    cols.append(lst[2])
                    if _dbType != 'mysql':
                        yield u"(%s %s ?)" % (lst[0], lst[1],)
                    else:
                        yield u"(%s %s %%s)" % (lst[0], lst[1],)
            else:
                yield u'(1 = 1)'
        else:
            yield u' %s ' % lst


def select_by_sql(sql):
    global _conn
    cursor = getcursor()
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            return [2, "", None]
        return [1, "", rows]
    except Exception as e:
        return [0, "", None]
    finally:
        cursor.close()


def select(columns, conditions, table, returnTyp=0, extra='', encoding=None):
    global _conn
    cursor = getcursor()
    try:
        sio = StringIO()
        cols = []
        for i in travelquery(conditions, cols):
            sio.write(i)
        conditionsql = sio.getvalue()
        sio.close()
        if not conditionsql:
            pass
        sql = 'select %s from %s %s %s' % (
            ','.join(columns), table, 'where ' + conditionsql if conditionsql else '', extra)
        if _logger:
            _logger.info(sql)
        if _dbType != 'mysql':
            cursor.execute(sql, cols)
        else:
            cursor.execute(sql, cols)
        description = [i[0].lower() for i in cursor.description]
        rows = cursor.fetchall()
        if len(rows) > 0 and encoding:
            rows = [[rows[x][y].encode(encoding) for y in range(len(rows[0]))] for x in range(len(rows))]
        if len(rows) == 0:
            return [2, "", cursor.rowcount, None]
        if returnTyp == 0:
            zipped = zip(*rows)
            result = dict()
            colnames = [j for i, j in enumerate(description)]
            x = 0
            for z in zipped:
                result[colnames[x]] = z
                x += 1
            return [1, "", cursor.rowcount, result]
        else:
            return [1, "", cursor.rowcount, rows]
    except Exception as e:
        print(traceback.format_exc())
        return [0, "", None, None]
    finally:
        cursor.close()


def update(values, conditions, table, commitFlag=True):
    global _conn
    cursor = getcursor()
    try:

        updsql = ','.join(
            ['set %s = %s' % (k, "'%s'" % save2db(v).replace("'", "''") if type(v) is str else str(v))
             for
             k, v in values])
        sio = StringIO()
        cols = []
        for i in travelquery(conditions, cols):
            sio.write(i)
        conditionsql = sio.getvalue()
        sio.close()
        sql = "update %s %s where %s" % (table, updsql, conditionsql)
        print(sql)
        if _dbType != 'mysql':
            cursor.execute(sql, cols)
        else:
            cursor.execute(sql, cols)
        if commitFlag:
            _conn.commit()
        return [1, "", cursor.rowcount, None]
    except Exception as e:
        print(traceback.format_exc())
        return [0, "", cursor.rowcount, None]
    finally:
        cursor.close()


def insert(values, table, commitFlag=True):
    global _conn
    cursor = getcursor()
    try:
        keysql = ",".join([i[0] for i in values])
        valuesql = ','.join(["'%s'" % v if type(v) is str else str(v) for k, v in values])
        sql = "insert into %s (%s) values (%s)" % (table, keysql, valuesql,)
        if _logger:
            _logger.info(sql)
        cursor.execute(sql)
        if commitFlag:
            _conn.commit()
        return [1, "", cursor.rowcount, None]
    except Exception as e:
        _logger.error(traceback.format_exc())
        return [0, "", None, None]
    finally:
        cursor.close()


def commit():
    global _conn
    _conn.commit()


def rollback():
    global _conn
    _conn.rollback()


def execute(sql, commitFlag=True):
    global _conn
    if _logger:
        _logger.info(sql)
    try:
        cursor = None
        cursor = getcursor()
        cursor.execute(sql)
        return [1, "", cursor.rowcount, cursor.fetchall()]
    except Exception as e:
        print(e)
        return [0, "", cursor.rowcount, None]
    finally:
        if cursor:
            cursor.close()
        if commitFlag:
            _conn.commit()
            pass


def gbk2utf8(s):
    return s.decode('gbk').encode('utf8')


if __name__ == '__main__':
    dbpath = "E:\\PycharmProjects\\PythonCode\\RunTmp\\sqlite3.db"

    db = sqlite3.connect(dbpath)
    cursor = db.cursor()
    # cursor.execute("select * from t_abc")
    setup('sqlite3', db, False)
    # execute("create table t_abs (a int, b char(10))")
    result = execute("insert into t_abs values(1, '中国')", True)
    cursor.execute("SELECT * FROM t_abs WHERE a = ?", [1])
    print(cursor.fetchall())
    # print(result)
    result = select(["*"], [['a', '=', 1]], "t_abs", 0)
    print(result)
    result = update([["a", 100]], [["a", "=", "1"]], "t_abs")
    print(result)
    result = select(["*"], [], "t_abs", 0)
    print(result)
