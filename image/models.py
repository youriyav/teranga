# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils import timezone


class Image(models.Model):
    idImage = models.AutoField(db_column='idImage',primary_key=True)
    dateCreation = models.DateTimeField(db_column="dateCreation", default=timezone.now)
    libelle = models.CharField(db_column="libelle", max_length=100, null=True)
    saveName = models.CharField(db_column="saveName", max_length=100, null=True)
    description = models.CharField(db_column="description", max_length=100, null=True)
    type=models.IntegerField(db_column="type",default=0)
    estSupprimer = models.IntegerField(db_column="estSupprimer", default=0)
    class Meta:
        db_table = 'image'