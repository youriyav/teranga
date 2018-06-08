from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# Create your models here.
class Visite(models.Model):
    idVisite= models.AutoField(db_column='idVisite',primary_key=True)
    dateVisite = models.DateTimeField(db_column="dateVisite", default=timezone.now)
    device = models.CharField(db_column="device", null=True, max_length=200)
    browser = models.CharField(db_column="browser", null=True, max_length=200)