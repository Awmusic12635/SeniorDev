from django.conf.urls import url
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from .views import admin
from .views import user, checkout, checkin,reservation, category, subcategory
from .views.items import item

urlpatterns = [
    url(r'^$', user.index, name='index'),
    url(r'^login', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout', auth_views.logout, name='logout'),
    url(r'^dashboard/$', user.dashboard, name='dashboard'),
    #items
    url(r'^item/$', item.list_item_types, name='itemList'),
    url(r'^item/add$', item.add_item_type, name='items'),
    url(r'^item/(?P<item_type_id>\d*)$', item.show_item_type, name='items'),
    url(r'^item/(?P<item_type_id>\d*)/edit$', item.edit_item_type, name='items'),
    url(r'^item/(?P<item_type_id>\d*)/delete$', item.delete_item_type, name='items'),
    url(r'^item/(?P<item_type_id>\d*)/add$', item.add_item, name='items'),
    url(r'^item/(?P<item_type_id>\d*)/items$', item.list_items, name='items'),
    url(r'^item/(?P<item_type_id>\d*)/(?P<item_id>\d*)$', item.show_item, name='items'),
    url(r'^item/(?P<item_type_id>\d*)/(?P<item_id>\d*)/edit$', item.edit_item, name='items'),
    url(r'^item/(?P<item_id>\d*)/checkout$', checkout.add_item, name='items'),
    #category
    url(r'^category/$', category.list_categories, name='categoryList'),
    url(r'^category/add$', category.add_category, name='categoryAdd'),
    url(r'^category/(?P<category_id>\d*)$', category.view_category, name='categoryView'),
    url(r'^category/(?P<category_id>\d*)/edit$', category.edit_category, name='categoryEdit'),
    url(r'^category/(?P<category_id>\d*)/subcategory$', subcategory.add_subcategory, name='subcategoryAdd'),
    url(r'^category/(?P<category_id>\d*)/subcategory/(?P<subcategory_id>\d*)$', subcategory.view_subcategory, name='subcategoryView'),
    url(r'^category/(?P<category_id>\d*)/subcategory/(?P<subcategory_id>\d*)/edit$', subcategory.edit_subcategory, name='subcategoryEdit'),
    #user
    url(r'^user/$', user.index, name='items'),
    url(r'^user/add$', user.index, name='items'),
    url(r'^user/(?P<id>\d*)$', user.index, name='items'),
    url(r'^user/(?P<id>\d*)/edit$', user.index, name='items'),
    #search
    url(r'^search$', user.index, name='items'),
    #checkout
    url(r'^checkout/$', checkout.get_pending_checkout, name='items'),
    url(r'^checkout/addItem/(?P<item_id>\d*)$', checkout.add_item, name='items'),
    url(r'^checkout/removeItem/(?P<item_id>\d*)$', checkout.remove_item, name='items'),
    url(r'^checkout/resetDueDate/(?P<checkoutitem_id>\d*)$', checkout.reset_duedate, name='items'),
    url(r'^checkout/(?P<checkoutitem_id>\d*)/overrideDate$', checkout.override_date, name='items'),
    url(r'^checkout/clear', checkout.clear, name='items'),
    url(r'^checkout/complete', checkout.complete, name='items'),
   #checkin
    url(r'^checkin/$', checkin.get_open_checkouts, name='items'),
    url(r'^checkin/(?P<checkout_id>\d*)$', checkin.view_checkout, name='items'),
    url(r'^checkin/checkin_item/(?P<checkoutitem_id>\d*)$', checkin.checkin_item, name='items'),
    #reservations
    url(r'^reservationRequest/$', reservation.request, name='reservationRequest'),
    url(r'^reservationRequest/pending$', reservation.view_requests, name='reservationRequestPending'),
    url(r'^reservationRequest/edit/(?P<request_id>\d*)$', reservation.edit_request, name='reservationRequestEdit'),
    url(r'^reservationRequest/decline/(?P<request_id>\d*)$', reservation.decline_request, name='reservationRequestDecline'),
    url(r'^reservation/$', reservation.list_reservations, name='reservationList')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)