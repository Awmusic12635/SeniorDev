from backend.models import ItemType, Item, ItemCategory, ItemSubCategory
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required
from backend.forms import ItemForm, ItemTypeForm
from pinax.eventlog.models import log


@login_required
def list_item_types(request):
    items = ItemType.objects.all()

    return render(request, 'itemTypeList.html', {'title': 'Items', 'items': items})


@login_required
def add_item_type(request):
    if request.method == "POST":
        form = ItemTypeForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.subCategoryID = get_object_or_404(ItemSubCategory, pk=request.POST['subCategory'])
            obj.save()
            # for now redirect back to item listings. Until detailed page is done

            log(
                user=request.user,
                action="ITEM_TYPE_CREATED",
                obj=obj,
                extra={
                }
            )
            return redirect('itemList')
    else:
        form = ItemTypeForm()
        form2 = ItemForm()
        categories = ItemCategory.objects.all()
        subcategories = ItemSubCategory.objects.all()
        return render(request, 'addItemType.html', {'title': 'Add Item', 'form': form, 'form2': form2, 'categories': categories, 'subcategories': subcategories})


@login_required
def show_item_type(request, item_type_id):
    itemType = get_object_or_404(ItemType, pk=item_type_id)

    return render(request, 'itemDetailed.html', {'title': itemType.name, 'itemType': itemType})


@login_required
def edit_item_type(request, item_type_id):
    item_type = get_object_or_404(ItemType, pk=item_type_id)
    if request.method == "POST":
        form = ItemTypeForm(request.POST, request.FILES, instance=item_type)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.subCategoryID = get_object_or_404(ItemSubCategory, pk=request.POST['subCategory'])
            oldValues = obj.tracker.changed()
            obj.save()

            #build the extras for the log
            extras = {}
            for key,value in oldValues:
                extras.update({'old'+key: value})
                extras.update({'new'+key: obj.tracker.previous(key)})

            log(
                user=request.user,
                action="ITEM_TYPE_MODIFIED",
                obj=obj,
                extra=extras
            )
            # for now redirect back to item listings. Until detailed page is done
            return redirect('itemList')
    else:
        form = ItemTypeForm(instance=item_type)
        categories = ItemCategory.objects.all()
        subcategories = ItemSubCategory.objects.all()
        catID = item_type.subCategoryID.itemCategoryID.id
        return render(request, 'editItemType.html', {'title': "Edit: " + item_type.name, 'form': form, 'item': item_type, 'categories': categories, 'subcategories': subcategories, 'categoryid': catID})


@login_required
def delete_item_type(request,item_type_id):
    log(
        user=request.user,
        action="ITEM_TYPE_DELETED",
        obj=item_type_id,
        extra={
        }
    )
    print("deleting item type")


@login_required
def add_item(request, item_type_id):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.ItemTypeID = get_object_or_404(ItemType, pk=item_type_id)
            obj.save()

            log(
                user=request.user,
                action="ITEM_CREATED",
                obj=obj,
                extra={
                }
            )
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
            log(
                user=request.user,
                action="ITEM_MODIFIED",
                obj=item,
                extra={
                }
            )
            return redirect('itemList')
    else:
        form = ItemForm(instance=item)
        return render(request, 'editItem.html', {'title': "Edit: " + itemType.name, 'form': form, 'item': item, 'itemType':
                itemType})


@login_required
def list_items(request,item_type_id):
    items = Item.objects.filter(ItemTypeID=item_type_id)

    return render(request, 'itemList.html', {'title': 'Items', 'items': items, 'item_type_id':item_type_id})


@login_required
def show_item(request,item_type_id,item_id):
    itemType = get_object_or_404(ItemType, pk= item_type_id)
    item = get_object_or_404(Item, pk=item_id)

    return render(request, 'itemDetailed.html', {'title': itemType.name, 'itemType': itemType, 'item':item})


