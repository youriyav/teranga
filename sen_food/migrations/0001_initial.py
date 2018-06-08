# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('idPersonne', models.AutoField(serialize=False, primary_key=True, db_column='idPersonne')),
                ('nomPersonne', models.CharField(max_length=100, db_column='nomPersonne')),
                ('prenomPersonne', models.CharField(max_length=100, db_column='prenomPersonne')),
                ('profilPersonne', models.CharField(default='', max_length=50, null=True, db_column='profilPersonne')),
                ('numeroPersonne', models.CharField(default='', max_length=20, db_column='numeroPersonne')),
                ('emailPersonne', models.CharField(default='', max_length=100, db_column='emailPersonne')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('dateModification', models.DateTimeField(null=True, db_column='dateModification')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('estModifier', models.IntegerField(default=0, db_column='estModifier')),
                ('createur', models.ForeignKey(related_name='createur', db_column='createur', to=settings.AUTH_USER_MODEL, null=True)),
                ('modificateur', models.ForeignKey(related_name='modificateur', db_column='modificateur', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'personne',
            },
        ),
    ]
