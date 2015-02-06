#coding=utf8
__author__ = 'ZT-ZH'

import datetime
import os
import time
import csv
import models
import iforms
# import django.db.models.query.RawQuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response, RequestContext
from django.db.models import Q
from iforms import ContactForm, PublisherForm
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.contrib.sessions.models import Session
from ilib import DynamicForm
from django.contrib import auth
from django.contrib.auth.views import login
from django.core.mail import send_mail
from django.db import connection

def testdb(request):
    tmp = u''
    if False:
        userid = request.session[u'ID_USER']
        user = models.UserInfo.objects.get(userid = userid)
        group = user.group
        grouplist = u'(' + u','.join(["'" + group[2 * i: 2 * i + 2] + "'" for i in xrange(len(group) / 2)]) + u')'
        # for u in models.UserInfo.objects.raw('select * from mysite_GroupAuth where groupid in %s and trancode = %s ' % (grouplist, "'thanks'") ):
        #     tmp += u.trancode
        x = len(models.UserInfo.objects.raw('select count(*) as count from mysite_GroupAuth where groupid in %s and trancode = %s ' % (grouplist, "'thanks'") ))
        raise Exception(str(x))
        return render_to_response('test/test1.html', {u'A' : u'', u'B' : u'', u'C' : tmp})
    # user = models.UserInfo.objects.get(userid = u'xx')
    # validgroup = [x.groupid for x in models.GroupAuth.objects.raw("select distinct groupid from mysite_GroupAuth")]
    # models.GroupAuth.objects.all().distinct()
    # return render_to_response('test/test1.html', {u'A' : u'', u'B' : u'', u'C' : str(validgroup)})
    cursor = connection.cursor()
    cursor.execute('select distinct groupid from mysite_GroupAuth')
    for r in cursor.fetchall():
        tmp += r[0]
    cursor.close()
    return render_to_response('test/test1.html', {u'A' : u'', u'B' : u'', u'C' : tmp})