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

from formule.views import listeFormule, creerFormule, modifierFormule, supprimerFormule, desactiverFormule, \
    activerFormule
from livreur.views import listeLivreur, newLivreur, editerLivreur, bloquerLivreur, activerLivreur, supprimerLivreur, \
    loginLivreur, logoutLivreur

urlpatterns = [
    url(r'^liste-livreur$', listeLivreur, name='liste_livreur'),
    url(r'^nouveau-livreur$', newLivreur, name='create_livreur'),
    url(r'^editer-livreur/(?P<idLivreur>\d+)$', editerLivreur, name='editer_livreur'),
    url(r'^desactiver-livreur/(?P<idLivreur>\d+)$', bloquerLivreur, name='desactiver_livreur'),
    url(r'^activer-livreur/(?P<idLivreur>\d+)$', activerLivreur, name='activer_livreur'),
    url(r'^supprimer-livreur/(?P<idLivreur>\d+)$', supprimerLivreur, name='supprimer_livreur'),
    url(r'^login-livreur$', loginLivreur, name='login_livreur'),
    url(r'^logout-livreur$', logoutLivreur, name='logout_livreur'),
    url(r'^register-mobil-livreur$', loginLivreur, name='register_mobil_livreur'),
    #url(r'^nouveau-formule/(?P<idEntite>\d+)$', creerFormule, name='nouveau_formule'),
    #url(r'^modifier-formule/(?P<idFormule>\d+)$', modifierFormule, name='modifier_formule'),
    #url(r'^supprimer-formule/(?P<idFormule>\d+)$', supprimerFormule, name='supprimer_formule'),
    #url(r'^desactiver-formule/(?P<idFormule>\d+)$', desactiverFormule, name='desactiver_formule'),
    #url(r'^activer-formule/(?P<idFormule>\d+)$', activerFormule, name='activer_formule'),
]
