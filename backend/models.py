from django.db import models
from django.contrib.auth.models import User

#classes with no FKs


class AccessRule(models.Model):
    name = models.CharField(max_length=100)
    criteria = models.CharField(max_length=200)


class ResponseType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)


class ItemState(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)


class ItemCategory(models.Model):
    categoryDescription = models.CharField(max_length=500)
    categoryName = models.CharField(max_length=100)


#classes with FKs


class CheckInOrOutListItem(models.Model):
    prompt = models.CharField(max_length=100)
    responseTypeID = models.ForeignKey(ResponseType, on_delete=models.CASCADE)


class ItemSubCategory(models.Model):
    itemCategoryID = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    subCategoryName = models.CharField(max_length=100)
    subCategoryDescription = models.CharField(max_length=500)
    parentSubCategoryID = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    defaultCheckoutLengthDays = models.IntegerField(null=True)


class ItemType(models.model):
    subCategoryID = models.ForeignKey(ItemSubCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    defaultCheckoutLengthDays = models.IntegerField(null=True)
    image = models.FileField(upload_to='uploads/itemImages', null= True)
    generalAccessRule = models.ForeignKey(AccessRule, on_delete=models.CASCADE, null=True)
    manufacturer = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=200, null=True)
    cost = models.DecimalField(decimal_places=2,max_digits=10, null=True)


class Item(models.Model):
    ItemTypeID = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    serial = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    itemState = models.ManyToManyField(ItemState, through='ItemStateLog', null=True)
    checkoutStatus = models.CharField(max_length=50, default="Checked in")


class ItemStateLog(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    itemState = models.ForeignKey(ItemState, on_delete=models.CASCADE)
    dateTimeChanged = models.DateTimeField()
    changedBy = models.ForeignKey(User, on_delete=models.CASCADE)


class CheckInOrOutList(models.Model):
    itemCategoryID = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    itemSubCategoryID = models.ForeignKey(ItemSubCategory, on_delete=models.CASCADE)
    itemID = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    inOrOut = models.CharField(max_length=3)  # nullable boolean?
    description = models.CharField(max_length=500)
    checkInListItems = models.ManyToManyField(CheckInOrOutListItem, through='CheckInListItems')


class CheckInListItems(models.Model):
    checkInOrOutList = models.ForeignKey(CheckInOrOutList, on_delete=models.CASCADE)
    checkInOrOutListItem = models.ForeignKey(CheckInOrOutListItem, on_delete=models.CASCADE)
    order = models.IntegerField()


class Checkout(models.Model):
    person = models.ForeignKey(User, related_name='checkedout_to_person', on_delete=models.CASCADE, null=True)
    dateTimeOut = models.DateTimeField(null=True)
    checkedOutBy = models.ForeignKey(User,related_name='checked_out_by_person', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, default="Pending")
    signatureFormFile = models.CharField(max_length=400, null=True)  # use a file field?
    #checkInListResults = models.ManyToManyField(CheckInOrOutList, through='CheckInListResults')


class CheckoutItem(models.Model):
    dateTimeDue = models.DateTimeField(null=True)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    dueDateOverridden = models.BooleanField(default=False)
    checkoutPermissionOverridden = models.BooleanField(default=False)
    dateTimeIn = models.DateTimeField(null=True)
    checkedInBy = models.ForeignKey(User,related_name='checked_in_by_person', on_delete=models.CASCADE, null=True)


class CheckInListResults(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    checkInOrOutListItem = models.ForeignKey(CheckInOrOutListItem)
    response = models.CharField(max_length=100)
    inOrOut = models.CharField(max_length=3)  # nullable boolean?


class ReservationRequest(models.Model):
    itemCategoryID = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, db_constraint=False, blank=True, null=True)
    itemSubCategoryID = models.ForeignKey(ItemSubCategory, on_delete=models.CASCADE, db_constraint=False, blank=True, null=True)
    itemTypeID = models.ForeignKey(ItemType, db_constraint=False, blank=True, null=True)
    requester = models.ForeignKey(User, related_name='requested_by', on_delete=models.CASCADE)
    personRequestedFor = models.ForeignKey(User,related_name='requested_for', on_delete=models.CASCADE, blank=True, null=True)
    classRequestedFor = models.CharField(max_length=100)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    lengthOfCheckout = models.IntegerField()
    quantity = models.IntegerField()
    approvedBy = models.ForeignKey(User, related_name='approved_by', on_delete=models.CASCADE)
    approvedOn = models.DateTimeField()


class Reservation(models.Model):
    itemTypeID = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    lengthOfCheckout = models.IntegerField()
    quantity = models.IntegerField()
    reservationRequestID = models.ForeignKey(ReservationRequest, on_delete=models.CASCADE)
