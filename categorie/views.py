# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Entite.models import Entite
from Entite.views import menuEntite
from categorie.models import Categorie
from image.models import Image
from log.models import Log
from restaurant.models import Restaurant
from sen_food.views import decodeString
from utilisateur.models import Utilisateur
from django.core.files.storage import FileSystemStorage

@login_required
def listeCategorie(request,idEntite):
    if request.user.is_authenticated() and request.user.is_superuser:
        is_error = 0
        entite=Entite()
        try:
            entite = Entite.objects.filter(idEntit=idEntite)[0]
        except:
            is_error = 1
        try:
            listeCategorie = Categorie.objects.filter(entite=entite,estSupprimer=0).order_by('libelleCat')
        except:
            listeCategorie=[]
        if is_error == 0:
            return render(request, 'liste_categorie.html', locals())
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())

@login_required
def creerCategorie(request,idEntite):
    global  myfile
    if request.user.is_authenticated() and request.user.is_superuser:
        is_error = 0
        try:
            entite = Entite.objects.filter(idEntit=idEntite)[0]
        except:
            is_error = 1
        if is_error == 0:
            listeImage=Image.objects.filter(estSupprimer=0,type=2)
            if request.POST:
                libelle=request.POST["libelle"]
                descript=request.POST["descript"]
                libelle=request.POST["libelle"]
                image=int(request.POST["image"])
                if libelle=="":
                    is_error=1
                    error_libelle="veuillez remplier ce champs"
                if descript=="":
                    is_error=1
                    error_descript="veuillez remplier ce champs"
                save_plus = request.POST.getlist('save_and')
                if image==0:
                    is_error=1
                    error_logo = "veuillez selectionner une image"
                if is_error==0:
                    ima = Image.objects.filter(idImage=image)[0]
                    categorie=Categorie()
                    categorie.logoCat=ima
                    categorie.createurCat=request.user
                    categorie.entite=entite
                    categorie.libelleCat=libelle
                    categorie.descriptionCat=descript
                    categorie.save() 
                    #entite.logoEntite="images/uploads/"+nom+"/"+logo_name 
                    log = Log()
                    log.utilisateur = request.user.username
                    log.action = u"Création catégorie pour entité " + entite.nomEntite
                    log.save()
                    messages.success(request, u'Catégorie ajoutée avec succès')
                    try:
                        _next = int(save_plus[0])
                    except:
                        _next = 0
                    if _next == 0:
                        return redirect(listeCategorie,idEntite)
                    else:
                        libelle = ""
                        descript=""
                        return render(request, 'nouveau_categorie.html', locals())
                else:
                    return render(request, 'nouveau_categorie.html', locals())
            else:
                return render(request, 'nouveau_categorie.html', locals())
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())


@login_required
def editerCategorie(request,idCategorie):
    global  myfile
    if request.user.is_authenticated() and request.user.is_superuser:
        is_error = 0
        is_image_change = 0
        try:
            categorie = Categorie.objects.filter(idCategorie=idCategorie)[0]
        except:
            is_error = 1
        if is_error == 0:
            listeImage = Image.objects.filter(estSupprimer=0, type=2)
            if request.POST:
                libelle=request.POST["libelle"]
                descript=request.POST["descript"]
                libelle=request.POST["libelle"]
                image = int(request.POST["image"])
                if libelle=="":
                    is_error=1
                    error_libelle="veuillez remplier ce champs"
                if descript=="":
                    is_error=1
                    error_descript="veuillez remplier ce champs"
                save_plus = request.POST.getlist('save_and')
                if image!=0:
                    is_image_change = 1
                if is_error==0:
                    entite=Entite.objects.filter(categorie=categorie)[0]
                    if is_image_change==1:
                        ima = Image.objects.filter(idImage=image)[0]
                        categorie.logoCat=ima
                    categorie.modificateurCat=request.user
                    categorie.libelleCat=libelle
                    categorie.descriptionCat=descript
                    categorie.estModifier=categorie.estModifier+1
                    categorie.save()
                    log = Log()
                    log.utilisateur = request.user.username
                    log.action = u"modification catégorie pour entité " + entite.nomEntite
                    log.save()
                    messages.success(request, u'Catégorie modifiée avec succès')
                    libelle = ""
                    descript=""
                    return redirect(listeCategorie,entite.idEntit)
                else:
                    return render(request, 'editer_categorie.html', locals())
            else:
                entite=Entite.objects.filter(categorie=categorie)[0]
                libelle=categorie.libelleCat
                descript=categorie.descriptionCat
                return render(request, 'editer_categorie.html', locals())
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())

@login_required
def loadImage(request,idEntite):
    global entite, myfile
    if request.user.is_authenticated() and request.user.is_superuser:
        is_error = 0
        try:
            entite = Entite.objects.filter(idEntit=idEntite)[0]
        except:
            is_error = 1
        if is_error == 0:
                try:
                    myfile = request.FILES['logo']
                except:
                    error_logo = "veuillez selectionner une image"
                    is_error = 1
                if is_error==0:
                    message="good"
                    return HttpResponse(message)
                else:
                    message = "bad"
                return HttpResponse(message)
        else:
            message ="entité inexistante"
            return  HttpResponse(message)


@login_required
def supprimerCategorie(request,idCategorie):
    global  myfile, categorie
    if request.user.is_authenticated() and request.user.is_superuser:
        is_error = 0
        try:
            categorie = Categorie.objects.filter(idCategorie=idCategorie)[0]
        except:
            is_error = 1
        if is_error == 0:
            categorie.estSupprimer=1
            categorie.save()
            log = Log()
            log.utilisateur = request.user.username
            log.action = u"Suppréssion catégorie pour entité " + categorie.entite.nomEntite
            log.save()
            messages.success(request, u'Catégorie supprimée avec succès')
            return redirect(listeCategorie, categorie.entite.idEntit)
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())

@login_required
def desactiverCategorie(request,idCategorie):
    global  myfile
    if request.user.is_authenticated() and request.user.is_superuser:
        is_error = 0
        try:
            categorie = Categorie.objects.filter(idCategorie=idCategorie)[0]
        except:
            is_error = 1
        if is_error == 0:
            categorie.estDesactiver=1
            categorie.save()
            log = Log()
            log.utilisateur = request.user.username
            log.action = u"désactivation catégorie pour entité " + categorie.entite.nomEntite
            log.save()
            messages.success(request, u'Catégorie désactivée avec succès')
            return redirect(listeCategorie, categorie.entite.idEntit)
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())


@login_required
def activerCategorie(request,idCategorie):
    global  myfile
    if request.user.is_authenticated() and request.user.is_superuser:
        is_error = 0
        try:
            categorie = Categorie.objects.filter(idCategorie=idCategorie)[0]
        except:
            is_error = 1
        if is_error == 0:
            categorie.estDesactiver=0
            categorie.save()
            log = Log()
            log.utilisateur = request.user.username
            log.action = u"activation catégorie pour entité " + categorie.entite.nomEntite
            log.save()
            messages.success(request, u'Catégorie activée avec succès')
            return redirect(listeCategorie, categorie.entite.idEntit)
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())