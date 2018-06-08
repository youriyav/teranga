# coding=utf-8
import os
import re
from tkSimpleDialog import _QueryDialog

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.context_processors import request

from Entite.models import Entite
from Entite.views import profilEntite
from log.models import Log
from restaurant.models import Restaurant
from sen_food.models import Personne
from sen_food.views import decodeString
from utilisateur.models import Utilisateur


@login_required
def listeRestaurant(request):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            listeEntite=Entite.objects.filter(estSupprimer=0)
            return render(request, 'listeRestaurant.html', locals())


@login_required
def createRestaurant(request,idEntite):
    global myfile, entite
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            global ckeck
            try:
                entite = Entite.objects.filter(idEntit=idEntite)[0]
                check=1
            except:
                check=0
            if check ==1:
                if request.POST:
                    is_error = 0
                    nom = request.POST["nom"]
                    quartier = request.POST["quartier"]
                    email = request.POST["email"]
                    numero = request.POST["numero"]
                    latitude = request.POST["latitude"]
                    longitude = request.POST["longitude"]
                    # couleur=request.POST["coleur"]
                    save_plus = request.POST.getlist('save_and')
                    if latitude == "":
                        error_latitude = "veuiller remplir ce champs"
                        is_error = 1
                    if longitude == "":
                        error_longitude = "veuiller remplir ce champs"
                        is_error = 1
                    if nom == "":
                        errer_nom = "veuiller remplir ce champs"
                        is_error = 1
                    if quartier == "":
                        error_quartier = "veuiller remplir ce champs"
                        is_error = 1
                    if email == "":
                        error_email = "veuiller remplir ce champs"
                        is_error = 1
                    else:
                        if re.search(r"^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]+", email) is None:
                            is_error = 1
                            error_email = "email incorrect"
                    if numero == "":
                        error_numero = "veuiller remplir ce champs"
                        is_error = 1
                    else:
                        if re.search(r"^[0-9]{9}$", numero) is None:
                            is_error = 1
                            error_numero = "numero incorrect"
                    try:
                        myfile = request.FILES['logo']
                    except:
                        error_logo = "veuillez selectionner une image"
                        is_error = 1
                    # fs = FileSystemStorage()
                    if is_error == 0:
                        restaurant=Restaurant()
                        restaurant.nomRestaurant=nom
                        restaurant.numeroRestaurant=numero
                        restaurant.emailRestaurant=email
                        restaurant.createurRestaurant=request.user
                        restaurant.entite=entite
                        restaurant.quartierRestaurant=quartier
                        restaurant.longiRestaurant=longitude
                        restaurant.latiRestaurant=latitude
                        entite_folder = "C:/Users/root/PycharmProjects/senfood/static/images/uploads/"
                        save_path = "C:/Users/root/PycharmProjects/senfood/static/images/uploads/" +decodeString(entite.nomEntite)
                        logo_name = "restau_" + nom + "_" + myfile.name
                        destination = open(os.path.join(save_path, logo_name), 'wb+')
                        restaurant.logoRestaurant = "images/uploads/" + decodeString(entite.nomEntite) + "/" + logo_name
                        restaurant.save()
                        for chunk in myfile.chunks():
                            destination.write(chunk)
                        destination.close()

                        log = Log()
                        log.utilisateur = request.user.username
                        log.action = "Creation restaurant " + nom+" pour l'entite "+decodeString(entite.nomEntite)
                        messages.success(request, 'Restaurant ajouté avec succès')
                        try:
                            _next = int(save_plus[0])
                        except:
                            _next = 0

                        if _next == 0:
                            v=5
                            #return render(request, 'creationRestaurant.html', locals())
                            return redirect(profilEntite,idEntite)
                        else:
                            nom = ""
                            quartier = ""
                            email = ""
                            numero = ""
                            longitude=""
                            latitude=""
                            return render(request, 'creationRestaurant.html', locals())
                    else:
                        # entite=Entite()
                        # entite.nomEntite=nom
                        # entite.sloganEntite=slogan
                        # entite.emailEntite=email
                        # entite.numeroEntite=numero
                        return render(request, 'creationRestaurant.html', locals())
                else:
                    return render(request, 'creationRestaurant.html', locals())
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())


@login_required
def editerRestaurant(request,idRestaurant):
    global myfile, restaurant
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            global ckeck
            try:
                restaurant=Restaurant.objects.filter(idRestaurant=idRestaurant)[0]
                check=1
            except:
                check=0
            if check ==1:
                if request.POST:
                    is_error = 0
                    nom = request.POST["nom"]
                    quartier = request.POST["quartier"]
                    email = request.POST["email"]
                    numero = request.POST["numero"]
                    latitude = request.POST["latitude"]
                    longitude = request.POST["longitude"]
                    # couleur=request.POST["coleur"]
                    if latitude == "":
                        error_latitude = "veuiller remplir ce champs"
                        is_error = 1
                    if longitude == "":
                        error_longitude = "veuiller remplir ce champs"
                        is_error = 1
                    if nom == "":
                        errer_nom = "veuiller remplir ce champs"
                        is_error = 1
                    if quartier == "":
                        error_quartier = "veuiller remplir ce champs"
                        is_error = 1
                    if email == "":
                        error_email = "veuiller remplir ce champs"
                        is_error = 1
                    else:
                        if re.search(r"^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]+", email) is None:
                            is_error = 1
                            error_email = "email incorrect"
                    if numero == "":
                        error_numero = "veuiller remplir ce champs"
                        is_error = 1
                    else:
                        if re.search(r"^[0-9]{9}$", numero) is None:
                            is_error = 1
                            error_numero = "numero incorrect"
                    # fs = FileSystemStorage()
                    if is_error == 0:
                        restaurant = Restaurant.objects.filter(idRestaurant=idRestaurant)[0]
                        restaurant.nomRestaurant=nom
                        restaurant.numeroRestaurant=numero
                        restaurant.emailRestaurant=email
                        restaurant.modificateurRestaurant=request.user
                        restaurant.estModifier=restaurant.estModifier+1
                        restaurant.quartierRestaurant=quartier
                        restaurant.longiRestaurant=longitude
                        restaurant.latiRestaurant=latitude
                        try:
                            myfile = request.FILES['logo']
                            entite_folder = "C:/Users/root/PycharmProjects/senfood/static/images/uploads/"
                            save_path = "C:/Users/root/PycharmProjects/senfood/static/images/uploads/" + restaurant.entite.nomEntite
                            logo_name = "restau_" + nom + "_" + myfile.name
                            destination = open(os.path.join(save_path, logo_name), 'wb+')
                            restaurant.logoRestaurant = "images/uploads/" +  restaurant.entite.nomEntite + "/" + logo_name
                            for chunk in myfile.chunks():
                                destination.write(chunk)
                            destination.close()
                        except:
                            v=1
                        restaurant.save()
                        log = Log()
                        log.utilisateur = request.user.username
                        log.action = "Modification restaurant " + nom+" pour l'entite "+decodeString(restaurant.entite.nomEntite)
                        log.save()
                        messages.success(request, 'Restaurant modifié avec succès')
                        return redirect(profilEntite,restaurant.entite.idEntit)
                    else:
                        # entite=Entite()
                        # entite.nomEntite=nom
                        # entite.sloganEntite=slogan
                        # entite.emailEntite=email
                        # entite.numeroEntite=numero
                        id = restaurant.entite.idEntit
                        return render(request, 'editerRestaurant.html', locals())
                else:
                    nom = restaurant.nomRestaurant
                    quartier = restaurant.quartierRestaurant
                    email = restaurant.emailRestaurant
                    numero = restaurant.numeroRestaurant
                    latitude = restaurant.latiRestaurant
                    longitude = restaurant.longiRestaurant
                    id=restaurant.entite.idEntit
                    return render(request, 'editerRestaurant.html', locals())
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())




@login_required
def desactiverRestaurant(request,idRestaurant):
    global myfile, restaurant
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            global ckeck
            try:
                restaurant=Restaurant.objects.filter(idRestaurant=idRestaurant)[0]
                check=1
            except:
                check=0
            if check ==1:
                restaurant.estDesactiver=1
                restaurant.save()
                log = Log()
                log.utilisateur = request.user.username
                log.action = u"Désactivation restaurant " + decodeString(restaurant.nomRestaurant) + " pour l'entite " + decodeString(
                    restaurant.entite.nomEntite)
                log.save()
                messages.success(request, 'Restaurant désactivé avec succès')
                return redirect(profilEntite, restaurant.entite.idEntit)
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())



@login_required
def activerRestaurant(request,idRestaurant):
    global myfile, restaurant
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            global ckeck
            try:
                restaurant=Restaurant.objects.filter(idRestaurant=idRestaurant)[0]
                check=1
            except:
                check=0
            if check ==1:
                restaurant.estDesactiver=0
                restaurant.save()
                log = Log()
                log.utilisateur = request.user.username
                log.action = "activation restaurant " + decodeString(
                    restaurant.nomRestaurant) + " pour l'entite " + decodeString(
                    restaurant.entite.nomEntite)
                log.save()
                messages.success(request, 'Restaurant activé avec succès')
                return redirect(profilEntite, restaurant.entite.idEntit)
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())



@login_required
def supprimerRestaurant(request):
    global message, restaurant
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            idRestaurant = request.POST["idRestaurant"]
            is_error = 0
            try:
                restaurant = Restaurant.objects.filter(idRestaurant=idRestaurant)[0]
            except:
                is_error = 1
            if is_error == 0:
                restaurant.estSupprimer = 1
                restaurant.save()
                log = Log()
                log.utilisateur = request.user.username
                log.action = u"suppréssion  du restaurant " + decodeString(restaurant.entite.nomEntite)
                log.save()
                message = u"Restaurant supprimé avec succès"
            else:
                message = "error"
            return HttpResponse(message)
            #if request.POST:


@login_required
def showOnMapRestaurant(request):
    global message, restaurant
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            idRestaurant = request.POST["idRestaurant"]
            is_error = 0
            try:
                restaurant = Restaurant.objects.filter(idRestaurant=idRestaurant)[0]
            except:
                is_error = 1
            if is_error == 0:
                restaurant.estSupprimer = 1
                restaurant.save()
                log = Log()
                log.utilisateur = request.user.username
                log.action = u"suppréssion  du restaurant " + decodeString(restaurant.entite.nomEntite)
                log.save()
                message = u"Restaurant supprimé avec succès"
            else:
                message = "error"
            return HttpResponse(message)
            #if request.POST:

