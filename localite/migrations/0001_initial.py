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
            name='Localite',
            fields=[
                ('idLocalite', models.AutoField(serialize=False, primary_key=True, db_column='idLocalite')),
                ('isActive', models.IntegerField(default=0, db_column='estBloquer')),
                ('isSuggest', models.IntegerField(default=0, db_column='isSuggest')),
                ('libelle', models.CharField(max_length=50, null=True, db_column='libelle')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('personne', models.ForeignKey(db_column='personne', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'localite',
            },
        ),
    ]
