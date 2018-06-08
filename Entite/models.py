from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Entite(models.Model):
    idEntit = models.AutoField(db_column='idEntite',primary_key=True)
    nomEntite= models.CharField(db_column='nomEntite',max_length=100)
    sloganEntite= models.CharField(db_column='sloganEntite',null=True,max_length=300)
    longitude= models.CharField(db_column='longitude',null=True,max_length=30,default="")
    latitude= models.CharField(db_column='latitude',null=True,max_length=30,default="")
    numeroEntite= models.CharField(db_column='numeroEntite',null=True,max_length=20)
    emailEntite= models.EmailField(db_column='emailEntite',null=True,max_length=200)
    logoEntite= models.CharField(db_column='logoEntite',null=True,max_length=200)
    couvertureEntite= models.EmailField(db_column='couvertureEntite',null=True,max_length=200)
    ColeurEntite= models.EmailField(db_column='ColeurEntite',null=True,max_length=200)
    dateCreation= models.DateTimeField(db_column="dateCreation",default=timezone.now)
    dateModification= models.DateTimeField(db_column="dateModification",null=True)
    createurEntite=models.ForeignKey(User,db_column="createurEntite",related_name="createurEntite",null=False)
    modificateurEntite=models.OneToOneField(User,db_column="modificateurEntite",related_name="modificateurEntite",null=True)
    estSupprimer=models.IntegerField(db_column="estSupprimer",default=0)
    estDesactiver = models.IntegerField(db_column="estDesactiver", default=1)
    estModifier=models.IntegerField(db_column="estModifier",default=0)
    isPartern=models.IntegerField(db_column="isPartern",default=0,null=True)
    class Meta:
        db_table = 'entite'
