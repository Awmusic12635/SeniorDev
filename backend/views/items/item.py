from backend.models import Item
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required
from backend.forms import ItemForm


@login_required
def listItems(request):
    items = Item.objects.all()

    return render(request, 'itemList.html', {'items': items})


@login_required
def addItem(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            # for now redirect back to item listings. Until detailed page is done
            return redirect('itemList')
    else:
        form = ItemForm()
        return render(request, 'addItem.html', {'form': form})


@login_required
def showItem(request, id):
    item = get_object_or_404(Item, pk=id)

    return render(request, 'itemDetailed.html', {'item': item})