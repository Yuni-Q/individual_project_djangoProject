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
