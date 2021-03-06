import django.db.models as models


class UserInfo(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    loginstatus = models.CharField(max_length=1)
    class Meta:
        db_table = 't_userinfo'


class ProjectDef(models.Model):
    project = models.CharField(primary_key=True, max_length=6)
    projectname = models.CharField(max_length=20)
    msgtype = models.CharField(max_length=1)
    trancodexpath = models.CharField(max_length=256)
    serialnoxpath = models.CharField(max_length=256)
    class Meta:
        db_table = 't_projectdef'

class ServerDefine(models.Model):
    project = models.CharField(primary_key=True, max_length=6)
    # project = models.OneToOneField(ProjectDef, primary_key=True)
    servtype = models.CharField(max_length=1)
    # maxthread = models.IntegerField(blank=True)
    listenport = models.CharField(max_length=6)
    headlen = models.CharField(max_length=10)
    headinclude = models.CharField(max_length=1)
    class Meta:
        db_table = 't_serverdefine'


class TranMsgMap(models.Model):
    project = models.CharField(max_length=6)
    transcode = models.CharField(max_length=16)
    template = models.CharField(max_length=20)
    userid = models.CharField(max_length=6)
    remark = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    active = models.CharField(max_length=1)
    class Meta:
        db_table = 't_tranmsgmap'

class DataMapDefine(models.Model):
    project = models.CharField(max_length=6)
    datamapid = models.CharField(max_length=10)
    keys = models.CharField(max_length=256)
    values = models.CharField(max_length=256)
    class Meta:
        db_table = 't_datamapdefine'

class DataMap(models.Model):
    project = models.CharField(max_length=6)
    datamapid = models.CharField(max_length=10)
    key1 = models.CharField(max_length=256)
    key2 = models.CharField(max_length=256)
    key3 = models.CharField(max_length=256)
    value1 = models.CharField(max_length=256)
    value2 = models.CharField(max_length=256)
    value3 = models.CharField(max_length=256)
    value4 = models.CharField(max_length=256)
    value5 = models.CharField(max_length=256)
    value6 = models.CharField(max_length=256)
    class Meta:
        db_table = 't_datamap'

class TranLog(models.Model):
    LOG_TYPES=(
        ('1', "HELLO"),
        ('2', "WORLD")
    )
    project = models.CharField(max_length=6)
    serno = models.CharField(max_length=20)
    transcode = models.CharField(max_length=6)
    logtype = models.CharField(max_length=1, choices=LOG_TYPES)
    errormsg = models.CharField(max_length=256)
    class Meta:
        db_table = 't_tranlog'
        unique_together = ("project", "serno")