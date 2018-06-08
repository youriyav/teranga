# -*- coding: utf-8 -*-
import hashlib
import os
import re
import smtplib
import urllib
from datetime import datetime, timedelta, time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from random import randint
import requests

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.utils import timezone

from Entite.models import Entite
from categorie.models import Categorie
from client.models import Client
from localite.models import Localite
from log.models import Log
from produit.models import Produit
from sen_food.models import Personne
from sen_food.views import  decodeString, myhome
from utilisateur.models import Utilisateur
from validation.models import Validation
from client.MyAuth import PasswordlessAuthBackend
from pyfcm import FCMNotification
@login_required
def listeClient(request):
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            listeClient=Client.objects.filter(personne__estSupprimer=0).order_by('personne__nomPersonne','personne__prenomPersonne')

            paginator = Paginator(listeClient, 10)
            #s = '2004/03/30'
            #date = datetime.strptime(s, "%Y/%m/%d")
            #modified_date = date + timedelta(days=1)
            #datetime.strftime(modified_date, "%Y/%m/%d")
            page = request.GET.get('page')
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                users = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                users = paginator.page(paginator.num_pages)

            return render(request, 'listeClient.html', locals())
def AftercreateClient(request,idClient):
    is_error=0
    try:
        #, validation__estConfirmer = 0
        client=Client.objects.filter(idclient=idClient,validation__estValider=0)[0]
        validation=Validation.objects.filter(client=client,estValider=0,estSupprimer=0)[0]
        validation.estConfirmer=1
        validation.save()
    except:
        is_error=1
    if is_error==0:
        #result = push_service.notify_single_device(registration_id=my_id, data_message=data_message,
         #                                          time_to_live=300000)
        return render(request, 'create_account_redirect.html', locals())
    else:
        message = "page introuvables"
        return render(request, '404.html', locals())

def sendSms(numero,code):
    payload = {'accountid': 'TERANGA', 'password': 't3R12345', 'text': 'Bienvenue sur Teranga-Food, votre code de validation est le '+str(code), 'to': "'00221"+str(numero)+"'",'sender': 'TerangaFood'}
    requests.get("http://lampush.lafricamobile.com/api", params=payload)

def createClient(request):
    if request.POST:
        save_plus = request.POST.getlist('save_and')
        nom = request.POST["nom"]
        prenom = request.POST["prenom"]
        email = request.POST["email"]
        numero = request.POST["numero"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        is_error = 0
        if nom == "":
            errer_nom = "veuillez remplir ce champs"
            is_error = 1
        if prenom == "":
            errer_prenom = "veuillez remplir ce champs"
            is_error = 1
        if email == "":
            error_email = "veuillez remplir ce champs"
            is_error = 1
        else:
            if re.search(r"^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]+", email) is None:
                is_error = 1
                error_email = "email incorrect"
        if numero == "":
            error_numero = "veuillez remplir ce champs"
            is_error = 1
        else:
            if re.search(r"^[0-9]{9}$", numero) is None:
                is_error = 1
                error_numero = "numero incorrect"
            else:
                try:
                    _user=User.objects.filter(username=numero,is_active=1)[0]
                    if _user:
                        is_error = 1
                        error_numero = "un compte est déjà enregistré avec ce numero"
                except:
                    v=1
        if password == "":
            error_password = "veuillez remplir ce champs"
            is_error = 1
        #try:
        #    user = User.objects.filter(username=numero)[0]
        #except:
        #    user = User()
        #    user.email = ""
        #if user.email != "":
        #    error_login = u"Login déjà utilisé"
        #    is_error = 1

        if password2 != password:
            error_password = "les mots de passe ne sont pas identiques"
            is_error = 1
        try:
            _next = int(save_plus[0])
        except:
            _next = 0
        if is_error == 0:
            check = 0
            exist = 0
            listeValidation=Validation.objects.filter(estValider=0)
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
                v=1
            user = User(username=numero, email=email, first_name=nom, last_name=prenom,is_active=0)
            user.set_password(password)
            user.save()
            client = Client()
            client.user = user
            client.personne = personne
            #client.code=password
            client.save()
            validation = Validation()
            validation.client = client
            validation.keyValidation=var_tmp
            validation.save()
            data_message = {
                "code": var_tmp,
                "numero": numero
            }
            sendSms(numero, var_tmp)
            #result = push_service.notify_single_device(registration_id="", data_message=data_message,time_to_live=300000)
            #tmp_hash = email + u"#_senfoood000new" + str(validation.idValidation) + str(client.idclient) + u"==!" + str(
              #  1)
            #hash_object = hashlib.md5(tmp_hash)
            #validation_key = hash_object.hexdigest()
            #validation.keyValidation = validation_key
            # envoie d'email de vérification
            #author = formataddr((str(Header(u'SenFood', 'utf-8')), "yavouckolye@gmail.com"))
            #me = "yavouckolye@gmail.com"
            #msg = MIMEMultipart('alternative')
            #msg['Subject'] = "Validation compte"
            #msg['From'] = author
            #msg['To'] = email
            #html = "<html>" \
            #       "<head>" \
            #       "</head>" \
            #       "<body>" \
            #       "<h2>Salut "+nom +" "+ prenom+" </h2>" \
            #       "<h3>Bienvenue sur SenFood</h3>" \
            #       "pour valider votre inscription, veuillez cliquez sur ce <a href=\"http://localhost:8000/compte/validation-compte/" + str(
            #   validation.keyValidation) + "\">lien</a> " \
            #                               " suivant." \
            #                               "</body>" \
            #                               "</html>"
            #part2 = MIMEText(html, 'html')
            #msg.attach(part2)
            #server = smtplib.SMTP('smtp.gmail.com', 587)
            #server.starttls()
            #server.login(me, "nkjqsajyzgkbueyy")
            #text = msg.as_string()
            #server.sendmail(me, email, text)
            #server.quit()
            log = Log()
            log.utilisateur = request.user.username
            log.action = "Creation compte client " + nom+" "+prenom +" "+numero
            log.save()
            return redirect(AftercreateClient,client.idclient)
        else:
            return render(request, 'create_client.html', locals())
    else:
        v = 1
        return render(request, 'create_client.html', locals())
def validerCompteClient(request):
    global code_erreur
    if request.POST:
        keyValidation=request.POST["keyValidation"]
        is_error=0
        if keyValidation=="":
            is_error=1
            code_erreur="veuillez remplir ce champs"
        if is_error==0:
            try:
                validation = Validation.objects.filter(keyValidation=keyValidation, estValider=0, estSupprimer=0)[0]
                if validation.keyValidation != "":
                    user = authenticate(token=keyValidation)
                    tmp = validation.dateCreation
                    date_save = datetime.strftime(tmp, '%Y-%m-%d %H:%M:%S')
                    currentDate = datetime.now()
                    diff = currentDate - datetime.strptime(date_save, '%Y-%m-%d %H:%M:%S')
                    diff1 = diff.total_seconds()
                    log = Log()
                    result = 1
                    user.is_active = 1
                    user.save()
                    # username = request.POST["username"]
                    # password = request.POST["password"]
                    # user = auth.authenticate(username=username, password=password)
                    if user:
                        auth.login(request, user)
                        return redirect(myhome)
                    log.action = "activation compte  pour le client " + validation.client.personne.numeroPersonne
                    log.save()
                        # return render(request, 'token_expired.html', locals())
                    return HttpResponse("succes")
                return HttpResponse("#erreur", status=405)
            except:
                code_erreur = "code erroné"
                return HttpResponse(code_erreur, status=405)
        else:
            return HttpResponse(code_erreur,status=403)
    else:
        return redirect(loginClient)

def regenererToken(request):
    global var_tmp
    if request.POST:
        keyValidation=request.POST["keyValidation"]
        is_error=0
        if keyValidation=="":
            is_error=1
            code_erreur="veuillez entrer votre code"
        if is_error==0:
            try:
                validation = Validation.objects.filter(keyValidation=keyValidation, estValider=0, estSupprimer=0)[0]
            except:
                validation=Validation()
                validation.keyValidation=""
            if validation.keyValidation!="":
                validation.estSupprimer=1
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
                log.action = u"regeneration token pour validation compte client pour " + decodeString(validation.client.user.username)
                log.save()
                return render(request, 'after_regener_validation.html', locals())
            else:
                message="page introuvable"
                return render(request, '404.html', locals())
        else:
            return render(request, 'create_account_redirect.html', locals())
    else:
        return redirect(loginClient)



def regenererTokenService(request):
    global var_tmp
    if request.POST:
        keyValidation=request.POST["keyValidation"]
        is_error=0
        if keyValidation=="":
            is_error=1
            code_erreur="veuillez entrer votre code"
        validation=None
        if is_error==0:
            try:
                validation = Validation.objects.filter(keyValidation=keyValidation, estValider=0, estSupprimer=0)[0]
            except:
                is_error=1
            if is_error==0:
                validations = Validation.objects.filter(client=validation.client)
                if validations.count()<3:
                    validation.estSupprimer=1
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
                    log.action = u"regénération token pour validation compte client pour " + str(validation.client.user.username)
                    log.save()
                    return HttpResponse(str(var_tmp))
                else:
                    date_save = datetime.strftime(validations.last().dateCreation, '%Y-%m-%d %H:%M:%S')
                    currentDate = datetime.now()
                    diff = currentDate - datetime.strptime(date_save, '%Y-%m-%d %H:%M:%S')
                    res = diff.seconds / 60
                    if res<60:
                        tmp=60-res
                        return HttpResponse("Désolé, Veuillez réessayer dans "+str(tmp)+" minute (s)", status=406)
            else:
                message="page introuvable"
                return HttpResponse("bad token", status=403)
        else:
            return HttpResponse("token invalid", status=401)
    else:
        return HttpResponse("bad request", status=402)




@login_required
def homeClient(request,idClient):
    client = Client.objects.filter(idclient=idClient)[0]
    listeEntite = Entite.objects.filter(estSupprimer=0, estDesactiver=0)
    #destination = open(os.path.join(entite_folder, logo_name), 'wb+')

    return render(request, 'homeClient.html', locals())

def loginClient(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            muser=User.objects.filter(username=username)[0]
            client=Client.objects.filter(user=muser)[0]
            validation=Validation.objects.filter(client=client,estValider=0,estSupprimer=0)[0]
            return redirect(AftercreateClient,client.idclient)
        except:
            v=1
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return  redirect(myhome)
        else:
            login_message="Login ou mot de passe incorrect"
            return render(request, 'login.html', locals())
    else:
        return render(request, 'login.html', locals())

def homeEntiteClient(request, idfastFood):
    is_error = 0
    try:
        listelocalite = Localite.objects.filter(estSupprimer=0,isActive=1)
        #nom = urllib.unquote(nomfastFood[2:]).decode('utf8')
        entite = Entite.objects.filter(idEntit=idfastFood)[0]
        listeCategorie = Categorie.objects.filter(entite=entite,estSupprimer=0,estDesactiver=0)
        #listeProduit = Produit.objects.filter(categorie__entite=entite,estSupprimer=0)
    except:
        is_error = 1
    if is_error == 0:
        return render(request, 'homefast.html', locals())
    else:
        if int(idfastFood) == 0:
            listeEntite=Entite.objects.filter(isPartern=0,estSupprimer=0, estDesactiver=0)
            zones= Localite.objects.filter(estSupprimer=0,isActive=1)
            return render(request, 'homeEntiteNonPartner.html', locals())
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())

def ListeProduitCategorie(request, idEntite,idCategorie):
    is_error = 0
    try:
        listelocalite=Localite.objects.filter(estSupprimer=0)
        entite = Entite.objects.filter(idEntit=idEntite)[0]
        zones = Localite.objects.all()
        categorie = Categorie.objects.filter(idCategorie=idCategorie)[0]
        listeProduit = Produit.objects.filter(categorie=categorie, estSupprimer=0,estDesactiver=0)
    except:
        is_error = 1
    if is_error == 0:
        return render(request, 'listeProduit.html', locals())
    else:
        message = "page introuvable"
        return render(request, '404.html', locals())
 #try:
        #client=Client.objects.filter(idclient=idClient,validation__estValider=1,personne__estSupprimer=0,user__is_active=1)[0]
        #return render(request, 'homeClient.html', locals())
    #except:
       # message = "page introuvables"
        #return render(request, '404.html', locals())

def changeImageProfil(request):
    global var_tmp
    if request.POST:
        is_error=0

        try:
            user = request.user
            myfile = request.FILES['logo']
            save_path = "C:/Users/root/PycharmProjects/senfood/static/images/uploads/client"
            last = myfile.name[myfile.name.rfind("."):len(myfile.name)]
            tmp_var = user.client.personne.estModifier + 1
            logo_name = "profil_" + decodeString(user.client.personne.numeroPersonne) + "_" + str(tmp_var) + last
            user.client.personne.profilPersonne ="images/uploads/client/"+logo_name
            user.client.personne.estModifier = tmp_var
            user.client.personne.save()
            destination = open(os.path.join(save_path, logo_name), 'wb+')
            # if destination.isatty
            for chunk in myfile.chunks():
                destination.write(chunk)
            destination.close()
        except:
            is_error = 1
        return HttpResponse("good "+str(is_error))



def searchClient(request):
    if request.POST:
        username = request.POST["username"]
        try:
            listeClient = Client.objects.filter(personne__estSupprimer=0).order_by('personne__nomPersonne','personne__prenomPersonne')
        except:
            v=1
        return render(request, 'login.html', locals())

@login_required
def bloquerClient(request,idClient):
    try:
        client=Client.objects.filter(idclient=idClient)[0]
        client.estBloquer=1
        client.save()
    except:
        v=1
    return redirect(listeClient)
@login_required
def debloquerClient(request,idClient):
    try:
        client=Client.objects.filter(idclient=idClient)[0]
        client.estBloquer=0
        client.save()
    except:
        v=1
    return redirect(listeClient)
