# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20150526_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eod',
            name='date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='intraday',
            name='time',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
