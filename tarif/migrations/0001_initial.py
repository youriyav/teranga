# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tarif',
            fields=[
                ('idTarif', models.AutoField(serialize=False, primary_key=True, db_column=b'idTarif')),
                ('prix', models.IntegerField(db_column=b'prix')),
                ('libelle', models.IntegerField(db_column=b'libelle')),
                ('estSupprimer', models.IntegerField(default=0, db_column=b'estSupprimer')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column=b'dateCreation')),
            ],
            options={
                'db_table': 'tarif',
            },
        ),
    ]
