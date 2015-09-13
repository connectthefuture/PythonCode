# coding=utf8

import views
import models
from django.conf.urls import patterns, include, url
# from django.conf.urls.defaults import *
from views import template1, now, hours_ahead, searchbook, testmodels, csvtest, contact, image, initdata, exportdata, \
    cleardata, ilogin, profile, test1, say_hello
from views_test import testdb
from django.contrib import admin
from django.contrib.auth.views import logout
from ifeed import LatestEntries, LatestEntriesByCategory

admin.autodiscover()

# patterns 函数接受一个公共的参数，提取出函数的公共部分，形如 'mysite.views'

publisher_info = {
    "queryset": models.UserInfo.objects.all(),
    'template_object_name': 'books/list_details.html',
    # "extra_context" : {'hello' : 'hello'}
}

feeds = {
    'latest': LatestEntries,
    'categories': LatestEntriesByCategory,
}

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'mysite.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/$', include(admin.site.urls)),
                       # url(r'^admin/login', ilogin),
                       # url(r'^admin/logout', logout),
                       url(r'^template1/$', template1),
                       url(r'^now/$', now),
                       url(r'^hours_ahead/plus/(\d+)$', hours_ahead),
                       url(r'^book/search/(\w+)$', searchbook),
                       # url(r'^book/search/(\w+)$', searchbook),
                       url(r'^testmodels/$', testmodels),
                       # url(r'^add/publisher$', publisher),
                       url(r'^csvtest$', csvtest),
                       url(r'^contact$', contact),
                       url(r'^image$', image),
                       url(r'^initdata/(\w+)$', initdata),
                       url(r'^exportdata/(\w+)$', exportdata),
                       url(r'^cleardata/(\w+)$', cleardata),
                       url(r'^showdata/(\w+)', u'mysite.views.showdata', {}),
                       url(r'^accounts/login/$', ilogin),
                       url(r'^accounts/logout/$', logout),
                       url(r'^accounts/profile/$', profile),
                       url(r'^test/test1/$', test1),
                       url(r'^test/testdb/$', testdb),
                       # 使用url   http://127.0.0.1:8000/hacker/xss/?name=yoo1
                       url(r'^hacker/xss/.*$', say_hello),
                       url(r'^hacker/aa/$', u'mysite.views.modelview', {u'template_name': u'hacker/say_aa.html',
                                                                        u'url': u'http://170.101.100.22/project/index.php?doLogout=true'}),
                       # 使用引号时，前面必须加上mysite ???
                       url(r'^thanks/$', 'mysite.views.thanks'),
                       # 使用命名组的例子
                       url(r'^articles/(?P<year>\d{4})/$', views.year_archive),
                       # 通过urlconf传递额外的参数给视图函数
                       url(r'^articles/(?P<year>\d{8})/$', views.year8_archive, {'template_name': 'template1.html'}),
                       url(r'list_details/(\w+)', u'mysite.views.list_details', publisher_info),
                       url(r'template_proc/$', u'mysite.views.template_proc'),
                       url(r'template_proc1/$', u'mysite.views.template_proc1'),
                       url(r'template_filter/$', u'mysite.views.template_filter'),
                       # url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds} ),
                       # userform
                       url(r'^registerform/$', u'mysite.views.registerform'),
                       url(r'^useless/$', u'mysite.views.useless'),

                       # urls 分级
                       # url(r'blog/', include(u'mysite.blogurls'), {}),

                       #bootstrap
                       url(r'test/test2/$', u'mysite.views.modelview', {u'template_name': u'test/test2.html'}),
                       url(r'csstest/$', u'mysite.views.modelview', {u'template_name': u'test/test3.html'}),
                       url(r'csstest1/$', u'mysite.views.modelview', {u'template_name': u'test/test4.html'}),
                       url(r'parsexml/$', u'mysite.views.modelview', {u'template_name': u'test/parsexml.html'}),
                       url(r'jquerytest/$', u'mysite.views.modelview', {u'template_name': u'test/jquerytest.html'}),
                       url(r'jstest/$', u'mysite.views.modelview', {u'template_name': u'test/test5.html'}),

                       #xml
                       url(r'xmltest/$', u'mysite.views.xmltest', {u'template_name': u'test/xmltest.html'}),
                       url(r'ajaxtest/$', u'mysite.views.ajaxtest', {u'template_name': u'test/ajaxtest.html'}),
                       url(r'foo/$', u'mysite.views.foo', ),
                       url(r'getxml/$', u'mysite.views.getxml', ),

                       #vocabulary
                       url(r'^initvocabulary/$', u'mysite.views.modelview',
                           {u'template_name': u'vocabulary/initvocabulary.html'}),
                       url(r'^localvocabulary/$', u'mysite.views.modelview',
                           {u'template_name': u'vocabulary/localvocabulary.html'}),
                       url(r'^indexdb/$', u'mysite.views.modelview', {u'template_name': u'vocabulary/indexdb.html'}),
                       url(r'^getjson/$', u'mysite.views.getjson', ),
                       url(r'^gettranslate/$', u'mysite.views.gettranslate'),

                       # url(r'^fetchchinadaily/$', u'mysite.views.fetchchinadaily'),
                       # url(r'^getchinadaily/$', u'mysite.views.getchinadaily'),
                       #
                       # url(r'^getweather/$', u'mysite.views.getweather'),
                       #
                       # url(r'^testpanels/$', u'mysite.views.getxml'),

                       # url(r'^xmlservice/(\w+)/(\w+)/$', u'mysite.views.xmlservice'),
)
