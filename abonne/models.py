from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils import timezone


class Abonne(models.Model):
    idAbonne= models.AutoField(db_column='idAbonne',primary_key=True)
    dateCreation = models.DateTimeField(db_column="dateCreation", default=timezone.now)
    email = models.CharField(db_column="email", null=True, max_length=200)