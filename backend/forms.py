from django import forms
from .models import Item, ItemCategory, ItemSubCategory, Checkout


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


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ('person', 'dateTimeOut', 'checkedOutBy', 'checkedInBy', 'status', 'signatureFormFile')