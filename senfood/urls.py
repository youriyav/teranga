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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

import utilisateur
from Entite.views import homeEntite
from client.views import loginClient, homeEntiteClient, createClient, validerCompteClient, regenererToken, \
    regenererTokenService, changeImageProfil, ListeProduitCategorie
from sen_food.views import myhome, logoutview, mesCommandes, mylogout, userCondition,getEntityCoordonne

urlpatterns = [
    url(r'^teranga-food-admin/', include('administration.urls')),
    url(r'^commande/', include('commande.urls')),
    url(r'^tarif/', include('tarif.urls')),
    url(r'^news-letter/', include('abonne.urls')),
    url(r'^manager-admin/', include('managerAdmin.urls')),
    url(r'^notification/', include('notification.urls')),
    url(r'^livreur/', include('livreur.urls')),
    url(r'^terminal/', include('terminal.urls')),
    url(r'^ios/', include('ios.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^client/', include('client.urls')),
    url(r'^compte/', include('validation.urls')),
    url(r'^home/', myhome, name='tohome'),
    url(r'^mes-commandes$', mesCommandes, name='mes_commandes'),
    url(r'^fast-food/(?P<idfastFood>\d+)$', homeEntiteClient, name='home_fast_food'),
    url(r'^menu/(?P<idEntite>\d+)/(?P<idCategorie>\d+)$', ListeProduitCategorie, name='liste_produit_cat'),
    url(r'^accounts/login$', loginClient , name='login'),
    url(r'^accounts/inscription$', createClient,name='inscription'),
    url(r'^accounts/validation$', validerCompteClient,name='validation_compte_client'),
    url(r'^accounts/regenerer-token$', regenererToken,name='regenerer_token'),
    url(r'^accounts/regenerer-tokenService$',regenererTokenService,name='regenerer_token_webservice'),
    url(r'^accounts/profil-utilisateur',regenererTokenService,name='client_profil'),
    url(r'^accounts/parametre-profil',changeImageProfil,name='set_profil_image_profil'),
    url(r'^$', myhome, name='main_acceuil'),
    #url(r'^login$', auth_views.login, name='login'),
    url(r'^logout$',mylogout, name='my_logout'),
    url(r'^get-entite-coordonne$',getEntityCoordonne, name='get_entity_coord'),
    url(r'^conditions-d-utilisation$', userCondition, name='reglee_confidence'),
    #url(r'^logout/$', auth_views.logout, {'template_name': 'blog/logout.html'}, name='logout'),
]
handler404 = 'sen_food.views.notFound'
