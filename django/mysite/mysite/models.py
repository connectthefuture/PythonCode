#coding=utf8
# from django.db import connection
import django.db.models as models

_tabledesc = ['Publisher', 'Author', 'Book', 'NewThing', 'UserInfo', 'AuthCode', 'GroupAuth', 'TestTable', 'Vocabulary']

class Publisher(models.Model):
    # _fielddesc = ['name', 'address', 'city', 'state_province', 'country', 'website']
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __str__(self):
        return 'Publisher : %s' % self.name

    class Meta:
        ordering = ['name']


class Author(models.Model):
    salutation = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    #headshot = models.ImageField(upload_to='/tmp')

    def __str__(self):
        return 'Author : %s %s' %(self.first_name, self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()

    def __str__(self):
        return 'Book : %s' % self.title


class Member(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class NewThing(models.Model):
    time = models.CharField(max_length=14)
    userid = models.CharField(max_length=8)


# 角色权限管理

class UserInfo(models.Model):
    userid = models.CharField(max_length=14, primary_key = True)
    group = models.CharField(max_length=40)
    class Meta:
        unique_together = [("userid",)]

class AuthCode(models.Model):
    trancode = models.CharField(max_length=10, primary_key = True)
    tranname = models.CharField(max_length=60)

class GroupAuth(models.Model):
    groupid = models.CharField(max_length=2, )
    trancode = models.CharField(max_length=10)


# 订票系统
class station(models.Model):
    station = models.CharField(max_length=20)
    stationname = models.CharField(max_length=60)
    citycode = models.CharField(max_length=6)

class TestTable(models.Model):
    a = models.CharField(max_length=10)
    b = models.CharField(max_length=10)

    class Mata:
        unique_together = [('a', 'b')]


# 字典
class Vocabulary(models.Model):
    index = models.CharField(max_length=6, primary_key=True)
    word = models.CharField(max_length=30)
    explain = models.CharField(max_length=256)
    level = models.CharField(max_length=1)
    modifydate = models.CharField(max_length=8)
    modifytime = models.CharField(max_length=6)
    # 0 同步 1 服务器更新 2 本地更新
    status = models.CharField(max_length=1)

class VocalRecord(models.Model):
    date = models.CharField(max_length=8)
    index = models.CharField(max_length=6)


class ChinaDaily(models.Model):
    idx = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,)
    content = models.TextField()
    pubdate = models.CharField(max_length=20)
    category = models.CharField(max_length=30)
    status = models.CharField(max_length=1)


class Words(models.Model):
    idx = models.AutoField(primary_key=True)
    word = models.CharField(max_length=30)
    translate = models.CharField(max_length=512)



