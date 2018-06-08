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

from utilisateur.views import listeUsers, createUser, editUser, editUserPass, desableUser, enableUser, deleteUser, \
    profilUser, paremetreUser, deleteUserPost

urlpatterns = [

    url(r'^liste-utilisateur', listeUsers, name='liste_users'),
    url(r'^nouveau-utilisateur', createUser, name='nouveau_user'),
    url(r'^modifier-utilisateur/(?P<idUtilisateur>\d+)$', editUser, name='editer_user'),
    url(r'^modifier-password/(?P<utilisateur>[\w\-]+)$', editUserPass, name='editer_user_pass'),
    url(r'^desactiver-utilisateur/(?P<idUtilisateur>\d+)$', desableUser, name='desactiver_user'),
    url(r'^activer-utilisateur/(?P<idUtilisateur>\d+)$', enableUser, name='activer_user'),
    url(r'^supprimer-utilisateur/(?P<idUtilisateur>\d+)$', deleteUser, name='supprimer_user'),
    url(r'^supprimer-utilisateur-post', deleteUserPost, name='supprimer_user_post'),
    url(r'^profil-utilisateur/(?P<utilisateur>[\w\-]+)$', profilUser, name='profil_user'),
    url(r'^parametre-utilisateur/(?P<utilisateur>\w+)$', paremetreUser, name='parametre_user'),
]
