# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0011_auto_20150605_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbol',
            name='g_symbol',
            field=models.CharField(max_length=30, verbose_name=b'Google Symbol', blank=True),
            preserve_default=True,
        ),
    ]
