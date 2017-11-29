"""coms572_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from scheduler import views as views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^buildings/$', views.buildings, name='buildings'),
    url(r'^buildings/(?P<obj_id>[0-9]+)$', views.building),
    url(r'^classrooms/$', views.classrooms, name='classrooms'),
    url(r'^classrooms/(?P<obj_id>[0-9]+)$', views.classroom),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^courses/(?P<obj_id>[0-9]+)$', views.course),
    url(r'^exams/$', views.exams, name='exams'),
    url(r'^exams/(?P<obj_id>[0-9]+)$', views.exam),
    url(r'^tas/$', views.tas, name='tas'),
    url(r'^tas/(?P<obj_id>[0-9]+)$', views.ta),
    url(r'^datagen/$', views.generate_data),
    url(r'^restart/$', views.truncate_db),
    url(r'^assign/$', views.assign_ta),
]
