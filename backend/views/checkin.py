from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from backend.models import Checkout, CheckoutItem, Item
from backend.forms import OverrideItemDueDate
from django.core.exceptions import ObjectDoesNotExist

CONST_STATUS_PENDING = "Pending"
CONST_STATUS_CHECKEDIN = "Checked in"
CONST_STATUS_CHECKEDOUT = "Checked out"
CONST_STATUS_OPEN = "Open"

@login_required
def get_open_checkouts(request):
    checkouts = Checkout.objects.filter(status=CONST_STATUS_OPEN)
    return render(request, 'checkin.html', {'title': 'Check In', 'checkouts': checkouts})


@login_required
def view_checkout(request, checkout_id):
    checkout = Checkout.objects.get(pk=checkout_id)
    return render(request, 'checkoutEdit.html', {'title': 'Check In', 'checkout': checkout})


@login_required
def checkin_item(request, checkoutitem_id):
    #fill checked in date for checkout item
    ci = CheckoutItem.objects.get(pk=checkoutitem_id)
    ci.dateTimeIn = datetime.now()

    #mark item as in
    item = Item.objects.get(pk=ci.item)
    item.checkoutStatus = CONST_STATUS_CHECKEDIN

    ci.save()
    item.save()

    return render(request, 'checkoutEdit.html', {'title': 'Check In', 'checkout': ci.checkout})