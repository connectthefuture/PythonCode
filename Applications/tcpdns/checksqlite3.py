import sqlite3
import time
import database

conn = sqlite3.connect("dns.db")
database.setup('sqlite3', conn, False)
database.execute("create table keyvalue (key varchar(10) PRIMARY key, value varchar(128))")
if 0:
    for i in xrange(1000000):
        database.insert([['key', str(i).rjust(10, '0')], ['value', str(i).rjust(10, '0')]], "keyvalue", False)
        if i % 5000 == 0:
            conn.commit()
else:
    for i in xrange(10000, 20000):
        t1 = time.time()
        result = database.select(["count(1)"], [["key", "=", str(i).rjust(10, '0')]], "keyvalue", 1)
        t2 = time.time()
        print(t2 - t1)

