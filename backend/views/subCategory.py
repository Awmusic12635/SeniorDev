from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from backend.forms import ItemSubCategoryForm
from backend.models import ItemSubCategory, ItemCategory
from backend.views import category

@login_required
def list_subcategories(request):
    subcats = ItemSubCategory.objects.all()
    return render(request, 'subCategoryList.html', {'subcategories': subcats})


@login_required
def view_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(ItemSubCategory, pk=subcategory_id)
    return render(request, 'subCategoryDetailed.html', {'subcategory': subcategory})


@login_required
def add_subcategory(request, category_id=None):
    if request.method == "POST":
        form = ItemSubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # for now redirect back to the same page
            if category_id is None:
                return redirect('subcategoryList')
            else:
                return redirect('categoryView')
                #return category.view_category(request, category_id)
    else:
        sub = ItemSubCategory
        if category_id is not None:
            sub.itemCategoryID = get_object_or_404(ItemCategory, pk= category_id)
        form = ItemSubCategoryForm(instance=sub)
        return render(request, 'addSubCategory.html', {'title': 'Add Sub Category', 'form': form, 'categoryID':category_id})


@login_required
def edit_subcategory(request,subcategory_id, category_id=None):
    subcat = get_object_or_404(ItemSubCategory, pk=subcategory_id)
    if request.method == "POST":
        form = ItemSubCategoryForm(request.POST, instance=subcat)
        if form.is_valid():
            form.save()
            # for now redirect back to item listings. Until detailed page is done
            if category_id is None:
                return redirect('subcategoryList')
            else:
                return redirect('categoryView')
    else:
        form = ItemSubCategoryForm(instance=subcat)
        action = ''
        if category_id is None:
            action = '/subcategory/' + subcat.id + '/edit'
        else:
            action = '/subcategory/' +category_id+'/'+ subcat.id + '/edit'
        return render(request, 'editSubCategory.html', {'title': "Edit: " + subcat.subCategoryName, 'form': form, 'subcategory': subcat, 'action':action })