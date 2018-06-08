# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarif', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarif',
            name='distanceMax',
            field=models.IntegerField(default=0, db_column=b'distanceMax'),
        ),
        migrations.AddField(
            model_name='tarif',
            name='distanceMin',
            field=models.IntegerField(default=0, db_column=b'distanceMin'),
        ),
    ]
