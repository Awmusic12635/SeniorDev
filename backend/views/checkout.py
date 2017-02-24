from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from backend.models import Checkout, CheckoutItem, Item
from django.core.exceptions import ObjectDoesNotExist

CONST_STATUS_PENDING = "Pending"
CONST_STATUS_CHECKEDIN = "Checked in"

@login_required
def get_pending_checkout(request):
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': get_pending_checkout})


def add_item(request, item_id):
    checkout = get_pending_checkout
    item = get_object_or_404(Item, pk=int(item_id))
    ci = CheckoutItem(checkout = checkout, item = item)
    ci.save()

    item.checkoutStatus = CONST_STATUS_PENDING
    item.save()

    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': checkout})


def remove_item(request, item_id):
    item = get_object_or_404(Item, pk=int(item_id))
    checkout = get_pending_checkout
    ci = CheckoutItem.objects.filter(item=item, checkout=checkout)
    ci.delete()

    item.checkoutStatus = CONST_STATUS_CHECKEDIN
    item.save()

    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': checkout})


def get_pending_checkout():
    checkout = Checkout.objects.filter(status=CONST_STATUS_PENDING).first()
    if checkout is None:
        checkout = Checkout(status=CONST_STATUS_PENDING)
        checkout.save()
    return checkout