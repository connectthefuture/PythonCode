# -*- coding: gbk -*-
import BeautifulSoup


class A:
    a = 0
    b = 0


a = A()
a.a = 100

b = A()
print(b.a)
print A.a
print(A.__dict__)
print(a.__dict__)

s = """<div class="zm-votebar">
<button class="up ">
<i class="icon vote-arrow"></i>
<span class="label">赞同</span>
<span class="count">19</span>
</button>
<button class="down ">
<i class="icon vote-arrow"></i>
<span class="label">反对</span>
</button>
</div>
"""

soup = BeautifulSoup.BeautifulSoup(s.decode('gbk'))
print(soup.button)
