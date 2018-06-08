import cgi
from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from commande.models import Commande
from utilisateur.models import Utilisateur


def homeManagerAdmin(request):
    if request.user.is_authenticated():
        user=request.user
        utilisateur = Utilisateur.objects.filter(user=user)[0]
        today = datetime.now()
        minDate = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + " 00:00:00"
        maxDate = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + " 23:59:59"
        nbrCommande=Commande.objects.filter(dateCreation__lte=maxDate,dateCreation__gte=minDate,entite=utilisateur.entite,state__gt=0).count()
        commandes=Commande.objects.filter(dateCreation__lte=maxDate,dateCreation__gte=minDate,entite=utilisateur.entite,state__gt=0)
        montant=0
        for cmd in commandes:
            montant+=cmd.get_montant()
        return render(request, 'home_manager_admin.html', locals())
    else:
        if request.POST:
            is_error=0
            username =cgi.escape(request.POST["username"], True)
            password = cgi.escape(request.POST["password"], True)
            user = auth.authenticate(username=username, password=password)
            if user:
                try:
                    utilisateur=Utilisateur.objects.filter(user=user)[0]
                    if utilisateur.droit == 2:
                        auth.login(request, user)
                        return redirect(homeManagerAdmin)
                    else:
                        return render(request, 'login_manager_admin.html')
                except:
                    username_error="login ou mot de passe incorrect"
                    return render(request, 'login_manager_admin.html', locals())
            else:
                v=1
                username_error = "login ou mot de passe incorrect"
                return render(request, 'login_manager_admin.html', locals())
        else:
            return render(request, 'login_manager_admin.html', locals())

def logoutAdminManager(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return redirect(homeManagerAdmin)
        #return render(request, 'home_manager_admin.html', locals())

@login_required
def parametreAdminManager(request):
    if request.POST:
        old_password=request.POST["old_password"]
        newPassword=request.POST["new_password"]
        newPasswordConf=request.POST["new_password_conf"]
        is_error = 0
        if old_password=="":
            error_old="veuillez remplir ce champs"
            is_error=1
        if newPassword=="":
            error_new="veuillez remplir ce champs"
            is_error=1
        if newPasswordConf=="":
            error_new_conf="veuillez remplir ce champs"
            is_error=1
        if is_error==0:
            if newPassword != newPasswordConf:
                error_new_conf = "les deux mot de passe ne sont pas identique"
                is_error = 1
        if is_error==0:
            user=request.user
            if user.check_password(old_password):
                user.set_password(newPassword)
                user.save()
                auth.logout(request)
                return redirect(homeManagerAdmin)
                #return redirect(logoutAdminManager)
            else:
                error_old="mot de passe incorrect"
                return render(request, 'parametre_manager_admin.html', locals())
        else:
            return render(request, 'parametre_manager_admin.html', locals())
    else:
        return render(request, 'parametre_manager_admin.html', locals())
        #return render(request, 'home_manager_admin.html', locals())
def updateHomeManagerAdmin(request):
    user=request.user
    utilisateur = Utilisateur.objects.filter(user=user)[0]
    today = datetime.now()
    minDate = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + " 00:00:00"
    maxDate = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + " 23:59:59"
    nbrCommande=Commande.objects.filter(dateCreation__lte=maxDate,dateCreation__gte=minDate,entite=utilisateur.entite,state__gt=0).count()
    commandes=Commande.objects.filter(dateCreation__lte=maxDate,dateCreation__gte=minDate,entite=utilisateur.entite,state__gt=0)
    montant=0
    for cmd in commandes:
        montant+=cmd.get_montant()
    res='{"commandes":'+str(nbrCommande)+',"montant":'+str(montant)+'}'
    return HttpResponse(res)