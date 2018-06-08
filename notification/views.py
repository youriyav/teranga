import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from client.models import Client
from notification.models import Notification


@login_required
def getNotification(request):
    global client
    user_request=request.user
    is_error=0
    try:
        client=Client.objects.filter(user=user_request)[0]
    except:
        is_error=1
    if is_error==0:
        #Q(client=client)|Q(Notitype=1)
        #try:
        notifications=Notification.objects.filter(client=client,is_sync=0)
        tmp=0
        for notification in notifications:
            tmp=tmp+1
            notification.is_sync=1
            notification.save()
        data=""
        if tmp!=0:
            data = serializers.serialize('json', list(notifications), fields=('dateCreation', 'content','Notitype','url','titre'))
        return HttpResponse(data)
        #except:
            #v=1
            #return HttpResponse('0',status=405)
    else:
        return HttpResponse('0', status=407)

@login_required
def readNotification(request,data):
    global client
    user_request=request.user
    is_error=0
    try:
        client=Client.objects.filter(user=user_request)[0]
    except:
        is_error=1
    if is_error==0:
        data_json = json.loads(data)
        for notif in data_json:
            notification = Notification.objects.filter(idNotification=notif["id"])[0]
            notification.is_read=1
            notification.save()
        return HttpResponse("succes")