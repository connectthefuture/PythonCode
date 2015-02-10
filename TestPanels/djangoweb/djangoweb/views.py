# coding=utf-8
from __future__ import unicode_literals
# import time
# import csv
# import json
# from xml.etree import ElementTree
# from django.template import Template
# from django.template.loader import get_template
# from django.db.models import Q
# from django.core.context_processors import csrf
# from django.contrib.auth.views import login
# from django.core.mail import send_mail
# from django.template import loader, Context, RequestContext
import datetime
from django.http import HttpResponse, HttpResponseRedirect
import models
import os
import toolutils
from toolutils import needlogin
import base
from base import render_to_response

logger = base.logger

_STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')


def login(request):
    if request.method == "GET":
        # 如果已经登录
        if not request.session.get('UserName') is None:
            return HttpResponseRedirect('/project')
        else:
            return render_to_response('public/hello.html', {})
    else:
        kv = dict(request.POST.items())
        username = kv['UserName']
        queryset = models.UserInfo.objects.filter(username=username)
        if not queryset:
            o = models.UserInfo(username=username)
            o.save()
            queryset = models.UserInfo.objects.filter(username=username)
        u = queryset[0]
        logger.debug('username=%s, userid=%s' % (u.username, u.userid))
        request.session['UserName'] = u.username
        request.session['UserId'] = u.userid
        return HttpResponseRedirect('/project')


def logout(request):
    if not request.session.get('UserName') is None:
        del request.session['UserName']
        del request.session['UserId']
    return HttpResponseRedirect('/login')


@needlogin
def projectlist(request):
    c = {}
    c['fielddesc'] = ['项目代码', '项目名称', '报文类型', '交易码XPATH', '流水号XPATH']
    c['fields'] = ['project', 'projectname', 'msgtype', 'trancodexpath', 'serialnoxpath']
    queryset = models.ProjectDef.objects.all()
    rows = [[getattr(q, field) for field in c['fields']] for q in queryset]
    c['queryset'] = rows
    return render_to_response('transaction/projectlist.html', c)


def addproject(request):
    if request.method == 'POST':
        logger.debug(str(request.POST))
        kv = dict(request.POST.items())
        project = kv['project']
        projectname = kv['projectname']
        msgtype = kv['msgtype']
        trancodexpath = kv['trancodexpath']
        serialnoxpath = kv['serialnoxpath']
        o = models.ProjectDef(project=project.lower(), projectname=projectname, msgtype=msgtype,
                              trancodexpath=trancodexpath, serialnoxpath=serialnoxpath)
        o.save()
        return HttpResponseRedirect('/project/')


@needlogin
def transaction(request, project):
    c = {}
    c['fielddesc'] = ['交易代码', '交易模板', '模板说明', '激活状态', '报文']
    c['fields'] = ['transcode', 'template', 'remark', 'active']
    c['project'] = project
    queryset = models.TranMsgMap.objects.filter(project=project).order_by('transcode', 'template', )
    rows = [[getattr(q, field) for field in c['fields']] for q in queryset]
    for row in rows:
        row[-1] = '激活' if row[-1] == '1' else '未激活'
        row.append('/project/%s/%s/%s/' % (project, row[0], row[1]))
    c['queryset'] = rows
    return render_to_response('transaction/transaction.html', c)


def makefile(fname):
    with open(fname, 'a') as fd:
        fd.close()


def addtranscode(request, ):
    if request.method == 'POST':
        kv = dict(request.POST.items())
        opertype = kv['opertype']
        project = kv['project']
        template = kv['template']
        # 新增报文模板
        if opertype == '1':
            filedir = os.path.join(_STATIC_DIR, "messages")
            filepath = os.path.join(filedir, "%s_%s_%s.html" % (project, kv['transcode'], template))
            makefile(filepath)
            t = models.TranMsgMap.objects.filter(project=project, transcode=kv['transcode'], template=kv['template'])
            if not t:
                o = models.TranMsgMap(project=project, transcode=kv['transcode'], userid=request.session['UserId'],
                                      remark=kv['remark'], template=kv['template'], timestamp=datetime.datetime.now())
                o.save()
        elif opertype == '2':
            queryset = models.TranMsgMap.objects.filter(project=project, transcode=kv['transcode'], template=template)
            for q in queryset:
                q.delete()
        elif opertype == '3':
            queryset = models.TranMsgMap.objects.filter(project=project, transcode=kv['transcode'], )
            for q in queryset:
                if q.template == template:
                    q.active = '1'
                    q.save()
                else:
                    q.active = '0'
                    q.save()
        return HttpResponseRedirect('/project/%s/' % project)


def xmlservice(request, project):
    ctx = toolutils.TradeContext(project, request.body)
    ctx.execute()
    # 得到模板，传入目标容器
    if ctx.config.msgtype == '1':
        return render_to_response(ctx.template, ctx.map2tmplate, mimetype='application/xml')


def bootstrap(request):
    return render_to_response('bootstrap/1.html', {'a': u'这个'})


def readfile(fname):
    with open(fname, "rb") as fd:
        return fd.read()


@needlogin
def transconfig(request, project, transcode):
    c = {}
    c['project'] = project
    c['transcode'] = transcode
    sourcedir = os.path.join(os.path.dirname(__file__), 'transconfig')
    fname = os.path.join(sourcedir, "%s_%s.py" % (project, transcode))
    if os.path.exists(fname):
        c['pysourcecode'] = readfile(fname)
    return render_to_response('transaction/transconfig.html', c)


def addtransconfig(request):
    sourcedir = os.path.join(os.path.dirname(__file__), 'transconfig')
    kv = dict(request.POST.items())
    logger.debug(str(kv))
    fname = os.path.join(sourcedir, "%s_%s.py" % (kv['project'], kv['transcode']), )
    logger.debug(fname)
    with open(fname, 'w') as fd:
        fd.write(kv['pysourcecode'].replace("\r", ""))
    return HttpResponseRedirect("/project/%s/%s/" % (kv['project'], kv['transcode']))


def datamaplist(request, ):
    pass


@needlogin
def templateconfig(request, project, transcode, template):
    c = {}
    c['project'] = project
    c['transcode'] = transcode
    c['template'] = template
    templatedir = os.path.join(os.path.dirname(__file__), 'transconfig')
    fname = os.path.join(templatedir, "%s_%s_%s.html" % (project, transcode, template))
    if os.path.exists(fname):
        c['pysourcecode'] = readfile(fname)
    return render_to_response('transaction/templateconfig.html', c)


def addtemplate(request):
    if request.method == 'POST':
        kv = dict(request.POST.items())
        templatedir = os.path.join(os.path.dirname(__file__), 'transconfig')
        fname = os.path.join(templatedir, "%s_%s_%s.html" % (kv['project'], kv['transcode'], kv['template']))
        with open(fname, 'w') as fd:
            fd.write(kv['templatecontent'].replace("\r", ""))
        return HttpResponseRedirect("/project/%s/%s/%s/" % (kv['project'], kv['transcode'], kv['template']))