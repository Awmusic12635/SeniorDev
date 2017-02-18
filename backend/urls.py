from django.conf.urls import url

from .views import admin
from .views import user

urlpatterns = [
    url(r'^$', user.index, name='index'),
    url(r'^login$', user.index, name='login'),
    url(r'^logout/$', user.index, name='login'),
    url(r'^items/$', user.index, name='items'),
    url(r'^items/add$', user.index, name='items'),
    url(r'^items/(?P<id>\d*)$', user.index, name='items'),
    url(r'^items/(?P<id>\d*)/edit$', user.index, name='items'),
    url(r'^items/(?P<id>\d*)/delete$', user.index, name='items'),
    url(r'^categories/$', user.index, name='items'),
    url(r'^categories/add$', user.index, name='items'),
    url(r'^categories/(?P<id>\d*)$', user.index, name='items'),
    url(r'^categories/(?P<id>\d*)/edit$', user.index, name='items'),
    url(r'^categories/(?P<id>\d*)/delete$', user.index, name='items'),
    url(r'^users/$', user.index, name='items'),
    url(r'^users/add$', user.index, name='items'),
    url(r'^users/(?P<id>\d*)$', user.index, name='items'),
    url(r'^users/(?P<id>\d*)/edit$', user.index, name='items'),
    url(r'^search$', user.index, name='items'),

]
