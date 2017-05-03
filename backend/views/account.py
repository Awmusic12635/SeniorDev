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
    return render(request, 'account.html', {'title': 'User Account', 'form': UserChangeForm(user=request.user)})


@login_required
def edit_user(request, user_id):
    if request.method == "POST":
        form = UserChangeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            # for now redirect back to item listings. Until detailed page is done

            log(
                user=request.user,
                action="USER_CHANGED_PASSWORD",
                obj=obj,
                extra={
                }
            )
            return redirect('itemList')
    return show(request)

