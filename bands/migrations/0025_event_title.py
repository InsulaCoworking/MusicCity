# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-02 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0024_auto_20170902_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.TextField(blank=True, null=True, verbose_name=b'T\xc3\xadtulo del evento'),
        ),
    ]
