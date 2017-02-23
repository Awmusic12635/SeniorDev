from backend.models import Item
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required
from backend.forms import ItemForm


@login_required
def list_items(request):
    items = Item.objects.all()

    return render(request, 'itemList.html', {'title': 'Items', 'items': items})


@login_required
def add_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            # for now redirect back to item listings. Until detailed page is done
            return redirect('itemList')
    else:
        form = ItemForm()
        return render(request, 'addItem.html', {'title': 'Add Item', 'form': form})


@login_required
def show_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    return render(request, 'itemDetailed.html', {'title': item.name, 'item': item})


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            # for now redirect back to item listings. Until detailed page is done
            return redirect('itemList')
    else:
        form = ItemForm(instance=item)
        return render(request, 'editItem.html', {'title': "Edit: " + item.name, 'form': form, 'item': item})
