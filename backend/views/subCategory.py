from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from backend.forms import ItemSubCategoryForm
from backend.models import ItemSubCategory


@login_required
def list_subcategories(request):
    subcats = ItemSubCategory.objects.all()
    return render(request, 'subCategoryList.html', {'subcategories': subcats})


@login_required
def view_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(ItemSubCategory, pk=subcategory_id)
    return render(request, 'subCategoryDetailed.html', {'subcategory': subcategory})


@login_required
def add_subcategory(request):
    if request.method == "POST":
        form = ItemSubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # for now redirect back to the same page
            return redirect('subcategoryList')
    else:
        form = ItemSubCategoryForm()
        return render(request, 'addSubCategory.html', {'title': 'Add Sub Category', 'form': form})


@login_required
def edit_subcategory(request,subcategory_id):
    subcat = get_object_or_404(ItemSubCategory, pk=subcategory_id)
    if request.method == "POST":
        form = ItemSubCategoryForm(request.POST, instance=subcat)
        if form.is_valid():
            form.save()
            # for now redirect back to item listings. Until detailed page is done
            return redirect('subcategoryList')
    else:
        form = ItemSubCategoryForm(instance=subcat)
        return render(request, 'editSubCategory.html', {'title': "Edit: " + subcat.subCategoryName, 'form': form, 'subcategory': subcat, })