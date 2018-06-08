# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('commande', '0001_initial'),
        ('livreur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Livraison',
            fields=[
                ('idLivraison', models.AutoField(serialize=False, primary_key=True, db_column='idLivraison')),
                ('numero', models.CharField(max_length=10, null=True, db_column='numero')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('commande', models.OneToOneField(db_column='commande', to='commande.Commande')),
                ('livreur', models.OneToOneField(db_column='livreur', to='livreur.Livreur')),
            ],
            options={
                'db_table': 'livraison',
            },
        ),
    ]
