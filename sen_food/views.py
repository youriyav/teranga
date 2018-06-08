import base64
import os
from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template.defaulttags import register

from Entite.models import Entite
from administration.views import homeAdmin
from client.models import Client
from commande.models import Commande
from ligne_commande.models import LigneCommande
from localite.models import Localite
from manager.views import homeUtilisateur
from parametre.models import Parametre
from visite.models import Visite
from Entite.models import Entite
from tarif.models import Tarif

def myhome(request):
    listeEntite = Entite.objects.filter(estSupprimer=0, estDesactiver=0,isPartern=1)
    entite_folder = "C:/Users/root/PycharmProjects/senfood/static/images/"
    #with open(os.path.join(entite_folder, "logo_sen_food.png"), "rb") as image_file:
       # encoded_string = base64.b64encode(image_file.read())
    #sessions=request.session
    try:
        listelocalite = Localite.objects.filter(estSupprimer=0)
        user_connecter = request.user
        mclient = Client.objects.filter(user=user_connecter)[0]
        nbrCommande = Commande.objects.filter(client=mclient, state__lt=3).count()
    except:
        nbrCommande=0
    jour=7
    dateLanc=datetime.strptime("2017-07-30 00:00:00", "%Y-%m-%d %H:%M:%S").date()
    date_save = datetime.strftime(dateLanc, '%Y-%m-%d %H:%M:%S')
    currentDate = datetime.now()
    diff = datetime.strptime(date_save, '%Y-%m-%d %H:%M:%S')-currentDate
    total=diff.total_seconds()
    res = diff.seconds/60
    res1 = diff.days
    jour=(total%86400)/86400
    reste=total/86400
    heure=0
    minute=0
    seconde=0
    reste=0
    visite=Visite()
    visite.browser=request.META['HTTP_USER_AGENT']
    #visite.device=request.META['REMOTE_HOST']
    visite.save()
    #return  render(request,"index_building.html",locals())
    today = datetime.now()
    heure=today.hour
        
    #return  render(request,"index_building.html",locals())
    return  render(request,"homeClient.html",locals())
@login_required
def logoutview(request):
    res=logout(request,'registration/login.html')
    res.delete_cookie('sessionid')
    #return render(request, 'registration/logout.html')

def decodeString(string):
    return unicode(string,'utf-8')
    #return render(request, 'registration/logout.html')

    #return render(request, 'registration/logout.html')

@login_required
def mesCommandes(request):
    user_connecter = request.user
    try:
        listelocalite = Localite.objects.filter(estSupprimer=0)
        client = Client.objects.filter(user=user_connecter)[0]
        listeCommande=Commande.objects.filter(client=client,estLivrer=0,state__lt=6)
        listeLigneCommande=LigneCommande.objects.filter(commande=listeCommande.last())
        #listeLigneCommande=LigneCommande.objects.filter(commande__client=mclient,commande__state__lt=6)
        nbrCommande=listeCommande.count()
        v=0
    except:
        nbrCommande=0
    return render(request,'mesCommandes.html',locals())
@login_required
def mylogout(request):
    auth.logout(request)
    return redirect(myhome)
def notFoudRequest(request):
    dateLanc=datetime.strptime("2017-07-01 00:00:00", "%Y-%m-%d %H:%M:%S").date()
    date_save = datetime.strftime(dateLanc, '%Y-%m-%d %H:%M:%S')
    currentDate = datetime.now()
    diff = datetime.strptime(date_save, '%Y-%m-%d %H:%M:%S')-currentDate
    total=diff.total_seconds()
    res = diff.seconds/60
    res1 = diff.days
    jour=(total%86400)/86400
    reste=total/86400
    heure=0
    minute=0
    seconde=0
    reste=0
    visite=Visite()
    visite.browser=request.META['HTTP_USER_AGENT']
    #visite.device=request.META['REMOTE_HOST']
    visite.save()
    return render(request, 'index_building.html', locals())

def userCondition(request):
    return  render(request,"confidence.html",locals())
def notFound(request):
    return  render(request,"404.html",locals())
def getEntityCoordonne(request):
    idEntite = request.POST["idEntite"]
    entite=Entite.objects.filter(idEntit=idEntite)[0]
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
    data='{"latitude":"'+entite.latitude+'","longitude":"'+entite.longitude+'","listeTarif":'+tarifTab+'}'
    return  HttpResponse(data)