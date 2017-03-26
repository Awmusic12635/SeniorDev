from django import forms
from .models import Item, ItemCategory, ItemSubCategory, Checkout, CheckoutItem, ItemType


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('serial', 'tag', 'location', 'ItemTypeID')


class ItemTypeForm(forms.ModelForm):
    class Meta:
        model = ItemType
        fields = ('name', 'description', 'manufacturer', 'model', 'cost', 'image')


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
        fields = ('person', 'dateTimeOut', 'checkedOutBy', 'status', 'signatureFormFile')

