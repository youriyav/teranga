from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from Entite.models import Entite
from sen_food.models import Personne


class Client(models.Model):
    idclient = models.AutoField(db_column='idclient',primary_key=True)
    user=models.OneToOneField(User,db_column="user")
    personne=models.OneToOneField(Personne,db_column="personne")
    estBloquer=models.IntegerField(db_column="estBloquer",default=0)
    code=models.CharField(db_column="tmp_code",max_length=8,null=True)
    type=models.IntegerField(db_column="type",null=True)
    class Meta:
        db_table = 'client'