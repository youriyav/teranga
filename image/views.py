# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

# Create your views here.
from image.models import Image
from senfood import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@login_required
def listeImage(request):
    if  request.user.is_authenticated():
        if request.user.is_superuser:
            listeImage=Image.objects.filter(estSupprimer=0)
            paginator = Paginator(listeImage, 10)
            page = request.GET.get('page')
            try:
                 users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            return render(request, 'listeImage.html', locals())

@login_required
def uploadImage(request):
    global  is_error, myfile
    is_error = 0
    if  request.user.is_authenticated():
        if request.user.is_superuser :
            if request.POST:
                libelle=request.POST["libelle"]
                type=request.POST["type"]
                description=request.POST["descript"]
                save_plus = request.POST.getlist('save_and')
                if libelle =="":
                    error_libelle="veuillez remplir ce champs"
                    is_error = 1
                if int(type) == 0:
                    error_type = "veuillez selectionner un type"
                    is_error = 1
                try:
                    myfile = request.FILES['image']
                except:
                    error_logo = "veuillez selectionner une image"
                    is_error = 1
                if is_error!=0:
                    return render(request, 'uploadImage.html', locals())
                else:
                    save_path = settings.MEDIA_ROOT
                    last = myfile.name[myfile.name.rfind("."):len(myfile.name)]
                    fs = FileSystemStorage()
                    currentId=0
                    try:
                        image=Image.objects.last()
                        currentId=image.idImage+1
                    except:
                        currentId=1
                    save_name = "teranga-food-upload-0" + str(currentId)  + last
                    fs.save(settings.MEDIA_ROOT +  save_name, myfile)
                    myImage=Image()
                    myImage.description=description
                    myImage.libelle=libelle
                    myImage.type=int(type)
                    myImage.saveName="/media/"+save_name
                    myImage.save()
                    try:
                        _next = int(save_plus[0])
                    except:
                        _next = 0
                    if _next == 0:
                        return redirect(listeImage)
                    else:
                        libelle = ""
                        description = ""
                        return render(request, 'uploadImage.html', locals())
            else:
                return render(request, 'uploadImage.html', locals())

@login_required
def supprimerImage(request,idImage):
    try:
        image=Image.objects.filter(idImage=idImage)[0]
        image.estSupprimer=1
        image.save()
        return redirect(listeImage)
    except:
        return render(request, '404-Admin.html', locals())


@login_required
def modifierImage(request,idImage):
    global is_error, myfile,is_cotinu
    try:
        image = Image.objects.filter(idImage=idImage)[0]
        if request.POST:
            libelle = request.POST["libelle"]
            type = request.POST["type"]
            description = request.POST["descript"]
            save_plus = request.POST.getlist('save_and')
            is_error=0
            if libelle == "":
                error_libelle = "veuillez remplir ce champs"
                is_error = 1
            if int(type) == 0:
                error_type = "veuillez selectionner un type"
                is_error = 1
            try:
                myfile = request.FILES['image']
                is_file = 1
            except:
                is_file = 0
            if is_error != 0:
                libelle = libelle
                type = int(type)
                descript = description
                return render(request, 'modifierImage.html', locals())
            else:
                if is_file==1:
                    save_path = settings.MEDIA_ROOT
                    last = myfile.name[myfile.name.rfind("."):len(myfile.name)]
                    fs = FileSystemStorage()
                    imag = Image.objects.last()
                    currentId = imag.idImage + 1
                    save_name = "teranga-food-upload-0" + str(currentId) + last
                    fs.save(settings.MEDIA_ROOT + save_name, myfile)
                    image.saveName = "/media/" + save_name
                image.description = description
                image.libelle = libelle
                image.type = int(type)
                image.save()
                return redirect(listeImage)
        else:
            libelle = image.libelle
            type = image.type
            descript = image.description
            return render(request, 'modifierImage.html', locals())
    except:
        return render(request, '404-Admin.html', locals())

