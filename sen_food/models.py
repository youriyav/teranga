from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Personne(models.Model):
    idPersonne = models.AutoField(db_column='idPersonne',primary_key=True)
    nomPersonne= models.CharField(db_column='nomPersonne',max_length=100)
    prenomPersonne= models.CharField(db_column='prenomPersonne',max_length=100)
    profilPersonne= models.CharField(db_column='profilPersonne',max_length=50,null=True,default="")
    numeroPersonne= models.CharField(db_column='numeroPersonne',max_length=20,default="")
    emailPersonne = models.CharField(db_column='emailPersonne', max_length=100, default="")
    dateCreation = models.DateTimeField(db_column="dateCreation",default=timezone.now)
    createur=models.ForeignKey(User,db_column="createur",related_name="createur",null=True)
    modificateur=models.ForeignKey(User,db_column="modificateur",null=True,related_name="modificateur")
    dateModification = models.DateTimeField(db_column="dateModification", null=True)
    estSupprimer = models.IntegerField(db_column="estSupprimer", default=0)
    estModifier = models.IntegerField(db_column="estModifier", default=0)
    class Meta:
        db_table = 'personne'