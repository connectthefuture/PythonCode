from django.db import connection

class QueryResult(object):
    def __init__(self):
        self._map = {}
    def __getitem__(self, key):
        return self._map.get(key)
    def __contains__(self, key):
        return key in self._map
    def __setitem__(self, key, val):
        self._map[key] = val

def execute(sql):
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

def select(sql, cols = None):
    cursor = None
    map = QueryResult()
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        zipped = zip(*cursor.fetchall())
        if not zipped:
            map.rownum = 0
        else:
            if cols is None:
                return zipped[0]
            else:
                for i, col in enumerate(cols):
                    map[col] = zipped[i]
                map.rownum = len(zipped[0])
        return map
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()