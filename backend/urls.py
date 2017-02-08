from django.conf.urls import url

from .views import admin
from .views import user

urlpatterns = [
    url(r'^$', user.index, name='index'),
]