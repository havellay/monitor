# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_auto_20150604_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbol',
            name='name',
            field=models.CharField(unique=True, max_length=30),
            preserve_default=True,
        ),
    ]
