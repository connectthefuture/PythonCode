# from django.contrib.auth.models import User

class TemplateTest:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def modify(self, x, y):
        # print(getattr(self, x))
        self.__dict__[x] = y
    modify.alters_data = True

class A(object):
    def __init__(self):
        self._map = {}
    def __getitem__(self, key):
        return self.map.get(key)

def foo():
    pass

if __name__ == '__main__':
    foo()