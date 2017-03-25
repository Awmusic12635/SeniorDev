from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from backend.models import ItemCategory
from backend.models import ItemSubCategory


@login_required
def lisSubtCategories(request):
    context = {'subCategory_list': ItemSubCategory.objects.all()}
    return render(request, 'app/subCategoryList.html', context)


@login_required
def getSubCategoryByID(request, subCategory_id):
    context = {'subCategory': ItemSubCategory.objects.get(pk=subCategory_id)}
    return render(request, 'app/subCategoryView.html', context)


@login_required
def getSubCategoryByParentSubID(request, subCategory_id):
    context = {'subCategories': ItemSubCategory.objects.filter(parentSubCategoryID=subCategory_id)}
    return render(request, 'app/subCategoryView.html', context)


@login_required
def getSubCategoryByCategoryID(request, category_id):
    context = {'subCategories': ItemSubCategory.objects.filter(itemCategoryID=category_id)}
    return render(request, 'app/subCategoryView.html', context)


@login_required
def deleteSubCategory(request, subCategory_id):
    context = {'deleted': ItemSubCategory.objects.filter(pk=subCategory_id).delete()}
    return render(request, 'app/subCategoryDelete.html', context)


@login_required
def createSubCategory(request):
    subCategory = ItemSubCategory()
    subCategory.itemCategoryID = request.POST['itemCategoryID']
    subCategory.subCategoryName = request.POST['subCategoryName']
    subCategory.subCategoryDescription = request.POST['subCategoryDescription']
    subCategory.parentSubCategoryID = request.POST['parentSubcategoryID']
    subCategory.save()
    return HttpResponseRedirect(reverse('app/subCategoryView.html', args=(subCategory.id,)))


@login_required
def updateCategory(request, category_id):
    subCategory = get_object_or_404(ItemSubCategory, pk=category_id)
    subCategory.itemCategoryID = request.POST['itemCategoryID']
    subCategory.subCategoryName = request.POST['subCategoryName']
    subCategory.subCategoryDescription = request.POST['subCategoryDescription']
    subCategory.parentSubCategoryID = request.POST['parentSubcategoryID']
    subCategory.save()
    return HttpResponseRedirect(reverse('app/subCategoryView.html', args=(subCategory.id,)))
