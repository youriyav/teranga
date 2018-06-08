from __future__ import unicode_literals

from django.db import models

# Create your models here.
from commande.models import Commande
from produit.models import Produit


class LigneCommande(models.Model):
    idLigne = models.AutoField(db_column='idLigne',primary_key=True)
    commande=models.ForeignKey(Commande,db_column="commande",null=True)
    produit=models.ForeignKey(Produit,db_column="produit")
    quantite=models.IntegerField(db_column="quantite")
    class Meta:
        db_table = 'ligne_commande'