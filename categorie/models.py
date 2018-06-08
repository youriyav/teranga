from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from Entite.models import Entite
from image.models import Image


class Categorie(models.Model):
    idCategorie = models.AutoField(db_column='idCategorie',primary_key=True)
    entite=models.ForeignKey(Entite,db_column='entite')
    libelleCat= models.CharField(db_column='libelleCat',max_length=100)
    descriptionCat= models.CharField(db_column='descriptionCat',null=True,max_length=500)
    logoCat= models.ForeignKey(Image,db_column='logoCat',null=True)
    dateCreation= models.DateTimeField(db_column="dateCreation",default=timezone.now)
    dateModification= models.DateTimeField(db_column="dateModification",null=True)
    createurCat=models.ForeignKey(User,db_column="createurCat",related_name="createurCat",null=False)
    modificateurCat=models.ForeignKey(User,db_column="modificateurCat",related_name="modificateurCat",null=True)
    estSupprimer=models.IntegerField(db_column="estSupprimer",default=0)
    estDesactiver = models.IntegerField(db_column="estDesactiver", default=0)
    estModifier=models.IntegerField(db_column="estModifier",default=0)
    class Meta:
        db_table = 'categorie'
