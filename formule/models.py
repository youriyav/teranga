from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from Entite.models import Entite
from categorie.models import Categorie


class Formule(models.Model):
    idFormule = models.AutoField(db_column='idFormule',primary_key=True)
    nomFormule= models.CharField(db_column='nomFormule',max_length=100)
    descriptFormule= models.TextField(db_column='descriptFormule',null=True,default="")
    logoFormule= models.CharField(db_column='logoFormule',null=True,max_length=200)
    prixFormule= models.CharField(db_column='prixFormule',null=True,max_length=6)
    dateCreation= models.DateTimeField(db_column="dateCreation",default=timezone.now)
    dateModification= models.DateTimeField(db_column="dateModification",null=True)
    createurFormule=models.ForeignKey(User,db_column="createurFormule",related_name="createurFormule",null=False)
    entite=models.ForeignKey(Entite,db_column="entite",null=False)
    modificateurFormule=models.ForeignKey(User,db_column="modificateurFormule",related_name="modificateurFormule",null=True)
    estSupprimer=models.IntegerField(db_column="estSupprimer",default=0)
    estDesactiver = models.IntegerField(db_column="estDesactiver", default=0)
    estModifier=models.IntegerField(db_column="estModifier",default=0)
    class Meta:
        db_table = 'formule'
