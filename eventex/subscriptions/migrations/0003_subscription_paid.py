# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-20 04:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_auto_20161215_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]