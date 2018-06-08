# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('idVersion', models.AutoField(serialize=False, primary_key=True, db_column='idVersion')),
                ('key', models.CharField(max_length=20, db_column='key')),
                ('value', models.IntegerField(db_column='value')),
                ('dateCreation', models.DateTimeField(default=datetime.datetime.now, db_column='dateCreation')),
                ('dateUpdate', models.DateTimeField(null=True, db_column='dateUpdate')),
            ],
            options={
                'db_table': 'version',
            },
        ),
    ]
