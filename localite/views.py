from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from localite.models import Localite

@login_required
def listeLocalite(request):
    if  request.user.is_authenticated():
        if request.user.is_superuser or request.user.utilisateur.isManager==0 :
            listeLocalite=Localite.objects.filter(estSupprimer=0)
            return render(request, 'listeLocalite.html', locals())
@login_required
def suggererLocalite(request):
    if request.user.is_authenticated():
        if request.POST:
            nom = request.POST["libelle"]
            localite = Localite()
            localite.libelle = nom
            localite.isSuggest=1
            localite.isSuggest=1
            localite.personne=request.user
            localite.save()
            return HttpResponse("good")
@login_required
def createLocalite(request):
    global myfile
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            if request.POST:
                is_error=0
                nom=request.POST["libelle"]
                save_plus = request.POST.getlist('save_and')
                if nom=="":
                    is_error=1
                    errer_nom="Veuillez remplir ce champs"
                if is_error!=0:
                    return render(request, 'creationLocalite.html', locals())
                else:
                    localite=Localite()
                    localite.libelle=nom
                    localite.save()
                    try:
                        _next = int(save_plus[0])
                    except:
                        _next = 0
                    if _next == 0:
                        return redirect(listeLocalite)
                    else:
                        nom = ""
                        return render(request, 'creationLocalite.html', locals())
            else:
                return render(request, 'creationLocalite.html', locals())


@login_required
def editerLocalite(request,idLocalite):
    global myfile
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            is_error=0
            try:
                localite=Localite.objects.filter(idLocalite=idLocalite)[0]
            except:
                is_error=1
            if is_error==0:
                if request.POST:
                    is_error=0
                    nom=request.POST["libelle"]
                    if nom=="":
                        is_error=1
                        errer_nom="Veuillez remplir ce champs"
                    if is_error!=0:
                        return render(request, 'editerLocalite.html', locals())
                    else:
                        localite.libelle=nom
                        localite.save()
                        return redirect(listeLocalite)
                else:
                    nom=localite.libelle
                    return render(request, 'editerLocalite.html', locals())
            else:
                return render(request, '404.html', locals())


@login_required
def activerLocalite(request,idLocalite):
    global myfile, localite
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            is_error=0
            try:
                localite=Localite.objects.filter(idLocalite=idLocalite)[0]
            except:
                is_error=1
            if is_error==0:
                localite.isActive=1
                localite.save()
                return redirect(listeLocalite)
            else:
                return render(request, '404.html', locals())

@login_required
def desactiverLocalite(request,idLocalite):
    global myfile, localite
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            is_error=0
            try:
                localite=Localite.objects.filter(idLocalite=idLocalite)[0]
            except:
                is_error=1
            if is_error==0:
                localite.isActive=0
                localite.save()
                return redirect(listeLocalite)
            else:
                return render(request, '404.html', locals())
@login_required
def supprimerLocalite(request,idLocalite):
    global myfile, localite
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            is_error=0
            try:
                localite=Localite.objects.filter(idLocalite=idLocalite)[0]
            except:
                is_error=1
            if is_error==0:
                localite.estSupprimer=1
                localite.save()
                return redirect(listeLocalite)
            else:
                return render(request, '404.html', locals())