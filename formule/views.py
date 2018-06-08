# coding=utf-8
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from Entite.models import Entite
from formule.models import Formule
from log.models import Log
from sen_food.views import decodeString


@login_required
def listeFormule(request,idEntite):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            try:
                entite = Entite.objects.filter(idEntit=idEntite)[0]
            except:
                is_error=1
            if is_error==0:
                listeFormule=Formule.objects.filter(entite=entite,estSupprimer=0).order_by('nomFormule')
                return render(request, 'listeFormule.html', locals())
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())

##création formule

@login_required
def creerFormule(request,idEntite):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            try:
                entite = Entite.objects.filter(idEntit=idEntite)[0]
            except:
                is_error=1
            if is_error==0:
                if request.POST:
                    libelle = request.POST["libelle"]
                    descript = request.POST["descript"]
                    prix = request.POST["prix"]
                    if libelle == "":
                        is_error = 1
                        error_libelle = "veuillez remplier ce champs"
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
                    try:
                        myfile = request.FILES['logo']
                    except:
                        error_logo = "veuillez selectionner une image"
                        is_error = 1
                    if is_error == 0:
                        entite_folder = "C:/Users/root/PycharmProjects/senfood/static/images/uploads/" + decodeString(entite.nomEntite)
                        last = myfile.name[myfile.name.rfind("."):len(myfile.name)]
                        forlmule=Formule()
                        forlmule.nomFormule=libelle
                        forlmule.descriptFormule=descript
                        forlmule.prixFormule=prix
                        forlmule.entite=entite
                        forlmule.createurFormule=request.user
                        forlmule.save()
                        logo_name = "form_" + decodeString(entite.nomEntite) + "_" + str(forlmule.idFormule) + last
                        forlmule.logoFormule = "images/uploads/" + decodeString(entite.nomEntite) + "/" + logo_name
                        forlmule.save()
                        destination = open(os.path.join(entite_folder, logo_name), 'wb+')
                        for chunk in myfile.chunks():
                            destination.write(chunk)
                        destination.close()
                        log = Log()
                        log.utilisateur = request.user.username
                        log.action = u"Création formule pour entité " + decodeString(entite.nomEntite)
                        log.save()
                        messages.success(request, u'formule ajoutée avec succès')
                        try:
                            _next = int(save_plus[0])
                        except:
                            _next = 0
                        if _next == 0:
                            return redirect(listeFormule, idEntite)
                        else:
                            libelle = ""
                            descript = ""
                            prix=""
                            return render(request, 'nouveau_formule.html', locals())
                    else:
                        return render(request, 'nouveau_formule.html', locals())
                else:

                    return render(request, 'nouveau_formule.html', locals())
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())


@login_required
def modifierFormule(request,idFormule):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            try:
                forlmule = Formule.objects.filter(idFormule=idFormule)[0]
                entite=Entite.objects.filter(formule=forlmule)[0]
            except:
                is_error=1
            if is_error==0:
                if request.POST:
                    is_image_change = 0
                    libelle = request.POST["libelle"]
                    descript = request.POST["descript"]
                    prix = request.POST["prix"]
                    if libelle == "":
                        is_error = 1
                        error_libelle = "veuillez remplier ce champs"
                    if prix == "":
                        is_error = 1
                        error_prix = "veuillez remplier ce champs"
                    else:
                        try:
                            int(prix)
                        except:
                            is_error = 1
                            error_prix = "champs incorrect"
                    try:
                        myfile = request.FILES['logo']
                    except:
                        is_image_change = 1
                    if is_error == 0:
                        forlmule.nomFormule = libelle
                        forlmule.descriptFormule = descript
                        forlmule.prixFormule = prix
                        if is_image_change==0:
                            entite_folder = "C:/Users/root/PycharmProjects/senfood/static/images/uploads/"+decodeString(forlmule.entite.nomEntite)
                            last=myfile.name[myfile.name.rfind("."):len(myfile.name)]
                            logo_name = "form_edit"+str(forlmule.estModifier+1) +"_"+ decodeString(forlmule.entite.nomEntite) + "_" + str(forlmule.idFormule) + last
                            forlmule.logoFormule= "images/uploads/" + decodeString(forlmule.entite.nomEntite) + "/" + logo_name
                            destination = open(os.path.join(entite_folder, logo_name), 'wb+')
                            for chunk in myfile.chunks():
                                destination.write(chunk)
                            destination.close()
                        forlmule.estModifier=forlmule.estModifier+1
                        forlmule.save()
                        log = Log()
                        log.utilisateur = request.user.username
                        log.action = u"Modification formule pour entité " + decodeString(forlmule.entite.nomEntite)
                        log.save()
                        messages.success(request, u'formule modifiée avec succès')
                        return redirect(listeFormule, forlmule.entite.idEntit)
                    else:
                        return render(request, 'editer_formule.html', locals())
                else:
                    libelle=forlmule.nomFormule
                    prix=forlmule.prixFormule
                    descript=forlmule.descriptFormule
                    return render(request, 'editer_formule.html', locals())
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())


@login_required
def supprimerFormule(request,idFormule):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            try:
                forlmule = Formule.objects.filter(idFormule=idFormule)[0]
            except:
                is_error=1
            if is_error==0:
                forlmule.estSupprimer=1
                forlmule.save()
                log = Log()
                log.utilisateur = request.user.username
                log.action = u"Suppèssion formule pour entité " + decodeString(forlmule.entite.nomEntite)
                log.save()
                messages.success(request, u'formule supprimée avec succès')
                return redirect(listeFormule, forlmule.entite.idEntit)
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())

@login_required
def desactiverFormule(request,idFormule):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            try:
                forlmule = Formule.objects.filter(idFormule=idFormule)[0]
            except:
                is_error=1
            if is_error==0:
                forlmule.estDesactiver=1
                forlmule.save()
                log = Log()
                log.utilisateur = request.user.username
                log.action = u"Désactivation formule pour entité " + decodeString(forlmule.entite.nomEntite)
                log.save()
                messages.success(request, u'formule désactivée avec succès')
                return redirect(listeFormule, forlmule.entite.idEntit)
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())

@login_required
def activerFormule(request,idFormule):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            is_error=0
            try:
                forlmule = Formule.objects.filter(idFormule=idFormule)[0]
            except:
                is_error=1
            if is_error==0:
                forlmule.estDesactiver=0
                forlmule.save()
                log = Log()
                log.utilisateur = request.user.username
                log.action = u"Activation formule pour entité " + decodeString(forlmule.entite.nomEntite)
                log.save()
                messages.success(request, u'formule activée avec succès')
                return redirect(listeFormule, forlmule.entite.idEntit)
            else:
                message = "page introuvable"
                return render(request, '404.html', locals())