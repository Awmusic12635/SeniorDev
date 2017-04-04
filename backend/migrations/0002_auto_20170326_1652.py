# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-26 16:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationrequest',
            name='approvedBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reservationrequest',
            name='approvedOn',
            field=models.DateTimeField(null=True),
        ),
    ]
