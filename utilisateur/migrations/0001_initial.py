# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Entite', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sen_food', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('idUtilisateur', models.AutoField(serialize=False, primary_key=True, db_column='idUtilisateur')),
                ('isManager', models.IntegerField(db_column='isManager')),
                ('droit', models.IntegerField(db_column='droit')),
                ('entite', models.ForeignKey(db_column='entite', to='Entite.Entite', null=True)),
                ('personne', models.OneToOneField(db_column='personne', to='sen_food.Personne')),
                ('user', models.OneToOneField(db_column='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'utilisateur',
            },
        ),
    ]
