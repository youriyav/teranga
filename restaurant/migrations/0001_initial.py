# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Entite', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('idRestaurant', models.AutoField(serialize=False, primary_key=True, db_column='idRestaurant')),
                ('nomRestaurant', models.CharField(max_length=100, db_column='nomRestaurant')),
                ('numeroRestaurant', models.CharField(max_length=20, null=True, db_column='numeroRestaurant')),
                ('emailRestaurant', models.EmailField(max_length=200, null=True, db_column='emailRestaurant')),
                ('logoRestaurant', models.CharField(max_length=200, null=True, db_column='logoRestaurant')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('dateModification', models.DateTimeField(null=True, db_column='dateModification')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('estDesactiver', models.IntegerField(default=0, db_column='estDesactiver')),
                ('longiRestaurant', models.CharField(max_length=20, null=True, db_column='longiRestaurant')),
                ('latiRestaurant', models.CharField(max_length=20, null=True, db_column='latiRestaurant')),
                ('estModifier', models.IntegerField(default=0, db_column='estModifier')),
                ('quartierRestaurant', models.CharField(max_length=30, null=True, db_column='quartierRestaurant')),
                ('createurRestaurant', models.ForeignKey(related_name='createurRestaurant', db_column='createurRestaurant', to=settings.AUTH_USER_MODEL)),
                ('entite', models.ForeignKey(to='Entite.Entite', db_column='entite')),
                ('modificateurRestaurant', models.ForeignKey(related_name='modificateurRestaurant', db_column='modificateurRestaurant', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'restaurant',
            },
        ),
    ]
