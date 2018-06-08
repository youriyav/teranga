# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
        ('categorie', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('idProduit', models.AutoField(serialize=False, primary_key=True, db_column='idProduit')),
                ('nomProduit', models.CharField(max_length=100, db_column='nomProduit')),
                ('descriptProduit', models.CharField(default='', max_length=500, null=True, db_column='descriptProduit')),
                ('prixProduit', models.CharField(max_length=6, null=True, db_column='prixProduit')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('dateModification', models.DateTimeField(null=True, db_column='dateModification')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('estDesactiver', models.IntegerField(default=0, db_column='estDesactiver')),
                ('estModifier', models.IntegerField(default=0, db_column='estModifier')),
                ('categorie', models.ForeignKey(to='categorie.Categorie', db_column='categorie')),
                ('createurProduit', models.ForeignKey(related_name='createurProduit', db_column='createurProduit', to=settings.AUTH_USER_MODEL)),
                ('logoProduit', models.ForeignKey(to='image.Image', db_column='logoProduit')),
                ('modificateurProduit', models.ForeignKey(related_name='modificateurProduit', db_column='modificateurProduit', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'produit',
            },
        ),
    ]
