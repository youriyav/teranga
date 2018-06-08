# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sen_food', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Livreur',
            fields=[
                ('idLivreur', models.AutoField(serialize=False, primary_key=True, db_column='idLivreur')),
                ('code', models.CharField(max_length=6, null=True, db_column='code')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('lastUpdate', models.DateTimeField(null=True, db_column='lastUpdate')),
                ('lastLogin', models.DateTimeField(null=True, db_column='lastLogin')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('estActif', models.IntegerField(default=1, db_column='estActif')),
                ('longitude', models.CharField(max_length=20, null=True, db_column='longitude')),
                ('latitude', models.CharField(max_length=20, null=True, db_column='latitude')),
                ('personne', models.OneToOneField(db_column='personne', to='sen_food.Personne')),
            ],
            options={
                'db_table': 'livreur',
            },
        ),
    ]
