# coding=utf-8
from __future__ import unicode_literals
import datetime
from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render_to_response
import logging
import models
import os
import toolutils
from toolutils import needlogin
from views import render_to_response
import base
from base import render_to_response
from django.db import connection

logger = base.logger


def requesttest(request):
    url = request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
    logger.debug(url)
    return HttpResponse(request.build_absolute_uri())


def modeltest(request):
    queryset = models.ProjectDef.objects.raw(
        "select project, project || msgtype  from djangoweb_projectdef where project = %s", ['dsdf'])
    i = 0
    for q in queryset:
        pass
    return HttpResponse(q.get('project'))


def rawsql(request):
    cursor = connection.cursor()
    cursor.execute("select project, project || msgtype as a  from djangoweb_projectdef where project = %s", ['dsdf'])
    desc = cursor.description
    row = cursor.fetchone()
    # t = models.TranLog(project='dsdf', serno='1000', transcode='1000', errormsg='haha', logtype='1')
    # t.save()
    t = models.TranLog.objects.get(project='dsdf', serno='1000')
    t.errormsg = 'Hello'
    t.save(update_fields=['errormsg'])
    t = models.TranLog.objects.get(project='dsdf', serno='1000')
    return HttpResponse(t.errormsg)
