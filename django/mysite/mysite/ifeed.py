#coding=utf8
__author__ = 'zt-zh'

import models
# from django.contrib.syndication.feeds import Feed

class LatestEntries():
    title = "Chicagocrime.org site news"
    link = "/sitenews/"
    description = "Updates on changes and additions to chicagocrime.org."
    def items(self):
        books = models.Book.objects.all()
        return books

class LatestEntriesByCategory():
    pass