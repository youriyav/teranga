from __future__ import unicode_literals

import datetime
from django.db import models

# Create your models here.
from django.utils import timezone

from sen_food.models import Personne


class Terminal(models.Model):
    idTerminal = models.AutoField(db_column='idTerminal',primary_key=True)
    numero = models.CharField(db_column="numero", null=True, max_length=15)
    numeroSerie = models.CharField(db_column="numeroSerie", null=True, max_length=50)
    model = models.CharField(db_column="model", null=True, max_length=50)
    marque = models.CharField(db_column="marque", null=True, max_length=50)
    token=models.TextField(db_column="token")
    dateCreation = models.DateTimeField(db_column="dateCreation", default=timezone.now)
    lastUpdate = models.DateTimeField(db_column="lastUpdate", null=True)
    estSupprimer = models.IntegerField(db_column="estSupprimer", default=0)
    estActif = models.IntegerField(db_column="estActif", default=1)
    isLivreur = models.IntegerField(db_column="isLivreur", default=0)
    longitude = models.CharField(db_column="longitude", null=True, max_length=20)
    latitude = models.CharField(db_column="latitude", null=True, max_length=20)
    utilisateur=models.OneToOneField(Personne,db_column='utilisateur',null=True)
    def get_lastUpdate(self):
        tmp = self.dateCreation
        date_save = datetime.strftime(tmp, '%Y-%m-%d %H:%M:%S')
        currentDate = datetime.now()
        diff = currentDate - datetime.strptime(date_save, '%Y-%m-%d %H:%M:%S')
        return  diff.seconds/60
    class Meta:
        db_table = 'terminal'