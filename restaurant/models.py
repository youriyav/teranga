from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from Entite.models import Entite


class Restaurant(models.Model):
    idRestaurant= models.AutoField(db_column='idRestaurant',primary_key=True)
    nomRestaurant= models.CharField(db_column='nomRestaurant',max_length=100)
    numeroRestaurant= models.CharField(db_column='numeroRestaurant',null=True,max_length=20)
    emailRestaurant= models.EmailField(db_column='emailRestaurant',null=True,max_length=200)
    logoRestaurant= models.CharField(db_column='logoRestaurant',null=True,max_length=200)
    dateCreation= models.DateTimeField(db_column="dateCreation",default=timezone.now)
    dateModification= models.DateTimeField(db_column="dateModification",null=True)
    createurRestaurant=models.ForeignKey(User,db_column="createurRestaurant",related_name="createurRestaurant",null=False)
    modificateurRestaurant=models.ForeignKey(User,db_column="modificateurRestaurant",related_name="modificateurRestaurant",null=True)
    estSupprimer=models.IntegerField(db_column="estSupprimer",default=0)
    estDesactiver = models.IntegerField(db_column="estDesactiver", default=0)
    longiRestaurant = models.CharField(db_column='longiRestaurant', null=True, max_length=20)
    latiRestaurant = models.CharField(db_column='latiRestaurant', null=True, max_length=20)
    estModifier=models.IntegerField(db_column="estModifier",default=0)
    quartierRestaurant = models.CharField(db_column='quartierRestaurant', null=True, max_length=30)
    entite=models.ForeignKey(Entite,db_column="entite")
    class Meta:
        db_table = 'restaurant'
