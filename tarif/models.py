from django.db import models
from django.utils import timezone
# Create your models here.
class Tarif(models.Model):
    idTarif = models.AutoField(db_column='idTarif',primary_key=True)
    prix= models.IntegerField(db_column='prix')
    distanceMin= models.IntegerField(db_column='distanceMin',default=0)
    distanceMax= models.IntegerField(db_column='distanceMax',default=0)
    libelle=models.IntegerField(db_column="libelle")
    estSupprimer=models.IntegerField(db_column="estSupprimer",default=0)
    dateCreation= models.DateTimeField(db_column="dateCreation",default=timezone.now)
    class Meta:
        db_table = 'tarif'