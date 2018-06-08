from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from log.models import Log


@login_required
def showLog(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        listelog=Log.objects.all()
        return render(request, 'listeLog.html', locals())
@login_required
def deleteLog(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        Log.objects.all().delete()
        return render(request, 'listeLog.html', locals())