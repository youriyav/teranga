# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
        ('Entite', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('idCategorie', models.AutoField(serialize=False, primary_key=True, db_column='idCategorie')),
                ('libelleCat', models.CharField(max_length=100, db_column='libelleCat')),
                ('descriptionCat', models.CharField(max_length=500, null=True, db_column='descriptionCat')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('dateModification', models.DateTimeField(null=True, db_column='dateModification')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('estDesactiver', models.IntegerField(default=0, db_column='estDesactiver')),
                ('estModifier', models.IntegerField(default=0, db_column='estModifier')),
                ('createurCat', models.ForeignKey(related_name='createurCat', db_column='createurCat', to=settings.AUTH_USER_MODEL)),
                ('entite', models.ForeignKey(to='Entite.Entite', db_column='entite')),
                ('logoCat', models.ForeignKey(db_column='logoCat', to='image.Image', null=True)),
                ('modificateurCat', models.ForeignKey(related_name='modificateurCat', db_column='modificateurCat', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'categorie',
            },
        ),
    ]
