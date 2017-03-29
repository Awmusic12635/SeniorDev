from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from backend.forms import ItemSubCategoryForm
from backend.models import ItemSubCategory, ItemCategory
from backend.views import category


@login_required
def view_subcategory(request, category_id, subcategory_id):
    subcategory = get_object_or_404(ItemSubCategory, pk=subcategory_id)
    return render(request, 'subCategoryDetailed.html', {'subcategory': subcategory})


@login_required
def add_subcategory(request, category_id):
    if request.method == "POST":
        form = ItemSubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # for now redirect back to the same page
            return redirect('categoryView')
    else:
        sub = ItemSubCategory
        sub.itemCategoryID = get_object_or_404(ItemCategory, pk= category_id)
        form = ItemSubCategoryForm(instance=sub)
        return render(request, 'addSubCategory.html', {'title': 'Add Sub Category', 'form': form, 'categoryID':category_id})


@login_required
def edit_subcategory(request,subcategory_id, category_id):
    subcat = get_object_or_404(ItemSubCategory, pk=subcategory_id)
    if request.method == "POST":
        form = ItemSubCategoryForm(request.POST, instance=subcat)
        if form.is_valid():
            form.save()
            return redirect('categoryView')
    else:
        form = ItemSubCategoryForm(instance=subcat)
        return render(request, 'editSubCategory.html', {'title': "Edit: " + subcat.subCategoryName, 'form': form, 'subcategory': subcat })
