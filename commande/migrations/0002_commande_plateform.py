# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commande', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='plateform',
            field=models.IntegerField(default=0, db_column='plateform'),
        ),
    ]
