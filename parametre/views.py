from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from parametre.models import Parametre


@login_required
def updateParam(request):
    if request.user.is_authenticated():
        user_connecter = request.user
        if request.user.is_active:
            if request.user.is_superuser:
                ukey=request.POST["key"]
                value=request.POST["value"]
                try:
                    parametre=Parametre.objects.filter(key=ukey)[0]
                    parametre.value=value
                    parametre.save()
                    return  HttpResponse("good")
                except:
                    return HttpResponse("bad",status=401)