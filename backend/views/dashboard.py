from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from backend.models import CheckoutItem, ItemType, Item



@login_required
def show(request):
    items = Item.objects.all()
    numberOfItems = items.count()
    numberOfItemsInInventory = Item.objects.all().count() - CheckoutItem.objects.all().count()
    numberOfItemsCheckedOut = CheckoutItem.objects.all().count()
    numberOfItemsDueToday = CheckoutItem.objects.filter(dateTimeDue__gte = datetime.today()).count()
    return render(request, 'dashboard.html', {
        'title': 'Dashboard',
        'numberOfItemsInInventory': numberOfItemsInInventory,
        'numberOfItemsCheckedOut' : numberOfItemsCheckedOut,
        'numberOfItems'           : numberOfItems,
        'numberOfItemsDueToday'   : numberOfItemsDueToday
    })

def search(request):
    if request.is_ajax():
        search_text = request.POST['search_text']
    else:
        search_text = ''

    print(search_text)
    itemTypes = ItemType.objects.filter(name__contains=search_text)
    itemsInfo = []
    for itemType in itemTypes:
        itemInfo = (itemType, Item.objects.all().filter(ItemTypeID_id = itemType.id).count())
        itemsInfo.append(itemInfo)

    for itemType, quantity in itemsInfo:
        print(quantity)

    return render(request,'search.html',{'itemTypes':itemsInfo})


