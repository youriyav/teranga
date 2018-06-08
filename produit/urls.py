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

from categorie.views import creerCategorie, editerCategorie, loadImage
from produit.views import listeProduit, creerProduit, modifierProduit, supprimeProduit, desactiverProduit, \
    activerProduit

urlpatterns = [
    url(r'^liste-produits/(?P<idEntite>\d+)/(?P<idCategorie>\d+)$', listeProduit, name='liste_produit'),
    url(r'^nouveau-produits/(?P<idEntite>\d+)$', creerProduit, name='creer_produit'),
    url(r'^modifier-produits/(?P<idProduit>\d+)$', modifierProduit, name='modifier_produit'),
    url(r'^supprimer-produits/(?P<idProduit>\d+)$', supprimeProduit, name='supprimer_produit'),
    url(r'^desactiver-produits/(?P<idProduit>\d+)$', desactiverProduit, name='desactiver_produit'),
    url(r'^activer-produits/(?P<idProduit>\d+)$', activerProduit, name='activer_produit'),
    # url(r'^editer-categorie/(?P<idCategorie>\d+)$', editerCategorie, name='editer_categorie'),
    #url(r'^load-image/(?P<idEntite>\d+)$', loadImage, name='load_image'),
    #url(r'^activer-utilisateur/(?P<idUtilisateur>\d+)$', enableUser, name='activer_user'),
    #url(r'^supprimer-utilisateur/(?P<idUtilisateur>\d+)$', deleteUser, name='supprimer_user'),
    #url(r'^profil-utilisateur/(?P<utilisateur>[\w\-]+)$', profilUser, name='profil_user'),
    #url(r'^parametre-utilisateur/(?P<utilisateur>[\w\-]+)$', paremetreUser, name='parametre_user'),
]
