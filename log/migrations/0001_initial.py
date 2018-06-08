# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('idLog', models.AutoField(serialize=False, primary_key=True, db_column='idLog')),
                ('utilisateur', models.CharField(max_length=100, null=True, db_column='utilisateur')),
                ('dateLog', models.DateTimeField(default=django.utils.timezone.now, db_column='dateLog')),
                ('action', models.CharField(max_length=100, db_column='action')),
            ],
            options={
                'db_table': 'log',
            },
        ),
    ]
