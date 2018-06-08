# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Entite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entite',
            name='isPartern',
            field=models.IntegerField(default=0, null=True, db_column='isPartern'),
        ),
    ]
