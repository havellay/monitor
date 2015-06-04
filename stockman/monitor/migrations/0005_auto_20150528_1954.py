# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20150527_1649'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eod',
            options={'ordering': ['date']},
        ),
        migrations.AlterModelOptions(
            name='intraday',
            options={'ordering': ['time']},
        ),
        migrations.AlterUniqueTogether(
            name='eod',
            unique_together=set([('symbol', 'date')]),
        ),
        migrations.AlterUniqueTogether(
            name='intraday',
            unique_together=set([('symbol', 'time')]),
        ),
    ]
