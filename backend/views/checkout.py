from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import UserManager
from datetime import datetime, timedelta
from backend.models import Checkout, CheckoutItem, Item, User
from django.core.exceptions import ObjectDoesNotExist
from pinax.eventlog.models import log
from templated_email import send_templated_mail
from .ldap import ldap
import json

CONST_STATUS_PENDING = "Pending"
CONST_STATUS_CHECKEDIN = "Checked in"
CONST_STATUS_CHECKEDOUT = "Checked out"
CONST_STATUS_OPEN = "Open"


@login_required
def get_pending_checkout(request):
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': create_pending_checkout()})


def add_item(request, item_id):
    checkout = create_pending_checkout()
    item = get_object_or_404(Item, pk=int(item_id))
    # check for item already being checked out
    if item.checkoutStatus == CONST_STATUS_CHECKEDIN:
        ci = CheckoutItem(checkout = checkout, item = item)

        ci.dateTimeDue = datetime.now() + timedelta(days=getDefaultCheckoutLength(item))
        ci.save()

        item.checkoutStatus = CONST_STATUS_PENDING
        item.save()

        log(
            user=request.user,
            action="ITEM_ADDED_TO_CART",
            obj=item,
            extra={
            }
        )
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': checkout})


def remove_item(request, item_id):
    item = get_object_or_404(Item, pk=int(item_id))
    checkout = create_pending_checkout()
    ci = CheckoutItem.objects.filter(item=item, checkout=checkout)
    ci.delete()

    item.checkoutStatus = CONST_STATUS_CHECKEDIN
    item.save()

    log(
        user=request.user,
        action="ITEM_REMOVED_FROM_CART",
        obj=item,
        extra={
        }
    )
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': checkout})


def override_date(request, checkoutitem_id):
    ci = CheckoutItem.objects.get(pk=checkoutitem_id)
    if request.method == "POST":
        ci.dateTimeDue = request.POST['overrideDate']
        ci.dueDateOverridden = True
        oldValues = ci.tracker.changed()
        # build the extras for the log
        ci.save()

        extras = {}
        for key in oldValues:
            extras.update({'old-' + key: oldValues[key]})
            extras.update({'new-' + key: ci.tracker.previous(key)})
        log(
            user=request.user,
            action="CHECKOUT_DUE_DATE_OVERRIDE",
            obj=ci,
            extra=extras
        )
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout':  ci.checkout})


def reset_duedate(request, checkoutitem_id):
    ci = CheckoutItem.objects.get(pk=checkoutitem_id)
    ci.dateTimeDue = datetime.now() + timedelta(days=getDefaultCheckoutLength(ci.item))
    ci.dueDateOverridden = False
    oldValues = ci.tracker.changed()
    # build the extras for the log
    ci.save()

    extras = {}
    for key in oldValues:
        extras.update({'old-' + key: oldValues[key]})
        extras.update({'new-' + key: ci.tracker.previous(key)})

    log(
        user=request.user,
        action="CHECKOUT_DUE_DATE_RESET",
        obj=ci,
        extra=extras
    )
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout':  ci.checkout})


def clear(request):
    Item.objects.filter(checkoutStatus=CONST_STATUS_PENDING).update(checkoutStatus = CONST_STATUS_CHECKEDIN)
    CheckoutItem.objects.filter(checkout=create_pending_checkout()).delete()
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': create_pending_checkout()})


def complete(request):
    checkout = create_pending_checkout()
    checkout.status = CONST_STATUS_OPEN
    checkout.checkedOutBy = request.user
    checkout.dateTimeOut = datetime.now()
    checkout.save()


    log(
        user=request.user,
        action="CHECKOUT_CREATED",
        obj=checkout,
        extra={
        }
    )

    nSent = send_templated_mail(
        template_name='checkoutReceipt',
        recipient_list=[checkout.person.email],
        from_email=None,
        fail_silently=True,
        context={
            'checkout': checkout
        }
    )
    if nSent == 0:
        log(
            user=request.user,
            action="EMAIL_SENDING_FAILED",
            obj=None,
            extra={
                'email': 'checkoutReceipt',
                'recipient_list': [checkout.person.email]
            }
        )
    else:
        log(
            user=request.user,
            action="EMAIL_SENT",
            obj=None,
            extra={
                'email': 'checkoutReceipt',
                'recipient_list': [checkout.person.email]
            }
        )
    Item.objects.filter(checkoutStatus=CONST_STATUS_PENDING).update(checkoutStatus = CONST_STATUS_CHECKEDOUT)

    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout': create_pending_checkout()})


def create_pending_checkout():
    checkout = Checkout.objects.filter(status=CONST_STATUS_PENDING).first()
    if checkout is None:
        checkout = Checkout(status=CONST_STATUS_PENDING)
        checkout.save()
    return checkout


def getDefaultCheckoutLength(item):
    checkoutlength = 1

    if item.ItemTypeID.subCategoryID.defaultCheckoutLengthDays is not None:
        checkoutlength = item.ItemTypeID.subCategoryID.defaultCheckoutLengthDays

    if item.ItemTypeID.defaultCheckoutLengthDays is not None:
        checkoutlength = item.ItemTypeID.defaultCheckoutLengthDays

    return checkoutlength


def find_user(request, username):
    ldap_user = ldap.get_user_by_username(username)
    return HttpResponse(ldap_user.cn)


def add_user(request, checkout_id, username):
    checkout = Checkout.objects.get(pk=checkout_id)

    #is this user in our table already
    user = User.objects.filter(username = username)
    print('fetched:' + user)
    if user is None:
        print('need to make:' + user)
        #get them from ldap again
        ldap_user = ldap.get_user_by_username(username)
        name_parts = ldap_user.cn.split()
        #add them
        user = UserManager.create_user(username, email = username+'@rit.edu', first_name=name_parts[0], last_name=name_parts[1])
        print('made:' + user)

    print(user)
    checkout.person = user;
    checkout.save
    return get_pending_checkout()