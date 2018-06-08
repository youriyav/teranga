from __future__ import unicode_literals



from django.db import models

# Create your models here.
from django.utils import timezone


class Parametre(models.Model):
    idParametre = models.AutoField(db_column='idParametre',primary_key=True)
    key=models.CharField(db_column="key",max_length=20,null=True)
    dateParametre=models.DateTimeField(db_column="dateParametre",default=timezone.now)
    value=models.CharField(db_column="value",max_length=300)
    class Meta:
        db_table = 'paremetre'