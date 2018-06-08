# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Entite', '0002_entite_ispartern'),
    ]

    operations = [
        migrations.AddField(
            model_name='entite',
            name='latitude',
            field=models.CharField(default='', max_length=30, null=True, db_column='latitude'),
        ),
        migrations.AddField(
            model_name='entite',
            name='longitude',
            field=models.CharField(default='', max_length=30, null=True, db_column='longitude'),
        ),
    ]
