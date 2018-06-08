from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from Entite.models import Entite
from sen_food.models import Personne
from django.utils import timezone

class Localite(models.Model):
    idLocalite = models.AutoField(db_column='idLocalite',primary_key=True)
    isActive=models.IntegerField(db_column="estBloquer",default=0)
    isSuggest=models.IntegerField(db_column="isSuggest",default=0)
    libelle=models.CharField(db_column="libelle",max_length=50,null=True)
    dateCreation = models.DateTimeField(db_column="dateCreation", default=timezone.now)
    estSupprimer=models.IntegerField(db_column="estSupprimer",default=0)
    personne=models.ForeignKey(User, db_column="personne",null=True)
    class Meta:
        db_table = 'localite'