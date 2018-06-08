# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commande', '0001_initial'),
        ('produit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('idLigne', models.AutoField(serialize=False, primary_key=True, db_column='idLigne')),
                ('quantite', models.IntegerField(db_column='quantite')),
                ('commande', models.ForeignKey(db_column='commande', to='commande.Commande', null=True)),
                ('produit', models.ForeignKey(to='produit.Produit', db_column='produit')),
            ],
            options={
                'db_table': 'ligne_commande',
            },
        ),
    ]
