from django import forms
from .models import Item, ItemCategory, ItemSubCategory


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'manufacturer', 'model', 'serial', 'tag', 'cost', 'location')


class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = ('categoryDescription', 'categoryName')


class ItemSubCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemSubCategory
        fields = ('subCategoryName', 'subCategoryDescription')
