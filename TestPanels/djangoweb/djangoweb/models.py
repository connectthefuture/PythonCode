import django.db.models as models


class UserInfo(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    loginstatus = models.CharField(max_length=1)


class ProjectDef(models.Model):
    project = models.CharField(primary_key=True, max_length=6)
    projectname = models.CharField(max_length=20)
    msgtype = models.CharField(max_length=1)
    trancodexpath = models.CharField(max_length=256)
    serialnoxpath = models.CharField(max_length=256)


class TranMsgMap(models.Model):
    project = models.CharField(max_length=6)
    transcode = models.CharField(max_length=16)
    template = models.CharField(max_length=20)
    userid = models.CharField(max_length=6)
    remark = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    active = models.CharField(max_length=1)

class DataMapDefine(models.Model):
    project = models.CharField(max_length=6)
    transcode = models.CharField(max_length=16)
    datamapid = models.CharField(max_length=10)
    keys = models.CharField(max_length=256)
    values = models.CharField(max_length=256)

class DataMap(models.Model):
    project = models.CharField(max_length=6)
    transcode = models.CharField(max_length=16)
    datamapid = models.CharField(max_length=10)
    key1 = models.CharField(max_length=20)
    key2 = models.CharField(max_length=20)
    key3 = models.CharField(max_length=20)
    value1 = models.CharField(max_length=20)
    value2 = models.CharField(max_length=20)
    value3 = models.CharField(max_length=20)
    value4 = models.CharField(max_length=20)
    value5 = models.CharField(max_length=20)
    value6 = models.CharField(max_length=20)

class TranLog(models.Model):
    project = models.CharField(max_length=6)
    serno = models.CharField(max_length=20)
    transcode = models.CharField(max_length=6)
    errormsg = models.CharField(max_length=256)