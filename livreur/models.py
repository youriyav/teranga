from __future__ import unicode_literals

import datetime
from django.db import models

# Create your models here.
from django.utils import timezone

from sen_food.models import Personne


class Livreur(models.Model):
    idLivreur = models.AutoField(db_column='idLivreur',primary_key=True)
    code = models.CharField(db_column="code", null=True, max_length=6)
    personne=models.OneToOneField(Personne,db_column="personne")
    dateCreation = models.DateTimeField(db_column="dateCreation", default=timezone.now)
    lastUpdate = models.DateTimeField(db_column="lastUpdate", null=True)
    lastLogin = models.DateTimeField(db_column="lastLogin",null=True)
    estSupprimer = models.IntegerField(db_column="estSupprimer", default=0)
    estActif = models.IntegerField(db_column="estActif", default=1)
    longitude = models.CharField(db_column="longitude", null=True, max_length=20)
    latitude = models.CharField(db_column="latitude", null=True, max_length=20)
    def get_lastUpdate(self):
        tmp = self.dateCreation
        date_save = datetime.strftime(tmp, '%Y-%m-%d %H:%M:%S')
        currentDate = datetime.now()
        diff = currentDate - datetime.strptime(date_save, '%Y-%m-%d %H:%M:%S')
        return  diff.seconds/60
    class Meta:
        db_table = 'livreur'