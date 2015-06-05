# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0009_config'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='config',
            name='blah',
        ),
        migrations.AlterField(
            model_name='config',
            name='predicate',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
