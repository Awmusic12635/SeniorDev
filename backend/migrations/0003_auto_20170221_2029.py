# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 20:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20170218_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='generalAccessRule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.AccessRule'),
        ),
        migrations.AlterField(
            model_name='item',
            name='itemState',
            field=models.ManyToManyField(null=True, through='backend.ItemStateLog', to='backend.ItemState'),
        ),
        migrations.AlterField(
            model_name='item',
            name='subCategoryID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.ItemSubCategory'),
        ),
    ]