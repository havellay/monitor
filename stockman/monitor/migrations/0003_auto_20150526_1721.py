# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20150522_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='symbol',
            name='nse_symbol',
            field=models.CharField(max_length=30, verbose_name=b'NSE India Symbol', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='symbol',
            name='g_symbol',
            field=models.CharField(max_length=30, verbose_name=b'Google Symbol', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='symbol',
            name='y_symbol',
            field=models.CharField(max_length=30, verbose_name=b'Yahoo Symbol', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
    ]
