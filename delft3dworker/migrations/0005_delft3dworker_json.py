# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 15:30
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('delft3dworker', '0004_auto_20160201_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='delft3dworker',
            name='json',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
