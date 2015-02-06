#coding=utf8
from django import template

register = template.Library()


@register.filter(name='yoo')
def yoo(value,):
    return 'yoo'

@register.filter(name='foobar')
def foobar(value, arg):
    return value + arg