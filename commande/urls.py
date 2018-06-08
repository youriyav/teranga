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

from commande.views import newCommande, relancerCommande, updateListCommande, localiserCommande, changeState, \
    commandeApproximite, updateLocation, ListCommandeSuper

urlpatterns = [
    url(r'^nouvelle-commande$', newCommande, name='nouvelle_commande'),
    url(r'^liste-commande$', ListCommandeSuper, name='liste_commande_super'),
    url(r'^relancer-commande$', relancerCommande, name='relancer_commande'),
    url(r'^update-liste-commande$', updateListCommande, name='update_liste_commande'),
    url(r'^change-state$', changeState, name='chenge_commande_state'),
    url(r'^commande-next', commandeApproximite, name='commande_approximite'),
    url(r'^localiser-commande/(?P<idCommande>\d+)$', localiserCommande, name='locate_commande'),
    url(r'^update-location-commande$', updateLocation, name='update_location_commande'),
]
