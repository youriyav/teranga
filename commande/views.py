# coding=utf-8
import json
from asyncore import loop
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models.functions import Lower
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Entite.models import Entite
from client.models import Client
from commande.models import Commande
from ligne_commande.models import LigneCommande
from livreur.models import Livreur
from localite.models import Localite
from notification.models import Notification
from parametre.models import Parametre
from produit.models import Produit
from sen_food.views import decodeString
from terminal.models import Terminal
from log.models import Log
@login_required
def ListCommandeSuper(request):
    today = datetime.now()
    minDate = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + " 00:00:00"
    maxDate = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + " 23:59:59"
    #listeCommande=Commande.objects.filter(dateCreation__lte=maxDate,dateCreation__gte=minDate)
    listeCommande=Commande.objects.all()
    listeRestaurant=Entite.objects.filter(estSupprimer=0)
    listeLivreur=Livreur.objects.filter(estSupprimer=0)
    if request.POST:
        entite=request.POST["entite"]
        livreur=request.POST["livreur"]

    else:
        listeCommande = Commande.objects.all()
    return render(request, 'listeCommandeSuper.html', locals())
@login_required
def newCommande(request):
    data = request.POST["data"]
    user = request.POST["client"]
    midEntite = request.POST["idEntite"]
    #idLocalite = request.POST["idLocalite"]
    password = request.POST["password"]
    is_error = 0
    try:
        user=User.objects.filter(username=user)[0]
        #localite=Localite.objects.filter(idLocalite=idLocalite)[0]
    except:
        is_error=1
    if is_error ==0:
        if user.check_password(password):
            data_json = json.loads(data)
            longitude= data_json["longitude"]#-17.493278#
            latitude=data_json["latitude"]#14.725083#
            priLivraison = request.POST["prixLivraison"]
            listeProduit=data_json["produits"]
            montantCommande=0

            parametreState = Parametre.objects.filter(key="state")[0]
            parametreDebut = Parametre.objects.filter(key="heure_debut")[0]
            parametreFin = Parametre.objects.filter(key="heure_fin")[0]
            if parametreState.value=="1":
                today = datetime.now()
                heure = today.hour
                commande = Commande()
                commande.prixLivraison=priLivraison
                if heure>=int(parametreDebut.value) and heure<=int(parametreFin.value):

                    try:
                        commande = Commande.objects.filter(client__user=user, estLivrer=0,state__lt=6)[0]
                        log = Log()
                        log.utilisateur = user.username
                        log.action = "commande impossible:got runing order"
                        log.save()
                        return HttpResponse(
                            "vous avez une commande en cours. Veuillez patienter le temps que celle-ci soit livrée avant de continuer",
                            status=409)
                    except:
                        entite = Entite.objects.filter(idEntit=midEntite)[0]
                        if entite.isPartern==1:
                            for produit in listeProduit:
                                mproduit = Produit.objects.filter(idProduit=produit["idProduit"])[0]
                                ligne = LigneCommande()
                                montantCommande += int(mproduit.prixProduit) * int(produit["quantite"])
                            if montantCommande > 10000:
                                try:
                                    listeCommande = Commande.objects.filter(client__user=user)
                                    if listeCommande.count() >= 2:
                                        client = Client.objects.filter(user=user)[0]
                                        if client.estBloquer == 0:
                                            
                                            entite = Entite.objects.filter(idEntit=midEntite)[0]
                                            commande.entite = entite
                                            commande.longitude = longitude
                                            commande.latitude = latitude
                                            client = Client.objects.filter(user=user)[0]
                                            commande.client = client
                                            #commande.localite = localite
                                            commande.save()
                                            tmp = ""
                                            for produit in listeProduit:
                                                # tmp=tmp+"|"+produit["idProduit"]+"_"+produit["quantite"]
                                                mproduit = Produit.objects.filter(idProduit=produit["idProduit"])[0]
                                                ligne = LigneCommande()
                                                ligne.commande = commande
                                                ligne.produit = mproduit
                                                ligne.quantite = produit["quantite"]
                                                ligne.save()
                                            tmp = str(client.idclient)
                                            numero = "sen-f00" + tmp + str(commande.idCommande)
                                            commande.numero = numero
                                            commande.save()
                                            return HttpResponse(numero + "#" + str(commande.idCommande))
                                        else:
                                            log = Log()
                                            log.utilisateur = user.username
                                            log.action = "commande impossible:compte bloquer"
                                            log.save()
                                            return HttpResponse(
                                                "désole,votre compte n'est pas autorisé à commander. \nveuillez contacter le service client pour tout détail",
                                                status=405)
                                    else:
                                        log = Log()
                                        log.utilisateur = user.username
                                        log.action = "commande impossible:bad authorization"
                                        log.save()
                                        return HttpResponse(
                                            "désole, vous n'êtes pas encore autorisé à commander pour plus de 10000 Fcfa ",
                                            status=402)
                                except:
                                    log = Log()
                                    log.utilisateur = user.username
                                    log.action = "commande impossible:bad authorization"
                                    log.save()
                                    return HttpResponse(
                                        "désole, vous n'êtes pas encore autorisé à commander pour plus de 10000 Fcfa ",
                                        status=406)
                            else:
                                client = Client.objects.filter(user=user)[0]
                                if client.estBloquer == 0:
                                    entite = Entite.objects.filter(idEntit=midEntite)[0]
                                    commande.entite = entite
                                    commande.longitude = longitude
                                    commande.latitude = latitude
                                    client = Client.objects.filter(user=user)[0]
                                    commande.client = client
                                    #commande.localite = localite
                                    commande.save()
                                    tmp = ""
                                    for produit in listeProduit:
                                        # tmp=tmp+"|"+produit["idProduit"]+"_"+produit["quantite"]
                                        mproduit = Produit.objects.filter(idProduit=produit["idProduit"])[0]
                                        ligne = LigneCommande()
                                        ligne.commande = commande
                                        ligne.produit = mproduit
                                        ligne.quantite = produit["quantite"]
                                        ligne.save()
                                    tmp = str(client.idclient)
                                    numero = "sen-f00" + tmp + str(commande.idCommande)
                                    commande.numero = numero
                                    commande.save()
                                    return HttpResponse(numero + "#" + str(commande.idCommande))
                                else:
                                    log = Log()
                                    log.utilisateur = user.username
                                    log.action = "commande impossible:compte bloquer"
                                    log.save()
                                    return HttpResponse(
                                        "désole,votre compte n'est pas autorisé à commander. \nveuillez contacter le service client pour tout détail",
                                        status=405)
                        else:
                            client = Client.objects.filter(user=user)[0]
                            if client.estBloquer == 0:
                                commande.entite=entite
                                commande.longitude=longitude
                                commande.latitude=latitude
                                commande.client=client
                                commande.save()
                                #commande.localite=localite
                                tmp=""
                                for produit in listeProduit:
                                    tmp+=produit["produit"]+":"+produit["quantite"]
                                    pr=Produit()
                                    pr.nomProduit=produit["produit"]
                                    pr.isTmp=1
                                    pr.save()
                                    myprod=Produit.objects.filter(idProduit=pr.idProduit)[0]                            
                                    ligne=LigneCommande()
                                    ligne.commande=commande
                                    ligne.produit=pr
                                    ligne.quantite=produit["quantite"]
                                    ligne.save()
                                tmp=str(client.idclient)
                                numero="sen-f00"+tmp+str(commande.idCommande)
                                commande.numero=numero
                                commande.save()
                                data = '{'
                                data += '"id":"' + str(commande.idCommande)+'",'
                                data += '"numero":"' + str(commande.numero)+'"'
                                data += '}'
                                return HttpResponse(data)
                else:
                    tmp_debut=""
                    tmp_fin=""
                    if(int(parametreDebut.value)<=9):
                        tmp_debut="0"+str(parametreDebut.value)+"h:00 min"
                    else:
                        tmp_debut=str(parametreDebut.value) + "h:00 min"
                    if (int(parametreFin.value) <= 9):
                        tmp_fin = "0" + str(parametreFin.value) + "h:00 min"
                    else:
                        tmp_fin = str(parametreFin.value) + "h:00 min"
                        log = Log()
                        log.utilisateur = user.username
                        log.action = "commande impossible:bad hour"
                        log.save()
                    return HttpResponse("Désolé, Nos services sont disponibe de "+tmp_debut+" à "+tmp_fin+".Veuillez réessayer ultérieument.",status=408)
            else:
                log = Log()
                log.utilisateur = user.username
                log.action = "commande impossible"
                log.save()
                return HttpResponse("Désolé, nos services sont momentanément indisponibles.\nVeuillez réessayer plus tard", status=417)
        else:
            log = Log()
            log.utilisateur = user.username
            log.action = "commande bad authentification "
            log.save()
            return HttpResponse("mot de passe incorrect", status=403)
            #password is not correct
    else:
        #user doesn't exist
        #return Response(content, status=status.HTTP_404_NOT_FOUND)
        return HttpResponse("cet utilisateur n'exite pas",status=401)

@login_required
def relancerCommande(request):
    global commande
    idCommande = request.POST["idCommande"]
    user_request=request.user
    is_error=0
    try:
        commande=Commande.objects.filter(idCommande=idCommande)[0]
    except:
        is_error=1
    if is_error==0:
        if commande.client.user== user_request:
            if commande.state==0:
                commande.relancer = commande.relancer+1
                commande.lastRelance=datetime.now()
                commande.save()
            return HttpResponse(u"commande relancé avec succèsp "+str(commande.relancer))
        else:
            return HttpResponse("action interdite", status=401)
    else:
        return HttpResponse("cet commande n'exite pas", status=403)

@login_required
def suivreLivraison(request,idCommande):
    user_request=request.user
    is_error=0
    try:
        commande=Commande.objects.filter(idCommande=idCommande)[0]
    except:
        is_error=1
    if is_error==0:
        if commande.client.user== user_request:
            if commande.enCoursDepreparion == 0 and commande.estEstEnCoursDeLivraison == 0:
                commande.estValider = 0
                commande.save()
            return render(request, "livraison.html", locals())
        else:
            message = "page introuvable"
            return render(request, "404.html", locals())
    else:
        message="page introuvable"
        return render(request,"404.html",locals())


@login_required
def updateListCommande(request):
    user_request=request.user
    is_error=0
    try:
        client=Client.objects.filter(user=user_request)[0]
        listeCommande=Commande.objects.filter(client=client,estLivrer=0,state__lt=6)
        listeLigneCommande=LigneCommande.objects.filter(commande=listeCommande.last())
    except:
        is_error=1
    if is_error==0:
        #json.dumps(list(listeCommande))
        #data = serializers.serialize('json', list(listeCommande), fields=('numero',''))
        data='['
        mstop=0
        for  cmd in listeCommande:
            mstop=mstop+1
            mstate=""
            my_state=0
            tmp='{'
            tmp=tmp+'"numero":"'+cmd.numero+'",'
            if cmd.entite.isPartern==1:
                tmp=tmp+'"montant":"'+str(cmd.get_montant())+'",'
            else:
                tmp=tmp+'"montant":"???",'
            tmp=tmp+'"duree":"'+str(cmd.get_duree())+'",'
            tmp=tmp+'"entite":"'+cmd.entite.nomEntite+'",'
            tmp=tmp+'"last":"'+str(cmd.get_duree_relance())+'",'
            tmp=tmp+'"idCommande":"'+str(cmd.idCommande)+'",'
            tmp=tmp+'"estRelancer":"'+str(cmd.relancer)+'",'
            if cmd.state==0:
                mstate="En cours de validation"
            if cmd.state == 1:
                my_state=1
                mstate = u"Validée"
            if cmd.state == 2:
                my_state=2
                mstate = u"En cours de préparation"
            if cmd.state == 3:
                my_state=3
                mstate = "En cours de livraison"
            tmp=tmp+'"state":"'+mstate+'",'
            tmp=tmp+'"my_state":"'+str(my_state)+'",'
            tmp += '"listeLigne":['
            tmpNbr=0
            for ligne in listeLigneCommande:
                tmpNbr=tmpNbr+1
                tmp+='{'
                tmp+='"libelle":"'+ligne.produit.nomProduit+'",'
                if cmd.entite.isPartern==1:
                    tmp+='"prix":"'+str(ligne.produit.prixProduit)+'",'
                else:
                    tmp+='"prix":"???",'
                tmp+='"quantite":"'+str(ligne.quantite)+'"'
                tmp+='}'
                if tmpNbr!=listeLigneCommande.count():
                    tmp+=','
            tmp += ']'
            tmp = tmp+'}'
            data=data+tmp
            if mstop!=listeCommande.count():
                data=data+","
        data = data+']'
        return HttpResponse(data)
    else:
        return HttpResponse("no")

def localiserCommande(request,idCommande):
    user_request=request.user
    is_error=0
    try:
        commande=Commande.objects.filter(idCommande=idCommande)[0]
    except:
        is_error=1
    if is_error==0:
        if commande.client.user== user_request:
            if commande.state==3:
                personne=commande.livreur.personne
                terminal=Terminal.objects.filter(utilisateur=personne)[0]
                return render(request, "localiser_commande_client.html", locals())
            else:
                message = "page introuvable"
                return render(request, "404.html", locals())
        else:
            message = "page introuvable"
            return render(request, "404.html", locals())
    else:
        return HttpResponse("cet commande n'exite pas", status=403)
@csrf_exempt
def changeState(request):
    idCommande=request.POST["idCommande"]
    token=request.POST["token"]
    state=request.POST["state"]
    user_request=request.user
    is_error=0
    try:
        commande=Commande.objects.filter(idCommande=idCommande)[0]
        terminal = Terminal.objects.filter(token=token)[0]
        try:
            terminalClient = Terminal.objects.filter(utilisateur=commande.client.personne)[0]
        except:
            v=1
        if int(state) == 2 or int(state)==3:
            commande.state = state
            notification = Notification()
            notification.titre = "info"
            notification.client = commande.client
            if int(state)==2:
                notification.content = "votre commande est en cours préparation"
                commande.datePreparation=datetime.now()
            if int(state)==3:
                notification.content = "votre commande est en cours livraison"
                commande.dateLivraicon = datetime.now()
            notification.url = "https://www.teranga-food.com/mes-commandes"
            notification.save()
        else:
            commande.state = state
            if int(state) == 4:
                commande.estLivrer=1
            if int(state) == 5:
                commande.estLivrer=2
        commande.save()
    except:
        is_error=1
    if is_error==0:
        return HttpResponse("good")
    else:
        return HttpResponse("cet commande n'exite pas", status=403)
@csrf_exempt
def commandeApproximite(request):
    idCommande=request.POST["idCommande"]
    token=request.POST["token"]
    is_error=0
    try:
        commande=Commande.objects.filter(idCommande=idCommande)[0]
        terminal = Terminal.objects.filter(token=token)[0]
        notification = Notification()
        notification.titre = "info"
        notification.Notitype=10
        notification.client = commande.client
        notification.content ="le livreur à proximité de vous"
        notification.url = "https://www.teranga-food.com/mes-commandes"
        notification.save()
    except:
        is_error=1
    if is_error==0:
        return HttpResponse("good")
    else:
        return HttpResponse("cet commande n'exite pas", status=403)



def updateLocation(request):
    user_request=request.user
    idCommande=request.POST["idCommande"]
    is_error=0
    try:
        commande=Commande.objects.filter(idCommande=idCommande)[0]
    except:
        is_error=1
    if is_error==0:
        if commande.client.user== user_request:
            if commande.state==3:
                personne=commande.livreur.personne
                terminal=Terminal.objects.filter(utilisateur=personne)
                data = serializers.serialize('json', list(terminal), fields=('longitude', 'latitude'))
                return HttpResponse(data)
            else:
                message = "page introuvable"
                return render(request, "404.html", locals())
        else:
            message = "page introuvable"
            return render(request, "404.html", locals())
    else:
        return HttpResponse("cet commande n'exite pas", status=403)
