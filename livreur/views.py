# coding=utf-8
import re
from datetime import datetime
from random import randint

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from livreur.models import Livreur
from log.models import Log
from sen_food.models import Personne
from sen_food.views import decodeString
from terminal.models import Terminal


@login_required
def listeLivreur(request):
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_staff:
                listeLivreur=Livreur.objects.filter(estSupprimer=0)
                return render(request, 'liste_livreur.html', locals())

@login_required
def newLivreur(request):
    global var
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_staff:
                if request.POST:
                    is_error = 0
                    nom = request.POST["nom"]
                    prenom = request.POST["prenom"]
                    numero = request.POST["numero"]
                    if nom == "":
                        errer_nom = "veuiller remplir ce champs"
                        is_error = 1
                    if prenom == "":
                        errer_prenom= "veuiller remplir ce champs"
                        is_error = 1
                    if numero == "":
                        errer_numero= "veuiller remplir ce champs"
                        is_error = 1
                    else:
                        if re.search(r"^[0-9]{9}$", numero) is None:
                            is_error = 1
                            errer_numero = "numero incorrect"
                        else:
                            try:
                                livreur=Livreur.objects.filter(personne__numeroPersonne=numero)[0]
                                is_error = 1
                                errer_numero = u"ce numero est déjà enregistré"
                            except:
                                v=1
                    if is_error == 0:
                        personne=Personne()
                        personne.nomPersonne=nom
                        personne.prenomPersonne=prenom
                        personne.numeroPersonne=numero
                        personne.save()
                        livreur=Livreur()
                        livreur.personne=personne
                        listeLivreurs=Livreur.objects.all()
                        check=0
                        exist=0
                        while check==0:
                            var = ""
                            while len(var) < 4:
                                    d = randint(0, 9)
                                    var =var+str(d)
                            #check=0
                            for mlivreur in listeLivreurs:
                                if mlivreur.code==var:
                                    exist=1
                            if exist == 0:
                                check=1
                        livreur.code=var
                        livreur.save()
                        return redirect(listeLivreur)
                    else:
                        return render(request, 'create_livreur.html', locals())
                else:
                    return render(request, 'create_livreur.html', locals())


@login_required
def editerLivreur(request,idLivreur):
    global var, livreur
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_staff:
                is_error = 0
                try:
                    livreur = Livreur.objects.filter(idLivreur=idLivreur)[0]
                except:
                    is_error = 1
                if is_error == 0:
                    if request.POST:
                        is_error = 0
                        nom = request.POST["nom"]
                        prenom = request.POST["prenom"]
                        numero = request.POST["numero"]
                        if nom == "":
                            errer_nom = "veuiller remplir ce champs"
                            is_error = 1
                        if prenom == "":
                            errer_prenom= "veuiller remplir ce champs"
                            is_error = 1
                        if numero == "":
                            errer_numero= "veuiller remplir ce champs"
                            is_error = 1
                        else:
                            if re.search(r"^[0-9]{9}$", numero) is None:
                                is_error = 1
                                errer_numero = "numero incorrect"
                        if is_error == 0:
                            personne=livreur.personne
                            personne.nomPersonne=nom
                            personne.prenomPersonne=prenom
                            personne.numeroPersonne=numero
                            personne.save()
                            livreur.save()
                            listeLivreur = Livreur.objects.all()
                            log = Log()
                            log.utilisateur = request.user.username
                            log.action = "modification livreur " + livreur.personne.nomPersonne +" "+ livreur.personne.prenomPersonne
                            log.save()
                            messages.success(request, 'livreur modifié avec succès')
                            return render(request, 'liste_livreur.html', locals())
                        else:
                            return render(request, 'create_livreur.html', locals())
                    else:
                        nom = livreur.personne.nomPersonne
                        prenom = livreur.personne.prenomPersonne
                        numero = livreur.personne.numeroPersonne
                        return render(request, 'editer_livreur.html', locals())
                else:
                    message = "page introuvable"
                    return render(request, '404.html', locals())

@login_required
def bloquerLivreur(request,idLivreur):
    global var, livreur
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_staff:
                is_error = 0
                try:
                    livreur = Livreur.objects.filter(idLivreur=idLivreur)[0]
                except:
                    is_error = 1
                if is_error == 0:
                    livreur.estActif=0
                    livreur.save()
                    listeLivreur = Livreur.objects.all()
                    log = Log()
                    log.utilisateur = request.user.username
                    log.action = "Desactivation livreur " + livreur.personne.nomPersonne + " " + livreur.personne.prenomPersonne
                    log.save()
                    messages.success(request, 'livreur désactivé avec succès')
                    return render(request, 'liste_livreur.html', locals())
                else:
                    message = "page introuvable"
                    return render(request, '404.html', locals())


@login_required
def activerLivreur(request,idLivreur):
    global var, livreur
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_staff:
                is_error = 0
                try:
                    livreur = Livreur.objects.filter(idLivreur=idLivreur)[0]
                except:
                    is_error = 1
                if is_error == 0:
                    livreur.estActif=1
                    livreur.save()
                    listeLivreur = Livreur.objects.all()
                    log = Log()
                    log.utilisateur = request.user.username
                    log.action = "Activation livreur " + livreur.personne.nomPersonne + " " + livreur.personne.prenomPersonne
                    log.save()
                    messages.success(request, 'livreur activé avec succès')
                    return render(request, 'liste_livreur.html', locals())
                else:
                    message = "page introuvable"
                    return render(request, '404.html', locals())



@login_required
def supprimerLivreur(request,idLivreur):
    global var, livreur
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_staff:
                is_error = 0
                try:
                    livreur = Livreur.objects.filter(idLivreur=idLivreur)[0]
                except:
                    is_error = 1
                if is_error == 0:
                    livreur.estSupprimer=1
                    livreur.save()
                    log = Log()
                    log.utilisateur = request.user.username
                    log.action = "Activation livreur " + livreur.personne.nomPersonne + " " + livreur.personne.prenomPersonne
                    log.save()
                    messages.success(request, 'livreur supprimé avec succès')
                    return redirect(listeLivreur)
                else:
                    message = "page introuvable"
                    return render(request, '404.html', locals())

#action terminaux
@csrf_exempt
def loginLivreur(request):
    global terminal
    numero = request.POST["numero"]
    code = request.POST["code"]
    token = request.POST["token"]
    is_error = 0
    try:
        terminal=Terminal.objects.filter(token=token)[0]
        #livreur = Livreur.objects.filter(personne__numeroPersonne=numero)[0]
    except:
        is_error=1
    if is_error==0:
        try:
            livreur = Livreur.objects.filter(personne__numeroPersonne=numero)[0]
            if livreur.code==code:
                terminal.lastUpdate=datetime.now()
                try:
                    #le livreur est déjà connecté sur un téléphone

                    tmp=livreur.personne.terminal
                    if tmp.token == terminal.token:
                        return HttpResponse("succès")
                    else:
                        return HttpResponse("bad information", status=403)
                except:
                    terminal.utilisateur=livreur.personne
                    terminal.save()
                    return HttpResponse("succès")
            else:
                return HttpResponse("bad information", status=402)
        except:
            return HttpResponse("bad information 2", status=402)
    else:
        return HttpResponse("vous n'etes pas autorisé", status=401)
    #return HttpResponse("{'message':'succès'}")

@csrf_exempt
def registerMobilLivreur(request):
    numero = request.POST["numero"]
    token = request.POST["token"]
    imei = request.POST["imei"]
    try:
        livreur = Livreur.objects.filter(personne__numeroPersonne=numero)[0]
    except:
        is_error=0
    return HttpResponse("{'message':'succès'}")





@csrf_exempt
def logoutLivreur(request):
    global terminal
    token = request.POST["token"]
    is_error = 0
    try:
        terminal=Terminal.objects.filter(token=token)[0]
        #livreur = Livreur.objects.filter(personne__numeroPersonne=numero)[0]
    except:
        is_error=1
    if is_error==0:
        terminal.lastUpdate = datetime.now()
        cursor = connection.cursor()
        cursor.execute("UPDATE terminal set utilisateur=null WHERE idTerminal="+str(terminal.idTerminal))
        return HttpResponse(u"déconnecté")
    else:
        return HttpResponse("vous n'etes pas autorisé", status=401)
    #return HttpResponse("{'message':'succès'}")