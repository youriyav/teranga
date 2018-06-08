# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visite',
            fields=[
                ('idVisite', models.AutoField(serialize=False, primary_key=True, db_column='idVisite')),
                ('dateVisite', models.DateTimeField(default=django.utils.timezone.now, db_column='dateVisite')),
                ('device', models.CharField(max_length=200, null=True, db_column='device')),
                ('browser', models.CharField(max_length=200, null=True, db_column='browser')),
            ],
        ),
    ]
