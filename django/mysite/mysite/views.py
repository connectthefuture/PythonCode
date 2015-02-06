# coding=utf8
import datetime
import time
import csv
import json
from xml.etree import ElementTree
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.db.models import Q
from django.core.context_processors import csrf
from django.contrib.auth.views import login
from django.core.mail import send_mail
from django.template import loader, Context, RequestContext
import models
import iforms
import errorutils
import checkutil
import StringIO
import urllib2
import BeautifulSoup
import logging
from iforms import ContactForm, UserForm
from models import ChinaDaily, Words

# from django.views.decorators.csrf import csrf_protect
# from django.contrib.sessions.models import Session
# from ilib import DynamicForm


def custom_proc(request):
    "A context processor that provides 'app', 'user' and 'ip_address'."
    return {'app': 'My app',
            'user': request.user,
            'ip_address': request.META['REMOTE_ADDR']
    }


def current_datetime(request):
    now = datetime.datetime.now()
    # return HttpResponse(html)


def hours_ahead(request, offset):
    # now = datetime.datetime.now()
    # offset = int(offset)
    # dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    t = Template("My Name is {{ name }}")
    c = Context({"name": "hello"})
    t.render(c)
    return HttpResponse(t.render(c))


class TemplateTest:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def modify(self):
        # print(getattr(self, x))
        # self.__dict__[x] = y
        self.a = 0
        self.b = 0

    def error(self):
        raise TemplateError("silent_variable_failure")

    modify.alters_data = True  # 如果有该属性，该方法在模板里就无法直接调用，重要的方法应该设置该属性


class TemplateError(Exception):
    # 设置了 silent_variable_failure属性为True后，如果模板中调用失败也不会抛异常
    silent_variable_failure = False


def template1(request):
    if 1:
        t = get_template('time.html')
        tt = TemplateTest(1, 2)
        person = {'name': 'Sally', 'age': '43', 'escape': '<>&"'}
        html = t.render(Context({'tag': '12345678901234567890', 'tt': tt, 'person': person}))
        return HttpResponse(html)
    else:
        # why problem
        return render_to_response('time.html', {'tag', 'tag'})


def testmodels(request, ):
    return HttpResponse('testmodels succ')


def publisher(request):
    return HttpResponse(request.GET.get('q'))


def publisher1(request, obj):
    return HttpResponse(request.GET.get('q'))
    pass


def searchbook(request, item):
    # query = request.GET.get('q', '')
    query = item
    if query:
        qset = (Q(title__icontains=query)
                | Q(authors__first_name__icontains=query)
                | Q(authors__last_name__icontains=query))
        results = models.Book.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("books/searchbook.html", {"results": results, "query": query})


def addbook(request, item):
    pass


def csvtest(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=unruly.csv'
    writer = csv.writer(response)
    writer.writerow(['Year', 'Unruly Airline Passengers'])
    UNRULY_PASSENGERS = [146, 184, 235, 200, 226, 251, 299, 273, 281, 304, 203]
    for (year, num) in zip(xrange(1995, 2006), UNRULY_PASSENGERS):
        writer.writerow([year, num])
    return response


# @csrf_protect
def contact(request):
    if request.method == 'GET':
        form = ContactForm()
        c = {'form': form}
        c.update(csrf(request))
        return render_to_response('contact.html', c)
    elif request.method == 'POST':
        # assert False
        # raise Exception(str(request.POST.items()))
        form = ContactForm(request.POST)
        try:
            if form.is_valid():
                topic = form.cleaned_data['topic']
                message = form.cleaned_data['message']
                sender = form.cleaned_data.get('sender', 'noreply@example.com')
                send_mail('Feedback from your site, topic: %s' % topic, message, sender, ['administrator@example.com'])
                return HttpResponseRedirect('/thanks')
            else:
                raise Exception('not valid input')
        except Exception as e:
            pass
        finally:
            return errorutils.error('000001', e.message, '')
            # return render_to_response('public/error.html', {'errorcode' : '000001', 'errormsg' : e.message})
            # return HttpResponseRedirect('/thanks')


def image(request):
    with open("C:/Users/zt-zh/desktop/Chrysanthemum.jpg", "rb") as fd:
        return HttpResponse(fd.read(), mimetype="image/jpg")


def now(request):
    current_datetime = time.strftime('%Y%m%d')
    raise Exception(request.session[u'nowtime'])
    return render_to_response('current_datetime.html', {'current_datetime': current_datetime})


def initdata(request, table):
    if request.method == 'GET':
        if not table in models._tabledesc:
            return render_to_response('public/error.html', {'errorcode': '999999', 'errormsg': u'不存在的表[%s]' % table})
        form_class = getattr(iforms, table + u'Form')
        form = form_class()
        c = {'form': form, 'posturl': u'./%s' % table, 'ID_USER': request.session.get('ID_USER', '')}
        c.update(csrf(request))
        return render_to_response('public/db_initdata.html', c)
    elif request.method == 'POST':
        form_class = getattr(iforms, table + u'Form')
        form = form_class(request.POST)
        form.is_valid()
        try:
            form.clean_message()
        except iforms.FormException as e:
            return render_to_response('public/error.html', {'errorcode': 'FORM9999', 'errormsg': e.message})
        except AttributeError as e:
            pass
        kv = dict(request.POST.items())
        map = dict((i, kv[i]) for i in kv)
        del map['csrfmiddlewaretoken']  # 必须要清除掉这个字段
        model_class = getattr(models, table)
        obj = apply(model_class, [], map)
        obj.save()
        return render_to_response('public/error.html', {'errorcode': '000000', 'errormsg': u'初始化数据成功'})


def exportdata(request, table):
    form_class = getattr(iforms, table + u'Form')
    model_class = getattr(models, table)
    for i in model_class.objects.all():
        tmp = i
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % table
    writer = csv.writer(response)
    writer.writerow(form_class._fielddesc)
    for obj in model_class.objects.all():
        writer.writerow([getattr(obj, key).encode('utf8') for key in form_class._fielddesc])
    return response


def showdata(request, table):
    model_class = getattr(models, table)
    form_class = getattr(iforms, table + u'Form')
    queryset = model_class.objects.all()
    queryset = [[getattr(row, col) for col in form_class._fielddesc] for row in queryset]
    fielddesc = [u'#'] + form_class._fielddesc
    # raise Exception(str(form_class._fielddesc))
    # raise Exception(str(queryset))
    if table in ('ChinaDaily'):
        translate = True
    else:
        translate = False
    return render_to_response('public/db_showdata.html',
                              {'queryset': queryset, 'fieldset': fielddesc, 'translate': translate})


def cleardata(request, table):
    if request.method == 'GET':
        model_class = getattr(models, table)
        model_class.objects.all().delete()
        return render_to_response('public/error.html', {'errorcode': '000000', 'errormsg': u'清理数据成功'})


def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    nowtime = time.strftime('%Y%m%d%H%M%S')
    request.session[u'nowtime'] = nowtime
    return render_to_response('public/db_showdata.html', {u'nowtime': nowtime, u'ID_USER': request.session[u'ID_USER']})


def ilogin(request):
    if request.method == 'GET':
        return login(request)
    elif request.method == 'POST':
        tmp = dict(request.POST.items())
        request.session[u'ID_USER'] = tmp[u'username']
        return login(request)


def test1(request):
    # A, B, C = u"", u"", u""
    # for p in models.UserInfo.objects.filter(userid=u'周菡'):
    # A += p.userid
    #     A += ','
    # # contains 等价于 sql like
    # for p in models.UserInfo.objects.filter(userid__icontains=u'a'):
    #     B += p.userid
    #     B += ','
    # for p in models.UserInfo.objects.order_by(u'-userid'):
    #     C += p.userid
    #     C += ','
    result = models.ChinaDaily.objects.filter(title='Senior court official under investigation')
    return HttpResponse(len(result))


def say_hello(request):
    name = request.GET.get('name', 'world')
    return render_to_response("hacker/hello.html", {"name": name})


def thanks(request):
    return render_to_response('thanks.html', {})


def year_archive(request, year):
    return HttpResponse('year = ' + year)


def year8_archive(request, year, template_name):
    return HttpResponse('year = %s,template_name = %s' % (year, template_name))


def archive(request):
    return render_to_response('public/error.html', {'errorcode': 'hello', 'errormsg': "archive"})


def list_details(request, list_objects, **kwargs):
    # queryset = model.objects.all()
    # template_name = 'mysite/%s_list.html' % model.__name__.lower()
    return render_to_response(kwargs['template_object_name'], {'queryset': kwargs['queryset']})
    # return render_to_response('books/list_details.html', {'queryset' : list_details})


def template_proc(request):
    t = loader.get_template('books/template11.html')
    c = RequestContext(request, {'message': 'I am view 1.'}, processors=[custom_proc])
    # c = RequestContext(request, {'message': 'I am view 1.'},)
    return HttpResponse(t.render(c))


# context增加自定义的数据
def template_proc1(request):
    return render_to_response('books/template11.html', {'message': 'I am the fourth view.'},
                              context_instance=RequestContext(request, processors=[custom_proc]))


# 自定义的filter函数
# 新建一个templatetags目录，新建一个包含自定义tag函数的py文件，在该文件里面定义filter函数
# 参考ifilter的写法
def template_filter(request):
    return render_to_response('books/testfilter.html', {'app': 'app'})


def rss(request):
    pass


def about(request):
    return "<?xml.version='1.0 encoding='utf8'?><root></root>"


def modelview(request, **kwargs):
    # map = deepcopy(kwargs)
    # del map[u'template_name']
    return render_to_response(kwargs[u'template_name'], kwargs)
    if checkutil.checkAuth(request, 'aa'):
        return render_to_response(kwargs[u'template_name'], kwargs)
    else:
        return errorutils.error('000111', '该用户无此权限')


def xmltest(request, **kwargs):
    return HttpResponse("<?xml.version='1.0' encoding='utf8'?><root></root>")


def foo(request):
    return HttpResponse("foo")


def getxml(request):
    sio = StringIO.StringIO()
    sio.write(u'<?xml version="1.0" encoding="UTF-8"?><message>')
    form_class = getattr(iforms, 'VocabularyForm')

    for o in models.Vocabulary.objects.filter(status="1"):
        sio.write(u'<table>')
        row = u'%s%s%s%s%s%s%s' % (o.index, o.word, o.explain, o.level, o.modifydate, o.modifytime, o.status)
        fieldlen = u','.join([str(len(getattr(o, i))) for i in form_class._fielddesc])
        tmp = [i for i in form_class._fielddesc]
        tmp[0] = u'idx'
        fielddesc = u','.join(tmp)
        sio.write(u'<_tabname>Vocabulary</_tabname><_fields>%s</_fields><_row>%s</_row><_fieldlen>%s</_fieldlen>' % (
            fielddesc, row, fieldlen))
        sio.write(u'</table>')
    sio.write(u'</message>')
    return HttpResponse(sio.getvalue())


def ajaxtest(request, **kwargs):
    return render_to_response('test/ajaxtest.html', {})


def getjson1(request):
    jsn = {}
    jsn['table'] = {}
    jsn['defines'] = {}
    table = request.GET['q']
    # vocabulary
    form_class = getattr(iforms, table + 'Form')
    jsn['defines']['table_' + table.lower()] = {}
    tmp = [i for i in form_class._fielddesc]
    tmp[0] = 'idx';
    jsn['defines']['table_' + table.lower()]['fielddesc'] = u','.join(tmp)
    vocabulary = []
    model_class = getattr(models, table)
    for o in model_class.objects.filter(status="1"):
        row = u''.join([getattr(o, i) for i in form_class._fielddesc])
        fieldlen = u','.join([str(len(getattr(o, i))) for i in form_class._fielddesc])
        vocabulary.append((fieldlen, row))
    jsn['table'][table.lower()] = vocabulary;
    jsn = json.dumps(jsn)
    return HttpResponse(request.GET.get("callbackparam", '') + '(' + jsn + ')', content_type="application/json")


def fetchchinadaily(request):
    logger = logging.getLogger("mysite.app")
    chinadailyurl = "http://www.chinadaily.com.cn/rss/cndy_rss.xml"
    try:
        u, u1 = None, None
        errorflag = None
        u = urllib2.urlopen(chinadailyurl)
        xml = u.read()
        xmltree = ElementTree.fromstring(xml)
        items = xmltree.find('channel').findall('item')
        news = []
        for it in items:
            kv = dict([(x.tag, x) for x in it.iter()])
            # for x in it.iter():
            # if x.tag in ('title', 'content', 'category', 'pubdate'):
            #         kv[x.tag] = x.text.replace("'", "")
            #     if x.tag == 'link':
            #         link = x.text
            kv['status'] = '1'
            news.append(kv)
        total = 0
        for n in news:
            if total == 20:
                break
            if len(models.ChinaDaily.objects.filter(title=n['title'].text)) > 0:
                continue
            try:
                logger.debug(n['link'].text)
                u1 = urllib2.urlopen(n['link'].text)
                soup = BeautifulSoup.BeautifulSoup(u1.read())
                artical = soup.find("div", {"id": "Content"})
                artical_text = "".join([p.text for p in artical.findAll('p')])
                n['content'] = artical_text
                data = {}
                for key in ('title', 'content', 'category', 'pubdate'):
                    if key == 'content':
                        data[key] = n[key]
                    else:
                        data[key] = n[key].text
                data['status'] = '1'
                logger.debug(data['title'])
                obj = apply(ChinaDaily, [], data)
                obj.save()
            except Exception as e:
                logger.error(e.message)
            finally:
                total += 1
                if u1:
                    u1.close()
    except Exception as e:
        errorflag = e
    finally:
        u.close()
        if errorflag:
            return HttpResponse(str(errorflag))
        else:
            return HttpResponse('sync %d news' % total)


def db2json(_table, _count=-1, _page='', _num='', ** kwargs):
    logger = logging.getLogger("mysite.app")
    jsn = {}
    jsn['table'] = {}
    jsn['defines'] = {}
    # vocabulary
    form_class = getattr(iforms, _table + 'Form')
    jsn['defines']['table_' + _table] = {}
    tmp = [i for i in form_class._fielddesc]
    jsn['defines']['table_' + _table]['fielddesc'] = u','.join(tmp)
    rows = []
    model_class = getattr(models, _table)
    for o in apply(model_class.objects.filter, [], kwargs):
        rowlist = [unicode(getattr(o, i)) for i in form_class._fielddesc]
        row = u"".join(rowlist)
        fieldlen = u','.join([str(len(i)) for i in rowlist])
        rows.append((fieldlen, row))
    jsn['table'][_table] = rows
    jsn = json.dumps(jsn)
    return jsn


def getchinadaily(request):
    return HttpResponse(request.GET.get("callbackparam", '') + '(' + db2json('ChinaDaily', status='1') + ')',
                        content_type="application/json")

def getjson(request):
    table = request.GET['q']
    page = request.GET.get('_page', "")
    num = request.GET.get('_num', "")
    logger = logging.getLogger("mysite.app")
    jsn = db2json(table, )
    # j = json.loads(jsn)
    # logger.debug(j['table']['Words'][0][1])
    return HttpResponse(request.GET.get("callbackparam", '') + '(' + jsn + ')',
                        content_type="application/json")

def gettranslate(request):
    logger = logging.getLogger("mysite.app")
    fd = None
    q = request.GET['q']
    try:
        fd = urllib2.urlopen(
            "http://openapi.baidu.com/public/2.0/translate/dict/simple?client_id=UBAECdRjhRokd1ASwzljpKvh&q=%s&from=en&to=zh" % q)
        s = fd.read()
        jsn = json.loads(s)
        parts = jsn['data']['symbols'][0]['parts']
        word = jsn['data']['word_name']
        r = Words.objects.filter(word=word)
        if r:
            return HttpResponse(r[0].translate)
        result = []
        for i in parts:
            result.append(i[u'part'] + ' ' + u",".join([j for j in i[u'means']]))
        translate = u";".join(result)
        logger.debug(translate)
        obj = Words(word=word, translate=translate)
        obj.save()
        return HttpResponse(translate)
    except Exception as e:
        logger.error(str(e))
        return HttpResponse("")
    finally:
        if fd:
            fd.close()


def registerform(request):
    logger = logging.getLogger("mysite.app")
    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)
        # logger.debug(str(request.FILES['headImg'].read()))
        if 1:
            logger.debug(uf.cleaned_data['headImg'])
            return HttpResponse('upload ok!')
        else:
            logger.error('error')

    uf = UserForm()
    kv = {'uf' : uf}
    kv.update(csrf(request))
    return render_to_response('register.html',kv)

def useless(request):
    xml = "<root></root>"
    kv = {}
    # return render_to_response('thanks.html', {'xml' : ""})
    return HttpResponse(xml, mimetype='text/xml',)

def getxml(request):
    kv = {'rspcode' : '000000', 'rspmsg' : '成功'}
    t = get_template('testpanels/firstxml.html')
    xml = t.render(Context(kv))
    return HttpResponse(xml, mimetype='text/xml')