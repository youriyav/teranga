from __future__ import unicode_literals


from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from Entite.models import Entite
from client.models import Client
#from ligne_commande.models import LigneCommande
from datetime import datetime, timedelta

from livreur.models import Livreur
from localite.models import Localite
from utilisateur.models import Utilisateur


class Commande(models.Model):
    idCommande = models.AutoField(db_column='idCommande',primary_key=True)
    numero = models.CharField(db_column="numero", null=True, max_length=50)
    client=models.ForeignKey(Client,db_column="client")
    livreur=models.ForeignKey(Livreur,db_column="livreur",null=True)
    entite=models.ForeignKey(Entite,db_column="entite",null=True)
    #listeProduit=models.ManyToManyField(LigneCommande)
    longitude=models.CharField(db_column="longitude",null=True,max_length=20)
    latitude=models.CharField(db_column="latitude",null=True,max_length=20)
    dateCreation = models.DateTimeField(db_column="dateCreation", default=timezone.now)
    dateLivraicon = models.DateTimeField(db_column="dateLivraicon",null=True)
    dateValidation = models.DateTimeField(db_column="dateValidation",null=True)
    datePreparation = models.DateTimeField(db_column="datePreparation",null=True)
    lastRelance = models.DateTimeField(db_column="lastRelance", null=True)
    estSupprimer = models.IntegerField(db_column="estSupprimer", default=0)
    estValider = models.IntegerField(db_column="estValider", default=0)
    isSynch = models.IntegerField(db_column="isSynch", default=0)
    enCoursDepreparion = models.IntegerField(db_column="enCoursDepreparion", default=0)
    estLivrer = models.IntegerField(db_column="estLivrer", default=0)
    state = models.IntegerField(db_column="state", default=0)
    relancer = models.IntegerField(db_column="relancer", default=0)
    estEstEnCoursDeLivraison = models.IntegerField(db_column="estEstEnCoursDeLivraison", default=0)
    manager=models.ForeignKey(Utilisateur,db_column="manager",null=True)    
    localite=models.ForeignKey(Localite,db_column="localite",null=True)
    plateform = models.IntegerField(db_column="plateform", default=0)
    prixLivraison = models.IntegerField(db_column="prixLivraison", default=0)
    def get_duree(self):
        #tmp = self.dateCreation
        date_save = datetime.strftime(self.dateCreation, '%Y-%m-%d %H:%M:%S')
        currentDate = datetime.now()
        try:
            date_liv = datetime.strftime(self.dateLivraicon, '%Y-%m-%d %H:%M:%S')
            diff = datetime.strptime(date_liv, '%Y-%m-%d %H:%M:%S') - datetime.strptime(date_save, '%Y-%m-%d %H:%M:%S')
        except:
            diff = currentDate - datetime.strptime(date_save, '%Y-%m-%d %H:%M:%S')
        res=diff.seconds/60
        return res
    def get_duree_relance(self):
        tmp = self.lastRelance
        try:
            date_save = datetime.strftime(tmp, '%Y-%m-%d %H:%M:%S')
            currentDate = datetime.now()
            diff = currentDate - datetime.strptime(date_save, '%Y-%m-%d %H:%M:%S')
            res=diff.seconds/60
        except:
            res=0
        return res
    def get_montant(self):
        ligne=self.lignecommande_set.all()
        somme=0
        for l in ligne:
            somme=somme+(int(l.produit.prixProduit)*int(l.quantite))
        return  somme
    class Meta:
        db_table = 'commande'