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

urlpatterns = [
    url(r'^liste-formule/(?P<idEntite>\d+)$', listeFormule, name='liste_formule'),
    url(r'^nouveau-formule/(?P<idEntite>\d+)$', creerFormule, name='nouveau_formule'),
    url(r'^modifier-formule/(?P<idFormule>\d+)$', modifierFormule, name='modifier_formule'),
    url(r'^supprimer-formule/(?P<idFormule>\d+)$', supprimerFormule, name='supprimer_formule'),
    url(r'^desactiver-formule/(?P<idFormule>\d+)$', desactiverFormule, name='desactiver_formule'),
    url(r'^activer-formule/(?P<idFormule>\d+)$', activerFormule, name='activer_formule'),
]
