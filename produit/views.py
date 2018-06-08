# coding=utf-8
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

# Create your views here.
from Entite.models import Entite
from categorie.models import Categorie
from image.models import Image
from log.models import Log
from produit.models import Produit
from sen_food.views import decodeString
from django.core.files.storage import FileSystemStorage

@login_required
def listeProduit(request,idEntite,idCategorie):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            try:
                entite = Entite.objects.filter(idEntit=idEntite)[0]
            except:
                is_error=1
            if is_error==0:
                if int(idCategorie)==0:
                    listeProduit=Produit.objects.filter(estSupprimer=0,categorie__entite__idEntit=idEntite)
                    paginator = Paginator(listeProduit, 10)
                    page = request.GET.get('page')
                    try:
                        users = paginator.page(page)
                    except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                        users = paginator.page(1)
                    except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                        users = paginator.page(paginator.num_pages)
                    return render(request, 'listeProdui.html', locals())
                else:
                    try:
                        listeProduit = Produit.objects.filter(estSupprimer=0,categorie__idCategorie=int(idCategorie))
                    except:
                        is_error=1
                    if is_error==0:
                        return render(request, 'listeProdui.html', locals())
                    else:
                        message = "page introuvable"
                        return render(request, '404.html', locals())
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())


@login_required
def creerProduit(request,idEntite):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            try:
                entite = Entite.objects.filter(idEntit=idEntite)[0]
            except:
                is_error=1
            if is_error==0:
                listeCategorie = Categorie.objects.filter(entite=entite, estSupprimer=0).order_by('libelleCat')
                listeImage = Image.objects.filter(estSupprimer=0, type=3).order_by('libelle')
                if request.POST:
                    libelle = request.POST["libelle"]
                    descript = request.POST["descript"]
                    prix = request.POST["prix"]
                    idcate = request.POST["categorie"]
                    image = int(request.POST["image"])
                    if libelle == "":
                        is_error = 1
                        error_libelle = "veuillez remplier ce champs"
                    if idcate == "":
                        is_error = 1
                        error_categorie = "veuillez sélectionner une catégorie"
                    if prix == "":
                        is_error = 1
                        error_prix = "veuillez remplier ce champs"
                    else:
                        try:
                            int(prix)
                        except:
                            is_error = 1
                            error_prix = "champs incorrect"
                    save_plus = request.POST.getlist('save_and')
                    if image == 0:
                        error_logo = "veuillez selectionner une image"
                        is_error = 1
                    if is_error == 0:
                        categorie = Categorie.objects.filter(idCategorie=idcate)[0]
                        ima = Image.objects.filter(idImage=image)[0]
                        produit=Produit()
                        produit.nomProduit=libelle
                        produit.descriptProduit=descript
                        produit.createurProduit= request.user
                        produit.categorie=categorie
                        produit.prixProduit=int(prix)
                        produit.logoProduit=ima
                        produit.isTmp=0
                        produit.save()
                        log = Log()
                        log.utilisateur = request.user.username
                        log.action = u"Création produit pour entité " + entite.nomEntite
                        log.save()
                        messages.success(request, u'Produit ajoutée avec succès')
                        try:
                            _next = int(save_plus[0])
                        except:
                            _next = 0
                        if _next == 0:
                            return redirect(listeProduit, idEntite,0)
                        else:
                            libelle = ""
                            descript = ""
                            prix=""
                            return render(request, 'nouveau_produit.html', locals())
                    else:
                        return render(request, 'nouveau_produit.html', locals())
                else:

                    return render(request, 'nouveau_produit.html', locals())
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())



@login_required
def modifierProduit(request,idProduit):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            is_image_change = 0
            try:
                produit = Produit.objects.filter(idProduit=idProduit)[0]
                entite = Entite.objects.filter(categorie__produit=produit)[0]
            except:
                is_error=1
            if is_error==0:
                listeCategorie = Categorie.objects.filter(entite=entite, estSupprimer=0).order_by('libelleCat')
                listeImage = Image.objects.filter(estSupprimer=0, type=3)
                if request.POST:
                    libelle = request.POST["libelle"]
                    descript = request.POST["descript"]
                    prix = request.POST["prix"]
                    idcate = request.POST["categorie"]
                    image = int(request.POST["image"])
                    if libelle == "":
                        is_error = 1
                        error_libelle = "veuillez remplier ce champs"
                    if idcate == "":
                        is_error = 1
                        error_categorie = "veuillez sélectionner une catégorie"
                    if prix == "":
                        is_error = 1
                        error_prix = "veuillez remplier ce champs"
                    else:
                        try:
                            int(prix)
                        except:
                            is_error = 1
                            error_prix = "champs incorrect"
                    if image != 0:
                        is_image_change = 1
                    if is_error ==0:
                        categorie = Categorie.objects.filter(idCategorie=idcate)[0]
                        produit.nomProduit = libelle
                        produit.descriptProduit = descript
                        produit.modificateurProduit= request.user
                        produit.categorie = categorie
                        produit.prixProduit = int(prix)
                        # on vérifie si l'image change on l'upluoad
                        if is_image_change==1:
                            ima = Image.objects.filter(idImage=image)[0]
                            produit.logoProduit=ima
                        produit.estModifier=produit.estModifier+1
                        produit.save()
                        # fin l'upluoad de d'image
                        log = Log()
                        log.utilisateur = request.user.username
                        log.action = u"Modification produit pour entité " + entite.nomEntite
                        log.save()
                        messages.success(request, u'Produit modifié avec succès')
                        return redirect(listeProduit, produit.categorie.entite.idEntit, 0)
                    else:
                        return render(request, 'editer_produit.html', locals())
                else:
                    libelle = produit.nomProduit
                    descript = produit.descriptProduit
                    prix = produit.prixProduit
                    idcate = produit.categorie.idCategorie
                    return render(request, 'editer_produit.html', locals())
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())

@login_required
def supprimeProduit(request,idProduit):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            try:
                produit = Produit.objects.filter(idProduit=idProduit)[0]
            except:
                is_error=1
            if is_error==0:
                produit.estSupprimer=1
                produit.save()
                log = Log()
                log.utilisateur = request.user.username
                log.action = u"supprèssion produit pour entité " + produit.categorie.entite.nomEntite
                log.save()
                messages.success(request, u'Produit supprimé avec succès')
                return redirect(listeProduit, produit.categorie.entite.idEntit, 0)
            message = "page introuvable"
            return render(request, '404.html', locals())

@login_required
def desactiverProduit(request,idProduit):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            try:
                produit = Produit.objects.filter(idProduit=idProduit)[0]
            except:
                is_error=1
            if is_error==0:
                produit.estDesactiver=1
                produit.save()
                log = Log()
                log.utilisateur = request.user.username
                log.action = u"désactivation produit pour entité " + produit.categorie.entite.nomEntite
                log.save()
                messages.success(request, u'Produit désactivé avec succès')
                return redirect(listeProduit, produit.categorie.entite.idEntit, 0)
            message = "page introuvable"
            return render(request, '404.html', locals())

@login_required
def activerProduit(request,idProduit):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            try:
                produit = Produit.objects.filter(idProduit=idProduit)[0]
            except:
                is_error=1
            if is_error==0:
                produit.estDesactiver=0
                produit.save()
                log = Log()
                log.utilisateur = request.user.username
                log.action = u"activation produit pour entité " + produit.categorie.entite.nomEntite
                log.save()
                messages.success(request, u'Produit activé avec succès')
                return redirect(listeProduit, produit.categorie.entite.idEntit, 0)
            message = "page introuvable"
            return render(request, '404.html', locals())