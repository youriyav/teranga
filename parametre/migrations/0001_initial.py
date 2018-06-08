# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parametre',
            fields=[
                ('idParametre', models.AutoField(serialize=False, primary_key=True, db_column='idParametre')),
                ('key', models.CharField(max_length=20, null=True, db_column='key')),
                ('dateParametre', models.DateTimeField(default=django.utils.timezone.now, db_column='dateParametre')),
                ('value', models.CharField(max_length=300, db_column='value')),
            ],
            options={
                'db_table': 'paremetre',
            },
        ),
    ]
