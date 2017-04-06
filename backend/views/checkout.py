from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from backend.models import Checkout, CheckoutItem, Item
from django.core.exceptions import ObjectDoesNotExist
from pinax.eventlog.models import log

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
        ci.save()

        log(
            user=request.user,
            action="CHECKOUT_DUE_DATE_OVERRIDE",
            obj=ci,
            extra={
            }
        )
    return render(request, 'checkout.html', {'title': 'Checkout', 'checkout':  ci.checkout})


def reset_duedate(request, checkoutitem_id):
    ci = CheckoutItem.objects.get(pk=checkoutitem_id)
    ci.dateTimeDue = datetime.now() + timedelta(days=getDefaultCheckoutLength(ci.item))
    ci.dueDateOverridden = False
    ci.save()

    log(
        user=request.user,
        action="CHECKOUT_DUE_DATE_RESET",
        obj=ci,
        extra={
        }
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