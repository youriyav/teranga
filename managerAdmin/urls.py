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
from livreur.views import listeLivreur, newLivreur, editerLivreur, bloquerLivreur, activerLivreur, supprimerLivreur
from manager.views import homeUtilisateur, listeCommande, detailCommande, listeLivreurManager, affecterCommande, \
    suivreCommande, updatelisteCommande
from managerAdmin.views import homeManagerAdmin, logoutAdminManager, parametreAdminManager, updateHomeManagerAdmin

urlpatterns = [
    url(r'^$', homeManagerAdmin, name='home_managerAdmin_fast'),
    url(r'^update-home-manager$', updateHomeManagerAdmin, name='update_home_managerAdmin_fast'),
    url(r'^logout$', logoutAdminManager, name='logout_managerAdmin_fast'),
    url(r'^parametre$', parametreAdminManager, name='parametre_managerAdmin_fast'),
    #url(r'^liste-commande$', listeCommande, name='liste_commande_manager'),
    #url(r'^update-liste-commande$', updatelisteCommande, name='update_liste_commande_manager'),
    #url(r'^liste-livreur$', listeLivreurManager, name='liste_livreur_manger'),
    #url(r'^detail-commande/(?P<idCommande>\d+)$', detailCommande, name='datail_commande_manager'),
    #url(r'^affecter-commande$', affecterCommande, name='affecter_commande_manager'),
    #url(r'^suivre-commande/(?P<idCommande>\d+)$', suivreCommande, name='suivre_commande_manager'),
]
