from django.shortcuts import render
from tarif.models import Tarif
from django.http import HttpResponse
from geopy.distance import vincenty
from Entite.models import Entite
# Create your views here.
def getTarif(request,idEntite,mlatitude,mlongitude):
	tarifs=Tarif.objects.filter(estSupprimer=0)
	dist=0

	#return HttpResponse(str(mlongitude))
	try:
		entite=Entite.objects.filter(idEntit=int(idEntite))[0]
		entiteCoord = (entite.latitude, entite.longitude)
		userCoord = (mlatitude, mlongitude)
		dist=vincenty(userCoord,entiteCoord).meters
	except:
		dist=0
	cpt=0
	if dist!=0:
		for tarif in tarifs:
			if dist>tarif.distanceMin and dist<=tarif.distanceMax :
				#return  HttpResponse(str(dist))
				data='[{"tarif":'+str(tarif.prix)+'}]'
				return  HttpResponse(data)
				cpt=1
		if cpt==0:
			tarif=Tarif.objects.filter(libelle="0")[0]
			data='[{"tarif":'+str(tarif.prix)+'}]'
			return  HttpResponse(data)
	else:
		tarif=Tarif.objects.filter(libelle="0")[0]
		data='[{"tarif":'+str(tarif.prix)+'}]'
		return  HttpResponse(data)