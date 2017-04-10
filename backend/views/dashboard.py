from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from backend.models import CheckoutItem, ItemType, Item


@login_required
def show(request):
    items = Item.objects.all()
    numberOfItems = items.count()
    numberOfItemsInInventory = Item.objects.all().count() - CheckoutItem.objects.all().count()
    numberOfItemsCheckedOut = CheckoutItem.objects.all().count()
    numberOfItemsDueToday = CheckoutItem.objects.filter(dateTimeDue__gte = datetime.today()).count()
    itemTypes = ItemType.objects.all()
    itemsInfo = []
    for itemType in itemTypes:
        itemInfo = (itemType, items.filter(ItemTypeID_id = itemType.id).count())
        itemsInfo.append(itemInfo)
    return render(request, 'dashboard.html', {
        'title': 'Dashboard',
        'numberOfItemsInInventory': numberOfItemsInInventory,
        'numberOfItemsCheckedOut' : numberOfItemsCheckedOut,
        'numberOfItems'           : numberOfItems,
        'numberOfItemsDueToday'   : numberOfItemsDueToday,
        'itemTypes'               : itemsInfo
    })


