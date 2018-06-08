# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('idValidation', models.AutoField(serialize=False, primary_key=True, db_column='idValidation')),
                ('keyValidation', models.TextField(null=True, db_column='keyValidation')),
                ('dateCreation', models.DateTimeField(default=datetime.datetime.now, db_column='dateCreation')),
                ('estValider', models.IntegerField(default=0, db_column='estValider')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('estConfirmer', models.IntegerField(default=0, db_column='estConfirmer')),
                ('client', models.ForeignKey(to='client.Client', db_column='user')),
            ],
            options={
                'db_table': 'validation',
            },
        ),
    ]
