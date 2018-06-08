# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sen_food', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('idclient', models.AutoField(serialize=False, primary_key=True, db_column='idclient')),
                ('estBloquer', models.IntegerField(default=0, db_column='estBloquer')),
                ('code', models.CharField(max_length=8, null=True, db_column='tmp_code')),
                ('type', models.IntegerField(null=True, db_column='type')),
                ('personne', models.OneToOneField(db_column='personne', to='sen_food.Personne')),
                ('user', models.OneToOneField(db_column='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'client',
            },
        ),
    ]
