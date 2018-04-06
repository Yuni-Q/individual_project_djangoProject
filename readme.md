# 장고 프로젝트 만들기

1. 장고 설치

```bash
$ pip3 install django 
```

2. 프로젝트 만들기

```bash
$ django-admin startproject mysite
```

3. 서버실행

```bash
$ python manage.py runserver
```

- 접속 (127.0.0.1:8000) or (localhost:8000)
- 접속 종료 (control+c)

4. Hello world 띄우기

```bash
python manage.py startapp elections
```

- mysite/elections/wiews.py

```python
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("Hello world")
```

- mysite/mysite/urls.py

```python
from django.contrib import admin
from django.urls import path, include #include 써서 추가

urlpatterns = [
	path('', include('elections.urls')), #elections app을 include 해주는것임. 
    path('admin/', admin.site.urls),
]
```

- mysite/elections/urls.py

```python
from django.urls import path
from . import views #.은 현재폴더의 디렉토리라는뜻. 즉 현재폴더의 views.py를 import하는것임

urlpatterns = [
path('', views.index),
]
```

5. 모델 클래스

- mysite/elections/models.py

```python
from django.db import models

# Create your models here.
class Candidate(models.Model)
	name = models.CharField(max_length=10)
	introduction = models.TextField()
	area = models.CharField(max_length=15)
	party_number = models.IntegerField(default=1)
```

6. 마이그래이션과 DB (SQLite3을 지원)

- mysite/mysite/settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'elections'
]
```

```bash
$ python manage.py makemigrations
```

```bash
$ python manage.py migrate
```

7. 장고 어드민

```bash
$ python manage.py createsuperuser
```

- Locallhost:8000/admin 접속
- mysite/elections/admin.py

```python
from django.contrib import admin

from .models import Candidate

# Register your models here.

admin.site.register(Candidate)
```

- mysite/elections/models.py

```python
from django.db import models

# Create your models here.
class Candidate(models.Model):
	name = models.CharField(max_length=10)
	introduction = models.TextField()
	area = models.CharField(max_length=15)
	party_number = models.IntegerField(default=1)

	def __str__(self):
		return self.name

# 모델을 이름으로 관리
```

8. 데이터 보여주기

- mysite/elections/views.py

```python
from django.shortcuts import render
from django.http import HttpResponse

from .models import Candidate

# Create your views here.
def index(request):
	candidates = Candidate.objects.all() #해당 테이블 모든 row 불러오기
	str = ''
	for candidate in candidates:
		str += "{} 기호 {}번 ({})<br>".format(candidate.name, candidate.party_number, candidate.area)
		str += candidate.introduction + "</p>"
	return HttpResponse(str)
```

9. shell

```bash
$ python manage.py shell
```

```bash
In [1]: from elections.models import Candidate

In [2]: Candidate.objects.all()
Out[2]: <QuerySet [<Candidate: 힐러리>, <Candidate: 트럼프>]>

In [3]: new_candidate = Candidate(name="루비오")

In [4]: new_candidate.save()

In [5]: Candidate.objects.all()
Out[5]: <QuerySet [<Candidate: 힐러리>, <Candidate: 트럼프>, <Candidate: 루비오>]>

In [7]: no1 = Candidate.objects.filter(party_number = 1)

In [8]: no1
Out[8]: <QuerySet [<Candidate: 힐러리>, <Candidate: 루비오>]>

In [9]: no1[0].party_number
Out[9]: 1

In [10]: no1[0].name
Out[10]: '힐러리'

In [11]: no1[0].introduction
Out[11]: '미국 최초의 여자 대통령이 되겠습니다.'

```

10. 템플릿으로 html 불러오기

- mysite/elections/templates/elections/index.html에 파일 추가
- mysite/elections/views.py

```python
from django.shortcuts import render
from django.http import HttpResponse

from .models import Candidate

# Create your views here.
def index(request):
	candidates = Candidate.objects.all()
	
	return render(request, 'elections/index.html')
```

11. 템플릿 정보 채우기

- mysite/elections/views.py

```Python
from django.shortcuts import render
from django.http import HttpResponse

from .models import Candidate

# Create your views here.
def index(request):
	candidates = Candidate.objects.all()
	context = {'candidates':candidates}	
	return render(request, 'elections/index.html', context)
```

- mysite/elections/templates/elections/index.html

```html
<tbody>
        {% for candidate in candidates %}
        <tr>
            <td>{{candidate.name}}</td>
            <td>{{candidate.introduction}}</td>
            <td>{{candidate.area}}</td>
            <td>{{candidate.party_number}}번</td>
        </tr>
        {% endfor %}
<tbody>
```

12. MVC 패턴
13. 여론조사 모델

- mysite/elections/models.py

```python
from django.db import models

# Create your models here.
class Candidate(models.Model):
	name = models.CharField(max_length=10)
	introduction = models.TextField()
	area = models.CharField(max_length=15)
	party_number = models.IntegerField(default=1)

	def __str__(self):
		return self.name


class Poll(models.Model):
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	area = models.CharField(max_length=15)

class Choice(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
	votes = models.IntegerField(default=0)
```

- mysite/elections/admin.py

```python
from django.contrib import admin

from .models import Candidate, Poll

# Register your models here.

admin.site.register(Candidate)
admin.site.register(Poll)
```

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

14. Url 다루기

- mysite/elections/templates/elections/index.html

```html
<td>
    <a href="areas/{{candidate.area}}">
    	{{candidate.area}}
	</a>
</td>
```

- mysite/elections/urls.py

```python
from django.urls import path
from . import views #.은 현재폴더의 디렉토리라는뜻. 즉 현재폴더의 views.py를 import하는것임

urlpatterns = [
path('', views.index),
path('areas/<str:area>/',views.areas)
]
```

- mysite/elections/viesw.py

```python
def areas(request, area):
	return HttpResponse(area)
```

15. 여론조사 화면 구성

- mysite/elections/templates/elections/area.html

```html
<!-- \mysite\templates\elections\area.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <title>{{area}}</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
</head>
<body>
<div class="container">
<h1>{{area}}</h1>
<br>
{% if poll %}
    <table class="table table-striped">
        <thead>
        <tr>
            <td><B>이름</B></td>
            <td><B>소개</B></td>
            <td><B>기호</B></td>
            <td><B>지지하기</B></td>
        </tr>
        </thead>
        <tbody>
        {% for candidate in candidates %}
        <tr>
            <td>{{candidate.name}}</td>
            <td>{{candidate.introduction}}</td>
            <td>{{candidate.party_number}}번</td>
            <td>
                <form action = "#" method="post">
                    <button name="choice" value="#">선택</button>
                </form>
            </td>
        </tr>
        {% endfor %}
        </tbody>
    </table>
    {% else %}
    여론조사가 없습니다.
    {% endif %}
</div>
</body>
```

- mysite/elections/viesw.py

```python
from django.shortcuts import render
from django.http import HttpResponse

from .models import Candidate, Poll, Choice

import datetime

# Create your views here.
def index(request):
	candidates = Candidate.objects.all()
	context = {'candidates':candidates}	
	return render(request, 'elections/index.html', context)

def areas(request, area):
	today = datetime.datetime.now()
	try:
		poll = Poll.objects.get(area = area, start_date__lte=today, end_date__gte=today)
	# start data < 오늘 < end date
		candidates = Candidate.objects.filter(area = area)
	#찾고자 하는 값이 없으면 에러
	except:
		poll = None
		candidates = None
	context = {'candidates':candidates, 'area':area, 'poll':poll}
	return render(request, 'elections/area.html', context)
```

16. 여론조사 결과저장

- mysite/elections/templates/elections/area.html

```html
<td>
  <form action = "/polls/{{poll.id}}/" method="post">
    {% csrf_token %}
    <button name="choice" value="{{candidate.id}}">선택</button>
  </form>
</td>
```

- mysite/elections/urls.py

```python
from django.urls import path
from . import views #.은 현재폴더의 디렉토리라는뜻. 즉 현재폴더의 views.py를 import하는것임

urlpatterns = [
path('', views.index),
path('areas/<str:area>/',views.areas),
path('polls/<int:poll_id>/', views.polls)
]
```

- mysite/elections/views.py

```python
def polls(request, poll_id):
	poll = Poll.objects.get(pk=poll_id)
	selection = request.POST['choice']

	try:
		choice = Choice.objects.get(poll_id = poll_id, candidate_id = selection)
		choice.votes += 1
		choice.save()
	except:
		choice = Choice(poll_id = poll_id, candidate_id = selection, votes=1)
		choice.save()

	return HttpResponse("finish")
```

- mysite/elections/admin.py

```python
from django.contrib import admin

from .models import Candidate, Poll, Choice

# Register your models here.

admin.site.register(Candidate)
admin.site.register(Poll)
admin.site.register(Choice)
```

17. http redirect하기

- mysite/elections/templates/elections/result.html

```html
<!-- C:\Code\mysite\elections\templates\elections\result.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <title>{{area}} 지역구 여론조사 결과</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
</head>
<body>
<div class="container">
<h1>{{area}} 지역구 여론조사 결과</h1>
<br>
<table class="table table-striped">
    <thead>
    <tr>
        <td><B>기간</B></td>
        {% for candidate in candidates %}
        <td><B>{{candidate.name}}</B></td>
        {% endfor %}       
    </tr>
    </thead>
    <tbody>
    {% for result in poll_results %}
    <tr>
        <td> {{result.start_date.year}} / {{result.start_date.month}} / {{result.start_date.day}} ~ {{result.end_date.year}} / {{result.end_date.month}} / {{result.end_date.day}}</td> <!-- 템플릿에서는 [] 대신 . 사용 -->
         {% for rate in result.rates %}
         <td> {{rate}}%</td>
         {% endfor %}
    </tr>    
    {% endfor %}
    <tbody>
</table>
</div>
</body>
```

- mysite/elections/urls.py

```python
from django.urls import path
from . import views #.은 현재폴더의 디렉토리라는뜻. 즉 현재폴더의 views.py를 import하는것임

urlpatterns = [
path('', views.index),
path('areas/<str:area>/',views.areas),
path('polls/<int:poll_id>/', views.polls),
path('areas/<str:area>/result/',views.result),
]
```

- mysite/elections/views.py

```python
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum

def polls(request, poll_id):
	poll = Poll.objects.get(pk=poll_id)
	selection = request.POST['choice']

	try:
		choice = Choice.objects.get(poll_id = poll_id, candidate_id = selection)
		choice.votes += 1
		choice.save()
	except:
		choice = Choice(poll_id = poll_id, candidate_id = selection, votes=1)
		choice.save()

	return HttpResponseRedirect("/area/{}/result".format(poll.area))

def result(request, area):
	candidates = Candidate.objects.filter(area = area)
	polls = Poll.objects.filter(area = area)
	poll_results = []
	for poll in polls:
		result = {}
		result['start_date'] = poll.start_date
		result['end_date'] = poll.end_date
		total_votes = Choice.objects.filter(poll_id = poll.id).aggregate(Sum('votes'))
		result['total_votes'] = total_votes['votes__sum']
		rates = []
		for candidate in candidates:
			try:
				choice = Choice.objects.get(poll_id = poll.id, candidate_id = candidate.id)
				rates.append(
					round(choice.votes *100 / result['total_votes'],1)
				)
			except:
				rates.append(0)
	
		result['rates'] = rates
		poll_results.append(result)

	context = {'candidates' : candidates, 'area' : area, 'poll_results' : poll_results}

	return render(request, 'elections/result.html', context)
```

18. 상세페이지( 404오류를 위한 )

- mysite/elections/urls.py

```python
from django.urls import path
from . import views #.은 현재폴더의 디렉토리라는뜻. 즉 현재폴더의 views.py를 import하는것임

urlpatterns = [
path('', views.index),
path('areas/<str:area>/',views.areas),
path('polls/<int:poll_id>/', views.polls),
path('areas/<str:area>/result/',views.result),
path('candidate/<str:area>/',views.candidate),
]
```

- mysite/elections/view.py

```python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404

def candidate(request, name):
	candidate = get_object_or_404(Candidate, name = name)
	# try:
	# 	candidate = Candidate.objects.get(name = name)
	# except:
	# 	raise Http404
	return HttpResponse(candidate.name)
```

19. 404페이지 변경하기

- mysite/mysite/settings.py

```python
# C:\Code\mystie\settings.py

# ...

DEBUG = False #True에서 False로 변경합니다

ALLOWED_HOSTS = ['localhost']

# ...

TEMPLATES = [
    {
        # ...
        'DIRS' : ['templates'],
        # ...
    }
]
```

- mysite\templates\404.html

```python
없는 페이지 입니다.
```

20. 템플릿 상속

- mysite\elections\templates\elections\layout.html

```Html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>{% block title %}{% endblock %}</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
</head>
<body>
{% block content %}{% endblock %}
</body>
</html>
```

- mysite\elections\templates\elections\index.html

```html
{% extends "elections/layout.html" %}
{% block title %}
선거 후보
{% endblock %}

{% block content %}
<div class="container">
    <table class="table table-striped">
        <thead>
        <tr>
            <td><B>이름</B></td>
            <td><B>소개</B></td>
            <td><B>출마지역</B></td>
            <td><B>기호</B></td>
        </tr>
        </thead>
        <tbody>
        {% for candidate in candidates %}
        <tr>
            <td>{{candidate.name}}</td>
            <td>{{candidate.introduction}}</td>
            <td>
            	<a href="areas/{{candidate.area}}">
            		{{candidate.area}}
            	</a>
            </td>
            <td>{{candidate.party_number}}번</td>
        </tr>
        {% endfor %}
        <tbody>
    </table>
{% endblock %}
```

- area.html && result.html 모두 적용

21. 네비게이션바 추가하기

```html
<body>
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <div class="navbar-header">
      <a class="navbar-brand" href="{% url 'elections:home' %}">사이트명</a>
    </div>
</nav>
```

- mysite/elections/urls.py

```python
from django.urls import path
from . import views #.은 현재폴더의 디렉토리라는뜻. 즉 현재폴더의 views.py를 import하는것임

app_name = 'elections'
urlpatterns = [
path('', views.index, name = 'home'),
path('areas/<str:area>/',views.areas),
path('polls/<int:poll_id>/', views.polls),
path('areas/<str:area>/result/',views.result),
path('candidate/<str:name>/',views.candidate),
]
```

22. 파일사용하기 ( 잘 안됨 )

- mysite\elections\static\elections 경로에 favicon 그림 파일 저장하기
- mysite\elections\layout.html

```python
<!-- C:\Code\mysite\elections\layout.html -->
{% load staticfiles %} <!-- 추가 -->

<!--기존는 유지하면서, <head> 태그 아래에 다음을 추가해주세요-->
    <link rel ="shortcut icon" type = "image/x-icon" href="{% static 'elections/favicon.ico' %}" />
```

