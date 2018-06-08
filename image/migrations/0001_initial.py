# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('idImage', models.AutoField(serialize=False, primary_key=True, db_column='idImage')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('libelle', models.CharField(max_length=100, null=True, db_column='libelle')),
                ('saveName', models.CharField(max_length=100, null=True, db_column='saveName')),
                ('description', models.CharField(max_length=100, null=True, db_column='description')),
                ('type', models.IntegerField(default=0, db_column='type')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
            ],
            options={
                'db_table': 'image',
            },
        ),
    ]
