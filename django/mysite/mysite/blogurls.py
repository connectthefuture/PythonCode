#coding=utf8
__author__ = 'zt-zh'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        (r'^archive/$', 'mysite.views.archive'),
        (r'^about/$', 'mysite.views.about'),
        (r'^rss/$', 'mysite.views.rss'),
)