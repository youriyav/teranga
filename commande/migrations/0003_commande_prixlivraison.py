# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commande', '0002_commande_plateform'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='prixLivraison',
            field=models.IntegerField(default=0, db_column='prixLivraison'),
        ),
    ]
