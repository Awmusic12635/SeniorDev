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
    #get pending checkout if there is one
    checkout = Checkout.objects.filter(status=CONST_STATUS_PENDING)
    if checkout is None:
        checkout = Checkout()
        checkout.status = CONST_STATUS_PENDING
        checkout.save()
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': checkout})

