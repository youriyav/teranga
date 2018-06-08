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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from Entite.views import listeEntite, createEntite, editEntite, desableEntite, enableEntite, supprimerEntite, \
    ajouterManagerEntite, profilEntite
from restaurant.views import listeRestaurant, createRestaurant, editerRestaurant, desactiverRestaurant, \
    activerRestaurant, supprimerRestaurant, showOnMapRestaurant
from utilisateur.views import listeUsers, createUser, editUser, editUserPass, desableUser, enableUser, deleteUser, \
    profilUser, paremetreUser

urlpatterns = [
    url(r'^liste-restaurant', listeRestaurant, name='liste_restaurant'),
    url(r'^nouveau-restaurant/(?P<idEntite>\d+)$', createRestaurant, name='nouveau_restaurant'),
    url(r'^editer-restaurant/(?P<idRestaurant>\d+)$', editerRestaurant, name='editer_restaurant'),
    url(r'^desactiver-restaurant/(?P<idRestaurant>\d+)$', desactiverRestaurant, name='desactiver_restaurant'),
    url(r'^activer-restaurant/(?P<idRestaurant>\d+)$', activerRestaurant, name='activer_restaurant'),
    url(r'^supprimer-restaurant', supprimerRestaurant, name='supprimer_restaurant_post'),
    url(r'^showOnMap-restaurant/(?P<coordone>[\w\-]+)$', showOnMapRestaurant, name='show_restaurant_onMap'),
    #url(r'^modifier-entite/(?P<idEntite>\d+)$', editEntite, name='editer_entite'),
    #url(r'^desactiver-entite/(?P<idEntite>\d+)$', desableEntite, name='desactiver_Entite'),
    #url(r'^activer-entite/(?P<idEntite>\d+)$', enableEntite, name='activer_Entite'),
    #url(r'^supprimer-entite/(?P<idEntite>\d+)$', supprimerEntite, name='supprimer_Entite'),
    #url(r'^ajouter-manager-entite/(?P<idEntite>\d+)$', ajouterManagerEntite, name='ajouterManagerEntite'),
    #url(r'^profil-entite/(?P<idEntite>\d+)$', profilEntite, name='profilEntite'),
    #url(r'^activer-utilisateur/(?P<idUtilisateur>\d+)$', enableUser, name='activer_user'),
    #url(r'^supprimer-utilisateur/(?P<idUtilisateur>\d+)$', deleteUser, name='supprimer_user'),
    #url(r'^profil-utilisateur/(?P<utilisateur>[\w\-]+)$', profilUser, name='profil_user'),
    #url(r'^parametre-utilisateur/(?P<utilisateur>[\w\-]+)$', paremetreUser, name='parametre_user'),
]
