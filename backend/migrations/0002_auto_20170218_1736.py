# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 17:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckoutItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTimeDue', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='checkout',
            name='expectedDateTimeIn',
        ),
        migrations.RemoveField(
            model_name='checkout',
            name='itemID',
        ),
        migrations.AddField(
            model_name='checkout',
            name='status',
            field=models.CharField(default='open', max_length=50),
        ),
        migrations.AddField(
            model_name='item',
            name='checkoutStatus',
            field=models.CharField(default='CheckedIn', max_length=50),
        ),
        migrations.AddField(
            model_name='checkoutitem',
            name='checkout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Checkout'),
        ),
        migrations.AddField(
            model_name='checkoutitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Item'),
        ),
    ]
