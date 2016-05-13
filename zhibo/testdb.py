import pymysql
import jinja2

conn = pymysql.connect(host='192.168.31.241', user='root', passwd='root', db='test', charset='utf8')
cursor = conn.cursor()
cursor.execute("select * from t_users")
print(cursor.fetchall())
