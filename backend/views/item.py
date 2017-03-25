from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from backend.models import Item


@login_required
def listItems(request):
    context = {'item_list': Item.objects.all()}
    return render(request, 'app/itemList.html', context)


@login_required
def getItemByID(request, item_id):
    context = {'item': Item.objects.get(pk=item_id)}
    return render(request, 'app/itemView.html', context)


@login_required
def deleteItem(request, item_id):
    context = {'deleted': Item.objects.filter(pk=item_id).delete()}
    return render(request, 'app/itemDelete.html', context)


@login_required
def createItem(request):
    item = Item()
    item.subCategoryID = request.POST['subCategoryID']
    item.name = request.POST['name']
    item.description = request.POST['description']
    item.manufacturer = request.POST['manufacturer']
    item.model = request.POST['model']
    item.serial = request.POST['serial']
    item.tag = request.POST['tag']
    item.cost = request.POST['cost']
    item.location = request.POST['location']
    item.generalAccessRule = request.POST['generalAccessRule']
    #item state
    item.save()
    return HttpResponseRedirect(reverse('app/itemView.html', args=(item.id,)))


@login_required
def updateItem(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.subCategoryID = request.POST['subCategoryID']
    item.name = request.POST['name']
    item.description = request.POST['description']
    item.manufacturer = request.POST['manufacturer']
    item.model = request.POST['model']
    item.serial = request.POST['serial']
    item.tag = request.POST['tag']
    item.cost = request.POST['cost']
    item.location = request.POST['location']
    item.generalAccessRule = request.POST['generalAccessRule']
    #item state
    context = {'saved':item.save()}
    return HttpResponseRedirect(reverse('app/itemView.html', args=(item.id,)))