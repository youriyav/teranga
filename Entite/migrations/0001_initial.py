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
            name='Entite',
            fields=[
                ('idEntit', models.AutoField(serialize=False, primary_key=True, db_column='idEntite')),
                ('nomEntite', models.CharField(max_length=100, db_column='nomEntite')),
                ('sloganEntite', models.CharField(max_length=300, null=True, db_column='sloganEntite')),
                ('numeroEntite', models.CharField(max_length=20, null=True, db_column='numeroEntite')),
                ('emailEntite', models.EmailField(max_length=200, null=True, db_column='emailEntite')),
                ('logoEntite', models.CharField(max_length=200, null=True, db_column='logoEntite')),
                ('couvertureEntite', models.EmailField(max_length=200, null=True, db_column='couvertureEntite')),
                ('ColeurEntite', models.EmailField(max_length=200, null=True, db_column='ColeurEntite')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('dateModification', models.DateTimeField(null=True, db_column='dateModification')),
                ('estSupprimer', models.IntegerField(default=0, db_column='estSupprimer')),
                ('estDesactiver', models.IntegerField(default=1, db_column='estDesactiver')),
                ('estModifier', models.IntegerField(default=0, db_column='estModifier')),
                ('createurEntite', models.ForeignKey(related_name='createurEntite', db_column='createurEntite', to=settings.AUTH_USER_MODEL)),
                ('modificateurEntite', models.OneToOneField(related_name='modificateurEntite', null=True, db_column='modificateurEntite', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'entite',
            },
        ),
    ]
