# coding=utf-8
from __future__ import unicode_literals
from django.http import HttpResponse
from jinja2 import Environment, PackageLoader
import logging

logger = logging.getLogger("djangoweb.app")
templateenv = Environment(loader=PackageLoader('djangoweb'))


def render_to_response(templatename, dictionary={}, ):
    template = templateenv.get_template(templatename)
    return HttpResponse(template.render(dictionary))