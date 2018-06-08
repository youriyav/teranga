#-*- coding: utf-8 -*-
import base64
import json
import os
from datetime import datetime
from itertools import product
from random import randint

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from tarif.models import Tarif
from Entite.models import Entite
from categorie.models import Categorie
from client.models import Client
from client.views import sendSms
from commande.models import Commande
from image.models import Image
from ligne_commande.models import LigneCommande
from localite.models import Localite
from log.models import Log
from parametre.models import Parametre
from produit.models import Produit
from sen_food.models import Personne
from sen_food.views import decodeString
from django.conf import settings

from senfood.settings import BASE_DIR
from terminal.models import Terminal
from validation.models import Validation


@csrf_exempt
def registerMobil(request):
    numero = request.POST["numero"]
    token = request.POST["token"]
    imei = request.POST["imei"]
    is_livreur = request.POST["is_livreur"]
    model = request.POST["model"]
    marque = request.POST["marque"]
    try:
        terminal=Terminal()
        terminal.numero=numero
        terminal.token=token
        terminal.numeroSerie=imei
        terminal.isLivreur=is_livreur
        terminal.model=model
        terminal.marque=marque
        terminal.save()
        return HttpResponse(u"{'message':'succès'}")
    except:
        is_error=0
        return HttpResponse("{'message':'error'}", status=401)


@csrf_exempt
def homeMobil(request):
    listeEntite = Entite.objects.filter(estSupprimer=0, estDesactiver=0)
    save_path = os.path.join("/home/teranga-admin")
    data = '{"listeEntite":['
    mstop = 0

    for entite in listeEntite:
        mstop = mstop + 1
        entite_folder = "C:/Users/root/PycharmProjects/senfood/static/"
        # save_path = os.path.join(BASE_DIR)
        with open(save_path + entite.logoEntite, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            # with open(os.path.join(entite_folder, entite.logoEntite), "rb") as image_file:
            #   encoded_string = base64.b64encode(image_file.read())
        tmp = '{'
        tmp += '"idEntite":"' + str(entite.idEntit) + '",'
        tmp += '"nom":"' + entite.nomEntite + '",'
        try:
            tmp += '"latitude":"' + entite.latitude + '",'
            tmp += '"longitude":"' + entite.longitude + '",'
        except:
            tmp += '"latitude":"",'
            tmp += '"longitude":"",'

        tmp += '"slogan":"' + entite.sloganEntite + '",'
        tmp += '"email":"' + entite.emailEntite + '",'
        tmp += '"numero":"' + entite.numeroEntite + '",'
        tmp += '"isPartner":' + str(entite.isPartern) + ','
        tmp += '"logo":"' + encoded_string + '"'
        tmp+='}'
        data +=tmp
        if mstop != listeEntite.count():
            data +=','
    data+=']'
    listeLocalite = Localite.objects.filter()
    localiteTab = '['
    localiteStop = 0
    for localite in listeLocalite:
        localiteStop = localiteStop + 1
        tmp= '{'
        tmp += '"id":' + str(localite.idLocalite) + ','
        tmp += '"libelle":"' + localite.libelle+'"'
        tmp += '}'
        if localiteStop != listeLocalite.count():
            tmp = tmp + ","
        localiteTab+=tmp
    localiteTab += ']'
    nbrVersion="1"
    try:
        parametre3 = Parametre.objects.filter(key="version")[0]
        nbrVersion=parametre3.value
    except:
        nbrVersion = "1"
    heureDebut=""
    heureFin=""
    prixMax=""
    try:
        parametre = Parametre.objects.filter(key="heure_debut")[0]
        heureDebut=parametre.value
        parametre3 = Parametre.objects.filter(key="heure_fin")[0]
        heureFin=parametre3.value
        parametre3 = Parametre.objects.filter(key="max_prix")[0]
        prixMax=parametre3.value
    except:
        heureDebut =""
        heureFin=""
        prixMax=""
    listeTarif=Tarif.objects.filter(estSupprimer=0)
    localiteStop = 0
    tarifTab="["
    for tarif in listeTarif:
        localiteStop = localiteStop + 1
        tmp= '{'
        tmp += '"id":' + str(tarif.idTarif) + ','
        tmp += '"libelle":"' + str(tarif.libelle)+'",'
        tmp += '"prix":"' + str(tarif.prix)+'",'
        tmp += '"min":"' + str(tarif.distanceMin)+'",'
        tmp += '"max":"' + str(tarif.distanceMax)+'"'
        tmp += '}'
        if localiteStop != listeTarif.count():
            tmp = tmp + ","
        tarifTab+=tmp
    tarifTab+="]"
    data = data + ',"listeLocalite":'+localiteTab+',"version":'+str(nbrVersion)+',"listeTarif":'+tarifTab+',"heure_debut":"'+heureDebut+'","heure_fin":"'+heureFin+'","max_prix":"'+prixMax+'"}'
    return HttpResponse(data)

@csrf_exempt
def getCategorie(request,idEntite):
    #identite=request.GET["idEntite"]
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
        tmpCategorie += '"id":"' + str(categorie.idCategorie) + '",'
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
        tmpProduit += '"id":"' + str(produit.idProduit) + '",'
        tmpProduit += '"idEntite":"' + str(produit.categorie.entite.idEntit) + '",'
        tmpProduit += '"nom":"' + produit.nomProduit + '",'
        tmpProduit += '"description":"' + produit.descriptProduit + '",'
        tmpProduit += '"prix":"' + produit.prixProduit + '",'
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


@csrf_exempt
def updateLocationMobil(request):
    token = request.POST["token"]
    longitude = request.POST["longitude"]
    latitude = request.POST["latitude"]
    try:
        terminal = Terminal.objects.filter(token=token)[0]
        terminal.longitude=longitude
        terminal.latitude=latitude
        terminal.lastUpdate = datetime.now()
        terminal.save()
        return HttpResponse(u"{'message':'succès'}")
    except:
        is_error=0
        return HttpResponse("{'message':'error'}", status=401)

@csrf_exempt
def initialiseLocationMobil(request):
   # token = request.POST["token"]
    #terminal = Terminal.objects.filter(token=token)[0]
    listeEntite = Entite.objects.filter(estSupprimer=0, estDesactiver=0)
    save_path = os.path.join("/home/teranga-admin")
    data = '{"listeEntite":['
    mstop = 0
    for entite in listeEntite:
        mstop = mstop + 1
        entite_folder = "C:/Users/root/PycharmProjects/senfood/static/"
        #save_path = os.path.join(BASE_DIR)
        with open(save_path+entite.logoEntite, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        #with open(os.path.join(entite_folder, entite.logoEntite), "rb") as image_file:
         #   encoded_string = base64.b64encode(image_file.read())
        tmp = '{'
        tmp +='"idEntite":"' + str(entite.idEntit) + '",'
        tmp +='"nom":"' + entite.nomEntite + '",'
        tmp +='"slogan":"' + entite.sloganEntite + '",'
        tmp +='"email":"' + entite.emailEntite + '",'
        tmp +='"numero":"' + entite.numeroEntite + '",'
        tmp +='"logo":"' + encoded_string + '",'
        tmp +='"couleur":"' + entite.ColeurEntite + '",'
        listeCategorie=Categorie.objects.filter(entite=entite,estSupprimer=0,estDesactiver=0)
        Categoriedata = '['
        catStop = 0
        for categorie in listeCategorie:
            catStop=catStop+1
            tmpCategorie = '{'
            tmpCategorie += '"id":"' + str(categorie.idCategorie) + '",'
            tmpCategorie += '"idEntite":"' + str(categorie.entite.idEntit) + '",'
            tmpCategorie += '"nom":"' + categorie.libelleCat + '",'
            tmpCategorie += '"description":"' + categorie.descriptionCat + '",'
            tmpCategorie += '"logo":"' + str(categorie.logoCat.idImage) + '"'
            tmpCategorie += '}'
            Categoriedata = Categoriedata + tmpCategorie
            if catStop != listeCategorie.count():
                Categoriedata = Categoriedata + ","
        Categoriedata = Categoriedata + ']'

        listeProduit = Produit.objects.filter(categorie__entite=entite,estSupprimer=0,estDesactiver=0)
        Produitdata = '['
        ProduitStop = 0
        for produit in listeProduit:
            ProduitStop = ProduitStop + 1
            tmpProduit = '{'
            tmpProduit += '"id":"' + str(produit.idProduit) + '",'
            tmpProduit += '"idEntite":"' + str(produit.categorie.entite.idEntit) + '",'
            tmpProduit += '"idCategorie":"' + str(produit.categorie.idCategorie) + '",'
            tmpProduit += '"nom":"' + produit.nomProduit + '",'
            tmpProduit += '"description":"' + produit.descriptProduit + '",'
            tmpProduit += '"prix":"' + str(produit.prixProduit) + '",'
            tmpProduit += '"logo":"' +str(produit.logoProduit.idImage) + '"'
            tmpProduit += '}'
            Produitdata = Produitdata + tmpProduit
            if ProduitStop != listeProduit.count():
                Produitdata = Produitdata + ","
        Produitdata = Produitdata + ']'


        tmp += '"categories":' + Categoriedata + ','
        tmp += '"produits":' + Produitdata + ''
        tmp = tmp + '}'
        data = data + tmp
        if mstop != listeEntite.count():
            data = data + ","
    nbrVersion="1"
    try:
        parametre3 = Parametre.objects.filter(key="version")[0]
        nbrVersion=parametre3.value
    except:
        nbrVersion = "1"


    listeLocalite = Localite.objects.filter()
    localiteTab = '['
    localiteStop = 0
    for localite in listeLocalite:
        localiteStop = localiteStop + 1
        tmp= '{'
        tmp += '"id":' + str(localite.idLocalite) + ','
        tmp += '"libelle":"' + localite.libelle+'"'
        tmp += '}'
        if localiteStop != listeLocalite.count():
            tmp = tmp + ","
        localiteTab+=tmp
    localiteTab += ']'


    listeImage = Image.objects.filter(estSupprimer=0)
    stop = 0
    imageTab = '['
    for image in listeImage:
        stop = stop + 1
        tmp = '{'
        tmp += '"id":' + str(image.idImage) + ','
        with open(save_path + image.saveName, "rb") as image_file:
            encoded_string_prod = base64.b64encode(image_file.read())
        tmp += '"content":"' + encoded_string_prod + '"'
        tmp += '}'
        if stop != listeImage.count():
            tmp += ','
        imageTab += tmp
    imageTab += ']'
    data = data + '],"version":' + nbrVersion +',"listeLocalite":'+localiteTab+',"listeImage":'+imageTab+'}'
    return HttpResponse(data)

@csrf_exempt
def updateMobil(request):
   # token = request.POST["token"]
    #terminal = Terminal.objects.filter(token=token)[0]
    data='['
    return HttpResponse(data)

@csrf_exempt
def loginClientMobil(request):
    #token = request.POST["token"]
    numero = request.POST["numero"]
    password = request.POST["password"]
    try:
        muser=User.objects.filter(username=numero)[0]
        client=Client.objects.filter(user=muser)[0]
        validation=Validation.objects.filter(client=client,estValider=0,estSupprimer=0)[0]
            #if validation:
        nom = muser.client.personne.nomPersonne
        prenom = muser.client.personne.prenomPersonne
        idClient = muser.client.idclient
        data = '{'
        data += '"nom":"' + nom + '",'
        data += '"prenom":"' + prenom + '",'
        data += '"idClient":"' + str(idClient) + '"'
        data += '}'
        return  HttpResponse(data, status=401)
    except:
        user = auth.authenticate(username=numero, password=password)
        if user:
            nom = user.client.personne.nomPersonne
            prenom = user.client.personne.prenomPersonne
            idClient = user.client.idclient
            data = '{'
            data += '"nom":"' + nom + '",'
            data += '"prenom":"' + prenom + '",'
            data += '"idClient":"' + str(idClient) + '"'
            data += '}'
            return HttpResponse(data)
        else:
            return HttpResponse("bad login", status=402)

@csrf_exempt
def inscriptionClientMobil(request):
    #token = request.POST["token"]
    nom = request.POST["nom"]
    prenom = request.POST["prenom"]
    email = request.POST["email"]
    numero = request.POST["numero"]
    password = request.POST["password"]
    try:
        _user = User.objects.filter(username=numero, is_active=1)[0]
        if _user:
            error_numero = "un compte est déjà enregistré avec ce numero"
            return HttpResponse(error_numero, status=402)
    except:
        check = 0
        exist = 0
        listeValidation = Validation.objects.filter(estValider=0)
        while check == 0:
            var_tmp = ""
            while len(var_tmp) < 6:
                d = randint(0, 9)
                var_tmp = var_tmp + str(d)
            for validation in listeValidation:
                if validation.keyValidation == var_tmp:
                    exist = 1
            if exist == 0:
                check = 1
        personne = Personne()
        personne.nomPersonne = nom
        personne.prenomPersonne = prenom
        personne.numeroPersonne = numero
        personne.emailPersonne = email
        personne.save()
        try:
            old_user = User.objects.filter(username=numero, is_active=0)[0]
            if old_user:
                old_user.delete()
        except:
            v = 1
        user = User(username=numero, email=email, first_name=nom, last_name=prenom, is_active=1)
        user.set_password(password)
        user.save()
        client = Client()
        client.user = user
        client.personne = personne
        # client.code=password
        client.type=2
        client.save()
        validation = Validation()
        validation.client = client
        validation.keyValidation = var_tmp
        validation.save()
        data_message = {
            "code": var_tmp,
            "numero": numero
        }
        sendSms(numero, var_tmp)
        #sendSms(data_message)
        log = Log()
        log.utilisateur = request.user.username
        log.action = "Creation compte client " + nom + " " + prenom + " " + numero
        log.save()
        nom = user.client.personne.nomPersonne
        prenom = user.client.personne.prenomPersonne
        idClient = user.client.idclient
        data = '{'
        data += '"nom":"' + nom + '",'
        data += '"prenom":"' + prenom + '",'
        data += '"idClient":"' + str(idClient) + '"'
        data += '}'
        return HttpResponse(data)


@csrf_exempt
def regenererTokenMobil(request):
    global var_tmp, validation
    idClient = request.POST["idClient"]
    is_error=0
    try:
        client=Client.objects.filter(idclient=idClient)[0]
        validation = Validation.objects.filter(client=client, estValider=0, estSupprimer=0).last()
    except:
        is_error=1
    if is_error==0:
        validations = Validation.objects.filter(client=validation.client)
        if validations.count() < 3:
            validation.estSupprimer = 1
            validation.save()
            validation1 = Validation()
            validation1.client = validation.client
            check = 0
            exist = 0
            listeValidation = Validation.objects.filter(estSupprimer=0)
            while check == 0:
                var_tmp = ""
                while len(var_tmp) < 6:
                    d = randint(0, 9)
                    var_tmp = var_tmp + str(d)
                for validati in listeValidation:
                    if validati.keyValidation == var_tmp:
                        exist = 1
                if exist == 0:
                    check = 1
            validation1.keyValidation = var_tmp
            validation1.estConfirmer = 1
            validation1.save()
            data_message = {
                "code": var_tmp,
                "numero": validation.client.personne.numeroPersonne
            }
            sendSms(validation.client.personne.numeroPersonne, var_tmp)
            log = Log()
            log.utilisateur = request.user.username
            log.action = u"regénération token pour validation compte client pour " + decodeString(
                validation.client.user.username)
            log.save()
            data = '{"statut":200}'
            return HttpResponse(data)
        else:
            date_save = datetime.strftime(validations.last().dateCreation, '%Y-%m-%d %H:%M:%S')
            currentDate = datetime.now()
            diff = currentDate - datetime.strptime(date_save, '%Y-%m-%d %H:%M:%S')
            res = diff.seconds / 60
            if res < 60:
                tmp = 60 - res
                data='{"statut":202,"delai":'+str(tmp)+'}'
                return HttpResponse(data)
            else:
                validation.estSupprimer = 1
                validation.save()
                validation1 = Validation()
                validation1.client = validation.client
                check = 0
                exist = 0
                listeValidation = Validation.objects.filter(estSupprimer=0)
                while check == 0:
                    var_tmp = ""
                    while len(var_tmp) < 6:
                        d = randint(0, 9)
                        var_tmp = var_tmp + str(d)
                    for validati in listeValidation:
                        if validati.keyValidation == var_tmp:
                            exist = 1
                    if exist == 0:
                        check = 1
                validation1.keyValidation = var_tmp
                validation1.estConfirmer = 1
                validation1.save()
                data_message = {
                    "code": var_tmp,
                    "numero": validation.client.personne.numeroPersonne
                }
                sendSms(validation.client.personne.numeroPersonne, var_tmp)
                log = Log()
                log.utilisateur = request.user.username
                log.action = u"regénération token pour validation compte client pour " + decodeString(
                    validation.client.user.username)
                log.save()
                data = '{"statut":200}'
                return HttpResponse(data)

    else:
        return HttpResponse("error", status=403)

@csrf_exempt
def validationCompteMobil(request):
    global var_tmp, validation
    code = request.POST["code"]
    is_error=0
    try:
        validation = Validation.objects.filter(keyValidation=code, estValider=0, estSupprimer=0)[0]
        if validation.keyValidation != "":
            user = authenticate(token=code)
            user.is_active = 1
            user.save()
            if user:
                nom = user.client.personne.nomPersonne
                prenom = user.client.personne.prenomPersonne
                idClient = user.client.idclient
                data = '{'
                data += '"nom":"' + nom + '",'
                data += '"prenom":"' + prenom + '",'
                data += '"idClient":"' + str(idClient) + '"'
                data += '}'
                return HttpResponse(data)
    except:
        is_error=1
        return HttpResponse("error", status=403)
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



    is_error = 0
    try:
        #user=User.objects.filter(username=user)[0]
        client=Client.objects.filter(idclient=user)[0]
        user=User.objects.filter(username=client.personne.numeroPersonne)[0]
        #localite=Localite.objects.filter(estSupprimer=0,isActive=1,idLocalite=idLocalite)[0]
    except:
        is_error=1
    if is_error ==0:
        commande = Commande()
        commande.prixLivraison=priLivraison
        parametreState = Parametre.objects.filter(key="state")[0]
        parametreDebut = Parametre.objects.filter(key="heure_debut")[0]
        parametreFin = Parametre.objects.filter(key="heure_fin")[0]
        if user.check_password(password):
            if parametreState.value == "1":
                today = datetime.now()
                heure = today.hour
                if heure >= int(parametreDebut.value) and heure <= int(parametreFin.value):
                    data_json = json.loads(data)
                    longitude= data_json["longitude"]
                    latitude=data_json["latitude"]
                    listeProduit=data_json["produits"]
                    montantCommande=0
                    try:
                        commande = Commande.objects.filter(client__user=user, estLivrer=0,state__lt=6)[0]
                        return HttpResponse("vous avez une commande en cours", status=409)
                    except:
                    	entite = Entite.objects.filter(idEntit=midEntite)[0]
                    	if entite.isPartern==1:
                    		for produit in listeProduit:
	                            mproduit=Produit.objects.filter(idProduit=produit["idProduit"])[0]
	                            ligne=LigneCommande()
	                            montantCommande+=int(mproduit.prixProduit)*int(produit["quantite"])
	                        if montantCommande>10000:
	                            try:
	                                listeCommande=Commande.objects.filter(client__user=user,estLivrer=1)
	                                if listeCommande.count()>=2:
	                                    client = Client.objects.filter(user=user)[0]
	                                    if client.estBloquer == 0:
	                                        
	                                        commande.entite = entite
	                                        commande.longitude = longitude
	                                        commande.latitude = latitude
	                                        commande.client = client
	                                        #commande.localite=localite
                                            commande.plateform=1
                                            commande.prixLivraison=priLivraison
                                            commande.save()
                                            tmp = ""
                                            for produit in listeProduit:
	                                                # tmp=tmp+"|"+produit["idProduit"]+"_"+produit["quantite"]
	                                            mproduit = Produit.objects.filter(idProduit=produit["idProduit"])[0]
	                                            ligne = LigneCommande()
	                                            ligne.commande = commande
	                                            ligne.produit = mproduit
	                                            ligne.quantite = produit["quantite"]
	                                            ligne.save()
                                            tmp = str(client.idclient)
                                            numero = "sen-f00" + tmp + str(commande.idCommande)
                                            commande.numero = numero
                                            commande.save()
                                            data = '{'
                                            data += '"id":"' + str(commande.idCommande) + '",'
                                            data += '"numero":"' + str(commande.numero) + '"'
                                            data += '}'
                                            return HttpResponse(data)  # str(commande.idCommande))
	                                else:
	                                    return HttpResponse("désole, vous n'êtes pas encore autorisé à commander pour plus de 10000 Fcfa ", status=402)
	                            except:
	                                return HttpResponse("désole, vous n'êtes pas encore autorisé à commander pour plus de 10000 Fcfa ", status=402)
	                        else:
	                            client = Client.objects.filter(user=user)[0]
	                            if client.estBloquer == 0:
	                                #commande=Commande()

                                    
	                                #entite=Entite.objects.filter(idEntit=midEntite)[0]
	                                commande.entite=entite
	                                commande.longitude=longitude
	                                commande.latitude=latitude
	                                commande.client=client
	                                commande.plateform=1
	                                commande.save()
	                                #commande.localite=localite
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
	                                return HttpResponse(data)#str(commande.idCommande))
	                            else:
	                                return HttpResponse("désole,votre compte n'est pas autorisé à commander. \nveuillez contacter le service client pour tout détail", status=405)
                    	else:
                    		client = Client.objects.filter(user=user)[0]
                    		if client.estBloquer == 0:
                    			#commande=Commande()
                                
                    			commande.entite=entite
                    			commande.longitude=longitude
                    			commande.latitude=latitude
                    			commande.client=client
                    			commande.plateform=1
                    			commande.save()
                    			#commande.localite=localite
                    			tmp=""
                    			for produit in listeProduit:
                    				tmp+=produit["produit"]+":"+produit["quantite"]
                    				pr=Produit()
                    				pr.nomProduit=produit["produit"]
                    				pr.isTmp=1
                    				pr.save()
                    				myprod=Produit.objects.filter(idProduit=pr.idProduit)[0]                    		
                    				ligne=LigneCommande()
                    				ligne.commande=commande
                    				ligne.produit=pr
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
                    			return HttpResponse(data)
                else:
                    tmp_debut = ""
                    tmp_fin = ""
                    if (int(parametreDebut.value) <= 9):
                        tmp_debut = "0" + str(parametreDebut.value) + "h:00 min"
                    else:
                        tmp_debut = str(parametreDebut.value) + "h:00 min"
                    if (int(parametreFin.value) <= 9):
                        tmp_fin = "0" + str(parametreFin.value) + "h:00 min"
                    else:
                        tmp_fin = str(parametreFin.value) + "h:00 min"
                        log = Log()
                        log.utilisateur = user.username
                        log.action = "echec commande,bad heure"
                        log.save()
                    return HttpResponse("Désolé, Nos services sont disponibe de " + tmp_debut + " à " + tmp_fin + ".Veuillez réessayer ultérieument.",status=406)
            else:
                log = Log()
                log.utilisateur = user.username
                log.action = "commande impossible"
                log.save()
                return HttpResponse("service temporairement indisponible", status=417)



            return HttpResponse("good")
        else:
            return HttpResponse("mot de passe incorrect", status=403)
    else:
            #user doesn't exist
            #return Response(content, status=status.HTTP_404_NOT_FOUND)
        return HttpResponse("cet utilisateur n'exite pas",status=401)


@csrf_exempt
def updateDureeCommandeMobil(request,idClient,idCommande):
    idCommande = idCommande
    idClient = idClient
    #token = request.POST["token"]
    is_error=0
    #try:
    #    terminal = Terminal.objects.filter(token=token)[0]
    #except:
    #    is_error=1
    #    return HttpResponse("forbiden", status=403)
    if is_error==0:
        client=Client.objects.filter(idclient=idClient)[0]
        try:
            commande=Commande.objects.filter(idCommande=idCommande)[0]
            if client.idclient==commande.client.idclient:
                data='{'
                data+='"dure":'+str(commande.get_duree())+',"state":'+str(commande.state)
                if commande.state==3:
                    try:
                        terminal=Terminal.objects.filter(utilisateur=commande.livreur.personne)[0]
                        data += ',"longitude":"' + str(terminal.longitude) + '","latitude":"' + str(terminal.latitude)+'"'
                    except:
                        v=1
                data+='}'
                return  HttpResponse(data)
            else:
                return HttpResponse("error", status=401)
        except:
            return HttpResponse("commande not found", status=404)


@csrf_exempt
def checkForUpdate(request):
    nbrVersion="1"
    try:
        parametre3 = Parametre.objects.filter(key="version")[0]
        nbrVersion=parametre3.value
    except:
        nbrVersion = "1"
    data='{'
    data+='"version":'+nbrVersion
    data+='}'
    return HttpResponse(data)


@csrf_exempt
def resetTerminal(request):
    listeEntite = Entite.objects.filter(estSupprimer=0, estDesactiver=0)
    save_path = os.path.join("/home/teranga-admin")
    data = '{"listeEntite":['
    mstop = 0

    for entite in listeEntite:
        mstop = mstop + 1
        entite_folder = "C:/Users/root/PycharmProjects/senfood/static/"
        # save_path = os.path.join(BASE_DIR)
        with open(save_path + entite.logoEntite, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            # with open(os.path.join(entite_folder, entite.logoEntite), "rb") as image_file:
            #   encoded_string = base64.b64encode(image_file.read())
        tmp = '{'
        tmp += '"idEntite":"' + str(entite.idEntit) + '",'
        tmp += '"nom":"' + entite.nomEntite + '",'
        try:
            tmp += '"latitude":"' + entite.latitude + '",'
            tmp += '"longitude":"' + entite.longitude + '",'
        except:
            tmp += '"latitude":"",'
            tmp += '"longitude":"",'
        tmp += '"slogan":"' + entite.sloganEntite + '",'
        tmp += '"email":"' + entite.emailEntite + '",'
        tmp += '"numero":"' + entite.numeroEntite + '",'
        tmp += '"isPartner":' + str(entite.isPartern) + ','
        tmp += '"logo":"' + encoded_string + '"'
        tmp+='}'
        data +=tmp
        if mstop != listeEntite.count():
            data +=','
    data+=']'
    listeLocalite = Localite.objects.filter()
    localiteTab = '['
    localiteStop = 0
    for localite in listeLocalite:
        localiteStop = localiteStop + 1
        tmp= '{'
        tmp += '"id":' + str(localite.idLocalite) + ','
        tmp += '"libelle":"' + localite.libelle+'"'
        tmp += '}'
        if localiteStop != listeLocalite.count():
            tmp = tmp + ","
        localiteTab+=tmp
    localiteTab += ']'
    nbrVersion="1"
    try:
        parametre3 = Parametre.objects.filter(key="version")[0]
        nbrVersion=parametre3.value
    except:
        nbrVersion = "1"
    heureDebut=""
    heureFin=""
    prixMax=""
    try:
        parametre = Parametre.objects.filter(key="heure_debut")[0]
        heureDebut=parametre.value
        parametre3 = Parametre.objects.filter(key="heure_fin")[0]
        heureFin=parametre3.value
        parametre3 = Parametre.objects.filter(key="max_prix")[0]
        prixMax=parametre3.value
    except:
        heureDebut =""
        heureFin=""
        prixMax=""



    listeTarif=Tarif.objects.filter(estSupprimer=0)
    localiteStop = 0
    tarifTab="["
    for tarif in listeTarif:
        localiteStop = localiteStop + 1
        tmp= '{'
        tmp += '"id":' + str(tarif.idTarif) + ','
        tmp += '"libelle":"' + str(tarif.libelle)+'",'
        tmp += '"prix":"' + str(tarif.prix)+'",'
        tmp += '"min":"' + str(tarif.distanceMin)+'",'
        tmp += '"max":"' + str(tarif.distanceMax)+'"'
        tmp += '}'
        if localiteStop != listeTarif.count():
            tmp = tmp + ","
        tarifTab+=tmp
    tarifTab+="]"
    data = data + ',"listeLocalite":'+localiteTab+',"version":'+str(nbrVersion)+',"listeTarif":'+tarifTab+',"heure_debut":"'+heureDebut+'","heure_fin":"'+heureFin+'","max_prix":"'+prixMax+'"}'
    return HttpResponse(data)



