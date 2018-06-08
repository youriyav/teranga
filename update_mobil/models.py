from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from Entite.models import Entite
from datetime import datetime
#table
    #1:fastFood
    #2:categorie
    #3:produit
#type:
    #1:insertion
    #2:update
    #3:delete
class Version(models.Model):
    idVersion = models.AutoField(db_column='idVersion',primary_key=True)
    key = models.CharField(db_column='key',max_length=20)
    value = models.IntegerField(db_column='value')
    dateCreation = models.DateTimeField(db_column="dateCreation", default=datetime.now)
    dateUpdate = models.DateTimeField(db_column="dateUpdate", null=True)
    class Meta:
        db_table = 'version'
