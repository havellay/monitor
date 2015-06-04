# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20150528_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbol',
            name='g_symbol',
            field=models.CharField(unique=True, max_length=30, verbose_name=b'Google Symbol', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='symbol',
            name='nse_symbol',
            field=models.CharField(unique=True, max_length=30, verbose_name=b'NSE India Symbol', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='symbol',
            name='y_symbol',
            field=models.CharField(unique=True, max_length=30, verbose_name=b'Yahoo Symbol', blank=True),
            preserve_default=True,
        ),
    ]
