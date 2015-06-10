# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0012_auto_20150609_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='is_triggered',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trigger',
            name='is_triggered',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
