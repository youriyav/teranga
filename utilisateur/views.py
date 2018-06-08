# coding=utf-8
import re
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.utils import timezone

from log.models import Log
from sen_food.models import Personne
from sen_food.views import logoutview, decodeString
from utilisateur.models import Utilisateur

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
@login_required
def listeUsers(request):
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            utilisateurs=Utilisateur.objects.all()
            return render(request, 'liste_users.html', locals())
@login_required
def createUser(request):
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
                user=User(username=login,email=email,first_name=nom,last_name=prenom,is_staff=1)
                user.set_password(password)
                user.save()
                utilisateur=Utilisateur()
                utilisateur.isManager=1
                utilisateur.droit=1
                utilisateur.user=user
                utilisateur.personne=personne
                utilisateur.save()
                log=Log()
                log.utilisateur=request.user.username
                log.action="Creation utilisateur "+login
                log.save()
                if _next==0:
                    return redirect(listeUsers)
                else:
                    login=""
                    nom=""
                    prenom=""
                    email=""
                    numero=""
                    return render(request, 'create_user.html', locals())

            else:
                return render(request, 'create_user.html', locals())
        else:
            v=1
            return render(request, 'create_user.html', locals())

@login_required
def editUser(request,idUtilisateur):
    if request.user.is_superuser or request.user.utilisateur.idUtilisateur==int(idUtilisateur)  :
        if request.POST:
            global utilisateurp
            nom = request.POST["nom"]
            prenom = request.POST["prenom"]
            email = request.POST["email"]
            numero = request.POST["numero"]
            login = request.POST["login"]
            is_error=0
            mcheck=0
            try:
                utilisateurp = Utilisateur.objects.filter(idUtilisateur=idUtilisateur)[0]
                if utilisateurp.user.username != login:
                    try:
                        mcheck = 1
                        muser = User.objects.filter(username=login)[0]
                    except:
                        muser = User()
                        muser.username = ""
                    if muser.username != "":
                        is_error = 4
                        error_login = u"Login déjà utilisé"
            except:
                is_error = 1
                message="page introuvable"
            if is_error==0:
                personne=Personne.objects.filter(utilisateur=utilisateurp)[0]
                personne.nomPersonne=nom
                personne.prenomPersonne=prenom
                personne.numeroPersonne=numero
                personne.emailPersonne=email
                personne.estModifier=personne.estModifier+1
                personne.dateModification=datetime.now()
                personne.save()
                user=User.objects.filter(utilisateur=utilisateurp)[0]
                user.username=login
                user.save()
                log = Log()
                log.utilisateur = request.user.username
                log.action = "Modification utilisateur " + login
                log.save()
                if request.user.is_superuser:
                    utilisateurp.droit=request.POST["droit"]
                    utilisateurp.save()
                    return  redirect(listeUsers)
                else:
                    return  redirect(profilUser,user.username)
            if is_error==1:
                return render(request, '404.html', locals())
            if is_error==4:
                return render(request, 'edit_user.html', locals())
        else:
            check=0
            try:
                utilisateur = Utilisateur.objects.filter(idUtilisateur=idUtilisateur)[0]
                nom = utilisateur.personne.nomPersonne
                prenom = utilisateur.personne.prenomPersonne
                email = utilisateur.personne.emailPersonne
                numero = utilisateur.personne.numeroPersonne
                login = utilisateur.user.username
                if request.user.is_superuser:
                    droit=utilisateur.droit
                #return render(request, 'edit_user.html', locals())
                check = 1
            except:
                check=0
            if check == 0:
                return render(request, '404.html', locals())
            else:
                return render(request, 'edit_user.html', locals())


@login_required
def editUserPass(request,utilisateur):
    if request.user.is_superuser ==1 or request.user.username==utilisateur:
        if request.POST:
            global password_cur, user
            global is_error
            password_new = request.POST["password_new"]
            password_conf = request.POST["password_conf"]
            is_error=0
            if password_new!=password_conf:
                error_password_new="Les deux mot de passe ne sont pas identiques"
                return render(request, 'edit_user_password.html', locals())
            else:
                try:
                    user = User.objects.filter(username=utilisateur)[0]
                except:
                    is_error = 1
                if is_error==0:
                    if request.user.is_superuser == 1:
                        try:
                            #utilisateur=Utilisateur.objects.filter(idUtilisateur=idUtilisateur)[0]
                            user=User.objects.filter(username=utilisateur)[0]
                            user.set_password(password_new)
                            user.save()
                        except:
                            is_error=1
                        if is_error == 0:
                            log = Log()
                            log.utilisateur = request.user.username
                            log.action = "Modification mot de passe utilisateur " + user.username
                            log.save()
                            return  redirect(listeUsers)
                    else:
                        password_cur = request.POST["password_cur"]
                        if user.check_password(password_cur):
                            user.set_password(password_new)
                            user.save()
                            log = Log()
                            log.utilisateur = request.user.username
                            log.action = "Modification mot de passe utilisateur " + user.username
                            log.save()
                            return  redirect(logoutview)
                        else:
                            errer_password="Mot de passe incorrect"
                            return render(request, 'edit_user_password.html', locals())


        else:
            return render(request, 'edit_user_password.html', locals())

@login_required
def desableUser(request,idUtilisateur):
    if request.user.is_superuser:
        is_error=0
        try:
            utilisateur = Utilisateur.objects.filter(idUtilisateur=idUtilisateur)[0]
            user = User.objects.filter(utilisateur=utilisateur)[0]
            user.is_active = 0
            user.save()
            log = Log()
            log.utilisateur = request.user.username
            log.action = "Desactivation  utilisateur " + user.username
            log.save()
        except:
            is_error = 1
        if is_error == 0:
            return redirect(listeUsers)
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())
        #if request.GET:

@login_required
def enableUser(request,idUtilisateur):
    if request.user.is_superuser:
        is_error=0
        try:
            utilisateur = Utilisateur.objects.filter(idUtilisateur=idUtilisateur)[0]
            user = User.objects.filter(utilisateur=utilisateur)[0]
            user.is_active = 1
            user.save()
            log = Log()
            log.utilisateur = request.user.username
            log.action = "Activation  utilisateur " + user.username
            log.save()
        except:
            is_error = 1
        if is_error == 0:
            return redirect(listeUsers)
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())
        #if request.GET:


@login_required
def deleteUser(request,idUtilisateur):
    if request.user.is_superuser:
        is_error=0
        try:
            utilisateur = Utilisateur.objects.filter(idUtilisateur=idUtilisateur)[0]
            personne=Personne.objects.filter(utilisateur=utilisateur)[0]
            personne.estSupprimer=1
            personne.save()
            log = Log()
            log.utilisateur = request.user.username
            log.action = "Suppression  utilisateur " + utilisateur.user.username
            log.save()
        except:
            is_error = 1
        if is_error == 0:
            return redirect(listeUsers)
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())
        #if request.GET:



@login_required
def deleteUserPost(request):
    global personne
    if request.user.is_superuser:
        is_error=0
        try:
            idUtilisateur = request.POST["idUtilisateur"]
            utilisateur = Utilisateur.objects.filter(idUtilisateur=idUtilisateur)[0]
            personne=Personne.objects.filter(utilisateur=utilisateur)[0]
            personne.estSupprimer=1
            personne.save()
            log = Log()
            log.utilisateur = request.user.username
            log.action = "Suppression  utilisateur " + utilisateur.user.username
            log.save()
        except:
            is_error = 1
        if is_error == 0:
            #return redirect(listeUsers)
            message = u"Utilisateur "+decodeString(personne.nomPersonne)+" "+decodeString(personne.prenomPersonne)+u" supprimé avec succès"
        else:
            message = "error"
        return HttpResponse(message)
        #return render(request, '404.html', locals())
        #if request.GET:





@login_required
def profilUser(request,utilisateur):
    if request.user.username==utilisateur or request.user.is_superuser:
        is_error = 0
        try:
            user = User.objects.filter(username=utilisateur)[0]
        except:
            is_error = 1
        if is_error == 0:
            return render(request, 'profil.html', locals())
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())
            #if request.GET:
    else:
        return render(request, '404.html', locals())


@login_required
def paremetreUser(request,utilisateur):
    if request.user.username==utilisateur or request.user.is_superuser:
        is_error = 0
        try:
            user = User.objects.filter(username=utilisateur)[0]
        except:
            is_error = 1
        if is_error == 0:
            return render(request, 'parametre.html', locals())
        else:
            message = "page introuvable"
            return render(request, '404.html', locals())
            #if request.GET:
    else:
        return render(request, '404.html', locals())





