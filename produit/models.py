from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from categorie.models import Categorie
from image.models import Image


class Produit(models.Model):
    idProduit = models.AutoField(db_column='idProduit',primary_key=True)
    nomProduit= models.CharField(db_column='nomProduit',max_length=100)
    descriptProduit= models.CharField(db_column='descriptProduit',null=True,default="",max_length=500)
    logoProduit=  models.ForeignKey(Image,db_column='logoProduit',null=True)
    prixProduit= models.CharField(db_column='prixProduit',null=True,max_length=6)
    categorie=models.ForeignKey(Categorie,db_column='categorie',null=True)
    dateCreation= models.DateTimeField(db_column="dateCreation",default=timezone.now)
    dateModification= models.DateTimeField(db_column="dateModification",null=True)
    createurProduit=models.ForeignKey(User,db_column="createurProduit",related_name="createurProduit",null=True)
    modificateurProduit=models.ForeignKey(User,db_column="modificateurProduit",related_name="modificateurProduit",null=True)
    estSupprimer=models.IntegerField(db_column="estSupprimer",default=0)
    estDesactiver = models.IntegerField(db_column="estDesactiver", default=0)
    estModifier=models.IntegerField(db_column="estModifier",default=0)
    isTmp=models.IntegerField(db_column="isTmp",default=0)
    class Meta:
        db_table = 'produit'
