# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0013_auto_20150610_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='trigger',
            name='attrib_cur_val',
            field=models.CharField(max_length=30, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trigger',
            name='is_triggered',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
