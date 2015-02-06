import models
import dbutils

def isbitset():
    pass

def checkAuth(request, trancode):
    userid = request.session[u'ID_USER']
    user = models.UserInfo.objects.get(userid = userid)
    group = user.group
    grouplist = u'(' + u','.join(["'" + group[2 * i: 2 * i + 2] + "'" for i in xrange(len(group) / 2)]) + u')'
    result = False
    sql = 'select trancode from mysite_GroupAuth where groupid in %s and trancode = %s ' % (grouplist, "'%s'" % trancode)
    queryset = dbutils.select(sql)
    if queryset.rownum > 0:
        result = True
    return result
