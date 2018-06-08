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
            name='Terminal',
            fields=[
                ('idTerminal', models.AutoField(serialize=False, primary_key=True, db_column='idTerminal')),
                ('numero', models.CharField(max_length=15, null=True, db_column='numero')),
                ('numeroSerie', models.CharField(max_length=50, null=True, db_column='numeroSerie')),
                ('model', models.CharField(max_length=50, null=True, db_column='model')),
                ('marque', models.CharField(max_length=50, null=True, db_column='marque')),
                ('token', models.TextField(db_column='token')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('lastUpdate', models.DateTimeField(null=True, db_column='lastUpdate')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('estActif', models.IntegerField(default=1, db_column='estActif')),
                ('isLivreur', models.IntegerField(default=0, db_column='isLivreur')),
                ('longitude', models.CharField(max_length=20, null=True, db_column='longitude')),
                ('latitude', models.CharField(max_length=20, null=True, db_column='latitude')),
                ('utilisateur', models.OneToOneField(null=True, db_column='utilisateur', to='sen_food.Personne')),
            ],
            options={
                'db_table': 'terminal',
            },
        ),
    ]
