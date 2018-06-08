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

from image.views import listeImage, uploadImage, supprimerImage, modifierImage
from localite.views import createLocalite, listeLocalite, editerLocalite, activerLocalite, desactiverLocalite, \
    supprimerLocalite, suggererLocalite

urlpatterns = [
    #url(r'^liste-livreur$', listeLivreur, name='liste_livreur'),
    url(r'^upload-image$', uploadImage, name='new_image'),
    url(r'^supprimer-image/(?P<idImage>\d+)$', supprimerImage, name='supprimerImage'),
    url(r'^modifier-image/(?P<idImage>\d+)$', modifierImage, name='modifierImage'),
    url(r'^$', listeImage, name='liste_image'),
]
