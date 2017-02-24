from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from backend.models import Checkout
from backend.models import CheckoutItem
from django.core.exceptions import ObjectDoesNotExist

CONST_STATUS_PENDING = "Pending"

@login_required
def get_pending_checkout(request):
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': create_pending_checkout})


def add_item(request, item_id):
    checkout = create_pending_checkout()
    ci = CheckoutItem()
    ci.checkout = checkout.id
    ci.item = item_id
    ci.save()
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': checkout})


def create_pending_checkout():
    checkout = Checkout.objects.filter(status=CONST_STATUS_PENDING).first()
    if checkout is None:
        checkout = Checkout(status=CONST_STATUS_PENDING)
        checkout.save()
    return checkout