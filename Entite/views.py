# -*- coding: utf-8 -*-
import base64
import os
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from Entite.models import Entite
from categorie.models import Categorie
from log.models import Log
from produit.models import Produit
from restaurant.models import Restaurant
from sen_food.models import Personne
from sen_food.views import decodeString
from utilisateur.models import Utilisateur


@login_required
def listeEntite(request):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            listeEntite=Entite.objects.filter(estSupprimer=0)
            return render(request, 'listeEntite.html', locals())


@login_required
def createEntite(request):
    global myfile
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            if request.POST:
                is_error=0
                nom=request.POST["nom"]
                slogan=request.POST["slogan"]
                email=request.POST["email"]
                numero=request.POST["numero"]
                couleur=request.POST["coleur"]
                save_plus = request.POST.getlist('save_and')
                if nom=="":
                    errer_nom="veuiller remplir ce champs"
                    is_error=1
                if slogan == "":
                    error_slogan = "veuiller remplir ce champs"
                    is_error = 1
                if email == "":
                    error_email = "veuiller remplir ce champs"
                    is_error = 1
                if numero == "":
                    error_numero = "veuiller remplir ce champs"
                    is_error = 1
                try:
                    myfile = request.FILES['logo']
                except:
                    error_logo="veuillez selectionner une image"
                    is_error=1
                #fs = FileSystemStorage()

                if is_error==0:
                    entite = Entite()
                    entite.createurEntite=request.user
                    entite.save()
                    try:
                        os.mkdir(os.path.join(settings.MEDIA_ROOT, str(entite.idEntit)))
                    except:
                        v=1
                    save_path = settings.MEDIA_ROOT + str(entite.idEntit)
                    last = myfile.name[myfile.name.rfind("."):len(myfile.name)]
                    logo_name = "logo_" + str(entite.idEntit)+ last
                    fs = FileSystemStorage()
                    fs.save(settings.MEDIA_ROOT + str(entite.idEntit)+"/" + logo_name, myfile)
                    entite.nomEntite = nom
                    entite.sloganEntite = slogan
                    entite.emailEntite = email
                    entite.numeroEntite = numero
                    entite.ColeurEntite=couleur
                    entite.createurEntite=request.user
                    entite.logoEntite="/media/"+str(entite.idEntit)+"/"+logo_name
                    entite.save()
                    log = Log()
                    log.utilisateur = request.user.username
                    log.action = u"Création entite " + nom
                    log.save()
                    data='{'
                    data+='"nom":"'+entite.nomEntite+'",'
                    data+='"slogan":"'+entite.sloganEntite+'"'
                    data+='"email":"'+entite.emailEntite+'",'
                    data+='"numero":"'+entite.numeroEntite+'",'
                    data+='"id":"'+str(entite.idEntit)+'",'
                    with open(os.path.join(save_path,logo_name ), "rb") as image_file:
                        encoded_string_prod = base64.b64encode(image_file.read())
                    data+='"logo":"'+encoded_string_prod+'"'
                    data+='}'
                    messages.success(request, 'Entité ajoutée avec succès')
                    try:
                        _next = int(save_plus[0])
                    except:
                        _next = 0
                    if _next == 0:
                        return redirect(listeEntite)
                    else:
                        nom = ""
                        slogan = ""
                        email = ""
                        numero = ""
                        return render(request, 'creationEntite.html', locals())
                else:
                    entite=Entite()
                    entite.nomEntite=nom
                    entite.sloganEntite=slogan
                    entite.emailEntite=email
                    entite.numeroEntite=numero
                    return render(request, 'creationEntite.html', locals())
            else:
                return render(request, 'creationEntite.html', locals())
@login_required
def editEntite(request,idEntite):
    global myfile,is_file
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            if request.POST:
                is_error=0
                nom=request.POST["nom"]
                slogan=request.POST["slogan"]
                email=request.POST["email"]
                numero=request.POST["numero"]
                couleur=request.POST["coleur"]
                save_plus = request.POST.getlist('save_and')
                if nom=="":
                    errer_nom="veuiller remplir ce champs"
                    is_error=1
                if slogan == "":
                    error_slogan = "veuiller remplir ce champs"
                    is_error = 1
                if email == "":
                    error_email = "veuiller remplir ce champs"
                    is_error = 1
                if numero == "":
                    error_numero = "veuiller remplir ce champs"
                    is_error = 1
                is_file=0
                try:
                    myfile = request.FILES['logo']
                    is_file=1
                except:
                    error_logo=""
                    #is_error=1
                fs = FileSystemStorage()
                #filename =  fs.save("C:\Users\root\PycharmProjects\senfood/static/"+myfile.name, myfile)
                if is_error==0:

                    #try:
                        entite = Entite.objects.filter(idEntit=idEntite)[0]
                        entite.nomEntite = nom
                        entite.sloganEntite = slogan
                        entite.emailEntite = email
                        entite.numeroEntite = numero
                        entite.ColeurEntite = couleur
                        entite.createurEntite = request.user
                        entite.estModifier = entite.estModifier + 1
                        entite.save()
                        if is_file==1:
                            save_path = settings.MEDIA_ROOT +str(entite.idEntit)
                            last = myfile.name[myfile.name.rfind("."):len(myfile.name)]
                            logo_name = "logo_" + str(entite.idEntit) + "_edit_"+str(entite.estModifier) + last
                            fs = FileSystemStorage()
                            fs.save(settings.MEDIA_ROOT + str(entite.idEntit) + "/" + logo_name, myfile)
                            entite.logoEntite = "/media/" + str(entite.idEntit) + "/" + logo_name
                        entite.save()
                        log = Log()
                        log.utilisateur = request.user.username
                        log.action = u"Modifier entité " + nom
                        log.save()
                        messages.success(request, 'Entité modifiée avec succès')
                        return redirect(listeEntite)
                    #except:
                      #  check = 1
                    #return redirect(listeEntite)
                else:

                    return render(request, 'editerEntite.html', locals())
            else:
                check=0
                try:
                    entite=Entite.objects.filter(idEntit=idEntite)[0]
                    nom=entite.nomEntite
                    slogan=entite.sloganEntite
                    email=entite.emailEntite
                    numero=entite.numeroEntite
                    couleur=entite.ColeurEntite
                except:
                    check=1
                if check ==0:
                    #test = entite.nomEntite
                    return render(request, 'editerEntite.html', locals())
                else:
                    message="intouvable"
                    return render(request, '404.html', locals())


@login_required
def desableEntite(request,idEntite):
    if request.user.is_superuser:
        is_error=0
        try:
            entite = Entite.objects.filter(idEntit=idEntite)[0]
            entite.estDesactiver=1
            entite.save()
            log = Log()
            log.utilisateur = request.user.username
            log.action = u"Desactivation  entité " + entite.nomEntite
            log.save()
            messages.success(request, u'Entité desactivée avec succès')
        except:
            is_error = 1
        if is_error == 0:
            return redirect(listeEntite)
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())
        #if request.GET:

@login_required
def enableEntite(request,idEntite):
    if request.user.is_superuser:
        is_error=0
        try:
            entite = Entite.objects.filter(idEntit=idEntite)[0]
            entite.estDesactiver=0
            entite.save()
            log = Log()
            log.utilisateur = request.user.username
            log.action = u"Activation  entité " + entite.nomEntite
            log.save()
            messages.success(request, u'Entité activée avec succès')
        except:
            is_error = 1
        if is_error == 0:
            return redirect(listeEntite)
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())
        #if request.GET:


@login_required
def supprimerEntite(request):
    global message
    if request.user.is_superuser:
        idEntite = request.POST["idEntite"]
        is_error=0
        try:
            entite = Entite.objects.filter(idEntit=idEntite)[0]
            entite.estSupprimer=1
            entite.save()
            log = Log()
            log.utilisateur = request.user.username
            log.action = u"suppréssion  entité " + decodeString(entite.nomEntite)
            log.save()
            message=u"Entité supprimée avec succès"
        except:
            is_error = 1
            message="error"
        return HttpResponse(message)
        #return render(request, '404.html', locals())

@login_required
def ajouterManagerEntite(request,idEntite):
    if request.user.is_superuser:
        if request.POST:
            save_plus = request.POST.getlist('save_and')
            nom = request.POST["nom"]
            prenom = request.POST["prenom"]
            email = request.POST["email"]
            numero = request.POST["numero"]
            login = request.POST["login"]
            password = request.POST["password"]
            password2 = request.POST["password2"]
            is_error=0
            if nom=="":
                errer_nom="veuillez remplir ce champs"
                is_error=1
            if prenom=="":
                errer_prenom="veuillez remplir ce champs"
                is_error=1
            if login == "":
                error_login = "veuillez remplir ce champs"
                is_error = 1
            if email=="":
                error_email="veuillez remplir ce champs"
                is_error=1
            else:
                if re.search(r"^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]+", email) is None:
                    is_error = 1
                    error_email = "email incorrect"
            if numero=="":
                error_numero="veuillez remplir ce champs"
                is_error=1
            else:
                if re.search(r"^[0-9]{9}$", numero) is None:
                    is_error = 1
                    error_numero = "numero incorrect"
            if password=="":
                error_password="veuillez remplir ce champs"
                is_error=1
            try:
                user = User.objects.filter(username=login)[0]
            except:
                user=User()
                user.email=""
            if user.email!="":
                error_login = u"Login déjà utilisé"
                is_error = 1
            else:
                if password2!=password:
                    error_password = "les mots de passe ne sont pas identiques"
                    is_error = 1
            try:
                _next=int(save_plus[0])
            except:
                _next=0
            if is_error==0:
                personne=Personne()
                personne.nomPersonne=nom
                personne.prenomPersonne=prenom
                personne.numeroPersonne=numero
                personne.emailPersonne=email
                personne.createur=request.user
                personne.save()
                user=User(username=login,email=email,first_name=nom,last_name=prenom)
                user.set_password(password)
                user.is_staff=1
                user.save()
                utilisateur=Utilisateur()
                utilisateur.isManager=1
                utilisateur.droit=2
                utilisateur.user=user
                utilisateur.personne=personne
                entite = Entite.objects.filter(idEntit=idEntite)[0]
                utilisateur.entite=entite
                utilisateur.save()
                log=Log()
                log.utilisateur=request.user.username
                tmpString=personne.nomPersonne
                log.action=decodeString("Création manager ")+tmpString+u" pour entité "+decodeString(entite.nomEntite)
                log.save()
                if _next==0:
                    return redirect(profilEntite,idEntite)
                else:
                    login=""
                    nom=""
                    prenom=""
                    email=""
                    numero=""
                    return render(request, 'addManager.html', locals())

            else:
                return render(request, 'addManager.html', locals())
        else:
            return render(request, 'addManager.html', locals())


@login_required
def profilEntite(request,idEntite):
    if request.user.is_superuser:
        is_error=0
        try:
            entite = Entite.objects.filter(idEntit=idEntite)[0]
            listeManager=Utilisateur.objects.filter(entite=entite,personne__estSupprimer=0)
            listeRestaurant=Restaurant.objects.filter(entite=entite,estSupprimer=0)
            nbrProduit=Produit.objects.filter(categorie__entite=entite).count()
            nbrCat=entite.categorie_set.filter(estSupprimer=0).count()
            nbrProd=Produit.objects.filter(categorie__entite=entite,estSupprimer=0).count()
        except:
            is_error = 1
        if is_error == 0:
            return render(request, 'profil_entite.html', locals())
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())
        #if request.GET:
@login_required
def menuEntite(request,idEntite):
    if request.user.is_authenticated() and request.user.is_superuser:
        is_error = 0
        try:
            entite = Entite.objects.filter(idEntit=idEntite)[0]
            listeCategorie = Categorie.objects.filter(entite=entite,estSupprimer=0).order_by('libelleCat')
            #listeRestaurant = Restaurant.objects.filter(entite=entite, estSupprimer=0)
        except:
            is_error = 1
        if is_error == 0:
            return render(request, 'menu.html', locals())
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())

def homeEntite(request,nomfastFood):
        is_error=0
        try:
            nom=nomfastFood[2:]
            entite = Entite.objects.filter(nomEntite=nom)[0]
            #listeCategorie=Categorie.objects.filter(entite=entite,estSupprimer=0)
            listeProduit=Produit.objects.filter(categorie__entite=entite,estSupprimer=0)
        except:
            is_error = 1
        if is_error == 0:
            return render(request, 'homefast.html', locals())
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())