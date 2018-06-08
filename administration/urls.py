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
from django.conf.urls import url, include

from administration.views import homeAdmin, mylogoutAdmin, parametreAdmin, updateHomeAdmin

urlpatterns = [
    url(r'^$', homeAdmin, name='home_administrator'),
    url(r'^update-home$', updateHomeAdmin, name='update_home_admin'),
    url(r'^parametre-admin$', parametreAdmin, name='parametre_administrator'),
    url(r'^logout$', mylogoutAdmin, name='logout_administrator'),
    #url(r'^$', homeAdmin, name='home_administrator'),
    url(r'^entite/', include('Entite.urls')),
    url(r'^restaurant/', include('restaurant.urls')),
    url(r'^produit/', include('produit.urls')),
    url(r'^log/', include('log.urls')),
    url(r'^produit/', include('produit.urls')),
    url(r'^utilisateur/', include('utilisateur.urls')),
    url(r'^formule/', include('formule.urls')),
    url(r'^utilisateur/', include('utilisateur.urls')),
    url(r'^livreur/', include('livreur.urls')),
    url(r'^categorie/', include('categorie.urls')),
    url(r'^localite/', include('localite.urls')),
    url(r'^commande/', include('commande.urls')),
    url(r'^parametre/', include('parametre.urls')),
    url(r'^image/', include('image.urls')),
]
