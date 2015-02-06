import re
import cStringIO
from django.http import HttpRequest

class DynamicFormException(Exception):
    pass

class DynamicForm:
    def __init__(self,):
        self.fielddesc = []
    #   property, max_length, pattern, enum
    def add(self, name, ** kwargs):
        self.fielddesc.append((name, kwargs))
    def valid(self):
        for x, y in self.fielddesc:
            pass
    def as_table(self):
        tmp = u'<tr><th><label for="id_%s">%s:</label></th><td><input id="id_%s" name="%s" type="text" /></td></tr>'
        cio = cStringIO.StringIO()
        for key, value in self.fielddesc:
            lower_key = key.lower()
            cio.write(tmp % (lower_key, key, lower_key, key))
        return cio.getvalue()
    def valid(self, request):
        # fields = [x for x, y in self.fielddesc]
        tmp = dict(self.fielddesc)
        for key, value,  in request.POST.items():
            if key in tmp:
                if 'max_length' in tmp[key] and len(value) > tmp[key]['max_length']:
                    raise DynamicFormException('field length too long')
                if 'pattern' in tmp[key] and not re.search(value, tmp[key]['pattern']):
                    raise DynamicFormException('value dont match pattern')

# def NeedLogin():
#     if not request.user.is_authenticated():
#         return HttpResponseRedirect('/accounts/login')

if __name__ == '__main__':
    df = DynamicForm()
    df.add('A')
    print(df.as_table())
