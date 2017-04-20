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


def find_user_name(request, username):
    ldap_users = ldap.get_user_by_username(username)
    ret_arr = []
    for user in ldap_users:
        ret_arr.append({'name': str(user.cn), 'username': str(user.uid)})
    return HttpResponse(json.dumps({'users': ret_arr}), content_type="application/json")


def find_user_id(request, uid):
    ldap_users = ldap.get_user_by_universityid(uid)
    ret_arr = []
    for user in ldap_users:
        ret_arr.append({'name': str(user.cn), 'username': str(user.uid)})
    return HttpResponse(json.dumps({'users': ret_arr}), content_type="application/json")


def add_user(request, checkout_id, username):
    checkout = Checkout.objects.get(pk=checkout_id)

    #is this user in our table already
    user = ''
    users = User.objects.filter(username = username)
    if not users:
        #get them from ldap again
        ldap_user = ldap.get_user_by_username(username)
        #add them
        user = User.objects.create_user(username=username, email = ldap.get_email(ldap_user))
        user.first_name=ldap.get_first_name(ldap_user)
        user.last_name=ldap.get_last_name(ldap_user)
        user.save()
    else:
        user = users[0]

    checkout.person = user;
    checkout.save()
    return get_pending_checkout(request)