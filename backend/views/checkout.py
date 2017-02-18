from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from backend.models import Checkout

@login_required
def checkoutItems(request):
    checkout = Checkout()
    checkout.person = request.POST['student']
    checkout.dateTimeOut = request.POST['dateTimeOut']
    checkout.checkedOutBy = request.POST['checkedOutBy']
    checkout.status = 'Open'

    #item state
    checkout.save()
    return HttpResponseRedirect(reverse('app/itemView.html', args=(checkout.id,)))