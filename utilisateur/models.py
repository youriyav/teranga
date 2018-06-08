from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from Entite.models import Entite
from sen_food.models import Personne


class Utilisateur(models.Model):
    idUtilisateur = models.AutoField(db_column='idUtilisateur',primary_key=True)
    user=models.OneToOneField(User,db_column="user")
    personne=models.OneToOneField(Personne,db_column="personne")
    isManager=models.IntegerField(db_column="isManager")
    droit=models.IntegerField(db_column="droit")
    entite=models.ForeignKey(Entite,db_column='entite',null=True)
    class Meta:
        db_table = 'utilisateur'