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
from ios.views import homeMobil,getCategorie,getProduit,updateMobil,login,newCommandeMobil,updateCommande
from produit.views import listeProduit, creerProduit, modifierProduit, supprimeProduit, desactiverProduit, \
    activerProduit

urlpatterns = [
    url(r'^liste-produits/(?P<idEntite>\d+)/(?P<idCategorie>\d+)$', listeProduit, name='liste_produit'),
    url(r'^initialize-terminal$', homeMobil, name='initialize_terminal'),
    url(r'^get-categorie/(?P<idEntite>\d+)$', getCategorie, name='get_categorie'),
    url(r'^get-produit/(?P<idCategorie>\d+)$', getProduit, name='getProduit'),
    url(r'^update/(?P<version>\d+)$', updateMobil, name='check_update'),
    url(r'^new-commande$', newCommandeMobil, name='new_commande'),
    url(r'^update-commande/(?P<idCommande>\d+)$', updateCommande, name='update_commande'),
    url(r'^login$', login, name='login'),
]
