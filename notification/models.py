from __future__ import unicode_literals

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from Entite.models import Entite
from client.models import Client

class Notification(models.Model):
    idNotification = models.AutoField(db_column='idNotification',primary_key=True)
    client=models.ForeignKey(Client,db_column="client")
    Notitype=models.IntegerField(db_column="type", default=0)
    is_read=models.IntegerField(db_column="is_read", default=0)
    is_sync=models.IntegerField(db_column="is_sync", default=0)
    dateCreation = models.DateTimeField(db_column="dateCreation", default=timezone.now)
    content = models.CharField(db_column="content",max_length=300)
    titre = models.CharField(db_column="titre",null=True,max_length=50)
    url = models.CharField(db_column="url",null=True,max_length=250)
    class Meta:
        db_table = 'notification'