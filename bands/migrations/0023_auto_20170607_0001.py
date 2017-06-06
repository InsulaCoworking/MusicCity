# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-06 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0022_auto_20170606_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='billinginfo',
            name='additional_text',
            field=models.TextField(blank=True, null=True, verbose_name='Observaciones'),
        ),
        migrations.AddField(
            model_name='billinginfo',
            name='multiple_bands',
            field=models.BooleanField(default=False, verbose_name='Factura a m\xe1s de una banda'),
        ),
    ]