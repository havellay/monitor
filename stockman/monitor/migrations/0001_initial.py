# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EoD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('close_qt', models.DecimalField(max_digits=9, decimal_places=2)),
                ('open_qt', models.DecimalField(max_digits=9, decimal_places=2)),
                ('high_qt', models.DecimalField(max_digits=9, decimal_places=2)),
                ('low_qt', models.DecimalField(max_digits=9, decimal_places=2)),
                ('volume', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Intraday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('quote', models.DecimalField(max_digits=9, decimal_places=2)),
                ('volume', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('y_symbol', models.CharField(max_length=30)),
                ('g_symbol', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attrib', models.CharField(max_length=100)),
                ('trig_val', models.CharField(max_length=30)),
                ('bias', models.CharField(max_length=30)),
                ('reminder', models.ForeignKey(to='monitor.Reminder')),
                ('symbol', models.ForeignKey(to='monitor.Symbol')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=40)),
                ('username', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reminder',
            name='user',
            field=models.ForeignKey(to='monitor.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='intraday',
            name='symbol',
            field=models.ForeignKey(to='monitor.Symbol'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eod',
            name='symbol',
            field=models.ForeignKey(to='monitor.Symbol'),
            preserve_default=True,
        ),
    ]
