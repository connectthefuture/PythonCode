import httplib
import urllib

conn = httplib.HTTPConnection("192.168.1.101:8090")
data = urllib.urlencode({"cust_name": "tom1", "id_type": "1", "id_no": "33333"})
print data
headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
# data = {"cust_name": "tom", "id_type": "1", "id_no": "123123"}
conn.request(method="POST", url="/module/addPerson", body=data, headers=headers)
response = conn.getresponse()
res = response.read()
print res
