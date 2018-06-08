from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
# Create your models here.
from django.utils import timezone

from client.models import Client


class Validation(models.Model):
    idValidation = models.AutoField(db_column='idValidation',primary_key=True)
    keyValidation= models.TextField(db_column='keyValidation',null=True)
    dateCreation = models.DateTimeField(db_column="dateCreation",default=datetime.now)
    client=models.ForeignKey(Client,db_column="user")
    estValider = models.IntegerField(db_column="estValider", default=0)
    estSupprimer = models.IntegerField(db_column="estSupprimer", default=0)
    estConfirmer = models.IntegerField(db_column="estConfirmer", default=0)
    class Meta:
        db_table = 'validation'