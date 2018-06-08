# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('produit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='isTmp',
            field=models.IntegerField(default=0, db_column='isTmp'),
        ),
        migrations.AlterField(
            model_name='produit',
            name='categorie',
            field=models.ForeignKey(db_column='categorie', to='categorie.Categorie', null=True),
        ),
        migrations.AlterField(
            model_name='produit',
            name='createurProduit',
            field=models.ForeignKey(related_name='createurProduit', db_column='createurProduit', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='produit',
            name='logoProduit',
            field=models.ForeignKey(db_column='logoProduit', to='image.Image', null=True),
        ),
    ]
