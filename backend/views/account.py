from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .ldap import ldap
from backend.models import Item, Checkout, CheckoutItem, User
from django.contrib.auth.models import UserManager
from django.contrib.auth.forms import UserChangeForm
from pinax.eventlog.models import log
from django.contrib.auth.decorators import login_required

@login_required
def show(request):
    return render(request, 'account.html', {'title': 'User Account'})


@login_required
def edit_user(request):
    if request.method == "POST":
        user = request.user

        if request.POST['password'] == request.POST['password2']:
            user.set_password(request.POST['password'])
            user.save()

        log(
            user=request.user,
            action="USER_MODIFIED",
            obj=user,
            extra={}
        )
    return show(request)

