from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from backend.forms import ItemCategoryForm
from backend.models import ItemCategory
from pinax.eventlog.models import log


@login_required
def list_categories(request):
    cats =  ItemCategory.objects.all()
    return render(request, 'categoryList.html', {'categories': cats})


@login_required
def view_category(request, category_id):
    category = get_object_or_404(ItemCategory, pk=category_id)
    return render(request, 'categoryDetailed.html', {'category': category})


@login_required
def add_category(request):
    if request.method == "POST":
        form = ItemCategoryForm(request.POST)
        if form.is_valid():
            obj = form.save()
            log(
                user=request.user,
                action="CATEGORY_CREATED",
                obj=obj,
                extra={
                }
            )

            # for now redirect back to the same page
            return redirect('categoryList')
    else:
        form = ItemCategoryForm()
        return render(request, 'addCategory.html', {'title': 'Add Category', 'form': form})


@login_required
def edit_category(request,category_id):
    cat = get_object_or_404(ItemCategory, pk=category_id)
    if request.method == "POST":
        form = ItemCategoryForm(request.POST, instance=cat)
        if form.is_valid():
            obj = form.save(commit=False)
            oldValues = obj.tracker.changed()
            # build the extras for the log
            obj.save()

            extras = {}
            for key in oldValues:
                extras.update({'old-' + key: oldValues[key]})
                extras.update({'new-' + key: obj.tracker.previous(key)})

            log(
                user=request.user,
                action="CATEGORY_MODIFIED",
                obj=obj,
                extra=extras
            )

            # for now redirect back to item listings. Until detailed page is done
            return redirect('categoryList')
    else:
        form = ItemCategoryForm(instance=cat)
        return render(request, 'editCategory.html', {'title': "Edit: " + cat.categoryName, 'form': form, 'category': cat, })