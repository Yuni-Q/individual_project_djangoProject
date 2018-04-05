from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('', include('elections.urls')), #elections app을 include 해주는것임. 
    path('admin/', admin.site.urls),
]
