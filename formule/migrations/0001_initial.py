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
            name='Formule',
            fields=[
                ('idFormule', models.AutoField(serialize=False, primary_key=True, db_column='idFormule')),
                ('nomFormule', models.CharField(max_length=100, db_column='nomFormule')),
                ('descriptFormule', models.TextField(default='', null=True, db_column='descriptFormule')),
                ('logoFormule', models.CharField(max_length=200, null=True, db_column='logoFormule')),
                ('prixFormule', models.CharField(max_length=6, null=True, db_column='prixFormule')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('dateModification', models.DateTimeField(null=True, db_column='dateModification')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('estDesactiver', models.IntegerField(default=0, db_column='estDesactiver')),
                ('estModifier', models.IntegerField(default=0, db_column='estModifier')),
                ('createurFormule', models.ForeignKey(related_name='createurFormule', db_column='createurFormule', to=settings.AUTH_USER_MODEL)),
                ('entite', models.ForeignKey(to='Entite.Entite', db_column='entite')),
                ('modificateurFormule', models.ForeignKey(related_name='modificateurFormule', db_column='modificateurFormule', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'formule',
            },
        ),
    ]
