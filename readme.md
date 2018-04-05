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

