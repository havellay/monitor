# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0007_auto_20150604_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trigger',
            name='attrib',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
