# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_auto_20150605_1234'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('subject', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('predicate', models.CharField(max_length=50)),
                ('blah', models.CharField(max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
