# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0001_initial'),
        ('client', '0001_initial'),
        ('Entite', '0001_initial'),
        ('livreur', '0001_initial'),
        ('localite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('idCommande', models.AutoField(serialize=False, primary_key=True, db_column='idCommande')),
                ('numero', models.CharField(max_length=50, null=True, db_column='numero')),
                ('longitude', models.CharField(max_length=20, null=True, db_column='longitude')),
                ('latitude', models.CharField(max_length=20, null=True, db_column='latitude')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('dateLivraicon', models.DateTimeField(null=True, db_column='dateLivraicon')),
                ('dateValidation', models.DateTimeField(null=True, db_column='dateValidation')),
                ('datePreparation', models.DateTimeField(null=True, db_column='datePreparation')),
                ('lastRelance', models.DateTimeField(null=True, db_column='lastRelance')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('estValider', models.IntegerField(default=0, db_column='estValider')),
                ('isSynch', models.IntegerField(default=0, db_column='isSynch')),
                ('enCoursDepreparion', models.IntegerField(default=0, db_column='enCoursDepreparion')),
                ('estLivrer', models.IntegerField(default=0, db_column='estLivrer')),
                ('state', models.IntegerField(default=0, db_column='state')),
                ('relancer', models.IntegerField(default=0, db_column='relancer')),
                ('estEstEnCoursDeLivraison', models.IntegerField(default=0, db_column='estEstEnCoursDeLivraison')),
                ('client', models.ForeignKey(to='client.Client', db_column='client')),
                ('entite', models.ForeignKey(db_column='entite', to='Entite.Entite', null=True)),
                ('livreur', models.ForeignKey(db_column='livreur', to='livreur.Livreur', null=True)),
                ('localite', models.ForeignKey(db_column='localite', to='localite.Localite', null=True)),
                ('manager', models.ForeignKey(db_column='manager', to='utilisateur.Utilisateur', null=True)),
            ],
            options={
                'db_table': 'commande',
            },
        ),
    ]
