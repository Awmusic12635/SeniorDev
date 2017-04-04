# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-26 15:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('criteria', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckInListItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('order', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckInListResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('response', models.CharField(max_length=100)),
                ('inOrOut', models.CharField(max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckInOrOutList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('inOrOut', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckInOrOutListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('prompt', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('dateTimeOut', models.DateTimeField(null=True)),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('signatureFormFile', models.CharField(max_length=400, null=True)),
                ('checkedOutBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checked_out_by_person', to=settings.AUTH_USER_MODEL)),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checkedout_to_person', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckoutItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('dateTimeDue', models.DateTimeField(null=True)),
                ('dueDateOverridden', models.BooleanField(default=False)),
                ('checkoutPermissionOverridden', models.BooleanField(default=False)),
                ('dateTimeIn', models.DateTimeField(null=True)),
                ('checkedInBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checked_in_by_person', to=settings.AUTH_USER_MODEL)),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Checkout')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('serial', models.CharField(max_length=200)),
                ('tag', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('checkoutStatus', models.CharField(default='Checked in', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('categoryDescription', models.CharField(max_length=500)),
                ('categoryName', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemStateLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('dateTimeChanged', models.DateTimeField()),
                ('changedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Item')),
                ('itemState', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ItemState')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('subCategoryName', models.CharField(max_length=100)),
                ('subCategoryDescription', models.CharField(max_length=500)),
                ('defaultCheckoutLengthDays', models.IntegerField(null=True)),
                ('itemCategoryID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ItemCategory')),
                ('parentSubCategoryID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.ItemSubCategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('defaultCheckoutLengthDays', models.IntegerField(null=True)),
                ('image', models.FileField(null=True, upload_to='uploads/itemImages')),
                ('manufacturer', models.CharField(max_length=100, null=True)),
                ('model', models.CharField(max_length=200, null=True)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('generalAccessRule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.AccessRule')),
                ('subCategoryID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.ItemSubCategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('lengthOfCheckout', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('itemTypeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ItemType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReservationRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('classRequestedFor', models.CharField(max_length=100)),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('lengthOfCheckout', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('approvedOn', models.DateTimeField()),
                ('approvedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to=settings.AUTH_USER_MODEL)),
                ('itemCategoryID', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.ItemCategory')),
                ('itemSubCategoryID', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.ItemSubCategory')),
                ('itemTypeID', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.ItemType')),
                ('personRequestedFor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requested_for', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResponseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='reservation',
            name='reservationRequestID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ReservationRequest'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='ItemTypeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ItemType'),
        ),
        migrations.AddField(
            model_name='item',
            name='itemState',
            field=models.ManyToManyField(null=True, through='backend.ItemStateLog', to='backend.ItemState'),
        ),
        migrations.AddField(
            model_name='checkoutitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Item'),
        ),
        migrations.AddField(
            model_name='checkinoroutlistitem',
            name='responseTypeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ResponseType'),
        ),
        migrations.AddField(
            model_name='checkinoroutlist',
            name='checkInListItems',
            field=models.ManyToManyField(through='backend.CheckInListItems', to='backend.CheckInOrOutListItem'),
        ),
        migrations.AddField(
            model_name='checkinoroutlist',
            name='itemCategoryID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ItemCategory'),
        ),
        migrations.AddField(
            model_name='checkinoroutlist',
            name='itemID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Item'),
        ),
        migrations.AddField(
            model_name='checkinoroutlist',
            name='itemSubCategoryID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ItemSubCategory'),
        ),
        migrations.AddField(
            model_name='checkinlistresults',
            name='checkInOrOutListItem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.CheckInOrOutListItem'),
        ),
        migrations.AddField(
            model_name='checkinlistresults',
            name='checkout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Checkout'),
        ),
        migrations.AddField(
            model_name='checkinlistitems',
            name='checkInOrOutList',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.CheckInOrOutList'),
        ),
        migrations.AddField(
            model_name='checkinlistitems',
            name='checkInOrOutListItem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.CheckInOrOutListItem'),
        ),
    ]
