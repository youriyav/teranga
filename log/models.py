from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Log(models.Model):
    idLog = models.AutoField(db_column='idLog',primary_key=True)
    utilisateur=models.CharField(db_column="utilisateur",max_length=100,null=True)
    dateLog=models.DateTimeField(db_column="dateLog",default=timezone.now)
    action=models.CharField(db_column="action",max_length=100)
    class Meta:
        db_table = 'log'