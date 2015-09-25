#!/home/afa/python/bin/python
import time, os, sys, _db2
sys.path.append('/home/afa/workspace/PyDll')

def connect2db():
    conn = _db2.connect('afa', 'afa', 'afa')
    return conn

_conn = connect2db()

def execsql(sql):
    cursor = _conn.cursor()
    cursor.execute(sql)
    result = []
    while 1:
        data = cursor.fetch()
        if data:
            result.append(data)
        else:
            break
    return [[i[0].lower() for i in cursor.description], result]

if __name__ == '__main__':
    try:
        sql = sys.argv[1]
        result = execsql(sql)
        maxlen = max((len(i) for i in result[0]))
        for i in xrange(len(result[1])):
            for j, k in enumerate(result[0]):
                #print("%s: %s" %(k.ljust(maxlen, ' '), str(result[1][i][j])))
                print("%s: %s" %(k.ljust(maxlen, ' '), result[1][i][j]))
            print("")
    finally:
        _conn.close()
