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
    loginLivreur
from terminal.views import registerMobil, updateLocationMobil, initialiseLocationMobil, updateMobil, loginClientMobil, \
    inscriptionClientMobil, regenererTokenMobil, validationCompteMobil, newCommandeMobil, updateDureeCommandeMobil, \
    checkForUpdate, resetTerminal,homeMobil,getCategorie,getProduit

urlpatterns = [
    #url(r'^liste-livreur$', listeLivreur, name='liste_livreur'),
    url(r'^nouveau-terminal$', registerMobil, name='new_terminal'),
    url(r'^update-location-terminal$', updateLocationMobil, name='update_location_terminal'),
    url(r'^initialize-terminal$', homeMobil, name='initialize_terminal'),
    #url(r'^initialize-terminal$', initialiseLocationMobil, name='initialize_terminal'),
    url(r'^update-terminal$', updateMobil, name='update_terminal'),
    url(r'^client-login', loginClientMobil, name='login_client_mobil'),
    url(r'^client-inscription', inscriptionClientMobil, name='inscription_client_mobil'),
    url(r'^compte-regenererToken-mobil$', regenererTokenMobil, name='regenerTokenMobil'),
    url(r'^compte-validation-mobil$', validationCompteMobil, name='validationCompteMobil'),
    url(r'^new-commande-mobil$', newCommandeMobil, name='nouvelle_commande_mobil'),
    url(r'^update-duree-commande-mobil/(?P<idClient>\d+)/(?P<idCommande>\d+)$', updateDureeCommandeMobil, name='update_duree_commande'),
    url(r'^check-update-terminal$', checkForUpdate, name='check_for_update'),
    url(r'^reset-terminal$', resetTerminal, name='reset_terminal'),
    url(r'^get-categorie/(?P<idEntite>\d+)$', getCategorie, name='get_categorie'),
    url(r'^get-products/(?P<idCategorie>\d+)$', getProduit, name='get_produit'),
    #url(r'^editer-livreur/(?P<idLivreur>\d+)$', editerLivreur, name='editer_livreur'),
    #url(r'^desactiver-livreur/(?P<idLivreur>\d+)$', bloquerLivreur, name='desactiver_livreur'),
    #url(r'^activer-livreur/(?P<idLivreur>\d+)$', activerLivreur, name='activer_livreur'),
    #url(r'^supprimer-livreur/(?P<idLivreur>\d+)$', supprimerLivreur, name='supprimer_livreur'),
    #url(r'^login-livreur$', loginLivreur, name='login_livreur'),
    #url(r'^register-mobil-livreur$', loginLivreur, name='register_mobil_livreur'),
    #url(r'^nouveau-formule/(?P<idEntite>\d+)$', creerFormule, name='nouveau_formule'),
    #url(r'^modifier-formule/(?P<idFormule>\d+)$', modifierFormule, name='modifier_formule'),
    #url(r'^supprimer-formule/(?P<idFormule>\d+)$', supprimerFormule, name='supprimer_formule'),
    #url(r'^desactiver-formule/(?P<idFormule>\d+)$', desactiverFormule, name='desactiver_formule'),
    #url(r'^activer-formule/(?P<idFormule>\d+)$', activerFormule, name='activer_formule'),
]
