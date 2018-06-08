import cgi
from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from Entite.models import Entite
from abonne.models import Abonne
from client.models import Client
from commande.models import Commande
from livreur.models import Livreur
from parametre.models import Parametre
from terminal.models import Terminal
from utilisateur.models import Utilisateur
from visite.models import Visite

def homeAdmin(request):
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_superuser:
                today=datetime.now()
                minDate=str(today.year)+"-"+str(today.month)+"-"+str(today.day)+" 00:00:00"
                maxDate=str(today.year)+"-"+str(today.month)+"-"+str(today.day)+" 23:59:59"
                nbrNewUsers=Client.objects.filter(personne__dateCreation__lte=maxDate,personne__dateCreation__gte=minDate).count()
                nbrNewCommande=Commande.objects.filter(dateCreation__lte=maxDate,dateCreation__gte=minDate).count()
                nbrCommande=Commande.objects.all().count()
                nbrUsers=Client.objects.all().count()
                nbrTerminal=Terminal.objects.all().count()
                nbrNewTerminal=Terminal.objects.filter(dateCreation__gte=minDate,dateCreation__lte=maxDate).count()
                nbrLivreurs=Livreur.objects.all().count()
                nbrEntite=Entite.objects.all().count()
                nbrAbonne=Abonne.objects.all().count()
                #nbrVisite=Visite.objects.all().count()
                listeCommande = Commande.objects.filter(dateCreation__lte=maxDate, dateCreation__gte=minDate)
                motantTotal=0
                for cmd in listeCommande:
                    motantTotal+=cmd.get_montant()
                nbrManager=Utilisateur.objects.filter(isManager=1).count()

                return render(request, 'home.html', locals())
    else:
        if request.POST:
            is_error=0
            username =cgi.escape(request.POST["username"], True)
            password = cgi.escape(request.POST["password"], True)
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(homeAdmin)
            else:
                return render(request, 'login_administrator.html')
        else:
            return render(request, 'login_administrator.html', locals())
# Create your views here.

def parametreAdmin(request):
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_superuser:
                debut="heure_debut"
                fin = "heure_fin"
                version = "version"
                state = "state"
                try:
                    parametre=Parametre.objects.filter(key=debut)[0]
                    parametre2=Parametre.objects.filter(key=fin)[0]
                    parametre3=Parametre.objects.filter(key=version)[0]
                    parametre4=Parametre.objects.filter(key=state)[0]
                except:
                    parametre=Parametre()
                    parametre.key="heure_debut"
                    parametre.value="00:00"
                    parametre.save()
                    parametre2 = Parametre()
                    parametre2.key = "heure_fin"
                    parametre2.value = "00:00"
                    parametre2.save()
                    parametre3 = Parametre()
                    parametre3.key = version
                    parametre3.value = "1"
                    parametre3.save()
                    parametre4 = Parametre()
                    parametre4.key = state
                    parametre4.value = "0"
                    parametre4.save()
                heure_debut=parametre.value
                heure_fin=parametre2.value
                version_db=parametre3.value
                state=parametre4.value
                return render(request, 'parametreAdmin.html', locals())

@login_required
def mylogoutAdmin(request):
    auth.logout(request)
    return redirect(homeAdmin)

        #return render(request, 'home_manager_admin.html', locals())
def updateHomeAdmin(request):
    today = datetime.now()
    minDate = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + " 00:00:00"
    maxDate = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + " 23:59:59"
    nbrCommande=Commande.objects.filter(dateCreation__lte=maxDate,dateCreation__gte=minDate,state__gt=0).count()
    commandes=Commande.objects.filter(dateCreation__lte=maxDate,dateCreation__gte=minDate,state__gt=0)
    nbrNewUsers = Client.objects.filter(personne__dateCreation__lte=maxDate,personne__dateCreation__gte=minDate).count()
    nbrNewTerminal = Terminal.objects.filter(dateCreation__gte=minDate, dateCreation__lte=maxDate).count()
    montant=0
    for cmd in commandes:
        montant+=cmd.get_montant()
    res='{"commandes":'+str(nbrCommande)+',"montant":'+str(montant)+',"user":'+str(nbrNewUsers)+',"terminal":'+str(nbrNewTerminal)+ '}'
    return HttpResponse(res)
