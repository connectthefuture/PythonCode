import sqlite3
import sys

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
print cursor.execute(sys.argv[1]).fetchall()
conn.commit()