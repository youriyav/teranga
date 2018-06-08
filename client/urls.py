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
from client.views import listeClient, createClient, AftercreateClient,  homeClient, bloquerClient, debloquerClient

urlpatterns = [
    url(r'^liste-client', listeClient, name='liste_client'),
    url(r'^nouveau-utilisateur', createClient, name='nouveau_client'),
    url(r'^red-utilisateur/(?P<idClient>\d+)$', AftercreateClient, name='redirect_client'),
    url(r'^bloquer-utilisateur/(?P<idClient>\d+)$', bloquerClient, name='bloquer_client'),
    url(r'^debloquer-utilisateur/(?P<idClient>\d+)$', debloquerClient, name='debloquer_client'),
    url(r'^acceuil/(?P<idClient>\d+)$', homeClient, name='home_client'),
    #url(r'^$', homeClient, name='home_client'),
    #url(r'^modifier-utilisateur/(?P<idUtilisateur>\d+)$', editUser, name='editer_user'),
    #url(r'^modifier-password/(?P<utilisateur>[\w\-]+)$', editUserPass, name='editer_user_pass'),
    #url(r'^desactiver-utilisateur/(?P<idUtilisateur>\d+)$', desableUser, name='desactiver_user'),
    #url(r'^activer-utilisateur/(?P<idUtilisateur>\d+)$', enableUser, name='activer_user'),
    #url(r'^supprimer-utilisateur/(?P<idUtilisateur>\d+)$', deleteUser, name='supprimer_user'),
    #url(r'^supprimer-utilisateur-post', deleteUserPost, name='supprimer_user_post'),
    #url(r'^profil-utilisateur/(?P<utilisateur>[\w\-]+)$', profilUser, name='profil_user'),
    #url(r'^parametre-utilisateur/(?P<utilisateur>[\w\-]+)$', paremetreUser, name='parametre_user'),
]
