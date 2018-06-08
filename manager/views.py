# coding=utf-8
import cgi

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models.functions import Coalesce
from django.db.models.functions import Lower
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.context_processors import request
from pyfcm import FCMNotification

from commande.models import Commande
from livraison.models import Livraison
from livreur.models import Livreur
from notification.models import Notification
from terminal.models import Terminal
from utilisateur.models import Utilisateur
from datetime import datetime, timedelta

def homeUtilisateur(request):
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_staff:
                manager=user_connecter.utilisateur
                listeCommande = Commande.objects.filter(manager=manager,estLivrer=0).order_by('idCommande')
                return render(request, 'listeCommande.html', locals())
    else:
        if request.POST:
            is_error=0
            username =cgi.escape(request.POST["username"], True)
            password = cgi.escape(request.POST["password"], True)
            user = auth.authenticate(username=username, password=password)
            if user and user.is_staff:
                utilisateur=Utilisateur.objects.filter(user=user)[0]
                if utilisateur.droit == 1:
                    auth.login(request, user)
                    return redirect(homeUtilisateur)
                else:
                    return render(request, 'login_manager.html')
            else:
                return render(request, 'login_manager.html')
        else:
            return render(request, 'login_manager.html', locals())
@login_required
def listeCommande(request):
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_staff:
                listeCommande=Commande.objects.all().order_by('idCommande')
                return render(request, 'listeCommande.html', locals())

@login_required
def updatelisteCommande(request):
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_staff:
                listeCommandeValide=Commande.objects.filter(manager=request.user.utilisateur,estLivrer=0).order_by('idCommande')
                listeCommandeNews=Commande.objects.filter(isSynch=0,estLivrer=0)[:5]
                #commandes validées par le manager
                data = '['
                mstop = 0
                for cmd in listeCommandeValide:
                    mstop = mstop + 1
                    tmp = '{'
                    tmp = tmp + '"numero":"' + cmd.numero + '",'
                    if cmd.state!=0:
                        tmp = tmp + '"livreur":"' + cmd.livreur.personne.nomPersonne + " " + cmd.livreur.personne.prenomPersonne + '",'
                    else:
                        tmp = tmp + '"livreur":"",'
                    tmp = tmp + '"entite":"' + cmd.entite.nomEntite + '",'
                    tmp = tmp + '"state":"' + str(cmd.state) + '",'
                    tmp = tmp + '"duree":"' + str(cmd.get_duree()) + '",'
                    tmp = tmp + '"id":"' + str(cmd.idCommande) + '"'
                    tmp = tmp + '}'
                    data = data + tmp
                    if mstop != listeCommandeValide.count():
                        data = data + ","
                data = data+']'
                #5 nouvelles commandes de plus
                data1 = '['
                mstop = 0
                for cmd in listeCommandeNews:
                    cmd.isSynch=1
                    cmd.manager=request.user.utilisateur
                    cmd.save()
                    mstop = mstop + 1
                    tmp = '{'
                    tmp = tmp + '"numero":"' + cmd.numero + '",'
                    if cmd.state!=0:
                        tmp = tmp + '"livreur":"' + cmd.livreur.personne.nomPersonne + " " + cmd.livreur.personne.prenomPersonne + '",'
                    else:
                        tmp = tmp + '"livreur":"",'
                    tmp = tmp + '"entite":"' + cmd.entite.nomEntite + '",'
                    tmp = tmp + '"state":"' + str(cmd.state) + '",'
                    tmp = tmp + '"duree":"' + str(cmd.get_duree()) + '",'
                    tmp = tmp + '"id":"' + str(cmd.idCommande) + '"'
                    tmp = tmp + '}'
                    data1 = data1 + tmp
                    if mstop != listeCommandeNews.count():
                        data1 = data1 + ","
                data1 = data1 + ']'
                return HttpResponse(data+"||"+data1)
@login_required
def listeLivreurManager(request):
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_staff:
                listeLivreur=Livreur.objects.all()
                return render(request, 'listeLivreurManager.html', locals())

@login_required
def detailCommande(request,idCommande):
    if request.user.is_authenticated():
        if request.user.is_active:
            if request.user.is_staff:
                is_error=0
                try:
                    commande=Commande.objects.filter(idCommande=idCommande)[0]
                    now = datetime.now()
                    now_minus_5 = now - timedelta(minutes=5)
                    listeLivreur = Livreur.objects.filter(personne__terminal__lastUpdate__gte=now_minus_5)
                    #listeLivreur = Livreur.objects.filter()
                    lignecommandes=commande.lignecommande_set.all()
                except:
                    is_error=1
                if is_error==0:
                    return render(request, 'detail_commande.html', locals())
                else:
                    message="page introuvable"
                    return render(request, '404.html', locals())


@login_required
def affecterCommande(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            if request.user.is_staff:
                if request.POST:
                    is_error= 0
                    listeLivreur = Livreur.objects.all()
                    idCommande = request.POST["idCommande"]
                    idLivreur = request.POST["livreur"]
                    if int(idLivreur)==0:
                        is_error=1
                        error_livreur = u"Veuillez sélectionner un livreur"
                        commande = Commande.objects.filter(idCommande=idCommande)[0]

                        now = datetime.now()
                        now_minus_10 = now - timedelta(minutes=5)

                        listeLivreur = Livreur.objects.filter(personne__terminal__lastUpdate__gte=now_minus_10)
                        messages.error(request, u"Veuillez sélectionner un livreur")
                        return redirect(detailCommande,idCommande)#render(request, 'detail_commande.html', locals())
                    else:
                        commande = Commande.objects.filter(idCommande=idCommande)[0]
                        livreur = Livreur.objects.filter(idLivreur=idLivreur)[0]
                        commande.livreur = livreur
                        commande.state = 1
                        commande.dateValidation=datetime.now()
                        commande.manager = request.user.utilisateur
                        commande.save()
                        notification = Notification()
                        notification.titre = "info"
                        notification.client = commande.client
                        notification.content = "votre commande <br>vient être validée"
                        notification.url = "http://192.168.1.17:8000/mes-commandes"
                        notification.save()
                        lignecommandes = commande.lignecommande_set.all()
                        data='['
                        mstop=0
                        for ligne in lignecommandes:
                            mstop = mstop + 1
                            tmp='{'
                            tmp+='"idProduit":"'+str(ligne.produit.idProduit)+'",'
                            tmp+='"produit":"'+ligne.produit.nomProduit+'",'
                            tmp+='"prix":"'+str(ligne.produit.prixProduit)+'",'
                            tmp+='"quantite":"'+str(ligne.quantite)+'"'
                            tmp+='}'
                            data+=tmp
                            if mstop != lignecommandes.count():
                                data = data + ","
                        data+=']'
                        data_message = {
                            "idCommande": str(commande.idCommande),
                            "longitude": str(commande.longitude),
                            "latitude": str(commande.latitude),
                            "montant": str(commande.get_montant()),
                            "entite": commande.entite.nomEntite,
                            "numero": commande.numero,
                            "heure": str(commande.dateCreation),
                            "client": commande.client.personne.nomPersonne+" "+commande.client.personne.prenomPersonne,
                            "numero_client": str(commande.client.personne.numeroPersonne),
                            "produits": '{"liste":'+data+'}'
                        }
                        #terminal=livreur.personne.terminal_set[0]
                        token=livreur.personne.terminal.token
                        
                        push_service = FCMNotification(api_key="AAAA9bOoHa8:APA91bHrbWMoCSvFYHD9_ORd8P4lv-D0RaPf3cWaP_yRBJ_JeyCF3tSVRJfrr0bzLSzPAkmaU2zodtF7OjysaOnkckRalzUFvox_ZumkcdLtoOG414BNhIJyuibxXtXHzIXR_-EyU3Aj")
                        result = push_service.notify_single_device(registration_id=token,data_message=data_message, time_to_live=300000)

                        return redirect(homeUtilisateur)


@login_required
def suivreCommande(request,idCommande):
    if request.user.is_authenticated():
        if request.user.is_active:
            if request.user.is_staff:
                is_error = 0
                try:
                    commande = Commande.objects.filter(idCommande=idCommande)[0]
                except:
                    is_error = 1
                if is_error == 0:
                    return render(request, 'suivre_commande_manager.html', locals())
                else:
                    message = "page introuvable"
                    return render(request, '404.html', locals())

#def sendCommande(dataMessage,receiver_key):

    #my_id="c_DcQPrZuFc:APA91bGWg-mSUwWZtNtJZxdmyMQaHFjx20hRzHA2oCauLDTRzrd9oYCBr0QXhikP-eROr9QYchiiVfM1RAFWLNp-mvuz9lrj6-FJ2VVtv5YiMIL-qaUfCeA02qNzVp0crKKeeKZutKML"
   # push_service = FCMNotification(api_key=firebase_kew)
    #result = push_service.notify_single_device(registration_id=receiver_key, data_message=dataMessage,time_to_live=300000)
@login_required
def logoutManager(request):
    auth.logout(request)
    return redirect(homeUtilisateur)