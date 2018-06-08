# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import os

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Entite.models import Entite
from senfood.settings import BASE_DIR
from categorie.models import Categorie
from produit.models import Produit
from image.models import Image
from parametre.models import Parametre
from django.contrib import auth
from client.models import Client
from sen_food.models import Personne
from datetime import datetime
from django.contrib.auth.models import User
from commande.models import Commande
from ligne_commande.models import LigneCommande
from terminal.models import Terminal
import json
@csrf_exempt
def homeMobil(request):
    listeEntite = Entite.objects.filter(estSupprimer=0, estDesactiver=0)
    save_path = os.path.join("/home/teranga-admin")
    data = '['
    mstop = 0

    for entite in listeEntite:
        mstop = mstop + 1

        # save_path = os.path.join(BASE_DIR)
        with open(save_path + entite.logoEntite, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            # with open(os.path.join(entite_folder, entite.logoEntite), "rb") as image_file:
            #   encoded_string = base64.b64encode(image_file.read())
        tmp = '{'
        tmp += '"idEntite":' + str(entite.idEntit) + ','
        tmp += '"nom":"' + entite.nomEntite + '",'
        try:
            tmp += '"latitude":' + entite.latitude + ','
            tmp += '"longitude":' + entite.longitude + ','
        except:
            tmp += '"latitude":"",'
            tmp += '"longitude":"",'

        tmp += '"slogan":"' + entite.sloganEntite + '",'
        tmp += '"email":"' + entite.emailEntite + '",'
        tmp += '"numero":"' + entite.numeroEntite + '",'
        #tmp += '"isPartner":' + str(entite.isPartern) + ','
        tmp += '"logo":"' + encoded_string + '"'
        tmp+='}'
        data +=tmp
        if mstop != listeEntite.count():
            data +=','
    nbrVersion="1"
    try:
        parametre3 = Parametre.objects.filter(key="version")[0]
        nbrVersion=parametre3.value
    except:
        nbrVersion = "1"
    data+=',{"version":"'+nbrVersion+'"}'
    data+=']'
    return HttpResponse(data)

@csrf_exempt
def getCategorie(request,idEntite):
    entite = Entite.objects.filter(estSupprimer=0, estDesactiver=0,idEntit=idEntite)[0]
    save_path = os.path.join("/home/teranga-admin")
    listeCategorie = Categorie.objects.filter(entite=entite, estSupprimer=0, estDesactiver=0)
    Categoriedata = '['
    catStop = 0
    for categorie in listeCategorie:
        #image=Image.objects.filter(idImage=categorie.logoCat.idImage,)[0]
        with open(save_path + categorie.logoCat.saveName, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        catStop = catStop + 1
        tmpCategorie = '{'
        tmpCategorie += '"id":' + str(categorie.idCategorie) + ','
        tmpCategorie += '"idEntite":"' + str(categorie.entite.idEntit) + '",'
        tmpCategorie += '"nom":"' + categorie.libelleCat + '",'
        tmpCategorie += '"description":"' + categorie.descriptionCat + '",'
        tmpCategorie += '"logo":"' + encoded_string + '"'
        tmpCategorie += '}'
        Categoriedata = Categoriedata + tmpCategorie
        if catStop != listeCategorie.count():
            Categoriedata = Categoriedata + ","
    Categoriedata = Categoriedata + ']'
    data = Categoriedata
    return HttpResponse(data)

@csrf_exempt
def getProduit(request,idCategorie):
    #identite=request.GET["idEntite"]
    listeProduit=Produit.objects.filter(categorie__idCategorie=idCategorie,estSupprimer=0,estDesactiver=0)
    save_path = os.path.join("/home/teranga-admin")
    Produitdata = '['
    catStop = 0
    listeImage=[]
    for produit in listeProduit:
        #image=Image.objects.filter(idImage=categorie.logoCat.idImage,)[0]
        exist=0
        for x in listeImage:
           if x.idImage==produit.logoProduit.idImage:
                exist=x.idProduit
        if exist == 0:
            with open(save_path + produit.logoProduit.saveName, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                imageProd=imageProduit(produit.logoProduit.idImage,produit.idProduit)
            listeImage.append(imageProd)
        catStop = catStop + 1
        tmpProduit = '{'
        tmpProduit += '"id":' + str(produit.idProduit) + ','
        tmpProduit += '"idEntite":' + str(produit.categorie.entite.idEntit) + ','
        tmpProduit += '"nom":"' + produit.nomProduit + '",'
        tmpProduit += '"description":"' + produit.descriptProduit + '",'
        tmpProduit += '"prix":' + produit.prixProduit + ','
        if exist == 0:
            tmpProduit += '"logo":"' + encoded_string + '"'
        else:
            tmpProduit += '"logo":"' + str(exist) + '"'
        tmpProduit += '}'
        Produitdata += tmpProduit
        if catStop != listeProduit.count():
            Produitdata +=","
    Produitdata += ']'
    data = Produitdata
    return HttpResponse(data)
    
class imageProduit:
    def __init__(self, idImage, idProduit):
        self.idImage = idImage
        self.idProduit = idProduit


def updateMobil(request,version):

    nbrVersion="1"
    try:
        parametre3 = Parametre.objects.filter(key="version")[0]
        nbrVersion=int(parametre3.value)
    except:
        nbrVersion = 1
    data="[]"
    if nbrVersion!=int(version):
        listeEntite = Entite.objects.filter(estSupprimer=0, estDesactiver=0)
        save_path = os.path.join("/home/teranga-admin")
        data = '['
        mstop = 0

        for entite in listeEntite:
            mstop = mstop + 1

            # save_path = os.path.join(BASE_DIR)
            with open(save_path + entite.logoEntite, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                # with open(os.path.join(entite_folder, entite.logoEntite), "rb") as image_file:
                #   encoded_string = base64.b64encode(image_file.read())
            tmp = '{'
            tmp += '"idEntite":' + str(entite.idEntit) + ','
            tmp += '"nom":"' + entite.nomEntite + '",'
            try:
                tmp += '"latitude":' + entite.latitude + ','
                tmp += '"longitude":' + entite.longitude + ','
            except:
                tmp += '"latitude":"",'
                tmp += '"longitude":"",'

            tmp += '"slogan":"' + entite.sloganEntite + '",'
            tmp += '"email":"' + entite.emailEntite + '",'
            tmp += '"numero":"' + entite.numeroEntite + '",'
            #tmp += '"isPartner":' + str(entite.isPartern) + ','
            tmp += '"logo":"' + encoded_string + '"'
            tmp+='}'
            data +=tmp
            if mstop != listeEntite.count():
                data +=','
        data+=',{"version":"'+str(nbrVersion)+'"}'
        data+=']'
    return HttpResponse(data)


@csrf_exempt
def login(request):
    #token = request.POST["token"]
    numero = "778399425"#request.POST["login"]
    password = "1234"#request.POST["password"]
    try:
        muser=User.objects.filter(username=numero)[0]
        client=Client.objects.filter(user=muser)[0]
        validation=Validation.objects.filter(client=client,estValider=0,estSupprimer=0)[0]
            #if validation:
        nom = muser.client.personne.nomPersonne
        prenom = muser.client.personne.prenomPersonne
        idClient = muser.client.idclient
        data = '[{'
        data += '"nom":"' + nom + '",'
        data += '"prenom":"' + prenom + '",'
        data += '"idClient":"' + str(idClient) + '"'
        data += '}]'
        return  HttpResponse(data, status=401)
    except:
        user = auth.authenticate(username=numero, password=password)
        if user:
            nom = user.client.personne.nomPersonne
            prenom = user.client.personne.prenomPersonne
            idClient = user.client.idclient
            data = '[{'
            data += '"nom":"' + nom + '",'
            data += '"prenom":"' + prenom + '",'
            data += '"idClient":"' + str(idClient) + '"'
            data += '}]'
            return HttpResponse(data)
        else:
            return HttpResponse("bad login", status=402)
@csrf_exempt
def updateCommande(request,idCommande):
    try:
        commande = Commande.objects.filter(idCommande=idCommande)[0]
        longitude=0
        latitude=0
        if commande.state>=3:
            personne=commande.livreur.personne
            terminal=Terminal.objects.filter(utilisateur=personne)[0]
            longitude=terminal.longitude
            latitude=terminal.latitude

        message="updated"
        
        return HttpResponse('[{"code":2,"message":"'+message+'","duree":'+str(commande.get_duree())+',"state":'+str(commande.state)+',"longitude":'+str(longitude)+',"latitude":'+str(latitude)+'}]')
    except:
        message="cette commande n'existe pas"
        return HttpResponse('[{"code":1,"message":"'+message+'"}]')


@csrf_exempt
def newCommandeMobil(request):
    #data ='{"longitude":"-17.4694231","latitude":"14.7227633","produits":[{"produit":"test","quantite":"1"}]}'#request.POST["data"]
    #idLocalite = 4
    #priLivraison = 500
    #user = 1
    #midEntite = 9
    #password = 1234

    data =request.POST["data"]
    #idLocalite = request.POST["idLocalite"]
    priLivraison = request.POST["prixLivraison"]
    user = request.POST["client"]
    midEntite = request.POST["idEntite"]
    password = request.POST["password"]
    mlongitude = request.POST["longitude"]
    mlatitude= request.POST["latitude"]
    is_error = 0
    try:
        client=Client.objects.filter(idclient=user)[0]
        user=User.objects.filter(username=client.personne.numeroPersonne)[0]
        parametreState = Parametre.objects.filter(key="state")[0]
        entite = Entite.objects.filter(idEntit=midEntite)[0]
        listeProduit=json.loads(data)#data
        commande = Commande()
        parametreDebut = Parametre.objects.filter(key="heure_debut")[0]
        parametreFin = Parametre.objects.filter(key="heure_fin")[0]
        if user.check_password(password):
            parametreState.value= "1"
            if parametreState.value == "1":
                today = datetime.now()
                heure = today.hour
                if heure >= int(parametreDebut.value) and heure <= int(parametreFin.value):
                    try:
                        commande = Commande.objects.filter(client__user=user, estLivrer=0,state__lt=6)[0]
                        message="Vous avez une commande en cours. veuillez patienter jusqu'à ce que celle ci soit livrée avant de pouvoir éffectuer une commande"
                        return  HttpResponse('[{"code":6,"message":"'+message+'"}]')
                    except:
                        if entite.isPartern==1:
                            montantCommande=0
                            for produit in listeProduit:
                                mproduit=Produit.objects.filter(idProduit=produit["idProduit"])[0]
                                ligne=LigneCommande()
                                montantCommande+=int(mproduit.prixProduit)*int(produit["quantite"])
                            if client.estBloquer == 0:
                                commande.entite=entite
                                commande.longitude=mlongitude
                                commande.latitude=mlatitude
                                commande.client=client
                                commande.plateform=1
                                commande.save()
                                tmp=""
                                for produit in listeProduit:
                                    mproduit=Produit.objects.filter(idProduit=produit["idProduit"])[0]
                                    ligne=LigneCommande()
                                    ligne.commande=commande
                                    ligne.produit=mproduit
                                    ligne.quantite=produit["quantite"]
                                    ligne.save()
                                tmp=str(client.idclient)

                                numero="sen-f00"+tmp+str(commande.idCommande)
                                commande.numero=numero 
                                commande.save()
                                data = '{'
                                data += '"id":"' + str(commande.idCommande)+'",'
                                data += '"numero":"' + str(commande.numero)+'"' 
                                data += '}' 
                                message="votre commande a été éffectuée avec succès. Vous pouvez dès maintenant suivre l'évolution de celle-ci jusqu'à la livraison."
                                    #mdata="numero":"'+numero+'","id":"'+str(commande.idCommande)+'"  
                                    #return HttpResponse(numero)
                                return HttpResponse('[{"code":8,"message":"'+message+'","numero":"'+str(commande.numero)+'","id":'+str(commande.idCommande)+'}]') #,"id:'+str(commande.idCommande)+'
                            else:
                                    #return HttpResponse("désole,votre compte n'est pas autorisé à commander. \nveuillez contacter le service client pour tout détail", status=405)
                                return HttpResponse('[{"code":9,"message":"désole,votre compte n est pas autorisé à commande"}]')

                else:
                    errorText="Désolé nos services sont disponibles entre "+parametreDebut.value+"h-"+parametreFin.value+"h. Veuillez réessayer plus tard"
                    return HttpResponse('[{"code":5,"message":"'+errorText+'"}]')

            else:
                return HttpResponse('[{"code":4,"message":"désolé, nos services sont  momentanément indisponibles. veuillez réessayer plus tard"}]')
        else:

            return HttpResponse('[{"code":2,"message":"votre code secret est incorrect. Veuillez entrer à nouveau"}]')
    except:
        return HttpResponse('[{"code":1,"message":"utilisateur n existe pas"}]')


