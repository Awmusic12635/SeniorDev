# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-27 21:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20170425_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtype',
            name='needsSignature',
            field=models.BooleanField(default=False),
        ),
    ]