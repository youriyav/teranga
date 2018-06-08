from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils import timezone

from commande.models import Commande
from livreur.models import Livreur


class Livraison(models.Model):
    idLivraison = models.AutoField(db_column='idLivraison',primary_key=True)
    numero = models.CharField(db_column="numero", null=True, max_length=10)
    livreur=models.OneToOneField(Livreur,db_column="livreur")
    commande=models.OneToOneField(Commande,db_column="commande")
    dateCreation = models.DateTimeField(db_column="dateCreation", default=timezone.now)
    estSupprimer = models.IntegerField(db_column="estSupprimer", default=0)
    class Meta:
        db_table = 'livraison'