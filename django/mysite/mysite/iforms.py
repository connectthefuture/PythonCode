#coding=utf8
__author__ = 'ZT-ZH'


from django import forms
import dbutils
import re

class FormException(Exception):
    pass

TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
)

class ContactForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField()
    sender = forms.EmailField(required=False)

    #如何自定义form的校验方法,抛出 ValidationError
    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        num_words = len(message.split())
        if num_words < 2:
            raise forms.ValidationError("Not enough words!")
        return message

class PublisherForm(forms.Form):
    _fielddesc = ['name', 'address', 'city', 'state_province', 'country', 'website']
    name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=60)
    state_province = forms.CharField(max_length=30)
    country = forms.CharField(max_length=50)
    website = forms.CharField()

class NewThingForm(forms.Form):
    _fielddesc = ['time', 'userid']
    time = forms.CharField(max_length=14)
    userid = forms.CharField(max_length=8)

class UserInfoForm(forms.Form):
    _fielddesc = ['userid', 'group']
    userid = forms.CharField(max_length=14)
    group = forms.CharField(max_length=20)

    def clean_message(self, ):
        group = self.cleaned_data.get('group', u'')
        # raise Exception(str(self.cleaned_data))
        if group is None or group == u'' or len(group) % 2 != 0:
            raise FormException(u'the length of group must be "\d{2}"')
        validgroup = dbutils.select(u'select distinct groupid from mysite_groupauth')
        for i in xrange(len(group) / 2):
            g = group[2 * i : 2 * i + 2]
            if g not in validgroup:
                raise FormException(u"no group %s" % g)
                return
        return True

class AuthCodeForm(forms.Form):
    _fielddesc = ['trancode', 'tranname']
    trancode = forms.CharField(max_length=10)
    tranname = forms.CharField(max_length=60)


class GroupAuthForm(forms.Form):
    _fielddesc = ['groupid', 'trancode']
    groupid = forms.CharField(max_length=2)
    trancode = forms.CharField(max_length=10)

    def clean_message(self, ):
        # trancodes = dbutils.select(u'select trancode from mysite_authcode')
        trancode = self.cleaned_data.get('trancode', u'')
        groupid = self.cleaned_data.get('groupid', u'')
        if groupid is None or groupid == u'' or not re.search('^\d{2}$', groupid, ):
            raise FormException(u'groupid must be \d{2}')
        if trancode == u'' or trancode is None:
            raise FormException(u'must not be none')
        try:
            forms.AuthCode.objects.get(trancode = trancode)
        except forms.AuthCode.DoesNotExist:
            raise FormException(u'no trancode %s' % trancode)
        return True

class TestTableForm(forms.Form):
    _fielddesc = ['a', 'b']
    a = forms.CharField(max_length=10)
    b = forms.CharField(max_length=10)

class VocabularyForm(forms.Form):
    _fielddesc = [u'index', u'word', u'explain', u'level', u'modifydate', u'modifytime', u'status']
    index = forms.CharField(max_length=6,)
    word = forms.CharField(max_length=30)
    explain = forms.CharField(max_length=256)
    level = forms.CharField(max_length=1)
    modifydate = forms.CharField(max_length=8)
    modifytime = forms.CharField(max_length=6)
    # 0 同步 1 服务器更新 2 本地更新
    status = forms.CharField(max_length=1)

class ChinaDailyForm(forms.Form):
    _fielddesc = [u'idx', u'title', u'content', u'pubdate', u'category', u'status']
    idx = forms.CharField(max_length=6,)
    title = forms.CharField(max_length=100,)
    content = forms.CharField(max_length=1000)
    pubdate = forms.CharField(max_length=20)
    category = forms.CharField(max_length=30)
    status = forms.CharField(max_length=1)

class WordsForm(forms.Form):
    _fielddesc = [u'idx', u'word', u'translate',]
    idx = forms.CharField(max_length=6)
    word = forms.CharField(max_length=30)
    translate = forms.CharField(max_length=512)

class UserForm(forms.Form):
    username = forms.CharField()
    headImg = forms.FileField()