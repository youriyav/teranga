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
    ajouterManagerEntite, profilEntite, menuEntite
from utilisateur.views import listeUsers, createUser, editUser, editUserPass, desableUser, enableUser, deleteUser, \
    profilUser, paremetreUser

urlpatterns = [
    url(r'^liste-entite', listeEntite, name='liste_entite'),
    url(r'^nouvelle-entite', createEntite, name='nouvelle_entite'),
    url(r'^modifier-entite/(?P<idEntite>\d+)$', editEntite, name='editer_entite'),
    url(r'^desactiver-entite/(?P<idEntite>\d+)$', desableEntite, name='desactiver_Entite'),
    url(r'^activer-entite/(?P<idEntite>\d+)$', enableEntite, name='activer_Entite'),
    url(r'^supprimer-entite', supprimerEntite, name='supprimer_Entite'),
    url(r'^ajouter-manager-entite/(?P<idEntite>\d+)$', ajouterManagerEntite, name='ajouterManagerEntite'),
    url(r'^profil-entite/(?P<idEntite>\d+)$', profilEntite, name='profilEntite'),
    url(r'^menu-entite/(?P<idEntite>\d+)$', menuEntite, name='menu_entite'),
    #url(r'^nouveau-categorie/(?P<idEntite>\d+)$', creerCategorie, name='creation_categorie'),
    #url(r'^activer-utilisateur/(?P<idUtilisateur>\d+)$', enableUser, name='activer_user'),
    #url(r'^supprimer-utilisateur/(?P<idUtilisateur>\d+)$', deleteUser, name='supprimer_user'),
    #url(r'^profil-utilisateur/(?P<utilisateur>[\w\-]+)$', profilUser, name='profil_user'),
    #url(r'^parametre-utilisateur/(?P<utilisateur>[\w\-]+)$', paremetreUser, name='parametre_user'),
]
