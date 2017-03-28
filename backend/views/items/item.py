from backend.models import ItemType, Item
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required
from backend.forms import ItemForm, ItemTypeForm


@login_required
def list_item_types(request):
    items = ItemType.objects.all()

    return render(request, 'itemList.html', {'title': 'Items', 'items': items})


@login_required
def add_item_type(request):
    if request.method == "POST":
        form = ItemTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # for now redirect back to item listings. Until detailed page is done
            return redirect('itemList')
    else:
        form = ItemTypeForm()
        form2 = ItemForm()
        return render(request, 'addItemType.html', {'title': 'Add Item', 'form': form, 'form2': form2})


@login_required
def show_item_type(request, item_type_id):
    item = get_object_or_404(ItemType, pk=item_type_id)

    return render(request, 'itemDetailed.html', {'title': item.name, 'item': item})


@login_required
def edit_item_type(request, item_type_id):
    item_type = get_object_or_404(ItemType, pk=item_type_id)
    if request.method == "POST":
        form = ItemTypeForm(request.POST, request.FILES, instance=item_type)
        if form.is_valid():
            form.save()
            # for now redirect back to item listings. Until detailed page is done
            return redirect('itemList')
    else:
        form = ItemTypeForm(instance=item_type)
        return render(request, 'editItem.html', {'title': "Edit: " + item_type.name, 'form': form, 'item': item_type})


@login_required
def delete_item_type(request,item_type_id):
    print("deleting item type")


@login_required
def add_item(request, item_type_id, item_id):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.ItemTypeID = item_type_id
            obj.save()
            # for now redirect back to the same page
            return redirect('itemList')
    else:
        form = ItemForm()
        return render(request, 'addItem.html', {'title': 'Add Item', 'form': form})


@login_required
def edit_item(request,item_type_id,item_id):
    item = get_object_or_404(Item, pk=item_id)
    itemType = get_object_or_404(ItemType, pk=item_type_id)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            # for now redirect back to item listings. Until detailed page is done
            return redirect('itemList')
    else:
        form = ItemForm(instance=item)
        return render(request, 'editItem.html', {'title': "Edit: " + item.name, 'form': form, 'item': item, 'itemType':
                itemType})


@login_required
def list_items(request,item_type_id):
    items = Item.objects.filter(ItemTypeID=item_type_id)

    return render(request, 'itemList.html', {'title': 'Items', 'items': items})


@login_required
def show_item(request,item_type_id,item_id):
    item = get_object_or_404(ItemType, pk=item_id, ItemTypeID=item_type_id)
    itemType = get_object_or_404(Item, pk=item_type_id)

    return render(request, 'itemDetailed.html', {'title': item.name, 'itemType': itemType, 'item':item})


