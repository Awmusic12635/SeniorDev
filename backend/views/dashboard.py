from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from backend.models import CheckoutItem, ItemType, Item



@login_required
def show(request):
    return render(request, 'dashboard.html', get_dashboard_context())


@login_required
def search(request):
    search_text = request.POST['search']
    items = ItemType.objects.filter(name__contains=search_text)

    context = get_dashboard_context()
    context['items'] = items
    context['searchedText'] = search_text
    context['searched'] = True

    return render(request,'dashboard.html',context)


def get_dashboard_context():
    items = Item.objects.all()
    numberOfItems = items.count()
    numberOfItemsInInventory = Item.objects.all().count() - CheckoutItem.objects.all().count()
    numberOfItemsCheckedOut = CheckoutItem.objects.all().count()
    numberOfItemsDueToday = CheckoutItem.objects.filter(dateTimeDue__gte=datetime.today()).count()
    return {
        'title': 'Dashboard',
        'numberOfItemsInInventory': numberOfItemsInInventory,
        'numberOfItemsCheckedOut' : numberOfItemsCheckedOut,
        'numberOfItems'           : numberOfItems,
        'numberOfItemsDueToday'   : numberOfItemsDueToday
    }