from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'djangoweb.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/$', include(admin.site.urls)),
                       # url(r'^xmlservice/(\w+)/(\w+)/$', u'djangoweb.views.xmlservice'),
                       url(r'^login/$', u'djangoweb.views.login'),
                       url(r'^logout/$', u'djangoweb.views.logout'),
                       url(r'^project/$', u'djangoweb.views.projectlist'),
                       url(r'^project/(\w+)/$', u'djangoweb.views.transaction'),
                       url(r'^project/(\w+)/(\w+)/$', u'djangoweb.views.transconfig'),
                       url(r'^project/(\w+)/(\w+)/(\w+)/$', u'djangoweb.views.templateconfig'),
                       url(r'^postservice/addproject/$', u'djangoweb.views.addproject'),
                       url(r'^postservice/addtranscode/$', u'djangoweb.views.addtranscode'),
                       url(r'^postservice/addtransconfig/$', u'djangoweb.views.addtransconfig'),
                       url(r'^postservice/addtemplate/$', u'djangoweb.views.addtemplate'),
                       url(r'^postservice/adddatamap/$', u'djangoweb.views.adddatamap'),
                       url(r'^project/datamaplist/$', u'djangoweb.views.datamaplist'),
                       url(r'^bootstrap/$', u'djangoweb.views.bootstrap'),
                       url(r'^xmlservice/(\w+)/$', u'djangoweb.views.xmlservice'),
                       url(r'^ajaxservice/(\w+)/$', u'djangoweb.ajaxservice.ajaxservice'),
                       url(r'^requesttest/$', u'djangoweb.studyview.requesttest'),
                       url(r'^modeltest/$', u'djangoweb.studyview.modeltest'),
                       url(r'^rawsql/$', u'djangoweb.studyview.rawsql'),
)
