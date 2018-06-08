"""senfood URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from localite.views import createLocalite, listeLocalite, editerLocalite, activerLocalite, desactiverLocalite, \
    supprimerLocalite, suggererLocalite

urlpatterns = [
    #url(r'^liste-livreur$', listeLivreur, name='liste_livreur'),
    url(r'^nouvelle-localite$', createLocalite, name='new_localite'),
    url(r'^suggerer-localite$', suggererLocalite, name='suggerer_localite'),
    url(r'^editer-localite/(?P<idLocalite>\d+)$', editerLocalite, name='editer_localite'),
    url(r'^activer-localite/(?P<idLocalite>\d+)$', activerLocalite, name='activer_localite'),
    url(r'^desactiver-localite/(?P<idLocalite>\d+)$', desactiverLocalite, name='desactiver_localite'),
    url(r'^supprimer-localite/(?P<idLocalite>\d+)$', supprimerLocalite, name='supprimer_localite'),
    url(r'^liste-localite$', listeLocalite, name='liste_localite'),
]
