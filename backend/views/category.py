from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from backend.models import ItemCategory


@login_required
def listCategories(request):
    context = {'category_list': ItemCategory.objects.all()}
    return render(request, 'app/categoryList.html', context)


@login_required
def getCategoryByID(request, category_id):
    context = {'category': ItemCategory.objects.get(pk=category_id)}
    return render(request, 'app/categoryView.html', context)


@login_required
def deleteCategory(request, category_id):
    context = {'deleted': ItemCategory.objects.filter(pk=category_id).delete()}
    return render(request, 'app/categoryDelete.html', context)


@login_required
def createCategory(request):
    category = ItemCategory()
    category.categoryName = request.POST['categoryName']
    category.categoryDescription = request.POST['categoryDescription']
    category.save()
    return HttpResponseRedirect(reverse('app/categoryView.html', args=(category.id,)))


@login_required
def updateCategory(request, category_id):
    category = get_object_or_404(ItemCategory, pk=category_id)
    category.categoryName = request.POST['categoryName']
    category.categoryDescription = request.POST['categoryDescription']
    category.save()
    return HttpResponseRedirect(reverse('app/categoryView.html', args=(category.id,)))