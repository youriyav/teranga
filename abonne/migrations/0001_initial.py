# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Abonne',
            fields=[
                ('idAbonne', models.AutoField(serialize=False, primary_key=True, db_column='idAbonne')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('email', models.CharField(max_length=200, null=True, db_column='email')),
            ],
        ),
    ]
