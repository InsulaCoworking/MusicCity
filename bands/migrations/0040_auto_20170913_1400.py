# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-13 12:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0039_auto_20170911_1652'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venue',
            options={'ordering': ['name'], 'permissions': (('manage_venue', 'Puede gestionar un espacio'),), 'verbose_name': 'Escenario', 'verbose_name_plural': 'Escenarios'},
        ),
    ]