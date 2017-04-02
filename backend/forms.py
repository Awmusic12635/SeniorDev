from django import forms
from .models import Item, ItemCategory, ItemSubCategory, Checkout, CheckoutItem, ItemType, ReservationRequest, Reservation


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
        fields = ('categoryName', 'categoryDescription')


class ItemSubCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemSubCategory
        fields = ('subCategoryName', 'subCategoryDescription', 'defaultCheckoutLengthDays')


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ('person', 'dateTimeOut', 'checkedOutBy', 'status', 'signatureFormFile')


class ReservationRequestForm(forms.ModelForm):
    class Meta:
        model = ReservationRequest
        fields = ('itemSubCategoryID','itemTypeID','personRequestedFor','classRequestedFor','startDate','endDate','lengthOfCheckout','quantity')

    def clean(self):
        form_data = self.cleaned_data
        if form_data['itemSubCategoryID'] is None and form_data['itemTypeID'] is None:
            self._errors["Item"] = ["Must select a sub category or item"]
        if form_data['personRequestedFor'] is None and form_data['classRequestedFor']:
            self._errors["RequestedFor"] = ["Must request for a person or a class"]
        return form_data


class ReservationRequestApprovalForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('startDate','endDate','lengthOfCheckout','quantity')
