from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import logging

from backend.models import Checkout
from backend.models import CheckoutItem
from django.core.exceptions import ObjectDoesNotExist

CONST_STATUS_PENDING = "Pending"
logger = logging.getLogger('ted')

@login_required
def get_pending_checkout(request):
    #get pending checkout if there is one
    checkout = Checkout.objects.filter(status=CONST_STATUS_PENDING)
    logger.debug('old'+ checkout)
    logger.debug('old'+ checkout.id)
    if checkout is None:
        checkout = Checkout(status = CONST_STATUS_PENDING)
        checkout.save()
        logger.debug('new' +checkout)
        logger.debug('new' +checkout.id)
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': checkout})

