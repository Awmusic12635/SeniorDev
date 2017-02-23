from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import admin
from .views import user
from .views.items import item

urlpatterns = [
    url(r'^$', user.index, name='index'),
    url(r'^login', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout', auth_views.logout, name='logout'),
    url(r'^dashboard/$', user.dashboard, name='dashboard'),
    url(r'^item/$', item.list_items, name='itemList'),
    url(r'^item/add$', item.add_item, name='items'),
    url(r'^item/(?P<item_id>\d*)$', item.show_item, name='items'),
    url(r'^item/(?P<item_id>\d*)/edit$', item.edit_item, name='items'),
    url(r'^item/(?P<item_id>\d*)/delete$', user.index, name='items'),
    url(r'^item/(?P<item_id>\d*)/checkout$', user.index, name='items'),
    url(r'^category/$', user.index, name='items'),
    url(r'^category/add$', user.index, name='items'),
    url(r'^category/(?P<id>\d*)$', user.index, name='items'),
    url(r'^category/(?P<id>\d*)/edit$', user.index, name='items'),
    url(r'^category/(?P<id>\d*)/delete$', user.index, name='items'),
    url(r'^user/$', user.index, name='items'),
    url(r'^user/add$', user.index, name='items'),
    url(r'^user/(?P<id>\d*)$', user.index, name='items'),
    url(r'^user/(?P<id>\d*)/edit$', user.index, name='items'),
    url(r'^search$', user.index, name='items'),
    url(r'^checkout$', user.index, name='items'),
    url(r'^checkout/addItem$', user.index, name='items'),
    url(r'^checkout/removeItem$', user.index, name='items'),
    url(r'^checkout/finalize$', user.index, name='items'),
]
